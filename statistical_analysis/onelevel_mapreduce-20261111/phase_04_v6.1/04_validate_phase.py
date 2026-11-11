#!/usr/bin/env python3
"""Phase 4 canonical and evidence-structure validation; no semantic certification."""
import json,collections,os
from pathlib import Path
BASE=Path('/mnt/data/oriondesk_phase4_v61');ROOT=Path('/mnt/data')
load=lambda p:[json.loads(x) for x in open(p) if x.strip()]
J=load(BASE/'04_atomic_judgments_final.jsonl');U=load(BASE/'03_canonical_universe_final.jsonl');V=load(BASE/'04_generated_claim_validity_final.jsonl');NA=load(BASE/'04_negative_control_assertion_audit_final.jsonl')
S=load(ROOT/'oriondesk_phase3_v61_redo/01_source_atoms_final.jsonl');N=load(ROOT/'oriondesk_phase3_v61_redo/01_source_negative_controls_final.jsonl');G=load(ROOT/'oriondesk_phase2_current_scored_8/02_generated_classes_final.jsonl');GO=load(ROOT/'oriondesk_phase2_current_scored_8/02_generated_atoms_final.jsonl');summ=json.load(open(BASE/'04_confusion_matrix_final.json'))
assert len(J)==len(U)==len(set(x['canonical_id'] for x in J))
assert set(x['canonical_id'] for x in J)==set(x['canonical_id'] for x in U)
assert len(G)==len(V)==len(set(x['generated_class_id'] for x in V))
assert len(N)==len(NA)
assert all(x['classification'] in ('PDF_ENTAILED','SUPPORTED_NONCOVERING','PDF_UNSUPPORTED','OUT_OF_SCOPE_NONDEFINITIVE') for x in V)
assert all(x['prediction_eligible']==(x['classification']!='OUT_OF_SCOPE_NONDEFINITIVE') for x in V)
assert all(x['generated_evidence'] for x in V)
assert all(x.get('pdf_evidence') for x in V if x['classification'] in ('PDF_ENTAILED','SUPPORTED_NONCOVERING'))
assert all(x['actual_label']==int(x['scoring_cell'] in ('TP','FN')) for x in J)
assert all(x['predicted_label']==int(x['scoring_cell'] in ('TP','FP')) for x in J)
assert len([x for x in J if x['actual_label']==1])==len(S)
assert len([x for x in J if x['origin_negative_control_ids']])==len(N)
assert all(x['pdf_evidence'] and x['generated_evidence'] for x in J if x['scoring_cell']=='TP')
assert all(x['pdf_evidence'] for x in J if x['scoring_cell']=='FN')
C=collections.Counter(x['scoring_cell'] for x in J)
assert C==collections.Counter(summ['confusion'])
assert C['TP']+C['FN']==len(S)
assert C['TN']+summ['universe']['asserted_negative_controls']==len(N)
assert C['FP']==summ['universe']['unsupported_generated_only_propositions']+summ['universe']['asserted_negative_controls']
assert len(J)==len(S)+len(N)+summ['universe']['unsupported_generated_only_propositions']
assert summ['universe']['canonical_predicted_positive_units']==C['TP']+C['FP']
assert len(GO)>=len(G)
assert all(os.path.exists(ROOT/x['generated_evidence'][0]['file']) for x in V)
assert all(x['protocol_version']=='6.1' for x in V+J)
assert all(x['method']=='current_scored_8' for x in V+J)
assert set(x['source_id'] for x in S)==set(x['canonical_id'] for x in J if x['actual_label']==1)
assert set(x['negative_control_id'] for x in N)==set(x['canonical_id'] for x in J if x['origin_negative_control_ids'])
print('PHASE4 STRUCTURAL PASS')
print('classes',len(V),'atoms',len(J),'source',len(S),'negative',len(N))
print('counts',dict(C))
print('possible_ineligible_class_extractions',sum(x['classification']=='OUT_OF_SCOPE_NONDEFINITIVE' for x in V))
print('semantic evidence certification: NOT CERTIFIED')
