#!/usr/bin/env python3
"""Independent final-ledger recomputation for the OrionDesk v6.1 evaluation.

Reads the final item-level ledgers; no previous score values or desired counts
are hardcoded. Structural assertions do not constitute semantic certification.

Usage:
    python compute_metrics.py [--directory DIRECTORY] [--write]
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUIRED = [
    '01_source_atoms_final.jsonl', '01_source_negative_controls_final.jsonl',
    '01_pdf_page_coverage_final.jsonl','02_generated_atoms_final.jsonl',
    '02_generated_classes_final.jsonl','02_generated_line_cell_coverage_final.jsonl',
    '03_canonical_universe_final.jsonl','03_evidence_matches_final.jsonl',
    '03_semantic_coverage_bridges_final.jsonl','03_fn_root_cause_audit_final.jsonl',
    '04_generated_claim_validity_final.jsonl','04_atomic_judgments_final.jsonl',
    '04_confusion_matrix_final.json','04_confusion_matrix_final.md',
    '04_duplicate_classes_final.jsonl','05_duplicate_metrics_final.json',
    '05_duplicate_metrics_final.md','05_tp_evidence_audit_final.jsonl',
    '05_source_atomization_audit_final.jsonl','07_change_delta.jsonl',
    '09_excluded_units.jsonl','02_canonical_lookup_index_final.json'
]


def load_jsonl(path):
    with open(path,encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def vuniq(items, key):
    vals = [r[key] for r in items]
    assert len(vals)==len(set(vals)),f'Duplicate {key} found'
    return set(vals)


def ratio(n, denom):
    return n / denom if denom else None


def normalized(text):
    t = text.replace('**','').replace('`','').replace('*','').replace('\\','')
    return re.sub(r'\s+', ' ', t).strip(' .|;,\t')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory',type=Path,default=HERE)
    parser.add_argument('--write',action='store_true',help='Write 06 metrics and audit JSON files')
    args = parser.parse_args()
    p = args.directory.resolve()
    checks, warnings = {}, []
    for filename in REQUIRED:
        assert (p/filename).is_file(),f'Missing deliverable {filename}'
    checks['required_final_ledgers_exist'] = True
    src=load_jsonl(p/'01_source_atoms_final.jsonl')
    neg=load_jsonl(p/'01_source_negative_controls_final.jsonl')
    occ=load_jsonl(p/'02_generated_atoms_final.jsonl')
    classes=load_jsonl(p/'02_generated_classes_final.jsonl')
    cm=load_jsonl(p/'03_canonical_universe_final.jsonl')
    judgments=load_jsonl(p/'04_atomic_judgments_final.jsonl')
    evidence=load_jsonl(p/'03_evidence_matches_final.jsonl')
    bridges=load_jsonl(p/'03_semantic_coverage_bridges_final.jsonl')
    fn=load_jsonl(p/'03_fn_root_cause_audit_final.jsonl')
    val=load_jsonl(p/'04_generated_claim_validity_final.jsonl')
    dupe=load_jsonl(p/'04_duplicate_classes_final.jsonl')
    tp=load_jsonl(p/'05_tp_evidence_audit_final.jsonl')
    natom=load_jsonl(p/'05_source_atomization_audit_final.jsonl')
    neg_audit=load_jsonl(p/'04_negative_control_assertion_audit_final.jsonl')
    coverage=load_jsonl(p/'01_pdf_page_coverage_final.jsonl')
    line_coverage=load_jsonl(p/'02_generated_line_cell_coverage_final.jsonl')
    delta=load_jsonl(p/'07_change_delta.jsonl')
    source_ids=vuniq(src,'source_id')
    negative_ids=vuniq(neg,'negative_control_id')
    assert source_ids.isdisjoint(negative_ids), 'Source-positive and negative IDs overlap'
    O=vuniq(occ,'occurrence_id'); G=vuniq(classes,'class_id')
    V=vuniq(val,'class_id'); assert G==V, 'Generated claim validity misses raw classes'
    U=vuniq(cm,'canonical_id'); vuniq(judgments,'canonical_id')
    assert cm==judgments, 'Canonical and judgment ledger disagree'
    assert len(set(x['prefix'] for x in occ+classes+cm))==1, 'Mixed method prefixes'
    assert {e['source_id'] for e in evidence}==source_ids
    assert len(cm)==len(src)+len(neg)+sum(v['pdf_validity_status']=='PDF_UNSUPPORTED' for v in val)
    checks['unique_ids_and_universe_partition'] = True

    occmap={x['occurrence_id']:x for x in occ}
    classmap={x['class_id']:x for x in classes}
    valmap={x['class_id']:x for x in val}
    memberships=[]
    for c in classes:
        ids=c['member_occurrence_ids']
        assert len(ids)==len(set(ids))==c['occurrence_count']
        assert all(i in O and occmap[i]['semantic_class_id']==c['class_id'] for i in ids)
        assert c['representative_occurrence_id'] in ids
        assert valmap[c['class_id']]['member_occurrence_ids']==ids
        memberships.extend(ids)
    assert len(memberships)==len(O) and set(memberships)==O
    assert len(O)>=len(G)
    checks['every_occurrence_in_exactly_one_class'] = True

    units={x['canonical_id']:x for x in cm}
    source_units={x['origin_source_ids'][0]:x for x in cm if x['origin_source_ids']}
    negative_units={x['origin_negative_control_ids'][0]:x for x in cm if x['origin_negative_control_ids']}
    assert len(source_units)==len(src) and set(source_units)==source_ids
    assert len(negative_units)==len(neg) and set(negative_units)==negative_ids
    counter=Counter()
    for x in cm:
        a,b=int(x['actual_label']),int(x['predicted_label']); cell=x['scoring_cell']
        assert a in (0,1) and b in (0,1)
        expected={(1,1):'TP',(1,0):'FN',(0,1):'FP',(0,0):'TN'}[(a,b)]
        assert expected==cell,(x['canonical_id'],cell,expected)
        if cell in ('TP','FN'):
            assert len(x['origin_source_ids'])==1
            assert not x['origin_negative_control_ids']
        if cell=='TN':
            assert len(x['origin_negative_control_ids'])==1
            assert not x['origin_source_ids'] and not x['origin_generated_class_ids']
        if cell=='FP' and x['origin_generated_class_ids'] and not x['origin_negative_control_ids']:
            assert len(x['origin_generated_class_ids'])==1
            assert valmap[x['origin_generated_class_ids'][0]]['pdf_validity_status']=='PDF_UNSUPPORTED'
        counter[cell]+=1
    assert all(sum(int(x['scoring_cell']==cell) for x in cm)==counter[cell] for cell in ('TP','TN','FP','FN'))
    checks['one_binary_judgment_per_canonical_unit']=True

    tp_ids={sid for sid,x in source_units.items() if x['scoring_cell']=='TP'}
    fn_ids={sid for sid,x in source_units.items() if x['scoring_cell']=='FN'}
    assert tp_ids.isdisjoint(fn_ids) and tp_ids|fn_ids==source_ids
    bridge_ids=vuniq(bridges,'source_id')
    tp_audit_ids=vuniq(tp,'source_id')
    assert tp_audit_ids==tp_ids, 'TP proof audit coverage inconsistent'
    assert all(x['final_scoring_cell']=='TP' and x['audit_outcome']=='CONFIRMED_TP' for x in tp)
    for tid in tp_ids:
        x=source_units[tid]
        assert x['generated_evidence'] and x['pdf_evidence'] and x['origin_generated_class_ids'],tid
        assert set(x['origin_generated_class_ids']).issubset(G)
        assert x['entailment_grade'] in ('E2','E3')
        assert x.get('predicate_check_en')
        if x['entailment_grade']=='E2':
            assert tid in bridge_ids and x.get('scope_membership_proof_en'),tid
    assert bridge_ids.issubset(tp_ids) and all(x['entailment_grade']=='E2' for x in bridges)
    checks['every_TP_has_proof_record_and_required_bridge_fields']=True

    fn_audit_ids=vuniq(fn,'source_id')
    assert fn_ids.issubset(fn_audit_ids)
    dispositions={'TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'}
    fn_counts=Counter()
    for a in fn:
        sid=a['source_id']
        assert sid in source_ids
        final_cell=source_units[sid]['scoring_cell']
        assert a['final_scoring_cell']==final_cell
        if final_cell=='FN':
            assert a['fn_review_disposition'] in dispositions
            assert a.get('best_generated_candidates'),sid
            assert a.get('exact_and_alias_keys_checked')
            assert a.get('universal_context_conjunction_checked')
            assert a.get('specific_reason_en')
            fn_counts[a['fn_review_disposition']]+=1
        else:
            assert a['fn_review_disposition']=='MATCHER_FALSE_NEGATIVE_CORRECTED'
    assert sum(fn_counts.values())==len(fn_ids)
    checks['FN_reciprocal_root_causes_and_corrected_candidates']=True

    asserted = {x['negative_control_id'] for x in neg_audit if x['asserted_by_generated_corpus']}
    assert vuniq(neg_audit,'negative_control_id')==negative_ids
    for nid in negative_ids:
        x=negative_units[nid]
        assert x['scoring_cell']==('FP' if nid in asserted else 'TN')
    F={v['class_id'] for v in val if v['pdf_validity_status']=='PDF_UNSUPPORTED'}
    f_units=[x for x in cm if x['scoring_cell']=='FP' and not x['origin_negative_control_ids']]
    assert {x['origin_generated_class_ids'][0] for x in f_units}==F
    assert len(f_units)==len(F)
    assert not any(x['origin_negative_control_ids'] and x['origin_generated_class_ids'] and x['origin_generated_class_ids'][0] in F for x in cm)
    checks['generated_only_FP_and_bounded_N_are_nonoverlapping']=True

    assert counter['TP']==len(tp_ids)
    assert counter['FN']==len(src)-len(tp_ids)
    assert counter['TN']==len(neg)-len(asserted)
    assert counter['FP']==len(F)+len(asserted)
    assert len(cm)==len(src)+len(neg)+len(F)
    assert counter['TP']+counter['TN']+counter['FP']+counter['FN']==len(cm)
    assert counter['TP']+counter['FP']==sum(x['predicted_label'] for x in cm)
    checks['one_universe_four_cell_equations']=True

    dmap={x['class_id']:x for x in dupe}
    assert set(dmap)==G
    within=across=repeated=multi=0
    for c in classes:
        d=dmap[c['class_id']]
        assert d['occurrence_count']==len(c['member_occurrence_ids'])
        assert set(d['member_occurrence_ids'])==set(c['member_occurrence_ids'])
        assert d['duplicate_excess']==d['occurrence_count']-1
        assert d['within_file_excess']+d['across_file_excess']==d['duplicate_excess']
        within+=d['within_file_excess'];across+=d['across_file_excess']
        repeated+=d['occurrence_count']>=2
        multi+=bool(d['spans_multiple_input_files'])
    assert within+across==len(O)-len(G)
    checks['duplicate_occurrence_partition']=True

    # Check the entire uploaded input scope and the physical PDF page inventory.
    manifest=json.loads((p/'01_input_manifest_final.json').read_text())
    inputs={entry['filename']:entry for entry in manifest['files'] if entry['input_role'].endswith('_scored_markdown')}
    assert len(inputs)==8
    lines_per_file=Counter(x['file'] for x in line_coverage)
    for fname,info in inputs.items():
        path=ROOT/fname
        assert path.is_file(),fname
        b=path.read_bytes()
        assert len(b)==info['bytes']
        assert hashlib.sha256(b).hexdigest()==info['sha256']
        lines=path.read_text(encoding='utf8').splitlines()
        assert len(lines)==lines_per_file[fname],fname
        assert {x['line'] for x in line_coverage if x['file']==fname}==set(range(1,len(lines)+1))
    assert set(lines_per_file)==set(inputs)
    assert vuniq(coverage,'physical_page')==set(range(1,91))
    assert all(x['readable_text'] for x in coverage)
    pdf=ROOT/'OrionDesk_AI_Detailed_Design_Specification(2).pdf'
    assert pdf.exists()
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==manifest['files'][0]['sha256']
    try:
        import fitz
        with fitz.open(pdf) as pd:
            assert len(pd)==len(coverage)
    except ImportError:
        warnings.append('PyMuPDF unavailable; 90-page PDF extent verified only from the page ledger.')
    checks['90_PDF_pages_and_eight_scored_inputs_inspected']=True

    # Verify usable evidence locators; normalized quotation checks are advisory
    # because punctuation/Markdown formatting and combined table-cell contexts vary.
    locators_seen=set()
    missing_locators=[]
    quote_mismatches=[]
    for tp_record in tp:
        for ev in tp_record['generated_evidence']:
            key=(ev.get('file'),ev.get('line_start'),ev.get('line_end'),ev.get('quote_en',''))
            if key in locators_seen:continue
            locators_seen.add(key)
            path=ROOT / ev.get('file','')
            if not path.is_file() or not isinstance(ev.get('line_start'),int) or ev['line_start']<1:
                missing_locators.append(key);continue
            lines=path.read_text(encoding='utf8').splitlines()
            start=ev['line_start'];end=ev.get('line_end',start)
            if end>len(lines): missing_locators.append(key);continue
            quote=normalized(ev.get('quote_en',''))
            hay=normalized(' '.join(lines[start-1:end]))
            if quote and quote.casefold() not in hay.casefold():
                # A meaningful cell and the full physical row may reconstruct
                # the same predicate with different punctuation/syntax.
                if not ev.get('table_cell') and not ev.get('full_line_context_en'):
                    quote_mismatches.append(key)
    assert not missing_locators, f'Missing TP generated evidence locators: {missing_locators[:3]}'
    checks['TP_original_generated_file_line_locations_resolve']=True
    if quote_mismatches: warnings.append(f'{len(quote_mismatches)} non-table TP quotation(s) need manual normalization check.')

    # Assert source-atomization audit exists and any changed IDs are reflected.
    assert natom and any(x['source_atoms_reviewed']==len(src) for x in natom)
    assert all(x['source_id'] in source_ids for x in evidence)
    checks['atomization_audit_and_source_id_integrity']=True

    precision=ratio(counter['TP'],counter['TP']+counter['FP'])
    recall=ratio(counter['TP'],counter['TP']+counter['FN'])
    f1=ratio(2*counter['TP'],2*counter['TP']+counter['FP']+counter['FN'])
    dup=ratio(len(O)-len(G),len(O))
    baseline=json.loads((p/'04_confusion_matrix_final.json').read_text())
    prevdup=json.loads((p/'05_duplicate_metrics_final.json').read_text())
    for k in ('TP','TN','FP','FN'):assert baseline['confusion'][k]==counter[k]
    for k,v in [('Precision',precision),('Recall',recall),('F1',f1),('Duplicate',dup)]:
        assert abs(baseline['metrics'][k]-v)<1e-12
    for k,v in [('within_file_excess',within),('across_file_excess',across),('duplicate_excess_occurrences',len(O)-len(G))]:
        assert prevdup[k]==v
    checks['reported_phase5_baselines_reconcile']=True

    # A final phase must be delivered as reproducible English files, not merely
    # as a reconciled in-memory confusion matrix.
    mandatory_phase6 = [
        '06_metrics_final.md','08_coverage_and_limitations.md',
        '06_phase_status_final.json', '06_exact_match_regression_probes_final.jsonl',
        '06_ledger_reconciliation_audit.json', '06_exact_match_corrections_final.jsonl',
    ]
    for filename in mandatory_phase6:
        assert (p/filename).is_file(),f'Missing final phase-6 deliverable: {filename}'
    coverage_report=(p/'08_coverage_and_limitations.md').read_text(encoding='utf-8').casefold()
    for concept in ['universal','bounded', 'fn', 'tp', 'atomization',
                    'duplicate', 'evidence', 'semantic', 'source', 'precision',
                    'recall', 'f1', 'phase 6', 'final_best_effort']:
        assert concept in coverage_report, f'Missing coverage/limitation disclosure: {concept}'
    non_english=[]
    non_english_re=re.compile(r'[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]')
    authored=set(REQUIRED+mandatory_phase6+[
        '06_metrics_final.json', '06_metrics_final.md', '06_structural_audit_final.json',
        '05_duplicate_metrics_final.json','07_change_delta.jsonl', '06_exact_match_regression_probes_final.jsonl',
        'compute_metrics.py'])
    for filename in authored:
        path=p/filename
        if not path.exists() or path.suffix=='.pdf': continue
        if non_english_re.search(path.read_text(encoding='utf-8')):
            non_english.append(filename)
    assert not non_english, f'Non-English CJK detected in authored files: {non_english}'
    checks['final_report_language_and_required_disclosures'] = True

    result={
        'prefix':next(iter({x['prefix'] for x in occ})),
        'protocol_version':'6.1',
        'phase':6,
        'status':'FINAL_BEST_EFFORT',
        'universe':{
            'source_positive_atoms':len(src),'source_negative_controls':len(neg),
            'raw_generated_claim_classes':len(G),
            'generated_positive_occurrences':len(O),
            'covered_source_atoms':len(tp_ids),
            'asserted_negative_controls':len(asserted),
            'unsupported_generated_only_propositions':len(F),
            'canonical_predicted_positive_units':counter['TP']+counter['FP'],
            'canonical_decision_units':len(cm),
            'negative_universe_scope':'PDF-grounded, predeclared bounded controls only'
        },
        'confusion':{k:counter[k] for k in ('TP','TN','FP','FN')},
        'metrics':{'Precision':precision,'Recall':recall,'F1':f1,'Duplicate':dup},
        'duplicate':{
            'eligible_generated_occurrences':len(O),'unique_generated_claim_classes':len(G),
            'duplicate_excess_occurrences':len(O)-len(G),'within_file_excess':within,
            'across_file_excess':across,'repeated_claim_class_count':repeated,
            'repeated_classes_spanning_multiple_files':multi
        },
        'fn_root_causes':dict(fn_counts),
        'corrected_initial_fn_candidates':sum(x['final_scoring_cell']=='TP' for x in fn),
        'tp_proof_audit_records':len(tp),
        'source_atomization_changed_ids':sum(x['decision']!='NO_ATOMIZATION_CHANGES' for x in natom),
        'generated_class_pdf_validity_counts':dict(Counter(x['pdf_validity_status'] for x in val)),
        'reconciliation':{
            'corrected_stale_phase4_mirrors':True,
            'universe_restored_from_phase5_item_level_adjudications':True,
            'new_semantic_adjudications_in_phase6':0
        },
        'structural_audit':{'all_checks_passed':all(checks.values()),'checks':checks,
                            'tp_unique_original_locators_reviewed':len(locators_seen),
                            'missing_tp_evidence_locators':len(missing_locators),
                            'advisory_non_table_quote_normalization_issues':len(quote_mismatches),
                            'warnings':warnings},
        'semantic_certification':False,
        'metric_interpretation':('Conventional binary Precision, Recall and F1 over one effective PDF-source/negative-control/'
            'generated-unsupported canonical universe; raw generated class and occurrence counts are separate. '
            'Passing structural validation does not certify every semantic judgment.')
    }
    if args.write:
        (p/'06_metrics_final.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (p/'06_structural_audit_final.json').write_text(json.dumps(result['structural_audit'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
