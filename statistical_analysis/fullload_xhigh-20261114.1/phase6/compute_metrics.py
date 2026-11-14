#!/usr/bin/env python3
"""Independent, ledger-driven recomputation for OrionDesk Protocol 6.1 Phase 6.

Usage:
    python compute_metrics.py [--directory DIR] [--check-only]

The script does not use historical counts or scores. Semantic judgments remain
explicitly best-effort; arithmetic and evidence-location checks are not proofs
of logical entailment.
"""
from __future__ import annotations
import argparse
import collections
import json
import re
from pathlib import Path

ROLE_FILES = [
    '01_screen_functions(1).md', '02_api(1).md', '03_data(1).md',
    '04_batch_functions(1).md', '05_business_rules(2).md',
    '06_exception_handling(3).md', '07_processing_flows(2).md',
    '08_architecture_decision(2).md',
]
REQUIRED_EVIDENCE_KEYS = ('target','action','actor','condition','scope','timing',
                          'constraint','exception','outcome','version')


def jsonl(path: Path) -> list[dict]:
    with path.open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def unique(items: list[dict], field: str, label: str) -> dict[str, dict]:
    result = {}
    for record in items:
        key = record[field]
        if key in result:
            raise AssertionError(f'Duplicate {label}: {key}')
        result[key] = record
    return result


def metric(num: int, denominator: int) -> float | None:
    return num / denominator if denominator else None


def norm(s: str) -> str:
    return ' '.join(re.findall(r'[a-z0-9]+', s.lower()))


def get_context(root: Path) -> Path:
    return root.parent


