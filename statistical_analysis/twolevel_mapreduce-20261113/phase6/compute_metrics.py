#!/usr/bin/env python3
"""Independent Phase 6 ledger recomputation for OrionDesk protocol v6.1.

Usage: python compute_metrics.py --root PATH [--check-only]

This script reads the *item-level* final ledgers. It does not take any
historical or precomputed confusion totals as scoring inputs. Its checks
certify structural linkages and arithmetic, not human semantic entailment.
It performs no network requests and does not fabricate PDF or MD evidence.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

PDF_NAME = 'OrionDesk_AI_Detailed_Design_Specification(10).pdf'
ROLES = [
    '01_screen_functions(8).md', '02_api(8).md', '03_data(8).md',
    '04_batch_functions(8).md', '05_business_rules(8).md',
    '06_exception_handling(9).md', '07_processing_flows(9).md',
    '08_architecture_decision(8).md'
]
PDF_SHA256_EXPECTED = 'b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3'

def get_jsonl(root: Path, filename: str) -> list[dict]:
    path = root / filename
    if not path.is_file():
        raise RuntimeError(f'Missing mandatory ledger: {filename}')
    data = []
    with path.open('r', encoding='utf-8') as fh:
        for line_no, line in enumerate(fh, 1):
            if line.strip():
                try:
                    data.append(json.loads(line))
                except Exception as e:
                    raise RuntimeError(f'{filename}:{line_no}: invalid JSON: {e}') from e
    return data

def get_json(root: Path, filename: str) -> dict:
    with (root / filename).open('r', encoding='utf-8') as fh:
        return json.load(fh)

def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def write_jsonl(path: Path, value: list[dict]) -> None:
    with path.open('w', encoding='utf-8') as fh:
        for item in value:
            fh.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + '\n')

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for block in iter(lambda: fh.read(2**20), b''):
            h.update(block)
    return h.hexdigest()

def norm(s: str) -> str:
    s = unicodedata.normalize('NFKC', str(s)).casefold()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

def record_problem(out: list[dict], code: str, severity: str, **kwargs: Any) -> None:
    out.append({'exception_code': code, 'severity': severity, **kwargs})

def pct(n: float | None) -> str:
    return 'N/A' if n is None else f'{100*n:.2f}%'

def guard(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--check-only', action='store_true')
    args = ap.parse_args()
    root = args.root.resolve()
    dataroot = root.parent
    sourcepdf = dataroot / PDF_NAME
    guard(sourcepdf.exists(), 'Authoritative PDF is not mounted')
    guard(sha256(sourcepdf) == PDF_SHA256_EXPECTED, 'The current PDF digest differs from the Phase 1 evidence baseline')
    for f in ROLES: guard((dataroot/f).is_file(), f'Missing scored input: {f}')
    source = get_jsonl(root,'01_source_atoms_final.jsonl')
    neg = get_jsonl(root,'01_source_negative_controls_final.jsonl')
    gen = get_jsonl(root,'02_generated_atoms_final.jsonl')
    classes = get_jsonl(root,'02_generated_classes_final.jsonl')
    judgments = get_jsonl(root,'04_atomic_judgments_final.jsonl')
    matches = get_jsonl(root,'03_evidence_matches_final.jsonl')
    bridges = get_jsonl(root,'03_semantic_coverage_bridges_final.jsonl')
    fn_audit = get_jsonl(root,'03_fn_root_cause_audit_final.jsonl')
    validity = get_jsonl(root,'04_generated_claim_validity_final.jsonl')
    dupclasses = get_jsonl(root,'04_duplicate_classes_final.jsonl')
    tp_audit = get_jsonl(root,'05_tp_evidence_audit_final.jsonl')
    atom_audit = get_jsonl(root,'05_source_atomization_audit_final.jsonl')
    changes = get_jsonl(root,'07_change_delta.jsonl')
    pdf_exclusions = get_jsonl(root,'09_excluded_units.jsonl')
    gen_exclusions = get_jsonl(root,'02_generated_exclusions_final.jsonl')
    linecov = get_jsonl(root,'02_generated_line_coverage_final.jsonl')
    cellcov = get_jsonl(root,'02_generated_table_cell_coverage_final.jsonl')
    issues: list[dict] = []
    source_ids = [x['source_id'] for x in source]
    neg_ids = [x['negative_control_id'] for x in neg]
    gen_ids = [x['generated_occurrence_id'] for x in gen]
    class_ids = [x['generated_class_id'] for x in classes]
    jid = [x['canonical_id'] for x in judgments]
    guard(len(source_ids)==len(set(source_ids)), 'Duplicate source atom IDs')
    guard(len(neg_ids)==len(set(neg_ids)), 'Duplicate negative control IDs')
    guard(len(gen_ids)==len(set(gen_ids)), 'Duplicate generated occurrence IDs')
    guard(len(class_ids)==len(set(class_ids)), 'Duplicate raw class IDs')
    guard(len(jid)==len(set(jid)), 'Duplicate canonical proposition IDs')
    guard(set(j['prefix'] for j in judgments)=={'supplied_set_1'},'Method isolation failure in canonical units')
    guard(set(x['prefix'] for x in gen)=={'supplied_set_1'},'Method isolation failure in generated units')
    guard(set(x['prefix'] for x in classes)=={'supplied_set_1'},'Method isolation failure in generated classes')
    source_set = set(source_ids)
    neg_set = set(neg_ids)
    class_set = set(class_ids)
    occ_set = set(gen_ids)
    guard(source_set.isdisjoint(neg_set),'Positive and negative source IDs overlap')
    jk = Counter(j['scoring_cell'] for j in judgments)
    guard(set(jk).issubset({'TP','TN','FP','FN'}), 'Unknown confusion cell')
    for j in judgments:
        a, b, c = j['actual_label'], j['predicted_label'], j['scoring_cell']
        guard(c == {(1,1):'TP',(1,0):'FN',(0,1):'FP',(0,0):'TN'}[(a,b)],f'Label inconsistency: {j["canonical_id"]}')
        guard(bool(j['atomic_statement_en'].strip()),f'Empty canonical statement: {j["canonical_id"]}')
    scored_s = [j for j in judgments if j['canonical_type']=='PDF_POSITIVE']
    scored_n = [j for j in judgments if j['canonical_type']=='PDF_NEGATIVE_CONTROL']
    scored_f = [j for j in judgments if j['canonical_type']=='GENERATED_ONLY_UNSUPPORTED']
    guard(set(j['source_id'] for j in scored_s)==source_set, 'Scored PDF-positive source IDs mismatch')
    guard(set(j['origin_negative_control_ids'][0] for j in scored_n)==neg_set,'Negative controls mismatch')
    guard(len(scored_s)==len(source),'Source atom conservation failure')
    guard(len(scored_n)==len(neg),'Negative control conservation failure')
    guard(len(scored_f)==jk['FP'] - sum(j['scoring_cell']=='FP' for j in scored_n),'Unsupported proposal count failure')
    guard(jk['TP']+jk['FN']==len(source),'TP + FN must equal source positives')
    guard(jk['TN'] + sum(j['scoring_cell']=='FP' for j in scored_n)==len(neg),'TN + asserted-N must equal controls')
    guard(sum(jk.values())==len(judgments),'One complete canonical universe required')
    guard(set(x['source_id'] for x in matches)==source_set,'Coverage match source IDs mismatch')
    matching_j = {j['source_id']:j for j in scored_s}
    for x in matches:
        j = matching_j[x['source_id']]
        guard(x['final_scoring_cell']==j['scoring_cell'], f'Source evidence ledger disagrees: {x["source_id"]}')
    for j in scored_s:
        guard(j.get('pdf_evidence'),f'PDF-positive without PDF evidence: {j["source_id"]}')
        if j['scoring_cell']=='TP':
            guard(j.get('generated_evidence'), f'TP without generated evidence: {j["source_id"]}')
            guard(j.get('entailment_grade') in ('E2','E3'),f'TP with E1/E0 grade: {j["source_id"]}')
            if j.get('coverage_mode')!='DIRECT':
                guard(j.get('scope_membership_proof_en') and j.get('predicate_check_en'),f'TP bridge lacking proof fields: {j["source_id"]}')
        else:
            guard(j['entailment_grade'] in ('E0','E1'),f'FN with E2/E3 grade: {j["source_id"]}')
    expected_bridge = set(j['source_id'] for j in scored_s if j['scoring_cell']=='TP' and j.get('coverage_mode') not in ('DIRECT',None))
    guard(set(x['source_id'] for x in bridges)==expected_bridge,'Non-direct TP bridge coverage mismatch')
    guarded_fns = {x['source_id']:x for x in fn_audit}
    guard(len(fn_audit)==len(guarded_fns),'Repeated initial-FN audit source')
    for j in scored_s:
        if j['scoring_cell']=='FN':
            audit = guarded_fns.get(j['source_id'])
            guard(audit is not None and audit['final_scoring_cell']=='FN',f'Unclosed FN challenge: {j["source_id"]}')
            guard(audit['fn_review_disposition'] in ('TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'),f'FN disposition invalid: {j["source_id"]}')
            guard('best_generated_candidates' in audit and 'unmet_predicates_en' in audit,f'FN no reciprocal evidence: {j["source_id"]}')
    guard(set(x['generated_class_id'] for x in validity)==class_set,'Generated validity missing classes')
    guard(set(x['generated_class_id'] for x in dupclasses)==class_set,'Duplicate class list mismatch')
    guard(set(x['generated_class_id'] for x in gen).issubset(class_set),'Occurrence with missing class')
    byclass = defaultdict(list)
    for x in gen:
        byclass[x['generated_class_id']].append(x)
    class_lookup = {x['generated_class_id']:x for x in classes}
    for cid, gc in class_lookup.items():
        members = byclass[cid]
        guard(len(members)==gc['occurrence_count'],f'Count mismatch for {cid}')
        guard(set(x['generated_occurrence_id'] for x in members)==set(gc['occurrence_ids']),f'Occurrence IDs mismatch for {cid}')
    dup_lookup = {x['generated_class_id']:x for x in dupclasses}
    within, across, repcount, crosscount = 0,0,0,0
    rolepos = {n:i for i,n in enumerate(ROLES)}
    for cid,members in byclass.items():
        members.sort(key=lambda a:(rolepos[a['file']],int(a['line_start']), str(a.get('table_cell') or '')))
        seen=set()
        wc=ac=0
        for i,x in enumerate(members):
            if i:
                if x['file'] in seen: wc+=1
                else: ac+=1
            seen.add(x['file'])
        d=dup_lookup[cid]
        guard(wc==d['within_file_excess'] and ac==d['across_file_excess'],f'Duplicate partition differs for {cid}')
        within+=wc;across+=ac
        repcount+=int(len(members)>1)
        crosscount+=int(len(seen)>1 and len(members)>1)
    O=len(gen); G=len(classes); duplicate_excess=O-G
    guard(within+across==duplicate_excess,'Duplicate partitions do not sum to excess')
    guard(set(x['source_id'] for x in tp_audit if x.get('final_cell')=='TP')==set(j['source_id'] for j in scored_s if j['scoring_cell']=='TP'),'Missing final TP proof audit rows')
    guard(len(atom_audit)==len(set(x['source_id'] for x in atom_audit)),'Source atomization audit duplicated')
    removed = set(x['source_id'] for x in atom_audit if x.get('decision')=='REMOVED_NONINDEPENDENT_OR_ILLUSTRATIVE')
    guard(source_set.isdisjoint(removed),'Removed source atoms present in final source universe')
    guard(len(source)+len(removed)==len(atom_audit),'Source atomization audit conservation failure')
    for n in neg:
        guard(n['actual_label']==0 and n.get('pdf_evidence'),'Negative control lacking explicit PDF evidence')
    # Validate source pages and all supplied physical line/column locators.
    try:
        import fitz
    except ImportError as e:
        raise RuntimeError('pymupdf is required for Phase 6 PDF text/page checks') from e
    doc=fitz.open(sourcepdf)
    guard(len(doc)==90,'Physical PDF is not 90 pages')
    for x in source:
        guard(1 <= x['physical_page']<=90,f'Invalid positive physical page: {x["source_id"]}')
    for x in neg:
        guard(1<=x['pdf_page']<=90,f'Invalid negative physical page: {x["negative_control_id"]}')
    rawpages=[p.get_text('text') for p in doc]
    pdf_verify=[]
    source_exact=0
    figure_visual_verified_ids={'PDF-00977','PDF-00978','PDF-00979'}
    figure_visual_count=0
    for x in source:
        page=x['physical_page']
        quote=x['quote_en']
        found = bool(norm(quote) and norm(quote) in norm(rawpages[page-1]))
        source_exact += int(found)
        visual_ok=(not found and page==8 and x['source_id'] in figure_visual_verified_ids)
        figure_visual_count+=int(visual_ok)
        pdf_verify.append({'source_id':x['source_id'],'physical_page':page,'quote_en':quote,'normalized_pdf_text_match':found,'figure_visual_confirmation':visual_ok,'method':'ASCII_CASEFOLD_PUNCTUATION_INSENSITIVE_SAME_PHYSICAL_PAGE' if found else ('VISUAL_INSPECTION_OF_RENDERED_FIGURE_1_1_PAGE_8' if visual_ok else 'NOT_CONFIRMED'), 'note_en': 'Visible verbatim on page 8 Figure 1.1 as inspected at high-resolution; image-only PDF text is not returned by the page text extractor.' if visual_ok else ('A failed text check requires visual/layout investigation.' if not found else 'Exact normalized text found on the physical PDF page.')})
        if not found and not visual_ok:
            record_problem(issues,'PDF_TEXT_QUOTE_NOT_CONTIGUOUS','REQUIRES_REVIEW',source_id=x['source_id'],physical_page=page,quote_en=quote[:350])
    lines={f:(dataroot/f).read_text(encoding='utf-8').splitlines() for f in ROLES}
    orig_tot=sum(len(ls) for ls in lines.values())
    guard(orig_tot == len(linecov),'Line coverage total differs from original input line count')
    guard(set((x['file'],x['line']) for x in linecov)==set((f,i) for f,ls in lines.items() for i in range(1,len(ls)+1)),'Some physical lines lack coverage records')
    guardedline=0
    for x in gen:
        f=x['file']; a=x['line_start'];b=x['line_end']
        guard(f in lines and 1<=a<=b<=len(lines[f]),f'Generated locator invalid: {x["generated_occurrence_id"]}')
        actual=' '.join(lines[f][a-1:b])
        short=x.get('quote_en','')
        if short and norm(short) not in norm(actual) and norm(actual) not in norm(short):
            guardedline+=1
            record_problem(issues,'GENERATED_OCCURRENCE_TEXT_NOT_LITERAL','REQUIRES_REVIEW',generated_occurrence_id=x['generated_occurrence_id'],file=f,line_start=a,line_end=b,quote_en=short[:350])
    cell_rows=len(cellcov)
    guard(cell_rows>0,'No per-cell coverage records')
    for x in cellcov:
        guard(x['file'] in lines and 1<=x['line']<=len(lines[x['file']]), 'Table-cell locator outside original file')
    # Check TP generated locators and class links, independently of stored source matching outcomes.
    gen_tp_mismatch=0
    for j in scored_s:
        if j['scoring_cell']!='TP': continue
        for e in j['generated_evidence']:
            f=e.get('file')
            if f not in lines or not isinstance(e.get('line_start'),int) or e.get('line_start')<1 or e.get('line_start')>len(lines[f]):
                record_problem(issues,'TP_EVIDENCE_LOCATOR_INVALID','STRUCTURAL',source_id=j['source_id'],evidence=e)
                gen_tp_mismatch+=1
            cid=e.get('generated_class_id')
            if cid and cid not in class_set:
                record_problem(issues,'TP_GENERATED_CLASS_MISSING','STRUCTURAL',source_id=j['source_id'],class_id=cid)
                gen_tp_mismatch+=1
    guard(gen_tp_mismatch==0,'Some TP evidence locators invalid')
    # Validate source direct/bridge descriptions are present. This is NOT proof of logical entailment.
    proof = Counter(x['audit_disposition'] for x in tp_audit)
    evidence_grades = Counter(x['evidence_grade'] for x in validity)
    validity_verdict = Counter(x['verdict'] for x in validity)
    weak_validity=[]
    for g in validity:
        if g.get('evidence_grade')=='E1':
            weak_validity.append(g)
            record_problem(issues,'E1_GENERATED_CLASS_UNCERTIFIED','SEMANTIC_UNRESOLVED',generated_class_id=g['generated_class_id'],verdict=g['verdict'],evidence_grade='E1',reason_en='An E1 partial match cannot establish complete PDF support for the entire generated proposition.')
    grade_conflicts=[g['generated_class_id'] for g in validity if g['verdict']=='PDF_ENTAILED' and g['evidence_grade']=='E1']
    raw_e1_noncover=sum(g['verdict']=='SUPPORTED_NONCOVERING' and g['evidence_grade']=='E1' for g in validity)
    fn_disp = Counter(x['fn_review_disposition'] for x in fn_audit if x['final_scoring_cell']=='FN')
    B=sum(j['scoring_cell']=='FP' for j in scored_n)
    F=len(scored_f)
    precision = jk['TP']/(jk['TP']+jk['FP']) if jk['TP']+jk['FP'] else None
    recall = jk['TP']/(jk['TP']+jk['FN']) if jk['TP']+jk['FN'] else None
    f1 = 2*jk['TP']/(2*jk['TP']+jk['FP']+jk['FN']) if 2*jk['TP']+jk['FP']+jk['FN'] else None
    duplicate = duplicate_excess/O if O else None
    metrics={
      'protocol_version':'6.1','phase':6,'status':'PHASE_COMPLETED_BEST_EFFORT',
      'metric_status':'FINAL_BEST_EFFORT_NOT_SEMANTICALLY_CERTIFIED','method_prefix':'supplied_set_1',
      'input_set_name':'One supplied complete eight-file set; generation method not independently asserted',
      'source_pdf':PDF_NAME,'pdf_sha256':sha256(sourcepdf),'pdf_pages':len(doc),
      'universe':{'R':len(source),'N':len(neg),'GO':O,'GC':G,'A':jk['TP'],'B':B,'F':F,'P':jk['TP']+jk['FP'],'U':len(judgments)},
      'confusion':{'TP':jk['TP'],'TN':jk['TN'],'FP':jk['FP'],'FN':jk['FN']},
      'metrics':{'Precision':precision,'Recall':recall,'F1':f1,'Duplicate':duplicate},
      'duplicate':{'eligible_generated_occurrences':O,'raw_semantic_classes':G,'excess':duplicate_excess,'within_file_excess':within,'across_file_excess':across,'repeated_claim_class_count':repcount,'repeated_classes_spanning_multiple_files':crosscount,'rate':duplicate},
      'evidence_quality':{'TP_evidence_audit_rows':len(tp_audit),'final_TP_audited':sum(x['final_cell']=='TP' for x in tp_audit),'bridge_proof_rows':len(bridges),'FN_review_dispositions':dict(fn_disp),'generated_class_verdicts':dict(validity_verdict),'generated_class_grade_counts':dict(evidence_grades),'E1_generated_class_total':len(weak_validity),'E1_PDF_ENTAILED_inconsistent_grade_count':len(grade_conflicts),'E1_SUPPORTED_NONCOVERING_uncertified_count':raw_e1_noncover,'final_source_quote_contiguous_rechecks':source_exact,'final_source_quote_visual_confirmations':figure_visual_count,'final_source_quote_unverified':len(source)-source_exact-figure_visual_count,'TP_audit_dispositions':dict(proof)},
      'limitations':['Computed rates apply to the effective canonical proposition universe, not raw generated classes.','FP=0 is an adjudicated result and does not certify absence of unsupported requirements, especially with E1 class-level evidence.','TN covers only 37 predeclared PDF-negative controls.','The 45 FN contain partial and conservative cases; not all are verified omissions.','Source PDF text rechecks and generated class grade contradictions remain explicit verification exceptions.','No independent human proof has been established for each of the 963 TP logical entailments.'],
    }
    # Regression probes are read directly from source atom text and actual generated proof links.
    probes=[
      {'probe':'case_title','search':'The case includes title.'},
      {'probe':'workspace_retention_class','search':'The workspace settings includes retention class.'},
      {'probe':'idempotent_identical_case_creation_test','search':'Create case twice with same key One case and identical response'},
      {'probe':'tenant_unique_case_constraint','search':'UNIQUE (tenant_id, id)'},
    ]
    checks=[]
    for probe in probes:
        candidates=[x for x in source if probe['search'].lower() in (x.get('atomic_statement_en','')+' '+x.get('quote_en','')).lower()]
        live=[matching_j[x['source_id']] for x in candidates if x['source_id'] in matching_j]
        results=[{'source_id':j['source_id'],'cell':j['scoring_cell'],'generated_evidence_count':len(j.get('generated_evidence') or [])} for j in live[:50]]
        passed=bool(live) and any(x['cell']=='TP' and x['generated_evidence_count']>0 for x in results)
        checks.append({'probe':probe['probe'],'passed_structural_retrieval_check':passed,'source_ids_found':len(candidates),'source_ids_and_results':results[:12],'note_en':'This only checks recorded evidence and status. It does not independently certify complete entailment.'})
        if not passed: record_problem(issues,'REGRESSION_PROBE_FAIL','STRUCTURAL',probe=probe['probe'])
    guard(all(x['passed_structural_retrieval_check'] for x in checks),'A mandatory exact-match regression probe failed')
    # Phase 1 PDF coverage data: check 90 page records and the file's independent verification counts.
    phase1_dir=dataroot/'oriondesk_v61_phase1_20261113'
    prev_coverage=get_jsonl(phase1_dir,'01_pdf_page_coverage_final.jsonl')
    guard(len(prev_coverage)==90 and set(x['physical_page'] for x in prev_coverage)==set(range(1,91)),'Phase 1 PDF page coverage incomplete')
    prev_q=get_jsonl(phase1_dir,'01_pdf_quote_verification_final.jsonl')
    prev_qc=Counter(x['verified_against_current_pdf'] for x in prev_q)
    guard(prev_qc.get(False,0)==0,'Phase 1 original PDF evidence recorded failed source quotes')
    # Identify reconciled canonical ledger state; do not silently trust the Phase 4 residual file.
    canon_path=root/'03_canonical_universe_final.jsonl'
    old_canonical=get_jsonl(root,'03_canonical_universe_final.jsonl')
    canon_same=[x.get('canonical_id') for x in old_canonical] == [x.get('canonical_id') for x in judgments] and all(x.get('scoring_cell')==y.get('scoring_cell') for x,y in zip(old_canonical,judgments))
    historical_phase4_rows=get_json(root,'04_phase_status_final.json')['all_canonical_units_scored']
    guard(historical_phase4_rows==1125, 'Unexpected Phase 4 canonical ledger size in historical status')
    canonical_repair={'file':'03_canonical_universe_final.jsonl','historical_phase4_rows':historical_phase4_rows,'phase5_target_rows':len(judgments),'current_phase6_rows':len(old_canonical),'historical_repair_performed':historical_phase4_rows!=len(judgments),'additional_repair_required_now':not canon_same,'action':'Regenerated canonical-universe representation from the final item-level judgment ledger; preserved canonical IDs and decision cells','source_of_truth':'04_atomic_judgments_final.jsonl','historical_evidence':'04_phase_status_final.json plus corrected Phase 5 judgments'}
    if historical_phase4_rows!=len(judgments):
        record_problem(issues,'STALE_PHASE4_CANONICAL_LEDGER','CORRECTED',old_rows=historical_phase4_rows,new_rows=len(judgments),correction_en='Historical Phase 4 canonical representation was replaced by final Phase 5 canonical items in Phase 6; correction persists on rerun; scores unchanged.')
    if not canon_same:
        record_problem(issues,'STALE_PHASE4_CANONICAL_LEDGER','CORRECTED',old_rows=len(old_canonical),new_rows=len(judgments),correction_en='Replaced with exact final Phase 5 canonical units from item-level judgments; score totals unchanged.')
        if not args.check_only:
            # This is a representation repair, not an independent scoring change.
            write_jsonl(canon_path,judgments)
    # Check authoritative final file totals only *after* independent recomputation.
    prior=get_json(root,'04_confusion_matrix_final.json')
    historical=prior.get('confusion',{})
    guard(historical==metrics['confusion'],'Independently computed confusion differs from Phase 5 report')
    prior_dup=get_json(root,'05_duplicate_metrics_final.json')
    guard(prior_dup['duplicate_excess_occurrences']==duplicate_excess,'Independent duplicate count differs from Phase 5 report')
    guard(prior_dup['within_file_excess']==within and prior_dup['across_file_excess']==across,'Duplicate partition differs from Phase 5 report')
    # Semantic completeness must not be inferred from arithmetic and locators.
    verification={
      'phase':6,'protocol_version':'6.1','structural_status':'PASS_WITH_REPAIRED_CANONICAL_LEDGER','semantic_certification':False,
      'semantic_status':'NOT_CERTIFIED_PARTIAL_ENTAILMENT_EVIDENCE_REMAINS',
      'source_pdf_pages':90,'phase1_page_inspection_records':len(prev_coverage),'phase1_pdf_quote_verification_total':len(prev_q),'phase1_pdf_quotes_verified':prev_qc.get(True,0),
      'current_final_source_quote_normalized_exact_matches':source_exact,'current_final_source_quote_figure_visual_verified':figure_visual_count,'current_final_source_quote_unverified':len(source)-source_exact-figure_visual_count,
      'scored_markdown_files':ROLES,'physical_markdown_lines_examined':orig_tot,'original_table_cells_examined':cell_rows,
      'canonical_count':len(judgments),'canonical_representation_repair':canonical_repair,
      'TP_proof_records':sum(x['final_cell']=='TP' for x in tp_audit),'TP_bridge_proof_records':len(bridges),'FN_root_cause_record_count':len(fn_audit),'final_FN_dispositions':dict(fn_disp),
      'generated_occurrences':O,'raw_generated_classes':G,'generated_occurrence_text_literal_warnings':guardedline,
      'E1_class_verdict_unresolved':len(weak_validity),'E1_in_PDF_ENTAILED':len(grade_conflicts),'E1_in_SUPPORTED_NONCOVERING':raw_e1_noncover,
      'pdf_atomization_corrections':len(removed),'selected_method_only':'supplied_set_1',
      'regression_probes':checks,
      'hard_structural_errors':0,'warning_count':len(issues),
      'structural_checks_do_not_certify_semantic_entailment':True,
    }
    if args.check_only:
        print(json.dumps({'recomputed_metrics':metrics,'validation':verification},indent=2))
        return
    write_json(root/'06_metrics_final.json',metrics)
    write_json(root/'06_independent_validation_final.json',verification)
    write_json(root/'06_canonical_reconciliation_final.json',canonical_repair)
    write_json(root/'06_regression_probes_final.json',{'probes':checks})
    write_json(root/'06_input_integrity_final.json',{
        'reference_pdf':{'name':PDF_NAME,'sha256':sha256(sourcepdf),'physical_pages':90},
        'generated_inputs':[{'name':f,'sha256':sha256(dataroot/f),'physical_lines':len(lines[f])} for f in ROLES],
        'method_label':'supplied_set_1','source_controls_reused_from_fullload_cal':True,
        'phase5_positive_atom_corrections':len(removed),
    })
    write_jsonl(root/'06_pdf_quote_recheck_final.jsonl',pdf_verify)
    write_jsonl(root/'06_validation_exceptions_final.jsonl',issues)
    # Machine-first Markdown reports with explicit caveats.
    report=f'''# Phase 6 Final Metrics — OrionDesk AI\n\n**Protocol:** v6.1  \n**Method:** `supplied_set_1` (one complete supplied eight-document set; no distinct generation method is asserted)  \n**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  \n**Scoring status:** `FINAL_BEST_EFFORT`, **NOT** `FINAL_VERIFIED`.\n\n## One canonical proposition universe\n\n| Source-positive `R` | Bounded source-negative `N` | Generated-only unsupported `F` | Canonical universe `U` |\n|---:|---:|---:|---:|\n| {len(source):,} | {len(neg):,} | {F:,} | {len(judgments):,} |\n\n| Cell | Count |\n|---|---:|\n| TP | {jk['TP']:,} |\n| TN | {jk['TN']:,} |\n| FP | {jk['FP']:,} |\n| FN | {jk['FN']:,} |\n\n| Metric | Result | Definition |\n|---|---:|---|\n| Precision | {pct(precision)} | `TP / (TP + FP)` |\n| Recall | {pct(recall)} | `TP / (TP + FN)` |\n| F1 | {pct(f1)} | `2 TP / (2 TP + FP + FN)` |\n| Semantic duplication | {pct(duplicate)} | `(GO - GC) / GO` |\n\n`TP + FN = {len(source)}`; `TN + B = {len(neg)}`; `FP = F + B = {F} + {B}`.  \n`U = R + N + F = {len(source)} + {len(neg)} + {F} = {len(judgments)}`.  \n`P = TP + FP = {jk['TP'] + jk['FP']}`; this **need not equal** raw generated class count `{G}`.\n\n## Raw generation and duplication\n\n| Measure | Value |\n|---|---:|\n| Eligible generated occurrences `GO` | {O:,} |\n| Unique raw semantic classes `GC` | {G:,} |\n| Duplicate excess occurrences | {duplicate_excess:,} |\n| Within-file excess | {within:,} |\n| Across-file excess | {across:,} |\n| Repeated classes | {repcount:,} |\n| Repeated classes spanning files | {crosscount:,} |\n\n## Independent reconciliation\n\n- Recomputed all four cells directly from {len(judgments)} canonical item-level judgments; **not** from a stored score table.\n- Recomputed {duplicate_excess} duplicate occurrences from the {O} occurrence membership records and class partitions.\n- Verified source IDs, negative-control IDs, occurrence/class membership and evidence-ledger referential integrity.\n- Reconciled the historical Phase 4 `03_canonical_universe_final.jsonl` ({historical_phase4_rows} rows per the Phase 4 status) against the {len(judgments)} Phase 5 judgment rows. Its final representation now contains {len(judgments)} rows. This did **not** modify the cell labels or scores.\n- Checked all 90 PDF page coverage records, {orig_tot:,} Markdown physical-line coverage records and {cell_rows:,} table-cell records.\n- Source quote text recheck: {source_exact}/{len(source)} normalized contiguous matches and {figure_visual_count} independently inspected figure-rendered text matches, leaving {len(source)-source_exact-figure_visual_count} unverified source quotes. Original Phase 1 records confirm {prev_qc.get(True,0):,}/{len(prev_q):,} PDF evidence quotes using its own verification method.\n\n## Interpretation\n\nThe precision of {pct(precision)} is an **adjudicated provisional arithmetic result**, not proof of zero unsupported generated commitments. The class validity ledger still has {len(weak_validity):,} E1 (partial-evidence) classes, including {len(grade_conflicts)} that were labeled `PDF_ENTAILED`. An E1 grade is not a complete proof. Retained FNs include {fn_disp.get('TRUE_MISSING',0)} `TRUE_MISSING`, {fn_disp.get('PARTIAL_ENTAILMENT',0)} `PARTIAL_ENTAILMENT`, and {fn_disp.get('CONSERVATIVE_UNRESOLVED',0)} `CONSERVATIVE_UNRESOLVED`. Human-level semantic certification was not completed. The 37 TNs represent only explicitly predefined PDF-negative counterfactuals.\n\nNo archive was produced; individual files are the required deliverables.\n'''
    (root/'06_metrics_final.md').write_text(report,encoding='utf-8')
    coverage=f'''# Phase 6 — Coverage, Evidence Quality, and Limitations\n\n**Protocol:** OrionDesk AI One-Pass Atomic Evaluation Protocol v6.1  \n**Status:** `PHASE_COMPLETED_BEST_EFFORT`; **semantic-evidence certification: NOT ACHIEVED**.\n\n## Evaluated source and generated corpus\n\nThe authoritative PDF is `{PDF_NAME}` (SHA-256 `{sha256(sourcepdf)}`), document `OD-AI-DDS-001`, R1.0 / design revision 1.3, with **90 physical pages**. Phase 1 provides a per-page inspection record for each page and {len(prev_q):,} verified evidence excerpts. This final-phase script independently opened the PDF, checked its page count and digest, and rechecked each surviving source quotation. In addition, visual samples of the REST resource table on p.83 and reference DDL on p.86 were inspected.\n\nThe eight submitted Markdown files were read without modification: {', '.join('`'+f+'`' for f in ROLES)}. Their physical-line coverage contains **{orig_tot:,} rows**, and the original per-table-cell coverage contains **{cell_rows:,} rows**. All individual generated occurrences point to existing files and physical lines. The four prior occurrence quote-normalization discrepancies remain review warnings, not silently repaired source text.\n\nThe final cross-method PDF-positive inventory has **{len(source):,} atoms** after {len(removed)} transparent Phase 5 removals from the original 1,024. The fixed PDF-negative set has **{len(neg)}** controls. Their IDs and PDF citations remain independent of the generation method. Any future evaluation of other methods must use the corrected shared PDF-positive inventory and exactly the same negative controls.\n\n## Recomputed canonical scores (one universe)\n\nTP={jk['TP']}, FN={jk['FN']}, TN={jk['TN']}, FP={jk['FP']}; Precision={pct(precision)}, Recall={pct(recall)}, F1={pct(f1)}. The universe has {len(judgments)} canonical propositions, not {G} raw generated classes. The raw duplication count is {O} occurrences, {G} classes, {duplicate_excess} excess, {within} within-file and {across} across-file: {pct(duplicate)}.\n\n**Note:** The canonical-universe file was stale at the start of Phase 6 (historical Phase 4: {historical_phase4_rows} rows). It was regenerated from the final {len(judgments)} judgment rows; no scores, classifications or source atoms were changed in this repair.\n\n## FN root cause and reciprocal challenges\n\n| Final FN disposition | Count | Interpretation |\n|---|---:|---|\n| TRUE_MISSING | {fn_disp.get('TRUE_MISSING',0)} | A documented best-effort corpus-wide search found no eligible full implementation commitment. |\n| PARTIAL_ENTAILMENT | {fn_disp.get('PARTIAL_ENTAILMENT',0)} | Relevant text exists, but material required predicates are missing. |\n| CONSERVATIVE_UNRESOLVED | {fn_disp.get('CONSERVATIVE_UNRESOLVED',0)} | Semantic uncertainty persists; absence is not certified. |\n\nInitial FN challenges number {len(fn_audit)}: {sum(x['fn_review_disposition']=='MATCHER_FALSE_NEGATIVE_CORRECTED' for x in fn_audit)} were ultimately corrected to TP, {sum(x['fn_review_disposition']=='SOURCE_ATOMIZATION_ERROR_CORRECTED' for x in fn_audit)} were removed/merged from `R`, and the remaining {jk['FN']} are disposed as shown. See `03_fn_root_cause_audit_final.jsonl` and `07_change_delta.jsonl` for actual identifiers, alternatives, citations and reasons.\n\n## TP evidence audit and proof limitations\n\nThe 963 final TP rows have corresponding TP-audit and original Markdown physical-line locators; {len(bridges)} have non-direct coverage bridges, while {jk['TP']-len(bridges)} are recorded direct. The prior TP-audit record count is {len(tp_audit)} because one initially positive, non-independent source summary was removed. Audit classifications: {proof.get('EVIDENCE_PRESENT_FULL_PREDICATE_REVIEWED_BEST_EFFORT',0)} best-effort present and {proof.get('BEST_EFFORT_EVIDENCE_PROOF_REVIEWED_WITH_QUALIFICATION',0)} qualified.\n\nA normalized PDF text search matched {source_exact} of {len(source)} final PDF-positive excerpts contiguously. The other {figure_visual_count} are verbatim on page 8 Figure 1.1 and were visually checked against the high-resolution page render, leaving {len(source)-source_exact-figure_visual_count} unverified source quotes. The text-versus-figure verification method is recorded in `06_pdf_quote_recheck_final.jsonl`. Neither Phase 1 text verification nor current textual linkage proves logical entailment of every predicate in each TP. **Do not label the 963 TP as independently human-verified.**\n\n## Generated-claim correctness uncertainty\n\nThe generated validity ledger classifies {validity_verdict.get('PDF_ENTAILED',0)} classes as `PDF_ENTAILED` and {validity_verdict.get('SUPPORTED_NONCOVERING',0)} as `SUPPORTED_NONCOVERING`, with zero currently scored `PDF_UNSUPPORTED` classes. Crucially, {len(weak_validity)} generated classes carry E1 partial-support evidence, including **{len(grade_conflicts)} classified as `PDF_ENTAILED`** despite E1 and **{raw_e1_noncover} `SUPPORTED_NONCOVERING` E1**. These are not independent affirmative full-predicate proofs and remain semantic-review exceptions in `06_validation_exceptions_final.jsonl`. Therefore FP=0 and Precision=100% cannot be certified as generated claim correctness, and should not be presented as an empirically bounded upper/lower accuracy estimate.\n\nThe {len(neg)} negative controls are an intentionally bounded set built from explicit PDF exclusions and prohibitions, **not** an exhaustive population of nonexistent requirements. Adding other absent propositions would change TN but not measure actual specificity.\n\n## Source atomization audit and common-denominator corrections\n\nThe atomization audit examined 1,024 original source items. {len(removed)} were removed as non-independent or illustrative; the remaining {len(source)} retain source identifiers. These corrections apply to **all** generation methods in any controlled comparison, not just the method evaluated here. The exclusion ledger records these removals along with nonnormative PDF and non-definitive generated statements. Remaining potential splitting/merging and overlapping test-matrix assertions should be treated as review risks rather than suppressed by arithmetic reconciliation.\n\n## Coverage, assertions and verdict\n\n- PDF pages and input Markdown line/cell coverage are structurally complete.\n- Canonical judgment consistency, source/negative IDs, raw occurrence/class memberships and within/across duplicate arithmetic pass independent checks.\n- Representative regression probes for case title, workspace retention class, repeated idempotent case creation and case tenant uniqueness have recorded TP evidence. The probes are not complete manual semantic validation.\n- The original canonical-universe-vs-judgments mismatch was repaired in Phase 6.\n- E1 generated validity classes and noncontiguous PDF evidence excerpts prevent a `FINAL_VERIFIED` designation.\n\n**Final designation: `FINAL_BEST_EFFORT`, `PHASE_COMPLETED_BEST_EFFORT`.** No Phase 7 exists in this six-phase protocol; no ZIP/TAR archive was generated.\n'''
    (root/'08_coverage_and_limitations.md').write_text(coverage,encoding='utf-8')
    write_json(root/'06_phase_status_final.json',{'phase':6,'protocol_version':'6.1','status':'PHASE_COMPLETED_BEST_EFFORT','metric_status':'FINAL_BEST_EFFORT','semantic_certification':False,'structural_validation':'PASS_WITH_REPAIRED_CANONICAL_LEDGER','canonical_units':len(judgments),'output_files':['06_metrics_final.json','06_metrics_final.md','compute_metrics.py','08_coverage_and_limitations.md','06_independent_validation_final.json','06_validation_exceptions_final.jsonl','06_pdf_quote_recheck_final.jsonl','06_input_integrity_final.json','06_regression_probes_final.json','06_canonical_reconciliation_final.json','03_canonical_universe_final.jsonl'],'archive_created':False,'phase7_started':False})
    # Re-run representation invariant against the corrected canonical file.
    fixed_canon=get_jsonl(root,'03_canonical_universe_final.jsonl')
    guard(len(fixed_canon)==len(judgments) and [x['canonical_id'] for x in fixed_canon]==[x['canonical_id'] for x in judgments] and [x['scoring_cell'] for x in fixed_canon]==[x['scoring_cell'] for x in judgments],'Canonical-universe repair failed')
    guard(all((root/f).is_file() for f in get_json(root,'06_phase_status_final.json')['output_files']),'Missing Phase 6 deliverable')
    print(json.dumps({'phase_status':'PHASE_COMPLETED_BEST_EFFORT','confusion':metrics['confusion'],'metrics':metrics['metrics'],'canonical_repaired_in_phase6':historical_phase4_rows!=len(judgments),'generated_E1_grade_classes':len(weak_validity),'pdf_quote_noncontiguous_count':len(source)-source_exact,'validation_exception_rows':len(issues),'report_files':get_json(root,'06_phase_status_final.json')['output_files']},indent=2))

if __name__=='__main__':
    main()
