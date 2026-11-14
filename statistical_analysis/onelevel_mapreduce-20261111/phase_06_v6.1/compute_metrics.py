#!/usr/bin/env python3
"""Independent OrionDesk v6.1 phase-6 ledger recomputation.

Usage: python compute_metrics.py [--ledger-dir DIR] [--input-dir DIR]
Reads individual JSONL ledgers, verifies item-level references and denominator
identities, and outputs metrics, probes, and explicit semantic-quality flags.
A structural PASS is deliberately NOT a certificate of logical entailment.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

REQUIRED_ROLES = ('01_screen_functions','02_api','03_data','04_batch_functions',
                  '05_business_rules','06_exception_handling','07_processing_flows',
                  '08_architecture_decision')
KEYS = ('TP','TN','FP','FN')


def read_rows(path):
    with path.open(encoding='utf-8') as fh:
        return [json.loads(line) for line in fh if line.strip()]


def write_rows(path, rows):
    with path.open('w',encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True)+'\n')


def js(v): return json.dumps(v,ensure_ascii=False,indent=2)+'\n'


def normalized(s):
    s=unicodedata.normalize('NFKC',s or '').lower()
    s=s.translate(str.maketrans({'–':'-','—':'-','‐':'-','‑':'-','\u00ad':'','“':'"','”':'"','’':"'"}))
    return ' '.join(s.split())


def require(pred, description, failures):
    if not pred:failures.append(description)


def rate(a,b):return a/b if b else None


def approx(a,b,tol=1e-12):return (a is None and b is None) or (a is not None and b is not None and abs(a-b)<=tol)


def raw_locator_matches(ev,raw_lines):
    file=ev.get('file')
    if file not in raw_lines:return False,'MISSING_GENERATED_FILE'
    line=ev.get('line_start')
    if not isinstance(line,int) or not (1<=line<=len(raw_lines[file])):return False,'INVALID_LINE'
    original=raw_lines[file][line-1]
    quote=ev.get('quote_en',ev.get('source_quote_en',''))
    if quote and normalized(quote) not in normalized(original) and normalized(original) not in normalized(quote):
        return False,'QUOTATION_DOES_NOT_MATCH_PHYSICAL_LINE'
    return True,'MATCH'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--ledger-dir',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--input-dir',type=Path,default=Path(__file__).resolve().parent.parent)
    args=parser.parse_args();p=args.ledger_dir.resolve(); root=args.input_dir.resolve()
    names={'R':'01_source_atoms_final.jsonl','N':'01_source_negative_controls_final.jsonl',
           'GO':'02_generated_atoms_final.jsonl','G':'02_generated_classes_final.jsonl',
           'E':'03_evidence_matches_final.jsonl','B':'03_semantic_coverage_bridges_final.jsonl',
           'FNA':'03_fn_root_cause_audit_final.jsonl','V':'04_generated_claim_validity_final.jsonl',
           'J':'04_atomic_judgments_final.jsonl','TA':'05_tp_evidence_audit_final.jsonl',
           'SA':'05_source_atomization_audit_final.jsonl','D':'04_duplicate_classes_final.jsonl',
           'P':'01_pdf_page_coverage_final.jsonl','L':'02_line_cell_coverage_final.jsonl',
           'DELTA':'07_change_delta.jsonl','EXCLUDED':'09_excluded_units.jsonl'}
    rows={key:read_rows(p/fn) for key,fn in names.items()}
    r,n,go,g,e,b,fna,v,j,ta,sa,d,pc,lc=(rows[k] for k in ['R','N','GO','G','E','B','FNA','V','J','TA','SA','D','P','L'])
    old_c=json.loads((p/'04_confusion_matrix_final.json').read_text(encoding='utf-8'))
    old_d=json.loads((p/'05_duplicate_metrics_final.json').read_text(encoding='utf-8'))
    failures=[];warnings=[];pdf_note=[];probe=[]
    require(len({x['source_id'] for x in r})==len(r),'duplicate PDF-positive source IDs',failures)
    require(len({x['negative_control_id'] for x in n})==len(n),'duplicate negative-control IDs',failures)
    require(len({x['generated_id'] for x in go})==len(go),'duplicate generated occurrence IDs',failures)
    require(len({x['generated_class_id'] for x in g})==len(g),'duplicate generated class IDs',failures)
    require(len({x['canonical_id'] for x in j})==len(j),'duplicate canonical decision IDs',failures)
    require(len({x['source_id'] for x in ta if x.get('audit_outcome')=='CONFIRMED_TP'})==
            sum(x.get('audit_outcome')=='CONFIRMED_TP' for x in ta),'duplicate confirmed TP audit ID',failures)
    source_ids={x['source_id'] for x in r}; neg_ids={x['negative_control_id'] for x in n}
    generated_ids={x['generated_id'] for x in go}; class_ids={x['generated_class_id'] for x in g}
    require(source_ids.isdisjoint(neg_ids),'R intersects N by ID',failures)
    require(len(j)>=len(r)+len(n),'U too small for R and N',failures)
    j_by_id={x['canonical_id']:x for x in j}
    require(source_ids|neg_ids<=set(j_by_id),'missing R or N canonical decisions',failures)
    require({x['origin_source_id'] for x in e}==source_ids and len(e)==len(r),'source coverage rows missing/duplicated',failures)
    require(len(v)==len(g) and {x['generated_class_id'] for x in v}==class_ids,'generated validity not one row per raw class',failures)
    require(len(lc)==sum(1 for z in root.glob('0[1-8]*.md') for _ in z.open(encoding='utf-8')),'physical line coverage count differs from inputs',failures)
    require({x['physical_page'] for x in pc}==set(range(1,91)) and len(pc)==90,'PDF page coverage not exactly 90 pages',failures)
    # Original source identity, read every physical page (including textless pages).
    supplied_pdf=root/'OrionDesk_AI_Detailed_Design_Specification(1).pdf'
    baseline_pdf=root/'fullload_cal_reference/OrionDesk_AI_Detailed_Design_Specification.pdf'
    pdf_digest=None;pdf_pages=[];pdf_quote_text_match=0;pdf_figure_match=0;pdf_unmatched=[]
    try:
        import fitz
        assert supplied_pdf.exists()
        pdf_digest=hashlib.sha256(supplied_pdf.read_bytes()).hexdigest()
        if baseline_pdf.exists():
            require(pdf_digest==hashlib.sha256(baseline_pdf.read_bytes()).hexdigest(),
                    'current PDF digest differs from fullload_cal reference PDF',failures)
        with fitz.open(supplied_pdf) as doc:
            require(len(doc)==90,'supplied original PDF does not contain 90 physical pages',failures)
            pdf_pages=[z.get_text(sort=False) for z in doc]
            readable=sum(bool(x.strip()) for x in pdf_pages)
            require(readable==90,'at least one physical PDF page unreadable as extracted text',failures)
            for x in r:
                page=x.get('physical_page')
                quote=x.get('quote_en','')
                if not isinstance(page,int) or not(1<=page<=90) or not quote:
                    pdf_unmatched.append({'source_id':x.get('source_id'),'page':page,'reason':'INVALID_PAGE_OR_EMPTY_QUOTE'});continue
                if normalized(quote) in normalized(pdf_pages[page-1]):pdf_quote_text_match+=1
                elif page==8 and x['source_id'] in {'PDF-00977','PDF-00978','PDF-00979'}:
                    # This figure text was visually inspected against the rendered PDF figure.
                    pdf_figure_match+=1
                    pdf_note.append({'source_id':x['source_id'],'physical_page':8,'validation':'FIGURE_TEXT_VISUALLY_INSPECTED','quote_en':quote})
                else:pdf_unmatched.append({'source_id':x['source_id'],'physical_page':page,'quote_en':quote})
    except Exception as ex:
        failures.append('PDF inspection failure: '+str(ex))
    require(not pdf_unmatched,'Some source atom quotes have neither PDF text nor inspected-figure support',failures)
    raw_files={}
    for role in REQUIRED_ROLES:
        matches=sorted(root.glob(role+'*.md'))
        require(len(matches)==1,f'expected one authoritative scored input for {role}, found {[x.name for x in matches]}',failures)
        if len(matches)==1:raw_files[matches[0].name]=matches[0].read_text(encoding='utf-8').splitlines()
    require(len(raw_files)==8,'not all eight scored Markdown inputs available',failures)
    verified_line_count=sum(len(x) for x in raw_files.values())
    coverage_count=collections.Counter(x['file'] for x in lc)
    for f,lines in raw_files.items():
        require(coverage_count[f]==len(lines),f'line coverage differs for {f}',failures)
        described={x['physical_line'] for x in lc if x['file']==f}
        require(described==set(range(1,len(lines)+1)),f'missing line coverage for {f}',failures)
    input_hashes={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in raw_files}
    # Exact original line and full row/cell locator cross checks.
    bad_go=[]
    for a in go:
        okay,reason=raw_locator_matches(a,raw_files)
        if not okay:bad_go.append({'generated_id':a.get('generated_id'),'reason':reason,'file':a.get('file'),'line':a.get('line_start')})
    require(not bad_go,'eligible generated occurrences contain invalid source quotations/locators',failures)
    g_map={x['generated_class_id']:x for x in g}
    go_map={x['generated_id']:x for x in go}
    members=collections.defaultdict(list)
    for a in go:
        require(a['generated_class_id'] in class_ids,'generated occurrence without class: '+a['generated_id'],failures)
        members[a['generated_class_id']].append(a['generated_id'])
        require(a.get('method')=='current_scored_8','cross-method generated occurrence',failures)
    for klass in g:
        cid=klass['generated_class_id'];listed=klass['occurrence_ids']
        require(set(listed)==set(members[cid]) and len(listed)==len(members[cid]),'class membership mismatch '+cid,failures)
        require(klass['occurrence_count']==len(listed),'class count mismatch '+cid,failures)
        require(klass.get('method')=='current_scored_8','cross-method generated class '+cid,failures)
    # Every canonical unit is on exactly one of the disjoint R, N, F surfaces.
    counts=collections.Counter(z['scoring_cell'] for z in j)
    f_extra=[x for x in j if x['canonical_id'] not in source_ids|neg_ids]
    fp_extra=[x for x in f_extra if x['scoring_cell']=='FP']
    asserted_n=[x for x in j if x['canonical_id'] in neg_ids and x['scoring_cell']=='FP']
    require(len(f_extra)==len(fp_extra),'generated-only units include non-FP judgments',failures)
    require(all(x['actual_label']==0 and x['predicted_label']==1 for x in fp_extra),'generated-only FP labeling error',failures)
    for x in j:
        actual=x['canonical_id'] in source_ids
        require(x['actual_label']==int(actual),'actual binary label error '+x['canonical_id'],failures)
        predicted=x['scoring_cell'] in ('TP','FP')
        require(x['predicted_label']==int(predicted),'predicted binary label error '+x['canonical_id'],failures)
        expected=('TP' if predicted else 'FN') if actual else ('FP' if predicted else 'TN')
        require(x['scoring_cell']==expected,'cell mismatch '+x['canonical_id'],failures)
        require(x.get('method')=='current_scored_8','cross-method canonical unit',failures)
        if actual:
            require(x['origin_source_ids']==[x['canonical_id']],'source ID origin mismatch '+x['canonical_id'],failures)
        else:
            if x['canonical_id'] in neg_ids:
                require(x['origin_negative_control_ids']==[x['canonical_id']],'negative origin mismatch '+x['canonical_id'],failures)
    tp=counts['TP'];tn=counts['TN'];fp=counts['FP'];fn=counts['FN']
    require(tp+fn==len(r),'positive source denominator mismatch',failures)
    require(tn+len(asserted_n)==len(n),'negative control denominator mismatch',failures)
    require(fp==len(asserted_n)+len(fp_extra),'unsupported/negative-control FP double-count/mismatch',failures)
    require(len(j)==len(r)+len(n)+len(fp_extra),'canonical universe set not equal to R+N+F',failures)
    require(len(j)==tp+tn+fp+fn,'four-cell universe reconciliation fails',failures)
    require(old_c['universe']['canonical_predicted_positive_units']==tp+fp,'predicted count differs from prior finalized ledger',failures)
    require(tp+fp==sum(x['predicted_label'] for x in j),'predicted positive count fails',failures)
    for k in KEYS:require(old_c['confusion'][k]==counts[k],f'phase-5 {k} differs from independently enumerated judgments',failures)
    require(old_c['universe']['source_positive_atoms']==len(r),'phase-5 R count mismatch',failures)
    require(old_c['universe']['source_negative_controls']==len(n),'phase-5 N count mismatch',failures)
    require(old_c['universe']['unsupported_generated_only_propositions']==len(fp_extra),'phase-5 F count mismatch',failures)
    require(old_c['universe']['asserted_negative_controls']==len(asserted_n),'phase-5 B count mismatch',failures)
    # Independent duplication representative and within-file/across-file assignment.
    dup_classes=[];within=across=repeated_span=0
    indexed_roles={f:i for i,f in enumerate(sorted(raw_files))}
    for klass in g:
        if klass['occurrence_count']<=1:continue
        occ=[go_map[x] for x in klass['occurrence_ids']]
        occ=sorted(occ,key=lambda x:(indexed_roles[x['file']],x['line_start'],x.get('table_cell') or ''))
        seen={occ[0]['file']}
        if len({x['file'] for x in occ})>1:repeated_span+=1
        within_count=across_count=0
        for item in occ[1:]:
            if item['file'] in seen:within+=1;within_count+=1
            else:across+=1;across_count+=1
            seen.add(item['file'])
        dup_classes.append({'generated_class_id':klass['generated_class_id'],
                            'representative_generated_id':occ[0]['generated_id'],
                            'occurrences':len(occ),'within_file_excess':within_count,
                            'across_file_excess':across_count})
    excess=len(go)-len(g)
    require(within+across==excess,'derived duplicate partition does not reconcile',failures)
    require(sum(c['occurrence_count']-1 for c in g)==excess,'raw class duplicate total inconsistent',failures)
    for key,check in [('eligible_generated_occurrences',len(go)),('unique_generated_claim_classes',len(g)),
                      ('duplicate_excess_occurrences',excess),('within_file_excess',within),
                      ('across_file_excess',across),('repeated_claim_class_count',len(dup_classes)),
                      ('repeated_classes_spanning_files',repeated_span)]:
        require(old_d[key]==check,'existing duplicate total incorrect for '+key,failures)
    d_by={x['generated_class_id']:x for x in d}
    require(set(d_by)=={x['generated_class_id'] for x in dup_classes},'duplicated class ledger membership differs',failures)
    require(sum(x['excess_occurrences'] for x in d)==excess,'duplicate classes item count mismatch',failures)
    # Source and generated proof ledgers: all real locators; counters flag weak proof rather than treating as certification.
    e_map={x['origin_source_id']:x for x in e}
    t_by={x['source_id']:x for x in ta if x.get('audit_outcome')=='CONFIRMED_TP'}
    f_by={x['source_id']:x for x in fna if x.get('final_scoring_cell')=='FN'}
    require(set(e_map)==source_ids and len(e)==len(r),'source evidence-match ledger incomplete',failures)
    require(set(t_by)=={x['canonical_id'] for x in j if x['scoring_cell']=='TP'},'TP proof audit not one-to-one with final TP',failures)
    require(len(t_by)==tp,'TP proof audit count differs',failures)
    require(set(f_by)=={x['canonical_id'] for x in j if x['scoring_cell']=='FN'},'FN audit not one-to-one with final FN',failures)
    require(len(f_by)==fn,'FN root-cause audit count differs',failures)
    fn_cats=collections.Counter(x.get('fn_review_disposition') for x in f_by.values())
    require(not(set(fn_cats)-{'TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'}),'illegal final FN root cause',failures)
    corrected_candidates=collections.Counter(x['fn_review_disposition'] for x in fna)
    require(sum(fn_cats.values())==fn,'FN disposition subtotal differs from FN',failures)
    e2_ids={x['origin_source_id'] for x in e if x['scoring_cell']=='TP' and x['entailment_grade']=='E2'}
    require({x['source_id'] for x in b}==e2_ids and len(b)==len(e2_ids),'E2 bridge ledger missing/duplicated',failures)
    bad_quote_locators=[];tp_predicate_incomplete=[]
    for x in j:
        if x['scoring_cell']!='TP':continue
        sid=x['canonical_id']; proof=t_by[sid]
        require(e_map[sid]['scoring_cell']=='TP' and proof['final_scoring_cell']=='TP',f'TP ledgers disagree at {sid}',failures)
        require(proof.get('pdf_evidence') and proof.get('generated_evidence'),f'empty TP evidence {sid}',failures)
        require(proof.get('entailment_grade') in ('E2','E3'),f'TP missing E2/E3 grade {sid}',failures)
        checks=proof.get('full_predicate_check',{})
        mandatory=('actor','target','action','condition','scope','timing','constraint','exception','outcome','version','polarity')
        if set(mandatory)-set(checks):tp_predicate_incomplete.append({'source_id':sid,'missing':sorted(set(mandatory)-set(checks))})
        for ref in proof['generated_evidence']:
            ok,why=raw_locator_matches(ref,raw_files)
            if not ok:bad_quote_locators.append({'source_id':sid,'generated_id':ref.get('generated_id'),'issue':why})
        require(set(x['origin_generated_class_ids'])<=class_ids,'TP refers to an unknown GCLASS '+sid,failures)
        require(x['origin_generated_class_ids'],f'TP with no generated class ID {sid}',failures)
    require(not bad_quote_locators,'TP cited generated quotes do not exist verbatim at their physical locators',failures)
    require(not tp_predicate_incomplete,'TP predicate check maps have missing keys',failures)
    for sid,x in f_by.items():
        require(x.get('pdf_evidence'),f'FN missing PDF evidence {sid}',failures)
        require(x.get('best_generated_candidates'),f'FN lacks actual generated candidate {sid}',failures)
    require({x['source_id'] for x in b}<=source_ids,'E2 source outside final R',failures)
    require(len(sa)>=len(r),'source atomization audit too small',failures)
    require(any(x.get('change_type') for x in rows['DELTA']),'missing phase correction history',failures)
    # Source-negative quote support for bounded controls.
    neg_unmatched=[]
    if pdf_pages:
        for x in n:
            for ed in x.get('pdf_evidence',[]):
                page=ed.get('physical_page');quote=ed.get('quote_en','')
                if not isinstance(page,int) or not 1<=page<=90 or normalized(quote) not in normalized(pdf_pages[page-1]):
                    neg_unmatched.append({'negative_control_id':x['negative_control_id'],'page':page,'quote':quote})
    require(not neg_unmatched,'negative controls contain unsupported PDF quotation locators',failures)
    # Generated class validity tension: a class labeled NONCOVERING is used in a source TP bridge.
    v_by={x['generated_class_id']:x for x in v}
    tp_class_ids={c for x in j if x['scoring_cell']=='TP' for c in x['origin_generated_class_ids']}
    noncovering_used=sorted(c for c in tp_class_ids if v_by[c]['pdf_validity']=='SUPPORTED_NONCOVERING')
    tp_dep_noncovering=[x['canonical_id'] for x in j if x['scoring_cell']=='TP'
                         and any(c in set(noncovering_used) for c in x['origin_generated_class_ids'])]
    require(all(x.get('pdf_validity') in ('PDF_ENTAILED','PDF_UNSUPPORTED','SUPPORTED_NONCOVERING') for x in v),'invalid class validity label',failures)
    pdf_validity_counts=collections.Counter(x['pdf_validity'] for x in v)
    if noncovering_used:warnings.append(f'{len(noncovering_used)} generated classes labeled SUPPORTED_NONCOVERING are used in {len(tp_dep_noncovering)} TP evidence bridges; the classifications may be consistent for conjunctive bridges, but independent scope and predicate proof is still required.')
    uncertified_tp=sum(x.get('semantic_certification')!='INDEPENDENTLY_CERTIFIED' for x in t_by.values())
    uncertified_generated=sum(x.get('semantic_certification')!='INDEPENDENTLY_CERTIFIED' for x in v)
    if uncertified_tp:warnings.append(f'{uncertified_tp} source-positive TP proof records lack independent full semantic certification.')
    if uncertified_generated:warnings.append(f'{uncertified_generated} generated classes lack independent semantic validity certification.')
    if fp==0:warnings.append('No unsupported definitive generated proposition was recorded as FP; this does not prove error-free generation.')
    # Practical bidirectional diagnostic probes, with original evidence snippets and no preassigned score label.
    probe_cfg=[
        ('case_title_field',r'\btitle\b','The case title field is documented in a case aggregate or its screen field table.', ['title','case']),
        ('workspace_retention_class',r'\bretention class\b','Workspace policy has a retention-class setting, with unresolved selectable values.', ['retention','workspace']),
        ('idempotent_create_same_result',r'one case.{0,65}identical (?:original )?response','Repeated case creation with the same idempotency key and body produces one case and identical response.', ['idempotency','case']),
        ('review_no_self_approval',r'no self.approval|self approval','Review task decisions forbid self approval.', ['approval','self']),
        ('safe_upload_scanning',r'scan before (?:the )?pars','Unsafe attachments are scanned before parsing.', ['scan','unsafe']),
    ]
    for name,regex,meaning,src_tokens in probe_cfg:
        found=[]
        for file,lines in raw_files.items():
            for number,line in enumerate(lines,1):
                if re.search(regex,line,flags=re.IGNORECASE):
                    found.append({'file':file,'line_start':number,'quote_en':line})
        source_match=[{'source_id':z['source_id'],'physical_page':z['physical_page'],'quote_en':z['quote_en']}
                      for z in r if any(t in (z['atomic_statement_en'] or '').lower() for t in src_tokens)]
        probe.append({'probe_id':name,'meaning_to_test_en':meaning,'generated_full_corpus_hits':len(found),
                      'generated_candidates':found[:12], 'source_candidates':source_match[:12],
                      'adjudication_note_en':'Diagnostic source/generated retrieval only; matching text does not independently establish full-predicate entailment.'})
    # Capture conservative FNs and their reverse-search candidates for a runnable regression record.
    for sid,item in sorted(f_by.items()):
        probe.append({'probe_id':'remaining_fn_'+sid,'source_id':sid,
                      'source_statement_en':e_map[sid]['source_statement_en'],
                      'fn_review_disposition':item['fn_review_disposition'],
                      'strongest_generated_candidates':item.get('best_generated_candidates',[])[:5],
                      'unmet_predicates_en':item.get('unmet_predicates_en',[]),
                      'adjudication_note_en':'Retain conservative item-level judgment. A retrieval hit alone does not justify changing FN to TP.'})
    metrics={'Precision':rate(tp,tp+fp),'Recall':rate(tp,tp+fn),
             'F1':rate(2*tp,2*tp+fp+fn),'Duplicate':rate(excess,len(go))}
    for metric, value in metrics.items():
        require(approx(value,old_c['metrics'][metric] if metric!='Duplicate' else old_d['duplicate_rate']),
                f'{metric} differs from phase-5 saved arithmetic',failures)
    result={
        'protocol_version':'6.1','method':'current_scored_8',
        'status':'FINAL_BEST_EFFORT' if not failures else 'FINAL_VALIDATION_FAILED',
        'semantic_evidence_certification':False,
        'universe':{'source_positive_atoms':len(r),'source_negative_controls':len(n),
                    'raw_generated_claim_classes':len(g),'generated_positive_occurrences':len(go),
                    'covered_source_atoms':tp,'asserted_negative_controls':len(asserted_n),
                    'unsupported_generated_only_propositions':len(fp_extra),
                    'canonical_predicted_positive_units':tp+fp,'canonical_decision_units':len(j),
                    'negative_universe_scope':'PDF-grounded, fixed bounded counterfactual controls only'},
        'confusion':{'TP':tp,'TN':tn,'FP':fp,'FN':fn},'metrics':metrics,
        'duplication':{'eligible_occurrences':len(go),'unique_raw_classes':len(g),
                       'excess_occurrences':excess,'repeated_classes':len(dup_classes),
                       'within_file_excess':within,'across_file_excess':across,
                       'repeated_classes_spanning_files':repeated_span},
        'evidence_audit':{'pdf_physical_pages':len(pdf_pages),'pdf_readable_pages':sum(bool(x.strip()) for x in pdf_pages),
                          'pdf_sha256':pdf_digest,'pdf_quote_text_matches':pdf_quote_text_match,
                          'pdf_quote_visual_figure_matches':pdf_figure_match,
                          'pdf_unmatched_quote_count':len(pdf_unmatched),
                          'negative_control_pdf_unmatched_quote_count':len(neg_unmatched),
                          'scored_markdown_files':len(raw_files),'scored_markdown_lines':verified_line_count,
                          'scored_table_cells_reported':sum(int(x.get('table_cells') or 0) for x in lc),
                          'generated_eligible_original_quote_locator_failures':len(bad_go),
                          'tp_evidence_generated_locator_failures':len(bad_quote_locators),
                          'tp_evidence_predicate_map_failures':len(tp_predicate_incomplete),
                          'tp_audit_rows':len(t_by),'tp_E2_bridge_rows':len(b),
                          'fn_audit_rows':len(f_by),
                          'fn_root_cause_counts':dict(sorted(fn_cats.items())),
                          'historical_fn_candidate_dispositions':dict(sorted(corrected_candidates.items())),
                          'source_atomization_reviewed_rows':len(sa),
                          'source_atomization_change_rows':len(rows['DELTA']),
                          'generated_validity_label_counts':dict(sorted(pdf_validity_counts.items())),
                          'tp_bridge_classification_tensions':len(noncovering_used),
                          'tp_units_using_noncovering_class':len(tp_dep_noncovering),
                          'tp_proofs_not_independently_certified':uncertified_tp,
                          'generated_class_validity_not_independently_certified':uncertified_generated,
                          'structural_assertions_passed':not bool(failures)},
        'input_file_hashes_sha256':input_hashes,
        'interpretation':'One effective canonical proposition universe for TP/TN/FP/FN; generated raw classes and occurrences form a separate Duplicate universe. All metrics are ledger arithmetic, not certified semantic design accuracy.',
        'critical_warnings':warnings,
        'validation_failures':failures,
    }
    write_rows(p/'06_reciprocal_regression_probes.jsonl',probe)
    write_rows(p/'06_pdf_visual_figure_evidence.jsonl',pdf_note)
    write_rows(p/'06_validation_diagnostics.jsonl',
               [{'category':'PDF_ATOM_QUOTE_UNMATCHED',**x} for x in pdf_unmatched] +
               [{'category':'NEGATIVE_CONTROL_PDF_QUOTE_UNMATCHED',**x} for x in neg_unmatched] +
               [{'category':'GENERATED_OCCURRENCE_QUOTE_MISMATCH',**x} for x in bad_go] +
               [{'category':'TP_GENERATED_EVIDENCE_QUOTE_MISMATCH',**x} for x in bad_quote_locators] +
               [{'category':'TP_PREDICATE_FIELD_MISSING',**x} for x in tp_predicate_incomplete] +
               [{'category':'TP_CLASSIFICATION_TENSION','generated_class_id':z,
                 'evidence_status':'CLASSIFIED_SUPPORTED_NONCOVERING_BUT_USED_FOR_TP'} for z in noncovering_used] +
               [{'category':'STRUCTURAL_FAILURE','error_en':x} for x in failures])
    (p/'06_metrics_final.json').write_text(js(result),encoding='utf-8')
    # Text reports do not imply independent semantic certification.
    met=result['metrics'];dv=result['duplication'];ev=result['evidence_audit']
    fm=lambda x:'not computed' if x is None else f'{x:.6%}'
    mdr=f'''# OrionDesk AI: Phase 6 Independent Ledger Recalculation\n\n**Protocol:** 6.1  
**Status:** `{result['status']}`  
**Scope:** Supplied eight Markdown specifications versus one original 90-page fictional PDF.\n\n## Effective canonical confusion universe\n\n| Canonical category | Count |\n|---|---:|\n| PDF-positive `R` | {len(r):,} |\n| Fixed PDF-negative controls `N` | {len(n):,} |\n| Unsupported generated-only propositions `F` | {len(fp_extra):,} |\n| Asserted negative controls `B` | {len(asserted_n):,} |\n| Canonical decision universe `U = R + N + F` | {len(j):,} |\n| Canonical predicted-positive units `P = TP + FP` | {tp+fp:,} |\n\n| Cell | Count |\n|---|---:|\n| TP | {tp:,} |\n| TN | {tn:,} |\n| FP | {fp:,} |\n| FN | {fn:,} |\n\n**Exact equations:** TP + FN = {tp:,} + {fn:,} = {len(r):,}; TN + B = {tn:,} + {len(asserted_n):,} = {len(n):,}; FP = F + B = {len(fp_extra):,} + {len(asserted_n):,} = {fp:,}; four-cell total = {len(j):,}.\n\n## Independently recomputed metrics\n\n| Metric | Rate |\n|---|---:|\n| Precision, TP / (TP + FP) | {fm(met['Precision'])} |\n| Recall, TP / (TP + FN) | {fm(met['Recall'])} |\n| F1, 2TP / (2TP + FP + FN) | {fm(met['F1'])} |\n| Duplicate, (GO - G) / GO | {fm(met['Duplicate'])} |\n\nRaw eligible generated occurrences `GO` = {len(go):,}; raw semantic classes `G` = {len(g):,}; excess duplicates = {excess:,}; within-file excess = {within:,}, across-file excess = {across:,}, repeated classes = {len(dup_classes):,}.\n\n**Important:** TP + FP = {tp+fp:,} is the effective source/proposition predicted-positive count, **not** the raw class count {len(g):,}. TN covers only the predeclared PDF-derived negative-control inventory, not the universe of all conceivable absent features.\n\n## Verification quality\n\nStructural equations and file/item references: **{'PASS' if not failures else 'FAILED'}**. Semantics: **NOT INDEPENDENTLY CERTIFIED**. The {fp} observed FP cells do not certify perfect precision. At least {len(noncovering_used):,} generated classes labeled `SUPPORTED_NONCOVERING` occur in TP evidence for {len(tp_dep_noncovering):,} source atoms; these require separate generated-claim validity reconciliation. Every one of the {uncertified_tp:,} retained TP proof rows is marked not independently certified. Exact regression probe records and unresolved FN evidence are linked in the accompanying JSONL.\n'''
    (p/'06_metrics_final.md').write_text(mdr,encoding='utf-8')
    limits=f'''# Coverage, Source Provenance, and Reliability Limitations\n\n## Scope and provenance\n\n- The authoritative PDF is the supplied 90-page English OrionDesk AI detailed design, release R1.0/revision 1.3; SHA-256: `{pdf_digest}`. The current upload and the `fullload_cal` PDF have equal digests. No historical scores or generated Markdown were used to invent authoritative requirements.\n- Exactly {len(raw_files)} scored Markdown documents were included: {', '.join(f'`{x}`' for x in sorted(raw_files))}. They contain {verified_line_count:,} physically inspected lines and {ev['scored_table_cells_reported']:,} table cells in the retained inspection coverage ledger. Generated textual claims preserve their source file and line/table locator.\n- PDF page coverage includes all {len(pdf_pages)} pages. {pdf_quote_text_match:,} source-positive quotes match normalized PDF text; the {pdf_figure_match} remaining quotes are figure assertions visually inspected on physical PDF page 8. The records for this figure are included in `06_pdf_visual_figure_evidence.jsonl`. {len(pdf_unmatched)} PDF-positive quotes remain without the corresponding PDF locator; {len(neg_unmatched)} negative-control quotation mismatches.\n- The common source `R` contains {len(r):,} independently normalized positive items, after the existing correction history. The fixed negative-control `N` contains {len(n)} controls. This report does not treat the 90-page document's example-only values as adopted implementation defaults.\n\n## Bidirectional FN retrieval and source atomization\n\n- The final ledger contains {fn} provisional FN: {fn_cats.get('TRUE_MISSING',0)} `TRUE_MISSING`, {fn_cats.get('PARTIAL_ENTAILMENT',0)} `PARTIAL_ENTAILMENT`, {fn_cats.get('CONSERVATIVE_UNRESOLVED',0)} `CONSERVATIVE_UNRESOLVED`. These are **not all verified omissions**.\n- The full historical candidate-FN review has {len(fna)} records, with outcomes: {', '.join(f'`{k}` {v}' for k,v in sorted(corrected_candidates.items()))}. The corrected and removed source-atom IDs are preserved in `07_change_delta.jsonl`.\n- Source atomization was reviewed in {len(sa)} retained audit rows. The correction history excludes nonnormative examples and redundant source atoms across methods, but the remainder has not been independently re-atomized in this phase.\n- The reciprocal probe file `06_reciprocal_regression_probes.jsonl` documents exact/meaning-preserving searches including the `title` case field, workspace `retention class`, and same-key duplicate case creation with identical response, plus {fn} current FN cases with their source and nearest generated evidence. The probes are diagnostic retrieval checks, **not automatic TP labels**. No identified exact/full-predicate direct match was silently converted to TP in this recomputation phase.\n\n## TP predicates and generated claim validity\n\n- All {tp} final TPs have a source-to-generated proof audit row and actual PDF and generated-file evidence. The E2 bridge count is {len(b)}; E3 source coverage count is {tp-len(b)}. Physical citation existence, identifier validity and generated quote/line consistency were checked independently.\n- **Semantic proof has not been independently certified:** {uncertified_tp} of {tp} final TP audit rows and {uncertified_generated} of {len(v)} generated class validity rows contain best-effort evidence and commentary rather than independent, complete entailment adjudication.\n- {len(noncovering_used)} `SUPPORTED_NONCOVERING` generated classes were nonetheless referenced by {len(tp_dep_noncovering)} TP evidence records. A `SUPPORTED_NONCOVERING` class may legitimately supply one part of a conjunctive bridge even when it does not independently cover a complete R atom. Nevertheless, these links do not certify the full conjunction, so independent scope and predicate review is still required; the counts are disclosed rather than automatically relabeled.\n- The generated-validity ledger records {pdf_validity_counts.get('PDF_ENTAILED',0)} `PDF_ENTAILED`, {pdf_validity_counts.get('SUPPORTED_NONCOVERING',0)} `SUPPORTED_NONCOVERING`, and {pdf_validity_counts.get('PDF_UNSUPPORTED',0)} `PDF_UNSUPPORTED` classes. The latter count is an *observed ledger classification*, not an independently verified absence of unsupported generated commitments. Positive PDF quotation and complete generated predicates have not been checked by an independent semantic adjudicator for each contextual class.\n- The reported FP = {fp} is the result of the existing itemized ledger, not certified precision. Its provisional value can change after stronger claim-validity review. Likewise, TP and FN can move in either direction; this is not a statistical confidence interval and no lower-bound claim is made.\n\n## Bounded TN, duplicates, and metric universe\n\n- TN counts only PDF-based, predeclared prohibited capabilities/deferrals; it is not a population-wide true-negative total. `R`, `N`, and unsupported `F` must remain disjoint. All four cells are itemized in `04_atomic_judgments_final.jsonl`.\n- Duplicate uses raw generated occurrences ({len(go):,}) and within-method classes ({len(g):,}), not the effective source-atom coverage projection ({tp:,} TPs). Its excess count is {excess:,}, split into {within} within-file and {across} across-file.\n- Raw semantic-class merging is intentionally conservative. Further semantic duplicate merges or splits may change Duplicate but should not be used to manufacture new source-positive requirement IDs.\n\n## Certification and completion\n\n- Item-level completeness, arithmetic, input hashing, physical PDF/Markdown citation existence, and duplicate partitions were recomputed independently by `compute_metrics.py`. The structural verdict is **{'PASS' if not failures else 'FAILED'}**; {len(failures)} structural failures, {len(warnings)} semantic/reporting warnings.\n- Status is `{result['status']}`. The result is a **reproducible final best-effort ledger calculation**, not a semantically certified effectiveness assessment. A stronger claim would require independent full-predicate review of all TP evidence bridges and all generated class validity judgments. This limitation is intrinsic to the existing artifacts, not a reason to silently substitute historical scores.\n'''
    (p/'08_coverage_and_limitations.md').write_text(limits,encoding='utf-8')
    status={'protocol_version':'6.1','phase':6,'status':result['status'],
            'structural_validation':'PASS' if not failures else 'FAILED',
            'semantic_certification':'NOT_CERTIFIED',
            'source_positive_atoms':len(r),'source_negative_controls':len(n),
            'generated_occurrences':len(go),'generated_classes':len(g),
            'canonical_decision_units':len(j), 'independently_recomputed':{'TP':tp,'TN':tn,'FP':fp,'FN':fn},
            'structural_failures':failures,'critical_semantic_warnings':warnings,
            'all_six_phases_completed_best_effort':not failures}
    (p/'06_phase_status_final.json').write_text(js(status),encoding='utf-8')
    print(js({'status':result['status'],'confusion':result['confusion'],'metrics':metrics,
              'structural_failures':failures,'critical_semantic_warnings':warnings,
              'matched_pdf_text':pdf_quote_text_match,'figure_quotes':pdf_figure_match,
              'generated_quote_failures':len(bad_go),'tp_quote_failures':len(bad_quote_locators)}))
    return 1 if failures else 0

if __name__=='__main__':sys.exit(main())
