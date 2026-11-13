#!/usr/bin/env python3
"""Read-only independent structural check for Phase-4 item ledgers."""
import json,collections,hashlib,sys
from pathlib import Path
p=Path('/mnt/data');d=p/'oriondesk_v6_1_phase4'
def l(a):return [json.loads(s) for s in (d/a).read_text().splitlines() if s.strip()]
def src(a):return [json.loads(s) for s in (p/a).read_text().splitlines() if s.strip()]
u=l('03_canonical_universe_final.jsonl');j=l('04_atomic_judgments_final.jsonl');v=l('04_generated_claim_validity_final.jsonl');f=l('04_unsupported_generated_propositions_final.jsonl');n=l('04_negative_control_assertion_audit_final.jsonl')
r=src('oriondesk_v6_1_phase1/01_source_atoms_final.jsonl');fixed=src('oriondesk_v6_1_phase1/01_source_negative_controls_final.jsonl');g=src('oriondesk_v6_1_phase3/02_generated_classes_corrected_phase3.jsonl');go=src('oriondesk_v6_1_phase3/02_generated_atoms_corrected_phase3.jsonl')
assert len(r)==1024 and len(fixed)==37 and len(g)==2624 and len(go)==2672
assert len({x['canonical_id'] for x in u})==len(u)==len(j)
assert len({x['generated_class_id'] for x in v})==len(g)
assert len({x['canonical_id'] for x in f})==len(f)
assert len({x['negative_control_id'] for x in n})==len(fixed)
assert set(x['canonical_id'] for x in u)==set(x['canonical_id'] for x in j)
C=collections.Counter(a['scoring_cell'] for a in j)
assert C['TP']+C['FN']==len(r)
assert C['TN']+sum(x['asserted_negative_counterfactual'] for x in n)==len(fixed)
assert C['FP']==len(f)+sum(x['asserted_negative_counterfactual'] for x in n)
assert len(u)==len(r)+len(fixed)+len(f)==sum(C.values())
assert set(x['canonical_id'] for x in u if x['unit_kind']=='PDF_POSITIVE')==set(x['source_id'] for x in r)
assert set(x['canonical_id'] for x in u if x['unit_kind']=='PREDECLARED_PDF_NEGATIVE_CONTROL')==set(x['negative_control_id'] for x in fixed)
assert set(x['canonical_id'] for x in u if x['unit_kind']=='GENERATED_ONLY_UNSUPPORTED')==set(x['canonical_id'] for x in f)
assert all(x['actual_label']==(1 if x['unit_kind']=='PDF_POSITIVE' else 0) for x in u)
assert all((x['actual_label'],x['predicted_label'])=={'TP':(1,1),'FN':(1,0),'TN':(0,0),'FP':(0,1)}[x['scoring_cell']] for x in u)
cm=json.loads((d/'04_confusion_matrix_final.json').read_text())
assert cm['confusion']=={x:C[x] for x in ['TP','TN','FP','FN']}
assert cm['universe']['canonical_decision_units']==len(u)
byclass=collections.Counter()
for q in go:byclass[q['class_id']]+=1
assert set(byclass)==set(x['class_id'] for x in g)
assert all(q['occurrence_count']==byclass[q['class_id']] for q in g)
bylabel=collections.Counter(x['validity_label'] for x in v)
assert bylabel['PDF_UNSUPPORTED']==len(f)
assert bylabel==cm['generated_class_validity']
# PDF and original generated evidence locator valid as recorded (string match to physical line).
files={x['file'] for x in (a['representative_generated_evidence'] for a in v)}
for filename in files:
 assert (p/filename).is_file()
 filelines=(p/filename).read_text().splitlines()
 for q in v:
  ev=q['representative_generated_evidence']
  if ev['file']!=filename:continue
  assert ev['quote_en'] in filelines[ev['line_start']-1]
for q in u:
 assert q['pdf_evidence']
 if q['scoring_cell']=='TP':assert q['generated_evidence']
 if q['scoring_cell']=='FN':assert q['origin_source_ids']
 if q['scoring_cell']=='FP':assert q['origin_generated_class_ids']
 if q['scoring_cell']=='TN':assert q['origin_negative_control_ids'] and not q['generated_evidence']
assert all(gd['validity_label'] in {'PDF_ENTAILED','PDF_UNSUPPORTED','SUPPORTED_NONCOVERING'} for gd in v)
assert cm['equations'] and all(cm['equations'].values())
print(json.dumps({'status':'PASSED_STRUCTURAL_ONLY','counts':dict(C),'universe':len(u),'generated_classes':len(v),'negative_controls':len(n),'semantic_certification':'NOT_CERTIFIED'},indent=2))
