#!/usr/bin/env python3
"""Independent structural checks for the Phase-5 corrected item-level ledgers.
This script does not certify semantic entailment or perform Phase 6.
"""
import json,collections,hashlib
from pathlib import Path
ROOT=Path('/mnt/data');D=ROOT/'oriondesk_v6_1_phase5'
read=lambda p:[json.loads(s) for s in (D/p).read_text().splitlines() if s.strip()]
R=read('01_source_atoms_final.jsonl'); N=read('01_source_negative_controls_final.jsonl');O=read('02_generated_atoms_final.jsonl');G=read('02_generated_classes_final.jsonl')
E=read('03_evidence_matches_final.jsonl');B=read('03_semantic_coverage_bridges_final.jsonl');F=read('03_fn_root_cause_audit_final.jsonl')
U=read('03_canonical_universe_final.jsonl');J=read('04_atomic_judgments_final.jsonl');V=read('04_generated_claim_validity_final.jsonl')
Dup=read('04_duplicate_classes_final.jsonl');TP=read('05_tp_evidence_audit_final.jsonl');A=read('05_source_atomization_audit_final.jsonl')
M=json.loads((D/'04_confusion_matrix_final.json').read_text());DUP=json.loads((D/'05_duplicate_metrics_final.json').read_text())
lines={p.name:p.read_text().splitlines() for p in ROOT.glob('0[1-8]*.md') if p.name[:2].isdigit()}
checks={}
def test(n,flag):checks[n]=bool(flag);assert flag,n
test('original_pdf_90_pages',__import__('fitz').open(ROOT/'OrionDesk_AI_Detailed_Design_Specification(6).pdf').page_count==90)
test('all_eight_scored_inputs_available',len(lines)==8)
test('source_atom_count',len(R)==1024)
test('source_ids_unique',len({x['source_id'] for x in R})==len(R))
test('negative_controls_same_as_phase1', (D/'01_source_negative_controls_final.jsonl').read_bytes()==(ROOT/'oriondesk_v6_1_phase1/01_source_negative_controls_final.jsonl').read_bytes())
test('source_quotes_and_pages_unchanged',all((r['source_id'],r['quote_en'],r['physical_page'])==(o['source_id'],o['quote_en'],o['physical_page']) for r,o in zip(R,[json.loads(s) for s in (ROOT/'oriondesk_v6_1_phase1/01_source_atoms_final.jsonl').read_text().splitlines()])))
test('source_audit_complete',len(A)==len(R) and set(x['source_id'] for x in A)==set(x['source_id'] for x in R))
test('unique_occurrences',len(O)==len({x['occurrence_id'] for x in O}))
test('unique_raw_classes',len(G)==len({x['class_id'] for x in G}))
test('classes_and_occurrences_bijective',set(x['class_id'] for x in O)==set(x['class_id'] for x in G) and sum(x['occurrence_count'] for x in G)==len(O))
test('generated_quotes_match_current_files',all(o['quote_en'].strip() in lines[o['file']][o['line_start']-1] for o in O))
test('validity_one_record_per_class',set(x['generated_class_id'] for x in V)==set(x['class_id'] for x in G))
test('evidence_source_one_per_atom',set(x['source_id'] for x in E)==set(x['source_id'] for x in R))
test('all_final_TPs_have_live_generated_classes',all(set(x['generated_class_ids'])<=set(g['class_id'] for g in G) and x['generated_evidence'] for x in E if x['scoring_cell']=='TP'))
test('bridges_only_for_final_TPs',all(next(x for x in E if x['source_id']==b['source_id'])['scoring_cell']=='TP' for b in B))
test('fn_audit_all_initial_and_final',all(x['source_id'] in {e['source_id'] for e in E} for x in F) and all(x['source_id'] in {f['source_id'] for f in F} for x in E if x['scoring_cell']=='FN'))
test('tp_audit_includes_all_TPs_and_corrected_TP_downgrades',set(x['source_id'] for x in TP)>=set(x['source_id'] for x in E if x['scoring_cell']=='TP') and len(TP)==676)
test('negative_controls_37',len(N)==37)
test('canonical_one_row_per_ID',len(U)==len({x['canonical_id'] for x in U}) and len(U)==len(J))
test('universe_cells_agree_with_judgments',all(x['canonical_id']==y['canonical_id'] and x['scoring_cell']==y['scoring_cell'] for x,y in zip(U,J)))
counts=collections.Counter(x['scoring_cell'] for x in U)
test('one_universe_equations',counts['TP']+counts['FN']==len(R) and counts['TN']==len(N) and counts['FP']==sum(v['validity_label']=='PDF_UNSUPPORTED' for v in V) and sum(counts.values())==len(U))
test('stored_four_cells_match_rows',all(M[k]==counts[k] for k in ('TP','FN','FP','TN')))
test('prediction_identity',M['canonical_predicted_positive_count']==counts['TP']+counts['FP'])
test('dedup_partition',sum(x['within_file_excess']+x['across_file_excess'] for x in Dup)==len(O)-len(G))
test('duplicate_excess_equals_occurrences_minus_classes',len(O)-len(G)==M['duplicate_excess_occurrences'])
test('duplicate_metrics_same_as_confusion_run',all(DUP[k]==M[k] for k in ('TP','TN','FP','FN','duplicate_rate')))
test('stage_not_advanced',json.loads((D/'05_phase_status_final.json').read_text())['phase6_performed'] is False)
report={'status':'STRUCTURAL_PASS_SEMANTICS_NOT_CERTIFIED','phase':5,'checks':checks,'passed':sum(checks.values()),'failed':0,
'quote_and_original_document_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('0[1-8]*.md') if p.name[:2].isdigit()},
'disclaimer_en':'Only item-level arithmetic, provenance-location, and reference integrity are certified. True semantic entailment and absence remain best-effort.'}
(D/'05_structural_verification_final.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],'checks:',report['passed'],'phase5:',M['TP'],M['FN'],M['FP'],M['TN'])
