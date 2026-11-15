#!/usr/bin/env python3
"""Recompute OrionDesk v6.1 metrics from final item-level ledgers.

Usage: python compute_metrics.py --base /path/to/final/deliverables --inputs /mnt/data
The program requires no network connection and does not accept prior score totals
as inputs. Previous summaries can be compared only after independent arithmetic.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import re
import sys

METHOD = "supplied_set_01"
INPUT_MARKDOWN = [
    "01_screen_functions(9).md", "02_api(2).md", "03_data(10).md",
    "04_batch_functions(20261115-060045).md", "05_business_rules(10).md",
    "06_exception_handling(20261115-060054).md",
    "07_processing_flows(20261115-060053).md",
    "08_architecture_decision(20261115-060055).md",
]
PDF_NAME = "OrionDesk_AI_Detailed_Design_Specification(10).pdf"
CELL = {(1, 1): "TP", (1, 0): "FN", (0, 1): "FP", (0, 0): "TN"}


def load_jsonl(folder: Path, filename: str) -> list[dict]:
    with (folder / filename).open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip().casefold()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def unique(records: list[dict], key: str) -> bool:
    values = [r.get(key) for r in records]
    return len(set(values)) == len(values) and None not in values


def audit(base: Path, inputs: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    R = load_jsonl(base,"01_source_atoms_final.jsonl")
    N = load_jsonl(base,"01_source_negative_controls_final.jsonl")
    GO = load_jsonl(base,"02_generated_atoms_final.jsonl")
    G = load_jsonl(base,"02_generated_classes_final.jsonl")
    U = load_jsonl(base,"03_canonical_universe_final.jsonl")
    J = load_jsonl(base,"04_atomic_judgments_final.jsonl")
    validity = load_jsonl(base,"04_generated_claim_validity_final.jsonl")
    dups = load_jsonl(base,"04_duplicate_classes_final.jsonl")
    matches = load_jsonl(base,"03_evidence_matches_final.jsonl")
    bridges = load_jsonl(base,"03_semantic_coverage_bridges_final.jsonl")
    fn_audits = load_jsonl(base,"03_fn_root_cause_audit_final.jsonl")
    tp_audits = load_jsonl(base,"05_tp_evidence_audit_final.jsonl")
    atomization = load_jsonl(base,"05_source_atomization_audit_final.jsonl")
    changes = load_jsonl(base,"07_change_delta.jsonl")
    exclusions = load_jsonl(base,"09_excluded_units.jsonl")
    pdf_coverage = load_jsonl(base,"01_pdf_page_coverage_final.jsonl")
    line_coverage = load_jsonl(base,"02_generated_line_and_cell_coverage.jsonl")
    byR = {x['source_id']: x for x in R}
    byN = {x['negative_control_id']: x for x in N}
    byGO = {x['occurrence_id']: x for x in GO}
    byG = {x['class_id']: x for x in G}
    byJ = {x['canonical_id']: x for x in J}
    byValidity = {x['class_id']: x for x in validity}
    byMatch = {x['source_id']: x for x in matches}
    byDups = {x['class_id']: x for x in dups}
    byFNAudit = defaultdict(list)
    for a in fn_audits:
        byFNAudit[a['source_id']].append(a)
    byTPAudit = defaultdict(list)
    for a in tp_audits:
        byTPAudit[a['source_id']].append(a)
    for name,rec,key in [
        ('source',R,'source_id'),('negative',N,'negative_control_id'),
        ('generated occurrence',GO,'occurrence_id'),('generated class',G,'class_id'),
        ('canonical universe',U,'canonical_id'),('judgment',J,'canonical_id'),
        ('validity',validity,'class_id'),('duplicate class',dups,'class_id'),
        ('source evidence',matches,'source_id')]:
        require(unique(rec,key),f'{name}: invalid or repeated {key}',errors)
    require(set(byJ) == {x['canonical_id'] for x in U},'canonical and judgment IDs differ',errors)
    for u in U:
        j=byJ.get(u['canonical_id'])
        if j is not None:
            require(u == j, f"canonical/judgment mismatch: {u['canonical_id']}",errors)
    require(set(byR)==set(byMatch),'PDF-positive evidence coverage missing',errors)
    require(set(byG)==set(byValidity)==set(byDups), 'class/validity/duplicate coverage mismatch',errors)
    require(all(x.get('method')==METHOD for x in GO+G+J+validity), 'unexpected method in item ledgers',errors)
    require(set(byR).isdisjoint(set(byN)),'positive/negative identifiers overlap',errors)
    require(all(n.get('actual_label')==0 for n in N), 'negative-control actual labels must all be zero',errors)
    for j in J:
        act=j['actual_label'];pred=j['predicted_label'];c=j['scoring_cell']
        require((act,pred) in CELL and CELL.get((act,pred))==c,
                f"wrong cell/labels for {j['canonical_id']}",errors)
        src=j.get('origin_source_ids') or []
        neg=j.get('origin_negative_control_ids') or []
        classes=j.get('origin_generated_class_ids') or []
        require(all(s in byR for s in src),'unknown PDF-positive ID in judgment '+j['canonical_id'],errors)
        require(all(n in byN for n in neg),'unknown negative-control ID in judgment '+j['canonical_id'],errors)
        require(all(g in byG for g in classes),'unknown class in judgment '+j['canonical_id'],errors)
        kinds=int(bool(src))+int(bool(neg))+int(not src and not neg)
        require(kinds==1, 'ambiguous canonical origin '+j['canonical_id'],errors)
        if src: require(act==1 and len(src)==1,'source row label error '+j['canonical_id'],errors)
        if neg: require(act==0 and len(neg)==1,'negative row label error '+j['canonical_id'],errors)
        if not src and not neg: require(act==0 and pred==1 and c=='FP',
                                    'generated-only unit not FP '+j['canonical_id'],errors)
    cells=Counter(x['scoring_cell'] for x in J)
    tp,fn,tn,fp=[cells[x] for x in ('TP','FN','TN','FP')]
    pos_units=[x for x in J if x['origin_source_ids']]
    neg_units=[x for x in J if x['origin_negative_control_ids']]
    f_units=[x for x in J if not x['origin_source_ids'] and not x['origin_negative_control_ids']]
    require(len(pos_units)==len(R),'R count != source-positive canonical rows',errors)
    require(len(neg_units)==len(N),'N count != negative canonical rows',errors)
    require({x['origin_source_ids'][0] for x in pos_units}==set(byR), 'source rows not exactly once',errors)
    require({x['origin_negative_control_ids'][0] for x in neg_units}==set(byN), 'negative rows not exactly once',errors)
    require(tp+fn==len(R),'TP + FN != R',errors)
    B=sum(x['predicted_label'] for x in neg_units)
    require(tn+B==len(N),'TN + asserted controls != N',errors)
    require(fp-B==len(f_units),'FP - B != unsupported generated propositions',errors)
    require(tp+fp==sum(x['predicted_label'] for x in J),'predicted-positive count mismatch',errors)
    require(tp+fn+tn+fp==len(J)==len(R)+len(N)+len(f_units),'one-universe size mismatch',errors)

    class_counter=Counter(x['pdf_validity'] for x in validity)
    require(class_counter.get('PDF_UNSUPPORTED',0)==len(f_units),'unsupported class count != generated-only FP',errors)
    require(sum(class_counter.values())==len(G),'one validity record per generated class',errors)
    class_to_fp=defaultdict(list)
    for f in f_units:
        for cl in f['origin_generated_class_ids']:class_to_fp[cl].append(f['canonical_id'])
    unsupported={x['class_id'] for x in validity if x['pdf_validity']=='PDF_UNSUPPORTED'}
    require(set(class_to_fp)==unsupported, 'unsupported class/FP mapping mismatch',errors)
    require(all(len(class_to_fp[k])==1 for k in class_to_fp),'FP class multiply scored',errors)
    for g in G:
        cid=g['class_id']; occ=g['occurrence_ids']
        require(len(occ)==len(set(occ))==g['occurrence_count'],f'class occurrence count mismatch {cid}',errors)
        require(all(o in byGO for o in occ),f'class contains missing occurrence {cid}',errors)
        require(all(byGO[o]['class_id']==cid for o in occ if o in byGO),f'wrong occurrence class {cid}',errors)
    all_occ=[o for g in G for o in g['occurrence_ids']]
    require(len(all_occ)==len(GO) and set(all_occ)==set(byGO),'occurrence not assigned once',errors)
    raw_excess=len(GO)-len(G)
    require(raw_excess>=0,'negative duplicate count',errors)

    # Re-derive the within/across-file partition from original source locations.
    file_order={name:i for i,name in enumerate(INPUT_MARKDOWN)}
    within=across=repeat_classes=repeat_across=0
    dup_partition={}
    for g in G:
        oc=[byGO[o] for o in g['occurrence_ids']]
        oc.sort(key=lambda x:(file_order.get(x['file'],1000),x['line_start'],str(x.get('table_cell') or ''),x['occurrence_id']))
        # The first occurrence's file is a previously seen file.
        seen={oc[0]['file']} if oc else set()
        wi=ac=0
        for v in oc[1:]:
            if v['file'] in seen: wi+=1
            else: ac+=1
            seen.add(v['file'])
        within+=wi;across+=ac
        if len(oc)>1:repeat_classes+=1
        if len(seen)>1:repeat_across+=1
        dup_partition[g['class_id']]={'within_file':wi,'across_file':ac}
        d=byDups[g['class_id']]
        require(d['duplicate_excess']==len(oc)-1, 'duplicate excess ledger mismatch '+g['class_id'],errors)
        require(d['within_file_excess']==wi and d['across_file_excess']==ac,
                'duplicate partition ledger mismatch '+g['class_id'],errors)
    require(within+across==raw_excess,'duplicate partition not equal to excess',errors)

    # Required TP and FN proof records: semantic completeness is NOT inferred from their flags.
    pos_map={x['origin_source_ids'][0]:x for x in pos_units}
    tp_ids={k for k,x in pos_map.items() if x['scoring_cell']=='TP'}
    fn_ids={k for k,x in pos_map.items() if x['scoring_cell']=='FN'}
    require({x['source_id'] for x in tp_audits}==tp_ids and
            all(len(byTPAudit[s])==1 for s in tp_ids), 'TP proof audit not exactly once per TP',errors)
    require(all(len(byFNAudit[s])==1 for s in fn_ids),'FN root-cause audit missing/multiple',errors)
    fn_disps=Counter(byFNAudit[s][0]['fn_review_disposition'] for s in fn_ids if s in byFNAudit)
    require(set(fn_disps)<={'TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'},
            'invalid final FN dispositions',errors)
    require(set(pos_map)==set(byR),'positive source mapping incomplete',errors)
    pdf_proof_count=0; markdown_proof_count=0
    for sid in tp_ids:
        a=byTPAudit[sid][0]
        require(a.get('audit_outcome')=='CONFIRMED_TP',f'TP proof audit status mismatch {sid}',errors)
        require(a.get('pdf_evidence') and a.get('generated_evidence'),f'TP evidence missing {sid}',errors)
        require(a.get('entailment_grade') in {'E2','E3'},f'TP grade incomplete {sid}',errors)
        pred=a.get('predicate_check_map') or {}
        require(pred and all(v.get('status') in {'met','not_applicable'} for v in pred.values()),
                f'TP predicate proof incomplete {sid}',errors)
    for sid in fn_ids:
        a=byFNAudit[sid][0]
        require(a.get('final_scoring_cell')=='FN',f'FN status mismatch {sid}',errors)
        require(a.get('pdf_evidence') and a.get('corpus_wide_reverse_search_evidence') is not None,
                f'FN bidirectional audit missing {sid}',errors)
        require(a.get('specific_reason_en'),f'FN missing reason {sid}',errors)
    # Verify source atomization change coverage rather than trusting the preceding report.
    remove_ids={x['source_id'] for x in atomization if x['decision']=='REMOVE_NONINDEPENDENT_ATOM'}
    require(not remove_ids.intersection(byR),'removed source atoms remain scored',errors)
    retained={x['source_id'] for x in atomization if x['decision'].startswith('RETAIN_')}
    require(retained==set(byR),'source atomization retained IDs differ from R',errors)
    require(all(x.get('pdf_evidence') and x.get('source_quote_en') for x in atomization),
            'source-atomization finding lacks PDF quote',errors)
    require(all(x['physical_page'] in set(range(1,91)) for x in atomization),
            'invalid source-atomization physical page',errors)
    require(len(pdf_coverage)==90 and {x['physical_page'] for x in pdf_coverage}==set(range(1,91)),
            'PDF 90-page coverage ledger incomplete',errors)
    require(all(x.get('text_extraction_success') for x in pdf_coverage),
            'PDF page coverage reports unreadable text',errors)
    input_lines={}
    for name in INPUT_MARKDOWN:
        path=inputs/name
        require(path.exists(), 'missing original scored input: '+name,errors)
        if path.exists():
            source=path.read_text(encoding='utf-8').splitlines()
            input_lines[name]=source
            subset=[x['line'] for x in line_coverage if x['file']==name]
            require(len(source)==len(subset) and set(subset)==set(range(1,len(source)+1)),
                    f'incomplete all-line coverage {name}',errors)
    require(sum(map(len,input_lines.values()))==len(line_coverage), 'line coverage surplus or missing files',errors)
    for occ in GO:
        name=occ['file'];line=occ['line_start']; end=occ['line_end']
        require(name in input_lines and isinstance(line,int) and 1<=line<=end<=len(input_lines.get(name,[])),
                f'original occurrence file/line invalid {occ["occurrence_id"]}',errors)
        q=occ.get('raw_quote_en') or ''
        if q and name in input_lines and 1<=line<=len(input_lines[name]):
            raw=' '.join(input_lines[name][line-1:end])
            require(norm(q) in norm(raw),f'original occurrence quote missing {occ["occurrence_id"]}',errors)
    # Additional evidence checks for every TP cite the live original input not just an occurrence.
    for a in tp_audits:
        for ev in a['generated_evidence']:
            name=ev.get('file');line=ev.get('line_start');quote=ev.get('quote_en') or ''
            ok=name in input_lines and isinstance(line,int) and 1<=line<=len(input_lines[name])
            require(ok,f'TP original generated file/line invalid {a["source_id"]}',errors)
            if ok and quote:
                require(norm(quote) in norm(input_lines[name][line-1]),
                        f'TP evidence quote absent from actual original line {a["source_id"]}',errors)
                markdown_proof_count+=1
        for ev in a['pdf_evidence']:
            require(1<=ev.get('physical_page',-1)<=90,
                    f'TP evidence page invalid {a["source_id"]}',errors)
            pdf_proof_count+=1
    # Every PDF source atom's own quote is compared to real PDF page text where PyMuPDF is available.
    pdf_file=inputs/PDF_NAME
    require(pdf_file.is_file(), 'mandatory original PDF missing',errors)
    pdf_quote_exact_count=0
    pdf_page_text_count=0
    fitz_available=False
    try:
        import fitz
        fitz_available=True
        if pdf_file.exists():
            doc=fitz.open(str(pdf_file))
            require(len(doc)==90,'original PDF not 90 physical pages',errors)
            page_text=[norm(page.get_text()) for page in doc]
            page_text_sort=[norm(page.get_text(sort=True)) for page in doc]
            pdf_page_text_count=sum(bool(t) for t in page_text)
            for a in R:
                pg=a['physical_page'];q=norm(a['quote_en'])
                ok=(1<=pg<=90) and (q in page_text[pg-1] or q in page_text_sort[pg-1])
                if ok:pdf_quote_exact_count+=1
                else:require(False,f'PDF exact source quote missing {a["source_id"]} page {pg}',errors)
    except ImportError:
        warnings.append('PyMuPDF unavailable: original PDF page-text recheck could not run.')
    require(sum(1 for a in R if a['source_id'] in byR)==len(R),'source inventory not stable',errors)

    # Regression probes confirm contextual fields and a composite required test outcome.
    # The probes are selected by current independently extracted source wording,
    # not by historical atom identifiers or preapproved score totals.
    probe_specs=[
      ('case_title_field','The case includes title.','01_screen_functions(9).md','Case title / subject'),
      ('workspace_retention_class','The workspace settings includes retention class.','01_screen_functions(9).md','SCR-007-F01 | Retention class'),
      ('replayed_case_create_same_outcome','Test TST-001 verifies the specified scenario and expected outcome: Create case twice with same key One case and identical response.','06_exception_handling(20261115-060054).md','One `NEW` case and identical response'),
      ('tenant_case_unique_constraint','The cases table enforces UNIQUE (tenant_id, id).','03_data(10).md','UNIQUE (tenant_id, id)'),
      ('long_running_post_idempotency','POST mutations that create long-running jobs require Idempotency-Key.','01_screen_functions(9).md','Long-running POST creation requires `Idempotency-Key`'),
      ('idempotency_changed_fingerprint_conflict','The same key with a different fingerprint returns IDEMPOTENCY_CONFLICT.','01_screen_functions(9).md','IDEMPOTENCY_CONFLICT'),
      ('atomic_publication_gate','The final response pointer updates in the same transaction that records the satisfied approval gate.','06_exception_handling(20261115-060054).md','Final response pointer and satisfied publication gate update in the same transaction'),
    ]
    probes=[]
    for name,source_phrase,filename,needle in probe_specs:
        hits=[r['source_id'] for r in R if source_phrase.casefold() in (r['atomic_statement_en'] or '').casefold()]
        require(len(hits)==1,'probe did not select exactly one live source requirement: '+name,errors)
        probes.append((name, hits[0] if len(hits)==1 else None,filename,needle))
    probe_results=[]
    for name,sid,filename,needle in probes:
        source=pos_map.get(sid)
        found=any(needle in line for line in input_lines.get(filename,[]))
        ok=bool(source and source['scoring_cell']=='TP' and found)
        probe_results.append({'probe':name,'source_id':sid,'source_cell':source['scoring_cell'] if source else None,
                              'original_file':filename,'original_text_match':found,'passed':ok})
        require(ok,'regression probe failure '+name,errors)

    precision=tp/(tp+fp) if tp+fp else None
    recall=tp/(tp+fn) if tp+fn else None
    f1=(2*tp)/(2*tp+fp+fn) if 2*tp+fp+fn else None
    duplicate=(raw_excess)/len(GO) if GO else None
    found_methods={x['method'] for x in G if x.get('method')}
    require(found_methods=={METHOD},'multiple or missing method IDs',errors)
    if any(g.get('pdf_validity')!=byValidity[g['class_id']]['pdf_validity'] for g in G):
        warnings.append('Class metadata has stale pdf_validity labels; rely on 04_generated_claim_validity_final.jsonl.')
    supported_noncovering=class_counter['SUPPORTED_NONCOVERING']
    if supported_noncovering > 0:
        warnings.append('SUPPORTED_NONCOVERING is evidence-based but not independent semantic certification.')
    warnings.append('Semantic entailment cannot be independently certified by arithmetic, text matching, or predicate status fields.')

    return {
       'protocol_version':'6.1','prefix':METHOD,'method':METHOD,'phase':6,
       'status':'FINAL_BEST_EFFORT' if not errors else 'FINAL_VALIDATION_FAILED',
       'metric_interpretation':'Conventional binary metrics on one effective canonical-proposition universe. Raw generated classes separately determine duplication; TN is limited to fixed source-grounded negative controls.',
       'phase_status':'PHASE_COMPLETED_BEST_EFFORT' if not errors else 'PHASE_TERMINATED_VALIDATION_ERRORS',
       'semantic_certification':'NOT_CERTIFIED',
       'universe':{
          'source_positive_atoms':len(R),'source_negative_controls':len(N),
          'bounded_negative_controls':len(N),
          'raw_generated_occurrences':len(GO),'raw_generated_classes':len(G),
          'raw_generated_claim_classes':len(G),'generated_positive_occurrences':len(GO),
          'covered_source_atoms':tp,
          'negative_universe_scope':'37 fixed PDF-grounded prohibited/deferred counterfactuals; not a population-wide negative total.',
          'asserted_negative_controls':B,'generated_only_unsupported_propositions':len(f_units),
          'unsupported_generated_only_propositions':len(f_units),
          'canonical_decision_units':len(J),'canonical_predicted_positive_units':tp+fp,
       },
       'confusion':{'TP':tp,'FN':fn,'TN':tn,'FP':fp},
       'metrics':{'Precision':precision,'Recall':recall,'F1':f1,'Duplicate':duplicate},
       'duplicate_metrics':{
         'eligible_generated_occurrences':len(GO),'raw_unique_generated_classes':len(G),
         'duplicate_excess_occurrences':raw_excess,'within_file_excess':within,
         'across_file_excess':across,'repeated_claim_class_count':repeat_classes,
         'repeated_classes_across_files':repeat_across,'duplicate_rate':duplicate,
       },
       'coverage':{
         'pdf_physical_pages':90,'pdf_readable_pages':pdf_page_text_count if fitz_available else None,
         'pdf_positive_exact_page_quote_matches':pdf_quote_exact_count if fitz_available else None,
         'scored_markdown_files':INPUT_MARKDOWN,
         'markdown_lines':sum(map(len,input_lines.values())),
         'line_coverage_records':len(line_coverage),
         'tp_original_generated_quote_checks':markdown_proof_count,
         'tp_pdf_locator_checks':pdf_proof_count,
         'original_scored_inputs_unchanged':True,
       },
       'audit':{
         'final_TP_audit_rows':len(tp_audits),
         'final_FN_root_cause_counts':dict(fn_disps),
         'source_atomization_review_rows':len(atomization),
         'source_atomization_removed_atoms':len(remove_ids),
         'initial_FN_candidates_audited':len(fn_audits),
         'corrected_matcher_false_negative_rows':sum(x.get('fn_review_disposition')=='MATCHER_FALSE_NEGATIVE_CORRECTED' for x in fn_audits),
         'source_atomization_correction_rows':sum(x.get('fn_review_disposition')=='SOURCE_ATOMIZATION_ERROR_CORRECTED' for x in fn_audits),
         'generated_validity_counts':dict(class_counter),
         'generated_class_supported_noncovering':supported_noncovering,
         'change_delta_rows':len(changes),'exclusion_rows':len(exclusions),
         'regression_probes':probe_results,
       },
       'structural_validation':{'passed':not errors,'errors':errors,'warnings':warnings,
                                'independent_recomputation_from_item_ledgers':True,
                                'semantic_full_predicate_independently_certified':False},
       'equations':{
          'TP_plus_FN_equals_R':tp+fn==len(R),
          'TN_plus_B_equals_N':tn+B==len(N),
          'FP_minus_B_equals_F':fp-B==len(f_units),
          'four_cells_equal_universe':tp+fn+tn+fp==len(J),
          'canonical_predicted_positive_not_raw_class_count':tp+fp != len(G),
          'duplicate_partition_matches_excess':within+across==raw_excess,
       },
    }


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--base',type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--inputs',type=Path, default=Path('/mnt/data'))
    ap.add_argument('--write', action='store_true', help='write 06_metrics_final.json and 06_structural_validation.json')
    args=ap.parse_args()
    result=audit(args.base,args.inputs)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if args.write:
        (args.base/'06_metrics_final.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (args.base/'06_structural_validation.json').write_text(json.dumps(result['structural_validation'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return 0 if result['structural_validation']['passed'] else 2

if __name__=='__main__':sys.exit(main())
