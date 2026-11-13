#!/usr/bin/env python3
"""Verify structural consistency of the Phase 2 best-effort ledgers.

A structural check is not a certification of semantic equivalence or of extracted atomicity.
"""
import json,hashlib,collections,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
INPUT=ROOT.parent
P1=INPUT/'oriondesk_v61_phase1_20261113'

def jl(name):return [json.loads(t) for t in (ROOT/name).read_text(encoding='utf-8').splitlines() if t.strip()]
A=jl('02_generated_atoms_final.jsonl')
C=jl('02_generated_classes_final.jsonl')
D=jl('04_duplicate_classes_final.jsonl')
E=jl('02_generated_exclusions_final.jsonl')
L=jl('02_generated_line_coverage_final.jsonl')
T=jl('02_generated_table_cell_coverage_final.jsonl')
X=jl('09_excluded_units.jsonl')
REV=jl('02_reverse_lookup_index_final.jsonl')
SUM=json.loads((ROOT/'02_phase_status_final.json').read_text())
FILES=[x['filename'] for x in SUM['per_file']]
assert len(FILES)==8==len(set(FILES))
assert len({x['generated_occurrence_id'] for x in A})==len(A)
assert len({x['generated_class_id'] for x in C})==len(C)
assert len({x['generated_class_id'] for x in D})==len(D)==len(C)
assert set(x['generated_class_id'] for x in C)==set(x['generated_class_id'] for x in D)
assert len(A)==SUM['generated_occurrences_GO_m']
assert len(C)==SUM['generated_classes_G_m']
assert len(E)==SUM['excluded_generated_segments']
assert len(L)==SUM['generated_physical_lines_inspected']
assert len(T)==SUM['generated_table_cells_inspected']
assert SUM['prefix']=='supplied_set_1'
assert SUM['status']=='PHASE_COMPLETED_BEST_EFFORT'
assert {a['file'] for a in A}<=set(FILES)
ids={a['generated_occurrence_id']:a for a in A}
class_members={}
for c in C:
 assert c['occurrence_count']==len(c['occurrence_ids'])==len(c['occurrences'])
 assert c['representative_occurrence_id']==c['occurrence_ids'][0]
 for o in c['occurrences']:
  i=o['generated_occurrence_id']
  assert i in ids and i not in class_members
  class_members[i]=c['generated_class_id']
  assert ids[i]['generated_class_id']==c['generated_class_id']
  assert o['file']==ids[i]['file'] and o['line_start']==ids[i]['line_start']
assert len(class_members)==len(A)
for a in A:
 src=(INPUT/a['file']).read_text(encoding='utf8').splitlines()[a['line_start']-1]
 assert a['line_start']==a['line_end'] and a['line_start']>0
 assert a['original_cell_en'] in src, (a['generated_occurrence_id'],a['file'],a['line_start'])
 if a['table_cell']:
  assert a['table_cell']['row_key_en'] and a['table_cell']['column_header_en']
  assert src.startswith('|') and src.rstrip().endswith('|')
 else: assert a['source_kind']!='table'

lookup={(x['file'],x['line']):x for x in L}
assert len(lookup)==len(L)
for file in FILES:
 lines=(INPUT/file).read_text(encoding='utf8').splitlines()
 assert len([x for x in L if x['file']==file])==len(lines)
 for i,line in enumerate(lines,1):
  rec=lookup[(file,i)]
  assert rec['raw_text_en']==line
  for oid in rec['generated_occurrence_ids']:
   assert oid in ids and ids[oid]['file']==file and ids[oid]['line_start']==i

table_ids={}
for x in T:
 key=(x['file'],x['line'],x['column_index'])
 assert key not in table_ids
 table_ids[key]=x
 for oid in x['occurrence_ids']:
  a=ids[oid]
  assert (a['file'],a['line_start'],a['table_cell']['column_index'])==key
for a in A:
 if a['table_cell']:
  assert a['generated_occurrence_id'] in table_ids[(a['file'],a['line_start'],a['table_cell']['column_index'])]['occurrence_ids']
assert set(x['origin'] for x in X)=={'PDF','GENERATED'}
assert sum(x['origin']=='GENERATED' for x in X)==len(E)
assert len({x['exclusion_id'] for x in X})==len(X)
assert len({x['lookup_key'] for x in REV})==len(REV)
assert all(set(x['generated_class_ids'])<=set(c['generated_class_id'] for c in C) for x in REV)
within=across=0
for c in C:
 seen=set()
 for o in c['occurrences']:
  if not seen:seen.add(o['file']);continue
  if o['file'] in seen:within+=1
  else:across+=1
  seen.add(o['file'])
assert within==SUM['within_file_excess'] and across==SUM['across_file_excess']
assert within+across==len(A)-len(C)==SUM['duplicate_excess_occurrences']
assert abs(SUM['duplicate_rate']-(len(A)-len(C))/len(A))<1e-12
for name in ['01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl']:
 assert hashlib.sha256((P1/name).read_bytes()).digest()==hashlib.sha256((ROOT/name).read_bytes()).digest()
assert sum(1 for _ in (ROOT/'01_source_atoms_final.jsonl').open())==SUM['source_positive_count_from_inherited_phase1']
assert sum(1 for _ in (ROOT/'01_source_negative_controls_final.jsonl').open())==SUM['source_negative_control_count_from_inherited_phase1']
result={'structural_verification':'PASS','semantic_equivalence_certification':'NOT_CLAIMED','phase_status':SUM['status'],'inputs':8,'lines':len(L),'cells':len(T),'eligible_occurrences':len(A),'raw_classes':len(C),'excess_duplicates':len(A)-len(C),'within_file_excess':within,'across_file_excess':across,'excluded_generated_fragments':len(E),'class_membership_checked':len(class_members),'original_cell_source_locations_checked':len(A),'table_cell_linkages_checked':sum(a['table_cell'] is not None for a in A),'phase1_ledger_bytes_identical':True,'phase3_performed':False}
(ROOT/'02_structural_validation_final.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,indent=2))
