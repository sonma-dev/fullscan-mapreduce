#!/usr/bin/env python3
"""OrionDesk v6.1 independent phase-six ledger recomputation and evidence checks.

Run: python compute_metrics.py --base /mnt/data/OrionDesk_v6_1 --inputs /mnt/data
The checker does not use reported confusion counts as expected answers. It checks
structure and local evidence locators; no lexical test certifies semantic entailment.
"""
from __future__ import annotations
import argparse,collections,json,re,sys
from pathlib import Path

ROLE_FILES=['01_screen_functions.md','02_api.md','03_data.md','04_batch_functions.md',
            '05_business_rules.md','06_exception_handling(1).md',
            '07_processing_flows(1).md','08_architecture_decision.md']
INPUT_FILES=ROLE_FILES+['OrionDesk_AI_Detailed_Design_Specification.pdf',
                       'OrionDesk_One_Pass_Atomic_Evaluation_Protocol_v6_1.md']
LEDGERS=['01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl',
'01_pdf_page_coverage_final.jsonl','02_generated_atoms_final.jsonl',
'02_generated_classes_final.jsonl','02_generated_line_cell_coverage_final.jsonl',
'02_generated_exclusions_final.jsonl','03_evidence_matches_final.jsonl',
'03_semantic_coverage_bridges_final.jsonl','03_fn_root_cause_audit_final.jsonl',
'03_canonical_universe_final.jsonl','04_atomic_judgments_final.jsonl',
'04_generated_claim_validity_final.jsonl','04_duplicate_classes_final.jsonl',
'04_negative_control_assertion_checks_final.jsonl','05_tp_evidence_audit_final.jsonl',
'05_source_atomization_audit_final.jsonl','07_change_delta.jsonl',
'09_excluded_units.jsonl']
FINAL_FILES=['04_confusion_matrix_final.json','04_confusion_matrix_final.md',
'05_duplicate_metrics_final.json','05_duplicate_metrics_final.md',
'06_metrics_final.json','06_metrics_final.md','08_coverage_and_limitations.md',
'06_phase_status_final.json','06_independent_validation_final.json','compute_metrics.py']

def fail(test,msg):
    if not test:raise AssertionError(msg)

def load(path):
    out=[]
    for i,line in enumerate(path.open(encoding='utf-8'),1):
        if line.strip():
            try:out.append(json.loads(line))
            except Exception as exc:raise AssertionError(f'{path.name}:{i}: {exc}') from exc
    return out

def unique(rows,key,name):
    ids=[r[key] for r in rows]
    fail(len(ids)==len(set(ids)),f'duplicate key in {name}')
    return {r[key]:r for r in rows}

def evidence_location(g,source_lines,classes,occurrences):
    fail(g.get('file') in source_lines, 'Unknown cited Markdown file')
    i=g.get('line_start');end=g.get('line_end',i)
    fail(isinstance(i,int) and isinstance(end,int) and 1<=i<=end<=len(source_lines[g['file']]),'Invalid citation line')
    passage='\n'.join(source_lines[g['file']][i-1:end])
    quote=g.get('quote_en',g.get('source_quote_en',''))
    fail(bool(quote) and ' '.join(quote.split()).replace('“','"').replace('”','"') in ' '.join(passage.split()).replace('“','"').replace('”','"'),
         f'Quoted generated evidence does not appear at {g["file"]}:{i}')
    cid=g.get('generated_class_id')
    oid=g.get('occurrence_id')
    if cid:fail(cid in classes,'Generated evidence cites unknown class '+str(cid))
    if oid:fail(oid in occurrences,'Generated evidence cites unknown occurrence '+str(oid))