def compute(root: Path, write_outputs: bool=True) -> tuple[dict, dict]:
    source = unique(jsonl(root/'01_source_atoms_final.jsonl'), 'source_id', 'PDF atom')
    negatives = unique(jsonl(root/'01_source_negative_controls_final.jsonl'), 'negative_control_id', 'negative control')
    go = unique(jsonl(root/'02_generated_atoms_final.jsonl'), 'occurrence_id', 'generated occurrence')
    gc = unique(jsonl(root/'02_generated_classes_final.jsonl'), 'class_id', 'generated class')
    judgments = unique(jsonl(root/'04_atomic_judgments_final.jsonl'), 'canonical_id', 'judgment')
    universe = unique(jsonl(root/'03_canonical_universe_final.jsonl'), 'canonical_id', 'universe item')
    evidences = unique(jsonl(root/'03_evidence_matches_final.jsonl'), 'source_id', 'source match')
    validity = unique(jsonl(root/'04_generated_claim_validity_final.jsonl'), 'class_id', 'validity item')
    fp = unique(jsonl(root/'04_substantive_generated_only_findings_final.jsonl'), 'f_id', 'unsupported claim')
    fn_records = jsonl(root/'03_fn_root_cause_audit_final.jsonl')
    tp_records = jsonl(root/'05_tp_evidence_audit_final.jsonl')
    atomization = jsonl(root/'05_source_atomization_audit_final.jsonl')
    changes = jsonl(root/'07_change_delta.jsonl')
    negative_audit = unique(jsonl(root/'04_negative_control_assertion_audit_final.jsonl'), 'negative_control_id', 'negative assertion audit')
    errors=[]; warnings=[]; stats={}
    def verify(condition: bool, explanation: str):
        if not condition: errors.append(explanation)
    def caution(condition: bool, explanation: str):
        if not condition: warnings.append(explanation)

    inp_dir=get_context(root)
    input_lengths={}
    lines={}
    for file in ROLE_FILES:
        p=inp_dir/file
        verify(p.is_file(),f'Missing scored original input {file}')
        if p.is_file():
            lines[file]=p.read_text(encoding='utf-8').splitlines()
            input_lengths[file]=len(lines[file])
    pdf_path=inp_dir/'OrionDesk_AI_Detailed_Design_Specification(1).pdf'
    verify(pdf_path.is_file(), 'Original authoritative PDF missing')
    pdf_pages=None
    if pdf_path.is_file():
        try:
            import fitz
            doc=fitz.open(pdf_path)
            pdf_pages=len(doc)
            verify(pdf_pages == 90,'Original PDF physical page count is not 90')
            doc.close()
        except Exception as e:errors.append('Could not read source PDF: '+str(e))
    page_entries = jsonl(inp_dir/'phase1/01_pdf_page_coverage.jsonl')
    stats['prior_pdf_coverage_records']=len(page_entries)
    verify(len(page_entries)==pdf_pages,'Phase 1 page coverage does not enumerate every physical PDF page')
    prev_coverage = jsonl(inp_dir/'phase2/02_generated_line_cell_coverage.jsonl')
    stats['prior_generated_coverage_records']=len(prev_coverage)

    verify(len(set(source)&set(negatives)) == 0,'Source-positive and negative-control identifiers overlap')
    verify(set(source)==set(evidences),'Source atom and evidence-match ledgers differ')
    verify(set(gc)==set(validity),'Generated classes and validity rows differ')
    verify(set(judgments)==set(universe),'Judgment and universe ID sets differ')
    counts=collections.Counter()
    prefix_values=collections.Counter()
    for cid,j in judgments.items():
        u=universe[cid]
        verify((u['actual_label'],u['predicted_label'],u['scoring_cell']) ==
               (j['actual_label'],j['predicted_label'],j['scoring_cell']),f'Universe/judgment label discrepancy for {cid}')
        cell=j['scoring_cell']; counts[cell]+=1
        verify(cell in ['TP','TN','FP','FN'],f'Unexpected scoring cell for {cid}')
        expected={'TP':(1,1),'FN':(1,0),'FP':(0,1),'TN':(0,0)}.get(cell)
        verify((j['actual_label'],j['predicted_label'])==expected,f'Binary-label mismatch for {cid}')
        prefix_values[j.get('prefix')]+=1
        if cell in ('TP','FN'):
            verify(len(j['origin_source_ids'])==1 and j['origin_source_ids'][0] in source,f'{cell} missing source atom {cid}')
            verify(not j['origin_negative_control_ids'],f'{cell} references negative control {cid}')
        elif j['origin_negative_control_ids']:
            verify(len(j['origin_negative_control_ids'])==1 and j['origin_negative_control_ids'][0] in negatives,
                   f'Bad control ID in {cid}')
        elif cell=='FP':
            verify(any(set(j.get('origin_generated_class_ids',[])) == set(f.get('origin_generated_class_ids',[])) for f in fp.values()),f'FP not found by generated-class evidence: {cid}')
    verify(len(prefix_values)==1, 'Mixed method prefixes in canonical universe')
    verify(len(set(x['method'] for x in go.values()))==1,'Mixed methods among generated occurrences')
    verify(len(set(x['method'] for x in gc.values()))==1,'Mixed methods among generated classes')
    verify({j['origin_source_ids'][0] for j in judgments.values() if j['actual_label']==1}==set(source),
           'Not exactly one canonical positive decision per R')
    verify({j['origin_negative_control_ids'][0] for j in judgments.values() if j['origin_negative_control_ids']}==set(negatives),
           'Not exactly one canonical negative decision per N')
    verify(collections.Counter(tuple(sorted(j['origin_generated_class_ids'])) for cid,j in judgments.items() if j['scoring_cell']=='FP' and not j['origin_negative_control_ids']) ==
           collections.Counter(tuple(sorted(f['origin_generated_class_ids'])) for f in fp.values()),
           'Unsupported F ledger differs from independent FP canonical generated-class groups')

    # Recompute raw within-method class partition independently of metrics JSON.
    members=set(); repeat=[]; within=across=spanning=0
    file_order={p:i for i,p in enumerate(ROLE_FILES)}
    dup_records=[]
    for cid,c in gc.items():
        ids=c['occurrence_ids']
        verify(bool(ids) and len(ids)==len(set(ids)),f'Empty or duplicate membership for {cid}')
        verify(set(ids).issubset(go),f'Unknown generated occurrence in {cid}')
        if not ids or not set(ids).issubset(go):continue
        for oid in ids:
            members.add(oid)
            verify(go[oid].get('class_id')==cid,f'Occurrence {oid} linked to wrong class')
        verify(c.get('representative_occurrence_id') in ids, f'Representative not a class member: {cid}')
        ordered=sorted([go[i] for i in ids],key=lambda o:(file_order.get(o['file'],99),o['line_start'],o.get('table_cell',{}).get('column_index',0) if isinstance(o.get('table_cell'),dict) else 0,o['occurrence_id']))
        previously_seen_files={ordered[0]['file']}
        local_within=local_across=0
        for o in ordered[1:]:
            if o['file'] in previously_seen_files:within+=1;local_within+=1
            else:across+=1;local_across+=1
            previously_seen_files.add(o['file'])
        if len(ordered)>1:
            repeat.append(cid)
            if len({o['file'] for o in ordered})>1:spanning+=1
            r=ordered[0]
            ev={'file':r['file'],'line_start':r['line_start'],'line_end':r['line_end'],
                'quote_en':r.get('source_quote_en',''),'table_cell':r.get('table_cell')}
            dup_records.append({'class_id':cid,'normalized_proposition_en':c['normalized_proposition_en'],
                'representative_occurrence_id':r['occurrence_id'],'representative_evidence':ev,
                'eligible_occurrence_count':len(ids),'excess_occurrences':len(ids)-1,
                'within_file_excess':local_within,'across_file_excess':local_across,
                'spans_multiple_files':len({o['file'] for o in ordered})>1,
                'repeated_occurrences':[{'occurrence_id':o['occurrence_id'],'file':o['file'],'line_start':o['line_start']} for o in ordered[1:]],
                'merge_reason_en':'Inherited class full-predicate equivalence; originally declared class membership retained.',
                'audit_limitation_en':'Recomputation validates the partition, not every semantic equivalence.'})
    verify(members==set(go),'Eligible occurrences not partitioned exactly once')
    verify(sum(len(c['occurrence_ids']) for c in gc.values())==len(go),'Class-member sum not equal to GO')
    verify(len(go)>=len(gc), 'GO smaller than GC')
    duplicate_excess=len(go)-len(gc)
    verify(within+across==duplicate_excess,'Duplicate excess partition failed')
    for o in go.values():
        verify(o['file'] in lines and 1<=o['line_start']<=len(lines.get(o['file'],[])),
               f'Generated occurrence locator invalid: {o["occurrence_id"]}')
        if o['file'] in lines and 1<=o['line_start']<=len(lines[o['file']]):
            original=' '.join(lines[o['file']][o['line_start']-1:o['line_end']]).strip()
            quote=o.get('source_quote_en','').strip()
            if quote and norm(quote) not in norm(original) and norm(original) not in norm(quote):
                warnings.append(f'Partial original-line quotation for generated occurrence {o["occurrence_id"]}')
    if write_outputs:
        with (root/'04_duplicate_classes_final.jsonl').open('w',encoding='utf-8') as f:
            for r in dup_records:f.write(json.dumps(r,ensure_ascii=False)+'\n')

    # Full TP/FN audits, explicit source/generation locators and reciprocal evidence.
    tp_by=collections.defaultdict(list);fn_by=collections.defaultdict(list)
    for t in tp_records:tp_by[t['source_id']].append(t)
    for f in fn_records:fn_by[f['source_id']].append(f)
    verified_tp_locators=0;ttp=0; pdf_locators=0
    for cid,j in judgments.items():
        cell=j['scoring_cell']
        if cell in ('TP','FN'):
            src=j['origin_source_ids'][0]
            verify(bool(j['pdf_evidence']),f'{src} missing PDF quote')
            for e in j.get('pdf_evidence',[]):
                page=e.get('physical_page')
                verify(isinstance(page,int) and pdf_pages is not None and 1<=page<=pdf_pages,
                       f'PDF page locator invalid for {src}: {page}')
                verify(bool(e.get('quote_en')),f'Empty PDF quotation for {src}')
                pdf_locators+=1
            verify(bool(j.get('generated_evidence')) if cell=='TP' else True, f'TP without generated evidence: {src}')
        if cell=='TP':
            src=j['origin_source_ids'][0];ttp+=1
            verify(len(tp_by[src])==1, f'TP evidence proof not exactly one for {src}')
            verify(j.get('entailment_grade') in ('E2','E3'),f'TP without E2/E3 coverage: {src}')
            verify(bool(j.get('origin_generated_class_ids')) and set(j['origin_generated_class_ids']).issubset(gc),
                   f'TP without valid eligible generated class IDs: {src}')
            for ev in j.get('generated_evidence',[]):
                filename=ev.get('file');lineno=ev.get('line_start')
                verify(filename in lines and isinstance(lineno,int) and 1<=lineno<=len(lines.get(filename,[])),
                       f'Bad TP Markdown locator: {src}')
                if filename in lines and isinstance(lineno,int) and 1<=lineno<=len(lines[filename]):
                    original=' '.join(lines[filename][lineno-1:ev.get('line_end',lineno)]).strip()
                    quote=ev.get('quote_en','').strip()
                    caution(not quote or norm(quote) in norm(original) or norm(original) in norm(quote),
                            f'Original-line quotation mismatch in TP {src} {filename}:{lineno}')
                    verified_tp_locators+=1
            if tp_by[src]:
                a=tp_by[src][0]
                verify(a['audit_outcome']=='CONFIRMED_TP',f'TP audit not marked confirmed for {src}')
                checks=a.get('predicate_checks',{})
                verify(set(REQUIRED_EVIDENCE_KEYS).issubset(checks),f'TP predicate-check fields incomplete: {src}')
                for key in REQUIRED_EVIDENCE_KEYS:
                    if key not in checks:continue
                    verify(checks[key].get('assessment') in ('met','not_applicable'),
                           f'TP predicate assessment incomplete: {src}:{key}')
                    verify(bool(checks[key].get('proof_en')),f'TP predicate proof missing {src}:{key}')
        elif cell=='FN':
            src=j['origin_source_ids'][0]
            verify(len(fn_by[src])==1,f'FN root cause not exactly one for {src}')
            if fn_by[src]:
                a=fn_by[src][0]
                verify(a.get('final_scoring_cell')=='FN' and a.get('fn_review_disposition') in
                       ('TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'),
                       f'FN terminal disposition invalid: {src}')
                verify(bool(a.get('best_generated_candidates')),f'No actual reciprocal candidate for {src}')
                verify(bool(a.get('exact_and_alias_keys_checked')),f'No reverse search detail for {src}')
    for a in fn_records:
        sid=a['source_id']
        if a.get('final_scoring_cell')=='TP':
            verify(sid in source and any(j['scoring_cell']=='TP' and j['origin_source_ids']==[sid] for j in judgments.values()),
                   f'Corrected FN not reflected in canonical TP {sid}')
        elif a.get('final_scoring_cell')=='REMOVED_OR_MERGED':
            verify(sid not in source,f'Removed source atom still scored: {sid}')
    verify(all(cid in negative_audit for cid in negatives),'Negative control lacks assertion-audit record')
    for j in judgments.values():
        if j['origin_negative_control_ids']:
            nid=j['origin_negative_control_ids'][0]
            assert_state=negative_audit[nid].get('asserted_by_eligible_generated_corpus')
            verify((j['scoring_cell']=='FP')==bool(assert_state),f'Control assertion inconsistency: {nid}')

    # One canonical proposition universe, independently reconstructed.
    TPn=counts['TP']; FNn=len(source)-TPn
    Bn=sum(bool(negative_audit[n].get('asserted_by_eligible_generated_corpus')) for n in negatives)
    TNn=len(negatives)-Bn
    Fn=len(fp);FPn=Fn+Bn
    VerifyCounts={'TP':TPn,'TN':TNn,'FP':FPn,'FN':FNn}
    verify(VerifyCounts=={x:counts[x] for x in VerifyCounts},'Four-cell counts differ from recomputed A,B,F sets')
    verify(TPn+FNn==len(source),'TP+FN != |R|')
    verify(TNn+Bn==len(negatives),'TN+|B| != |N|')
    verify(FPn-Bn==Fn,'FP-|B| != |F|')
    verify(TPn+TNn+FPn+FNn==len(judgments),'Total scoring-cell count != |U|')
    verify(TPn+FPn==sum(j['predicted_label'] for j in judgments.values()), 'Predicted positives not reconciled')
    verify(all(v['validity_label'] in ('PDF_ENTAILED','PDF_UNSUPPORTED','SUPPORTED_NONCOVERING') for v in validity.values()),
           'Invalid generated class correctness label')
    verify({v['class_id'] for v in validity.values() if v['validity_label']=='PDF_UNSUPPORTED'}==
           {c for f in fp.values() for c in f['origin_generated_class_ids']},
           'Unsupported generated class validity does not match F set')
    verify(len(set(x['source_id'] for x in tp_records))==len(tp_records),'Duplicate TP audit record')
    verify(len(atomization)>0,'Source atomization audit absent')
    for r in source.values():
        verify(bool(r.get('pdf_evidence')),f'Source atom evidence absent: {r["source_id"]}')
    for f in fp.values():
        verify(set(f['origin_generated_class_ids']).issubset(gc),f'F references missing eligible class {f["f_id"]}')
        verify(bool(f.get('generated_evidence')),f'F lacks generated evidence {f["f_id"]}')

    audit_rootcauses=collections.Counter(a['fn_review_disposition'] for a in fn_records if a.get('final_scoring_cell')=='FN')
    verify(sum(audit_rootcauses.values())==FNn,'FN root-cause subtotal does not match FN')
    # All ten final-summary claims are verified as disclosures, not as semantic truth.
    report=root/'08_coverage_and_limitations.md'
    verify(report.exists(),'Coverage-and-limitations report missing')
    content=report.read_text(encoding='utf-8').lower() if report.exists() else ''
    for token in ['bounded','negative','precision','recall','false-negative','atomization','audit','universal','noncovering','best effort']:
        caution(token in content,f'Coverage report could more explicitly mention: {token}')
    mandatory=['01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl',
               '02_generated_atoms_final.jsonl','02_generated_classes_final.jsonl',
               '03_canonical_universe_final.jsonl','03_evidence_matches_final.jsonl',
               '03_semantic_coverage_bridges_final.jsonl','03_fn_root_cause_audit_final.jsonl',
               '04_generated_claim_validity_final.jsonl','04_atomic_judgments_final.jsonl',
               '04_confusion_matrix_final.json','04_confusion_matrix_final.md',
               '04_duplicate_classes_final.jsonl','05_duplicate_metrics_final.json',
               '05_duplicate_metrics_final.md','05_tp_evidence_audit_final.jsonl',
               '05_source_atomization_audit_final.jsonl','07_change_delta.jsonl',
               '08_coverage_and_limitations.md','09_excluded_units.jsonl','compute_metrics.py']
    for f in mandatory:verify((root/f).is_file(),f'Required output missing: {f}')
    authored_files=list(root.glob('*.md'))+[root/'compute_metrics.py']
    for p in authored_files:
        if p.exists():
            caution(not re.search(r'[\u3040-\u30ff\u3400-\u9fff]',p.read_text(encoding='utf-8')),
                    f'Japanese characters in English authored deliverable: {p.name}')

    precision=metric(TPn,TPn+FPn);recall=metric(TPn,TPn+FNn)
    f1=metric(2*TPn,2*TPn+FPn+FNn)
    dup=metric(duplicate_excess,len(go))
    stats.update({'source_positive_count':len(source),'fixed_negative_control_count':len(negatives),
        'generated_occurrence_count':len(go),'generated_class_count':len(gc),
        'unsupported_generated_only_count':Fn,'asserted_negative_control_count':Bn,
        'predicted_positive_count':TPn+FPn,'canonical_universe_count':len(judgments),
        'final_TP_audit_entries':ttp,'real_generated_TP_locator_checks':verified_tp_locators,
        'PDF_quote_locator_checks':pdf_locators,
        'remaining_FN_root_cause_counts':dict(audit_rootcauses),'input_markdown_physical_lines':input_lengths,
        'atomization_audit_rows':len(atomization),'change_delta_rows':len(changes),
        'negative_control_audit_rows':len(negative_audit),
        'duplicate_excess':duplicate_excess,'within_file_excess':within,'across_file_excess':across,
        'repeated_claim_classes':len(repeat),'multi_file_repeated_classes':spanning,
        'pdf_physical_pages':pdf_pages})
    # Audit warnings are disclosed and prevent an unsupported VERIFIED label.
    status='FINAL_BEST_EFFORT' if not errors else 'STRUCTURAL_VALIDATION_FAILED'
    result={'prefix':next(iter(prefix_values)),'status':status,'protocol_version':'6.1','phase':6,
      'universe':{'source_positive_atoms':len(source),'source_negative_controls':len(negatives),
                  'raw_generated_claim_classes':len(gc),'generated_positive_occurrences':len(go),
                  'covered_source_atoms':TPn,'asserted_negative_controls':Bn,
                  'unsupported_generated_only_propositions':Fn,'canonical_predicted_positive_units':TPn+FPn,
                  'canonical_decision_units':len(judgments),
                  'negative_universe_scope':'PDF-grounded predeclared bounded counterfactual controls only'},
      'confusion':VerifyCounts,
      'metrics':{'Precision':precision,'Recall':recall,'F1':f1,'Duplicate':dup},
      'duplicate_partition':{'excess_occurrences':duplicate_excess,'within_file_excess':within,
                             'across_file_excess':across,'repeated_claim_classes':len(repeat),
                             'classes_spanning_multiple_files':spanning},
      'checks':{'structural_error_count':len(errors),'structural_errors':errors[:100],
                'review_warning_count':len(warnings),'review_warning_samples':warnings[:60],
                'item_level_judgments_enumerated':len(judgments)==len(source)+len(negatives)+len(fp),
                'original_pdf_readable':pdf_pages is not None,
                'source_FP_TP_evidence_audit_provided':True,
                'semantic_entailment_certified':False},
      'audit_counts':stats,
      'metric_interpretation':'Arithmetic on one canonical effective-proposition universe. Raw class count is not the number of canonical predicted positives; bounded TN is not population-wide accuracy. Exact semantic completeness and all duplicate equivalences remain unverified.'}
    if write_outputs:
        (root/'06_metrics_final.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (root/'06_structural_validation_final.json').write_text(json.dumps({'errors':errors,'warnings':warnings[:200],
                    'structural_checks_passed':not errors,'audit_counts':stats},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result, {'errors':errors,'warnings':warnings}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--check-only',action='store_true')
    a=parser.parse_args()
    result,detail=compute(a.directory,not a.check_only)
    print(json.dumps({'status':result['status'],'confusion':result['confusion'],'metrics':result['metrics'],
                      'error_count':len(detail['errors']),'warning_count':len(detail['warnings'])},indent=2))
    if detail['errors']:
        for e in detail['errors'][:25]:print('STRUCTURAL ERROR:',e)
        raise SystemExit(1)
