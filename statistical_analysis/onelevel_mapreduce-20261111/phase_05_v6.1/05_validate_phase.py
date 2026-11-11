#!/usr/bin/env python3
"""Phase-5 structural consistency and evidence-locator audit (not semantic certification)."""
from pathlib import Path
import json,collections,sys
P=Path(__file__).resolve().parent;ROOT=P.parent

def read(name):
 with (P/name).open(encoding='utf-8') as f:return [json.loads(z) for z in f if z.strip()]
S=read('01_source_atoms_final.jsonl');N=read('01_source_negative_controls_final.jsonl');
GO=read('02_generated_atoms_final.jsonl');G=read('02_generated_classes_final.jsonl')
E=read('03_evidence_matches_final.jsonl');B=read('03_semantic_coverage_bridges_final.jsonl')
J=read('04_atomic_judgments_final.jsonl');T=read('05_tp_evidence_audit_final.jsonl')
FNA=read('03_fn_root_cause_audit_final.jsonl');SA=read('05_source_atomization_audit_final.jsonl')
D=read('04_duplicate_classes_final.jsonl');C=json.loads((P/'04_confusion_matrix_final.json').read_text())
M=json.loads((P/'05_duplicate_metrics_final.json').read_text())
assert len(S)==len(set(x['source_id'] for x in S))
assert len(N)==len(set(x['negative_control_id'] if 'negative_control_id' in x else x.get('source_negative_id',x.get('control_id')) for x in N))
assert len(G)==len(set(x['generated_class_id'] for x in G))
assert len(GO)==len(set(x['generated_id'] for x in GO))
assert len(J)==len(set(x['canonical_id'] for x in J))
assert len(E)==len(S) and {x['origin_source_id'] for x in E}=={x['source_id'] for x in S}
assert len(J)==len(S)+len(N)
valid_classes={x['generated_class_id'] for x in G}
occ_by_class=collections.defaultdict(set)
for r in GO:
 assert r['generated_class_id'] in valid_classes
 occ_by_class[r['generated_class_id']].add(r['generated_id'])
for g in G:
 assert occ_by_class[g['generated_class_id']]==set(g['occurrence_ids'])
 assert g['occurrence_count']==len(g['occurrence_ids'])
assert all(len(x['origin_generated_class_ids']) and set(x['origin_generated_class_ids'])<=valid_classes for x in J if x['scoring_cell']=='TP')
ct=collections.Counter(x['scoring_cell'] for x in J)
assert all(ct[c]==C['confusion'][c] for c in ('TP','TN','FP','FN'))
assert ct['TP']+ct['FN']==len(S) and ct['TN']==len(N)
assert len([t for t in T if t['audit_outcome']=='CONFIRMED_TP'])==ct['TP']
assert {t['source_id'] for t in T if t['audit_outcome']=='CONFIRMED_TP'}=={x['canonical_id'] for x in J if x['scoring_cell']=='TP'}
assert set(x['source_id'] for x in B)=={x['origin_source_id'] for x in E if x['scoring_cell']=='TP' and x['entailment_grade']=='E2'}
assert len([z for z in FNA if z.get('final_scoring_cell')=='FN'])==ct['FN']
assert {z['source_id'] for z in FNA if z.get('final_scoring_cell')=='FN'}=={x['canonical_id'] for x in J if x['scoring_cell']=='FN'}
assert sum(x['duplicate_excess_count'] for x in G)==len(GO)-len(G)
assert M['duplicate_excess_occurrences']==len(GO)-len(G)
assert M['within_file_excess']+M['across_file_excess']==len(GO)-len(G)
assert sum(x['excess_occurrences'] for x in D)==len(GO)-len(G)
assert abs(M['duplicate_rate']-(len(GO)-len(G))/len(GO))<1e-12
assert abs(C['metrics']['Recall']-ct['TP']/(ct['TP']+ct['FN']))<1e-12
assert abs(C['metrics']['F1']-2*ct['TP']/(2*ct['TP']+ct['FP']+ct['FN']))<1e-12
assert C['metrics']['Precision'] == ct['TP']/(ct['TP']+ct['FP'])
assert len(SA)>=len(S)
mdfiles={p.name:p.read_text(encoding='utf-8').splitlines() for p in ROOT.glob('*.md')}
assert len(mdfiles)>=8
for r in GO:
 assert r['file'] in mdfiles and 0<r['line_start']<=len(mdfiles[r['file']])
 line=mdfiles[r['file']][r['line_start']-1]
 assert r['source_quote_en'] in line or line in r['source_quote_en'], (r['generated_id'],r['file'],r['line_start'])
for r in T:
 if r['audit_outcome']=='CONFIRMED_TP':
  assert r['pdf_evidence'] and r['generated_evidence']
  for e in r['generated_evidence']:
   assert e['file'] in mdfiles and 0<e['line_start']<=len(mdfiles[e['file']])
for r in S:
 assert r['pdf_evidence'] and all(1<=p['physical_page']<=90 for p in r['pdf_evidence'])
print(json.dumps({'structural_validation':'PASS','semantic_certification':False,'source_positive':len(S),'source_negative':len(N),'generated_occurrences':len(GO),'generated_classes':len(G),'TP':ct['TP'],'TN':ct['TN'],'FP':ct['FP'],'FN':ct['FN'],'duplicate_rate':M['duplicate_rate'],'TP_audit_records':len(T),'FN_audit_records':len(FNA)},indent=2))