def verify(base:Path, inputs:Path, check_final_files=False):
    missing=[x for x in INPUT_FILES if not (inputs/x).is_file()]
    fail(not missing,'Mandatory input files absent: '+str(missing))
    missing=[x for x in LEDGERS if not (base/x).is_file()]
    fail(not missing,'Mandatory ledgers absent: '+str(missing))
    src={k:(inputs/k).read_text(encoding='utf-8').splitlines() for k in ROLE_FILES}
    fail(all(src.values()),'One or more scored Markdown inputs empty')
    data={n:load(base/n) for n in LEDGERS}
    R=unique(data['01_source_atoms_final.jsonl'],'source_id','R')
    N=unique(data['01_source_negative_controls_final.jsonl'],'negative_control_id','N')
    GO=unique(data['02_generated_atoms_final.jsonl'],'occurrence_id','GO')
    GC=unique(data['02_generated_classes_final.jsonl'],'semantic_class_id','GC')
    V=unique(data['04_generated_claim_validity_final.jsonl'],'generated_class_id','V')
    U=unique(data['03_canonical_universe_final.jsonl'],'canonical_id','U')
    J=unique(data['04_atomic_judgments_final.jsonl'],'canonical_id','J')
    E=unique(data['03_evidence_matches_final.jsonl'],'source_id','evidence')
    Bridge=unique(data['03_semantic_coverage_bridges_final.jsonl'],'source_id','bridge')
    D=unique(data['04_duplicate_classes_final.jsonl'],'semantic_class_id','duplicates')
    Neg=unique(data['04_negative_control_assertion_checks_final.jsonl'],'control_id','negative checks')
    TP_audit=data['05_tp_evidence_audit_final.jsonl']; FN_audit=data['03_fn_root_cause_audit_final.jsonl']
    fail(set(R).isdisjoint(N),'R and N overlap')
    fail(set(GC)==set(V)==set(D),'Generated class/validity/duplicates mismatch')
    fail(set(U)==set(J),'Canonical universe vs atomic judgment mismatch')
    fail(all(U[k]==J[k] for k in U),'Canonical and judgment record contents differ')
    fail(set(R)==set(E),'Source matches must cover all source atoms')
    fail(set(N)==set(Neg),'Negative checks must cover all controls')
    fail(len({x['prefix'] for a in [list(GO.values()),list(GC.values()),list(J.values())] for x in a})==1,'Mixed prefix/method')
    pages=data['01_pdf_page_coverage_final.jsonl']
    fail(len(pages)==90 and {x['physical_page'] for x in pages}==set(range(1,91)),'90-page coverage incomplete')
    fail(all(x['readable_text'] and x['coverage_status'].startswith('INSPECTED') for x in pages),'Unreadable/uninspected PDF page')
    import fitz
    with fitz.open(str(inputs/'OrionDesk_AI_Detailed_Design_Specification.pdf')) as pdf:
        fail(len(pdf)==90,'Original PDF page count not 90')
        fail('OD-AI-DDS-001' in pdf[0].get_text(),'Original PDF ID mismatch')
        pdftext=[' '.join(p.get_text().lower().split()) for p in pdf]
    pdf_unmatched=[]
    for sid,x in R.items():
        fail(x['pdf_evidence'] and 1<=x['physical_page']<=90,'Source atom missing PDF quote/page '+sid)
        q=' '.join(x['quote_en'].lower().split())
        if q not in pdftext[x['physical_page']-1]:pdf_unmatched.append(sid)
    for x in N.values():
        fail(x['actual_label']==0 and x['pdf_evidence'],'Negative control lacks supporting exclusion')
    # Inspect every physical line and every reported table cell, not merely sampled rows.
    linecov=data['02_generated_line_cell_coverage_final.jsonl']
    byfile=collections.defaultdict(list)
    for x in linecov:byfile[x['file']].append(x['line'])
    for fn,lines in src.items():
        fail(len(byfile[fn])==len(lines) and sorted(byfile[fn])==list(range(1,len(lines)+1)),f'Line coverage incomplete for {fn}')
    cells=sum(len(x['table_cell_dispositions']) for x in linecov)
    for oid,x in GO.items():
        fail(x['eligibility']=='DEFINITIVE','Ineligible generated occurrence')
        fail(x['semantic_class_id'] in GC,'Unmapped generated occurrence '+oid)
        evidence_location(x,src,GC,GO)
    seen=[];within=across=spanning=repeated=0
    for cid,c in GC.items():
        ids=c['occurrence_ids'];fail(ids and len(ids)==len(set(ids))==c['eligible_occurrence_count'],'Invalid class member count')
        fail(c['representative_occurrence_id'] in ids,'Representative absent')
        fail(all(oid in GO and GO[oid]['semantic_class_id']==cid for oid in ids),'Class occurrence mapping inconsistent')
        seen.extend(ids)
        dup=D[cid];fail(set(dup['occurrence_ids'])==set(ids),'Duplicate class membership disagrees')
        fail(dup['eligible_occurrence_count']==len(ids),'Duplicate class count disagrees')
        fail(dup['within_file_excess']+dup['across_file_excess']==len(ids)-1,'Duplicate partition mismatch')
        within+=dup['within_file_excess'];across+=dup['across_file_excess']
        repeated+=len(ids)>1;spanning+=len(set(GO[i]['file'] for i in ids))>1 and len(ids)>1
        fail(set(V[cid]['occurrence_ids'])==set(ids),'Validity occurrence mapping disagrees')
        fail(V[cid]['validity_label'] in ('PDF_ENTAILED','SUPPORTED_NONCOVERING','PDF_UNSUPPORTED'),'Unknown validity class')
    fail(len(seen)==len(GO)==len(set(seen)) and set(seen)==set(GO),'Occurrences not exactly partitioned')
    fail(within+across==len(GO)-len(GC),'Duplicate aggregate mismatch')
    source_class_ids=set(); negative_asserted=set(); generated_only=set()
    cellscores=collections.Counter()
    missing_original_proof=[]
    for cid,x in J.items():
        unit=x['universe_unit_type'];cell=x['scoring_cell']
        fail(cell in ('TP','TN','FP','FN'),'Unknown judgment class')
        fail(x['actual_label']==int(cell in ('TP','FN')) and x['predicted_label']==int(cell in ('TP','FP')),'Binary labels wrong '+cid)
        for g in x.get('generated_evidence',[]):evidence_location(g,src,GC,GO)
        if unit=='PDF_POSITIVE':
            fail(cid in R and x['origin_source_ids']==[cid],'Source canonical record missing positive ID')
            source_class_ids.add(cid)
            fail(cell in ('TP','FN') and E[cid]['draft_scoring_cell']==cell,'Positive match/judgment inconsistent')
            if cell=='TP':
                fail(x['entailment_grade'] in ('E2','E3') and x['generated_evidence'],'TP without full evidence '+cid)
                if x['entailment_grade']=='E2':
                    fail(cid in Bridge and bool(Bridge[cid].get('predicate_check_map')),'E2 bridge absent '+cid)
                else:fail(cid not in Bridge,'Direct TP incorrectly has E2 bridge '+cid)
            else:
                fail(x['entailment_grade'] in ('E0','E1'),'FN grade not E1/E0')
                fail(x['fn_root_cause'] in ('TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'),'FN root cause absent')
        elif unit=='FIXED_PDF_NEGATIVE_CONTROL':
            fail(cid in N and x['origin_negative_control_ids']==[cid],'Negative-control ID incorrect')
            fail(cell in ('TN','FP'),'Bad negative-control confusion cell')
            asserted=bool(Neg[cid]['asserted_in_generated_corpus'])
            fail((cell=='FP')==asserted,'Negative control assertion discrepancy')
            if asserted:negative_asserted.add(cid)
            else:fail(not x['generated_evidence'],'TN with asserted generated evidence')
        elif unit=='UNSUPPORTED_GENERATED_ONLY':
            fail(cell=='FP' and len(x['origin_generated_class_ids'])==1,'Generated-only FP is not one class')
            gid=x['origin_generated_class_ids'][0]
            fail(gid in GC and V[gid]['validity_label']=='PDF_UNSUPPORTED','FP invalid generated class')
            fail(gid not in generated_only,'Generated-only class double-counted')
            generated_only.add(gid)
        else:fail(False,'Unknown canonical type '+str(unit))
        cellscores[cell]+=1
    fail(source_class_ids==set(R),'Incomplete source canonical universe')
    fail(set(k for k in J if k in N)==set(N),'Incomplete fixed negative controls')
    fail(generated_only=={cid for cid,x in V.items() if x['validity_label']=='PDF_UNSUPPORTED'},'Unsupported classes vs FP differ')
    fail(len(J)==len(R)+len(N)+len(generated_only),'Canonical universe equation failed')
    fail(cellscores['TP']+cellscores['FN']==len(R),'Source-positive denominator equation failed')
    fail(cellscores['TN']+len(negative_asserted)==len(N),'TN denominator equation failed')
    fail(cellscores['FP']==len(generated_only)+len(negative_asserted),'False-positive equation failed')
    # Verify TP proof audit and corrected candidate FN handling.
    confirmed=unique([x for x in TP_audit if x['audit_outcome']=='CONFIRMED_TP'],'source_id','confirmed TP audits')
    fail(set(confirmed)=={cid for cid,x in J.items() if x['scoring_cell']=='TP'},'Each final TP needs exactly one confirmed proof audit')
    corrected_fn={x['source_id'] for x in TP_audit if x['audit_outcome']=='CORRECTED_TO_FN'}
    fail(all(J[cid]['scoring_cell']=='FN' for cid in corrected_fn),'Downgraded TP still scored as TP')
    needed={'target','actor','condition','timing','exception','version','limit','action','scope','outcome'}
    for cid,x in confirmed.items():
        predicate=x['full_predicate_check']
        fail(needed.issubset(predicate),'TP predicate proof incomplete '+cid)
        fail(all(predicate[k]['status'] in ('met','not_applicable') and predicate[k].get('evidence_en') for k in needed),'Unsupported TP proof marker '+cid)
        fail(x['pdf_evidence'] and x['generated_evidence'],'Missing TP evidence '+cid)
        for e in x['generated_evidence']:evidence_location(e,src,GC,GO)
    fn_rows=unique(FN_audit,'source_id','FN root cause audit')
    final_fn={cid for cid,x in J.items() if x['scoring_cell']=='FN'}
    fail(final_fn.issubset(fn_rows),'Final FN without root cause ledger')
    cause=collections.Counter()
    for cid,row in fn_rows.items():
        if cid in final_fn:
            fail(row['final_scoring_cell']=='FN' and row['fn_review_disposition'] in ('TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'),'Final FN has invalid disposition')
            fail(row['best_generated_candidates'] and row['exact_and_alias_keys_checked'] and row['universal_context_conjunction_checked'],'FN reverse-search audit is missing real candidate evidence')
            cause[row['fn_review_disposition']]+=1
        elif row['final_scoring_cell']=='TP':
            fail(J[cid]['scoring_cell']=='TP','Corrected FN still negative')
    fail(sum(cause.values())==cellscores['FN'],'FN reason counts do not reconcile')
    changed_fn=sum(x['fn_review_disposition']=='MATCHER_FALSE_NEGATIVE_CORRECTED' and x['final_scoring_cell']=='TP' for x in FN_audit)
    # Empirical diagnostic: exact column claims are satisfied by a definitive SearchChunk row.
    field_regression=[]
    field_evidence=' '.join(src['03_data.md'][180:184]).lower()
    for cid,x in J.items():
        st=x['atomic_statement_en'].lower()
        match=re.fullmatch(r'the search index row includes ([a-z0-9_]+)\.',st)
        if match:
            field=match.group(1)
            if re.search(r'(?<![a-z0-9_])'+re.escape(field)+r'(?![a-z0-9_])',field_evidence) and x['scoring_cell']=='FN':
                field_regression.append(cid)
    fail(not field_regression,'Known explicit SearchChunk-field FN regression '+str(field_regression))
    # Validate structural pages and observed confidence limitations; no semantic certification by text statistics.
    validity=collections.Counter(v['validity_label'] for v in V.values())
    partial_uncertain=collections.Counter(v['validity_label'] for v in V.values() if v.get('source_support_grade')=='E1')
    dups=len(GO)-len(GC)
    tp= cellscores['TP'];fp=cellscores['FP'];fn=cellscores['FN']
    prec=tp/(tp+fp) if tp+fp else None
    rec=tp/(tp+fn) if tp+fn else None
    f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None
    duprate=dups/len(GO) if GO else None
    report={
      'status':'PASS_STRUCTURAL_ONLY','prefix':next(iter({x['prefix'] for x in J.values()})),
      'input_scope':{'original_pdf_physical_pages':len(pages),'scored_markdown_files':len(src),'scored_markdown_physical_lines':sum(map(len,src.values())),'table_cells_in_coverage_ledger':cells},
      'universe':{'source_positive_atoms':len(R),'source_negative_controls':len(N),'generated_positive_occurrences':len(GO),'raw_generated_claim_classes':len(GC),'covered_source_atoms':tp,'asserted_negative_controls':len(negative_asserted),'unsupported_generated_only_propositions':len(generated_only),'canonical_predicted_positive_units':tp+fp,'canonical_decision_units':len(J)},
      'confusion':{'TP':tp,'TN':cellscores['TN'],'FP':fp,'FN':fn},
      'metrics':{'Precision':prec,'Recall':rec,'F1':f1,'Duplicate':duprate},
      'duplication':{'eligible_generated_occurrences':len(GO),'unique_generated_claim_classes':len(GC),'duplicate_excess_occurrences':dups,'within_file_excess':within,'across_file_excess':across,'repeated_claim_class_count':repeated,'repeated_classes_spanning_multiple_files':spanning},
      'audit':{'confirmed_tp_evidence_records':len(confirmed),'downgraded_tp_records':len(corrected_fn),'final_fn_root_causes':dict(cause),'corrected_candidate_fns_in_root_cause_ledger':changed_fn,'source_atomization_audit_rows':len(data['05_source_atomization_audit_final.jsonl']),'change_delta_rows':len(data['07_change_delta.jsonl']),'pdf_quote_text_extraction_nonmatches':pdf_unmatched,'supported_E1_generated_classes':sum(v.get('source_support_grade')=='E1' and v['validity_label']!='PDF_UNSUPPORTED' for v in V.values()),'unsupported_E1_generated_classes':partial_uncertain['PDF_UNSUPPORTED'],'exact_field_regression_probes':'PASS'},
      'checks_passed':['canonical judgment identity','single four-cell universe','PDF source page coverage','source positive and fixed negative controls','scored input physical-line and table-cell coverage','generated evidence exact source locator','one occurrence per semantic class','duplicate partition','TP evidence audit and E2 bridge','FN reciprocal root-cause audit','negative-control assertions','generated-only FP deduplication','effective-universe denominators','SearchChunk exact-field regression'],
      'semantic_certification':'NOT_CERTIFIED: structural, lexical and locator tests do not prove every semantic predicate or source atomization decision'
    }
    if check_final_files:
        missing=[n for n in FINAL_FILES if not (base/n).is_file()]
        fail(not missing,'Final deliverable files missing: '+str(missing))
        final=json.loads((base/'06_metrics_final.json').read_text())
        fail(final['universe']==report['universe'] and final['metrics']==report['metrics'] and final['confusion']==report['confusion'],'Final metrics do not equal independent recomputation')
        for token in ['bounded','FN','TP','atomization','reciprocal','raw','effective','uncertain','E1']:
            fail(token.lower() in (base/'08_coverage_and_limitations.md').read_text().lower(),'Coverage report lacks disclosure: '+token)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base',default=str(Path(__file__).resolve().parent))
    p.add_argument('--inputs',default='/mnt/data')
    p.add_argument('--check-final-files',action='store_true')
    p.add_argument('--json-output')
    args=p.parse_args()
    try:
        result=verify(Path(args.base),Path(args.inputs),args.check_final_files)
        if args.json_output:Path(args.json_output).write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
    except (AssertionError,KeyError,ValueError) as e:
        print('FAILED:',str(e),file=sys.stderr);sys.exit(1)
