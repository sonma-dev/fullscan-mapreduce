#!/usr/bin/env python3
"""Independent structural validation for Phase 2 ledgers (not semantic certification)."""
import json,hashlib,re,collections
from pathlib import Path
ROOT=Path('/mnt/data'); OUT=ROOT/'oriondesk_phase2'; PH1=ROOT/'oriondesk_phase1'

def jl(p):
 with (OUT/p).open(encoding='utf8') as f:
  for i,s in enumerate(f,1):
   if s.strip():yield json.loads(s)

status=json.loads((OUT/'02_phase_status_final.json').read_text())
occ=list(jl('02_generated_atoms_final.jsonl'))
classes=list(jl('02_generated_classes_final.jsonl'))
dup=list(jl('04_duplicate_classes_final.jsonl'))
cov=list(jl('02_generated_line_coverage_final.jsonl'))
cells=list(jl('02_generated_table_cell_coverage_final.jsonl'))
ex=list(jl('02_generated_exclusions_final.jsonl'))
idx={a['occurrence_id']:a for a in occ};cls={a['class_id']:a for a in classes}
assert len(idx)==len(occ) and len(cls)==len(classes)
assert status['eligible_generated_occurrences']==len(occ)
assert status['raw_generated_semantic_classes']==len(classes)
assert len(dup)==len(classes)
assert sum(x['occurrence_count'] for x in classes)==len(occ)
assert all(x['class_id'] in cls for x in occ)
assert all(x['occurrence_id'] in cls[x['class_id']]['occurrence_ids'] for x in occ)
assert all(len(set(c['occurrence_ids']))==len(c['occurrence_ids']) for c in classes)
assert all(len(c['occurrence_ids'])==c['occurrence_count'] for c in classes)
assert all(d['representative_occurrence_id'] in d['occurrence_ids'] for d in dup)
assert len(cov)==sum(x['lines'] for x in status['input_files'])
assert len(cells)==status['table_cell_coverage_records']
assert len({(x['file'],x['line']) for x in cov})==len(cov)
assert len({(x['file'],x['line'],x['cell']) for x in cells})==len(cells)
assert sum(1 for x in cells if x['status']=='ELIGIBLE')==status['table_cells_with_eligible_assertions']
assert status['within_file_excess']+status['across_file_excess']==len(occ)-len(classes)
assert sum(x['within_file_excess'] for x in dup)==status['within_file_excess']
assert sum(x['across_file_excess'] for x in dup)==status['across_file_excess']
assert all(sum(r['duplicate_role']!='representative' for r in x['occurrence_roles'])==x['occurrence_count']-1 for x in dup)
files={}; all_actual=[];errs=[]
for f in status['input_files']:
 p=ROOT/f['file'];data=p.read_bytes();assert hashlib.sha256(data).hexdigest()==f['sha256']
 lines=data.decode('utf-8-sig').splitlines();files[f['file']]=lines
 assert len(lines)==f['lines'];all_actual.extend((f['file'],i) for i in range(1,len(lines)+1))
assert {(x['file'],x['line']) for x in cov}==set(all_actual)
for x in occ:
 ev=x['evidence'];f=ev['file'];line=ev['line_start'];assert f in files and 1<=line<=len(files[f]); assert ev['line_end']>=line
 q=ev['quote_en'].strip();source=files[f][line-1].strip()
 if q not in source:
  # In Markdown cell parsing, escaped pipes can be represented unchanged in the quote.
  if q.replace('\\|','|') not in source.replace('\\|','|'):
   errs.append({'id':x['occurrence_id'],'file':f,'line':line,'quote':q[:150], 'source':source[:180]})
for x in cells:
 if x['status']=='ELIGIBLE':
  assert x.get('claim_ids') and all(y in idx for y in x['claim_ids'])
 else: assert not x.get('claim_ids')
assert not errs,errs[:5]
for k in ['01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl']:
 p=PH1/k;assert p.exists() and p.stat().st_size>1000
assert status['status']=='PHASE_COMPLETED_BEST_EFFORT' and status['next_phase_executed'] is False
# A mechanical exact check does not claim full meaning or faithful atomization.
res={'phase':2,'structural_check':'PASSED','semantic_certification':'NOT_CLAIMED',
 'physical_lines_checked':len(cov),'table_cells_checked':len(cells),
 'eligible_occurrences_with_verifiable_evidence':len(occ),
 'raw_classes_checked':len(classes),'source_files_checked':len(files),
 'quote_mismatch_count':len(errs), 'within_file_excess':status['within_file_excess'],
 'across_file_excess':status['across_file_excess'],
 'source_ledger_reuse_verified':True,
 'limits':'Verifies structure and source-quote existence, not completeness of semantic atomization or meaning-preserving class merges.'}
(OUT/'02_phase2_validation_final.json').write_text(json.dumps(res,indent=2)+'\n',encoding='utf8')
print(json.dumps(res,indent=2))
