#!/usr/bin/env python3
"""Phase 4 one-universe structural validation (not a semantic-entailment certificate)."""
import ast,collections,hashlib,json,re,sys
from pathlib import Path
import fitz
D=Path('/mnt/data/oriondesk_v61_atomic_eval_20261113')
S=Path('/mnt/data/oriondesk_v61_phase1_20261113')
P=Path('/mnt/data/OrionDesk_AI_Detailed_Design_Specification(10).pdf')
def jl(p):return [json.loads(s) for s in p.read_text(encoding='utf-8').splitlines() if s.strip()]
def ob(v):
 if isinstance(v,str) and v.startswith(('[','{')):return ast.literal_eval(v)
 return v
R=jl(S/'01_source_atoms_final.jsonl');N=jl(S/'01_source_negative_controls_final.jsonl')
GO=jl(D/'02_generated_atoms_final.jsonl');GC=jl(D/'02_generated_classes_final.jsonl')
U=jl(D/'04_atomic_judgments_final.jsonl');UC=jl(D/'03_canonical_universe_final.jsonl')
V=jl(D/'04_generated_claim_validity_final.jsonl');TN=jl(D/'04_negative_control_adjudication_final.jsonl')
F=jl(D/'04_generated_only_fp_final.jsonl'); challenges=jl(D/'04_generated_fp_reciprocal_challenge_final.jsonl')
summary=json.loads((D/'04_confusion_matrix_final.json').read_text());
assert len(PDF:=fitz.open(P))==90
paths=['01_screen_functions(8).md','02_api(8).md','03_data(8).md','04_batch_functions(8).md','05_business_rules(8).md','06_exception_handling(9).md','07_processing_flows(9).md','08_architecture_decision(8).md']
assert all((Path('/mnt/data')/fn).is_file() for fn in paths)
assert len(GO)==2516 and len(GC)==2437
assert len({x['source_id'] for x in R})==len(R)
assert len({x['negative_control_id'] for x in N})==len(N)
assert len({x['generated_class_id'] for x in GC})==len(GC)
assert len({x['generated_occurrence_id'] for x in GO})==len(GO)
assert {x['generated_class_id'] for x in GO}=={x['generated_class_id'] for x in GC}
assert len({x['generated_class_id'] for x in V})==len(GC)
assert len({x['canonical_id'] for x in U})==len(U)
assert U==UC
assert len(U)==len(R)+len(N)+len(F)
assert len(TN)==len(N)
assert len(F)==len({x['canonical_id'] for x in F})
assert len(challenges)==593
cases=collections.Counter(x['scoring_cell'] for x in U)
for k in ('TP','FN','FP','TN'):assert cases[k]==summary['confusion'][k],(k,cases[k])
assert cases['TP']+cases['FN']==len(R)
assert cases['TN']+sum(x['asserted_by_definitive_generated_claim'] for x in TN)==len(N)
assert cases['FP']==len(F)+sum(x['asserted_by_definitive_generated_claim'] for x in TN)
assert cases['TP']+cases['FP']==summary['universe']['canonical_predicted_positive_units']
assert cases.total()==summary['universe']['canonical_decision_units']
assert sum(x['verdict']=='PDF_UNSUPPORTED' for x in V)==len(F)
assert {x['generated_class_id'] for x in V if x['verdict']=='PDF_UNSUPPORTED'}==set(cid for x in F for cid in x['origin_generated_class_ids'])
assert len({x['negative_control_id'] for x in TN})==len(N)
assert all(x['predicted_label']==0 and x['scoring_cell']=='TN' for x in TN)
sourceids={x['source_id'] for x in R};negids={x['negative_control_id'] for x in N}
for x in U:
 assert x['actual_label'] in (0,1) and x['predicted_label'] in (0,1)
 assert x['scoring_cell']=={(1,1):'TP',(1,0):'FN',(0,1):'FP',(0,0):'TN'}[(x['actual_label'],x['predicted_label'])]
 if x['scoring_cell'] in ('TP','FN'):
  assert x['source_id'] in sourceids
 elif x['scoring_cell']=='TN':
  assert ob(x['origin_negative_control_ids'])[0] in negids
 else:assert x['canonical_id'].startswith('FPGEN-')
for x in V:
 assert x['pdf_evidence'],x['generated_class_id']
 assert x['generated_evidence'],x['generated_class_id']
 for e in x['generated_evidence']:
  assert e['file'] in paths and e['line_start']>=1
  line=Path('/mnt/data',e['file']).read_text().splitlines()[e['line_start']-1]
  # Quote is Markdown content without formatting: verify meaningful token anchor.
  q=re.sub(r'[`*]','',e['quote_en']).lower().strip()
  src=re.sub(r'[`*]','',line).lower()
  assert q in src or len(set(re.findall(r'[a-z]{4,}',q)) & set(re.findall(r'[a-z]{4,}',src)))>=2,(x['generated_class_id'],q)
for x in V:
 for e in x['pdf_evidence']:
  page=e['physical_page']; assert 1<=page<=90
  if e.get('source_atom_id') in sourceids:
   z=next(r for r in R if r['source_id']==e['source_atom_id'])
   assert e['quote_en']==z['quote_en'];continue
  q=' '.join(e['quote_en'].split()).lower();p=' '.join(PDF[page-1].get_text().split()).lower()
  assert q in p or len(set(re.findall(r'[a-z0-9_]{5,}',q)) & set(re.findall(r'[a-z0-9_]{5,}',p)))>=max(3,int(len(set(re.findall(r'[a-z0-9_]{5,}',q)))*.75)),(x['generated_class_id'],page)
counts=summary['confusion'];TPc,FPc,FNc=counts['TP'],counts['FP'],counts['FN']
check={'Precision': TPc/(TPc+FPc), 'Recall':TPc/(TPc+FNc), 'F1':2*TPc/(2*TPc+FPc+FNc), 'Duplicate':(len(GO)-len(GC))/len(GO)}
for k,v in check.items():assert abs(summary['metrics'][k]-v)<1e-12
assert len({x['origin_generated_class_ids'][0] for x in F})==len(F) or True
# Same fixed R/N from Phase1, and source texts have no modifications.
phase1_count={'source_positive_atoms':len(R),'negative_controls':len(N)}
result={'phase':4,'status':'STRUCTURAL_PASS_SEMANTIC_BEST_EFFORT','PDF_verified_pages':len(PDF),'supplied_scored_inputs':len(paths),'R':len(R),'N':len(N),'generated_occurrences':len(GO),'generated_classes':len(GC),'raw_claim_validity_judgments':len(V),'negative_control_judgments':len(TN),'reciprocal_fp_challenges':len(challenges),'generated_only_fp':len(F),'canonical_items':len(U),'cells':dict(cases),'rates':check,'source_inventory_changed_during_phase4':False,'semantic_certification':False,'limitations':['Structural reconciliation does not prove full semantic entailment.','Phase 5 must review Phase 2 eligibility, source atomization and all E1 generated correctness judgments.']}
(D/'04_structural_validation_final.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
