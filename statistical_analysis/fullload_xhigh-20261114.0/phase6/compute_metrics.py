#!/usr/bin/env python3
"""Independent Phase-6 ledger recomputation for OrionDesk R1.0 (protocol v6.1).

Reads finalized item-level evidence; does not trust previous summary counts.
The results validate structural/evidence-locator integrity, NOT logical entailment.
No expected totals or historic scores are hardcoded.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib, re, math

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent
FNS={
 'R':'01_source_atoms_final.jsonl','N':'01_source_negative_controls_final.jsonl',
 'GO':'02_generated_atoms_final.jsonl','GC':'02_generated_classes_final.jsonl',
 'U':'03_canonical_universe_final.jsonl','M':'03_evidence_matches_final.jsonl',
 'FN':'03_fn_root_cause_audit_final.jsonl','B':'03_semantic_coverage_bridges_final.jsonl',
 'V':'04_generated_claim_validity_final.jsonl','J':'04_atomic_judgments_final.jsonl',
 'D':'04_duplicate_classes_final.jsonl','TP':'05_tp_evidence_audit_final.jsonl',
 'SA':'05_source_atomization_audit_final.jsonl','CH':'07_change_delta.jsonl',
}

def read_lines(fname):
 with (HERE/fname).open(encoding='utf-8') as f:return [json.loads(line) for line in f if line.strip()]

def unique(items,name):
 assert len(items)==len(set(items)), f'Duplicate {name} identifiers'

def path_md(file):
 assert pathlib.Path(file).name==file and file in SOURCE_NAMES, f'Non-input source pathname {file}'
 return ROOT/file

def eqnum(x,y): return x==y if isinstance(x,int) and isinstance(y,int) else math.isclose(x,y,rel_tol=1e-10,abs_tol=1e-12)

def norm(s): return re.sub(r'\s+',' ',str(s)).strip()

def pct(a,b):return (a/b) if b else None

SOURCE_NAMES={p.name for p in ROOT.glob('0[1-8]_*.md')}

def main():
 rec={k:read_lines(n) for k,n in FNS.items()}
 for k,v in rec.items():assert v,f'Empty mandatory ledger: {k}'
 R={x['source_id']:x for x in rec['R']};N={x['negative_control_id']:x for x in rec['N']}
 GO={x['occurrence_id']:x for x in rec['GO']};GC={x['class_id']:x for x in rec['GC']}
 U={x['canonical_id']:x for x in rec['U']};J={x['canonical_id']:x for x in rec['J']}
 FN=rec['FN'];TP={x['source_id']:x for x in rec['TP']};B={x['source_id']:x for x in rec['B']}
 VAL={x['generated_class_id']:x for x in rec['V']}; D={x['class_id']:x for x in rec['D']}
 M=rec['M'];Mids=[x.get('origin_source_ids',[None])[0] for x in M]
 for k,src,ids in [('R',rec['R'],R),('N',rec['N'],N),('GO',rec['GO'],GO),('GC',rec['GC'],GC),('U',rec['U'],U),('J',rec['J'],J),('TP',rec['TP'],TP),('B',rec['B'],B),('V',rec['V'],VAL),('D',rec['D'],D)]:
  assert len(src)==len(ids), f'Nonunique {k}'
 assert set(R).isdisjoint(set(N)), 'Positive and negative IDs overlap'
 assert set(GC)==set(VAL)==set(D), 'Generated claim/class validity/duplicate ledgers disagree'
 assert set(U)==set(J), 'Canonical universe != judgment ledger'
 assert set(Mids)==set(R) and len(Mids)==len(R), 'Source matches not one-to-one with R'
 assert len(SOURCE_NAMES)==8 and len({f.split('_',1)[0] for f in SOURCE_NAMES})==8, 'Missing scored Markdown role'
 manifest=json.loads((HERE/'01_input_manifest_final.json').read_text(encoding='utf-8'))
 for entry in manifest['scored_markdown_inputs']:
  assert entry['actual_uploaded_filename'] in SOURCE_NAMES
  actual=hashlib.sha256((ROOT/entry['actual_uploaded_filename']).read_bytes()).hexdigest()
  assert actual==entry['sha256'], f'Input content changed: {entry["actual_uploaded_filename"]}'
 assert hashlib.sha256(next(ROOT.glob('OrionDesk_AI_Detailed_Design_Specification*.pdf')).read_bytes()).hexdigest()==manifest['pdf']['sha256'], 'PDF source changed'
 assert all(x.get('method','fullload')=='fullload' for x in rec['GO']+rec['GC']+rec['V']+rec['U']+rec['J']), 'Method leakage'
 # Raw occurrence/class relationships and independently computed repetition partition.
 seen=[]; dup_inside=dup_cross=repeat=multi=0
 source_file_lines={name:path_md(name).read_text(encoding='utf-8').splitlines() for name in SOURCE_NAMES}
 source_line_count=sum(len(lines) for lines in source_file_lines.values())
 for g in GC.values():
  ids=g['occurrence_ids']; seen.extend(ids)
  assert len(ids)==len(set(ids)) and len(ids)==g['occurrence_count']
  assert all(z in GO and GO[z]['class_id']==g['class_id'] for z in ids),g['class_id']
  files=[GO[z]['source_file'] for z in ids]
  if len(ids)>1:repeat+=1
  if len(set(files))>1:multi+=1
  order=sorted(ids,key=lambda z:(sorted(SOURCE_NAMES).index(GO[z]['source_file']),GO[z]['line_start'],str(GO[z].get('table_cell') or ''),z))
  observed=set()
  for i,z in enumerate(order):
   f=GO[z]['source_file']
   if i>0:
    if f in observed:dup_inside+=1
    else:dup_cross+=1
   observed.add(f)
  assert g['occurrence_count']==D[g['class_id']]['occurrence_count'],'Duplicate class size mismatch'
  assert D[g['class_id']]['within_file_excess']==sum(1 for i,z in enumerate(order) if i>0 and GO[z]['source_file'] in {GO[v]['source_file'] for v in order[:i]}), 'Within-file duplicate partition mismatch'
  assert D[g['class_id']]['across_file_excess']==sum(1 for i,z in enumerate(order) if i>0 and GO[z]['source_file'] not in {GO[v]['source_file'] for v in order[:i]}), 'Across-file duplicate partition mismatch'
 assert set(seen)==set(GO) and len(seen)==len(GO), 'Occurrence not partitioned exactly once'
 for z in GO.values():
  f=z['source_file'];assert f in source_file_lines
  n=z['line_start']; assert 1<=n<=z['line_end']<=len(source_file_lines[f]);assert z['quote_en']
 # Source universe and per-row truth labels.
 source_to_cell={};nc_to_cell={};FP_only=[];B_asserted=[]; counter=collections.Counter()
 for id,x in J.items():
  assert x==U[id], f'Judgment/universe content divergence: {id}'
  a,b,cell=x['actual_label'],x['predicted_label'],x['scoring_cell']
  assert (a,b,cell) in [(1,1,'TP'),(1,0,'FN'),(0,1,'FP'),(0,0,'TN')]
  counter[cell]+=1
  src=x.get('origin_source_ids') or []; neg=x.get('origin_negative_control_ids') or []
  if a==1:
   assert len(src)==1 and not neg and src[0] in R
   assert src[0] not in source_to_cell
   source_to_cell[src[0]]=cell
  elif neg:
   assert len(neg)==1 and not src and neg[0] in N and neg[0] not in nc_to_cell
   nc_to_cell[neg[0]]=cell
   if cell=='FP':B_asserted.append(neg[0])
  else:
   assert cell=='FP' and not src and x.get('origin_generated_class_ids')
   assert all(g in GC for g in x['origin_generated_class_ids']);FP_only.append(id)
 assert set(source_to_cell)==set(R), 'Not one judgment per source-positive atom'
 assert set(nc_to_cell)==set(N), 'Not one judgment per negative control'
 assert counter['TP']==len(TP)==len(B)
 assert set(TP)==set(B)=={sid for sid,c in source_to_cell.items() if c=='TP'}
 assert counter['FN']==len(R)-len(TP)
 assert counter['TN']==len(N)-len(B_asserted)
 assert counter['FP']==len(FP_only)+len(B_asserted)
 assert len(J)==len(R)+len(N)+len(FP_only)
 assert len(GO)>=len(GC)
 assert len(GO)-len(GC)==dup_inside+dup_cross
 # Per-claim validity / FP nonoverlap.
 label_counter=collections.Counter(x.get('validity_label') for x in rec['V'])
 for v in rec['V']:
  assert v['occurrence_count']==len(v['occurrence_ids'])==GC[v['generated_class_id']]['occurrence_count']
  assert v.get('method')=='fullload'
 for row in J.values():
  for cid in row.get('origin_generated_class_ids',[]):assert cid in GC
  if row['scoring_cell']=='FP' and row.get('origin_negative_control_ids'):
   assert row['canonical_id'] not in FP_only
 # Exact source/line evidence and independent PDF text presence.
 import fitz
 pdf_files=list(ROOT.glob('OrionDesk_AI_Detailed_Design_Specification*.pdf'))
 assert len(pdf_files)==1,'Wrong/missing PDF'
 doc=fitz.open(str(pdf_files[0]));pages=len(doc)
 assert pages==90,'PDF physical-page extent differs from the controlled baseline'
 page_text=[norm(x.get_text()) for x in doc]
 page_nonempty=sum(bool(t) for t in page_text)
 assert page_nonempty==pages
 def checkpdf(e):
  p=e.get('physical_page');q=e.get('quote_en');assert isinstance(p,int) and 1<=p<=pages and q
  return bool(norm(q).lower() in page_text[p-1].lower())
 pdf_quote_exact=sum(checkpdf(x['pdf_evidence'][0]) for x in rec['R'])
 for x in rec['N']: checkpdf(x['pdf_evidence'][0]) # validates actual page and non-empty quotation
 for s in R.values(): assert s.get('pdf_evidence') and 1<=s['physical_page']<=pages
 for n in N.values():assert n.get('pdf_evidence') and 1<=n['pdf_page']<=pages
 tp_source_exact=0; tp_generated_exact=0
 for sid,t in TP.items():
  assert t['final_cell']=='TP' and t['pdf_evidence'] and t['generated_evidence']
  assert t['entailment_grade'] in ('E2','E3')
  assert t.get('predicate_checks') and all('status' in d and d['status'] in ('met','not_applicable') for d in t['predicate_checks'].values())
  for e in t['pdf_evidence']:
   assert 1<=e['physical_page']<=pages and e['quote_en']
   if norm(e['quote_en']).lower() in page_text[e['physical_page']-1].lower():tp_source_exact+=1
  for e in t['generated_evidence']:
   f=e['file'];ln=e['line_start']; assert f in source_file_lines and 1<=ln<=len(source_file_lines[f])
   assert e.get('class_id') in GC
   actual=source_file_lines[f][ln-1]
   assert norm(e['quote_en']) in norm(actual),f'Invented/incorrect TP quote at {sid} / {f}:{ln}'
   tp_generated_exact+=1
  assert source_to_cell[sid]=='TP'
 fn_final={x['source_id']:x for x in FN if x['final_scoring_cell']=='FN'}
 initial_root_counts=collections.Counter(x['fn_review_disposition'] for x in FN)
 assert len(fn_final)==counter['FN']
 assert set(fn_final)=={sid for sid,c in source_to_cell.items() if c=='FN'}
 assert all(x['fn_review_disposition'] in ('PARTIAL_ENTAILMENT','TRUE_MISSING','CONSERVATIVE_UNRESOLVED') for x in fn_final.values())
 assert all(x.get('best_generated_candidates') and x.get('exact_and_alias_keys_checked') and x.get('specific_reason_en') for x in fn_final.values())
 root_resolution=collections.Counter(x['final_scoring_cell'] for x in FN)
 assert root_resolution['FN']==counter['FN']
 assert all(x['fn_review_disposition']=='MATCHER_FALSE_NEGATIVE_CORRECTED' for x in FN if x['final_scoring_cell']=='TP')
 retired={z for x in rec['SA'] if x.get('result')=='CORRECTED_PARENT_OR_COMPOUND' for z in x['old_source_ids']}
 assert not retired.intersection(R)
 # Raw source-file coverage records are independently reconciled to original inputs.
 covers=read_lines('02_generated_line_coverage_final.jsonl'); line_cov=collections.Counter(x['file'] for x in covers)
 assert sum(line_cov.values())==source_line_count
 assert all(line_cov[f]==len(lines) for f,lines in source_file_lines.items())
 page_cov=read_lines('01_pdf_page_coverage_final.jsonl')
 assert len(page_cov)==pages and sorted(x['pdf_physical_page'] for x in page_cov)==list(range(1,pages+1))
 table_cov=read_lines('02_generated_table_cell_coverage_final.jsonl')
 assert table_cov and all(r['file'] in source_file_lines for r in table_cov)
 # Required regression probes, not pre-approved truth labels.
 probes={
 'case_title':['title'], 'workspace_retention_class':['retention class'],
 'replay_identical_case_creation':['same key','same key and identical response','same key'],
 'foreign_tenant_denial':['foreign-tenant','cross-tenant'],
 'source_acl_restrictions':['acl'], 'citation_exact_version':['immutable source versions'],
 'event_payload_and_consumer':['CaseCreated','ApprovalDecisionRecorded','AccessDenied'],
 }
 probe_rows=[]
 for test,words in probes.items():
  matches=[x for x in J.values() if x['actual_label']==1 and any(w.lower() in x['atomic_statement_en'].lower() for w in words)]
  probe_rows.append({'probe_id':test,'source_matches':len(matches),'tp':sum(x['scoring_cell']=='TP' for x in matches),'fn':sum(x['scoring_cell']=='FN' for x in matches),'source_id_samples':[x['origin_source_ids'][0] for x in matches[:15]],'interpretation_en':'Diagnostic retrieval evidence only, not a preapproved source or semantic label.'})
 # Find *potentially* missed exact source quotes, but do not silently change semantics.
 def n(s):return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
 all_lines=[(f,k+1,n(q)) for f,lines in source_file_lines.items() for k,q in enumerate(lines) if q.strip()]
 exact_exceptions=[]
 for sid,c in source_to_cell.items():
  if c!='FN':continue
  q=n(R[sid]['pdf_evidence'][0].get('quote_en',''))
  if len(q)<24:continue
  found=[(f,k) for f,k,z in all_lines if q in z]
  if found:exact_exceptions.append({'source_id':sid,'source_quote_en':R[sid]['pdf_evidence'][0]['quote_en'],'generated_exact_line_hits':[{'file':f,'line':k} for f,k in found[:3]],'review_status':'MANDATORY_SEMANTIC_REVIEW_EXCEPTION_NOT_AUTOMATIC_TP'})
 go_n=len(GO);gc_n=len(GC);TPn=counter['TP'];TNn=counter['TN'];FPn=counter['FP'];FNn=counter['FN']
 den1=TPn+FPn;den2=TPn+FNn;den3=2*TPn+FPn+FNn
 metrics={'Precision':pct(TPn,den1),'Recall':pct(TPn,den2),'F1':pct(2*TPn,den3),'Duplicate':pct(go_n-gc_n,go_n)}
 counters={'TP':TPn,'TN':TNn,'FP':FPn,'FN':FNn}
 report={'protocol_version':'6.1','prefix':'fullload','phase':6,'status':'FINAL_BEST_EFFORT','source_baseline':'OD-AI-DDS-001 / R1.0 revision 1.3',
 'universe':{'source_positive_atoms':len(R),'source_negative_controls':len(N),'raw_generated_claim_classes':gc_n,'generated_positive_occurrences':go_n,'covered_source_atoms':TPn,'asserted_negative_controls':len(B_asserted),'unsupported_generated_only_propositions':len(FP_only),'canonical_predicted_positive_units':TPn+FPn,'canonical_decision_units':len(U),'negative_universe_scope':'Only PDF-grounded predeclared bounded controls'},
 'confusion':counters,'metrics':metrics,'duplicate':{'eligible_occurrences':go_n,'unique_generated_classes':gc_n,'duplicate_excess':go_n-gc_n,'within_file_excess':dup_inside,'across_file_excess':dup_cross,'repeated_claim_class_count':repeat,'cross_file_repeated_class_count':multi},
 'fn_root_causes':dict(initial_root_counts),'final_fn_root_causes':dict(collections.Counter(x['fn_review_disposition'] for x in fn_final.values())),'corrected_initial_fn_candidates':root_resolution['TP'], 'source_atomization_corrected_parents':len(retired),
 'tp_proof_audit':{'records':len(TP),'generated_direct_quote_locators_verified':tp_generated_exact,'pdf_text_quote_exact_locators':tp_source_exact,'qualification':'Predicate checks are recorded; exhaustive independent semantic certification is not established.'},
 'source_pdf':{'actual_uploaded_filename':pdf_files[0].name,'physical_pages':pages,'extractable_text_pages':page_nonempty,'source_quote_exact_line_normalized_count':pdf_quote_exact},
 'generated_input_coverage':{'scored_inputs':len(SOURCE_NAMES),'physical_lines':source_line_count,'line_coverage_rows':len(covers),'table_cell_coverage_rows':len(table_cov)},
 'generated_class_validity_labels':dict(label_counter),
 'generated_pdf_support_unverified':sum(v.get('semantic_certification')=='NOT_VERIFIED' for v in rec['V']),
 'remaining_exact_quote_fn_exception_count':len(exact_exceptions),
 'metric_interpretation':'Conventional binary rates over one canonical effective-proposition universe. Precision is unverified because many PDF-support labels are provisional. TN is only the predeclared bounded negative controls; Duplicate uses raw occurrences and classes.',
 'semantic_certification':'NOT_VERIFIED',
 'equations':{'TP_plus_FN_equals_R':TPn+FNn==len(R),'TN_plus_B_equals_N':TNn+len(B_asserted)==len(N),'FP_equals_F_plus_B':FPn==len(FP_only)+len(B_asserted),'four_cells_equals_U':sum(counters.values())==len(U),'canonical_predictions':TPn+FPn,'raw_prediction_classes_are_distinct':True,'duplicate_partition':dup_inside+dup_cross==go_n-gc_n}}
 with (HERE/'06_metrics_final.json').open('w',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
 with (HERE/'06_regression_probes_final.jsonl').open('w',encoding='utf8') as f:
  for row in probe_rows:f.write(json.dumps(row)+'\n')
 with (HERE/'06_residual_exact_match_exceptions_final.jsonl').open('w',encoding='utf8') as f:
  for row in exact_exceptions:f.write(json.dumps(row)+'\n')
 print(json.dumps({'status':report['status'],'cells':counters,'metrics':metrics,'generated_occurrences':go_n,'classes':gc_n,'source_quote_exact':pdf_quote_exact,'remaining_exact_fn_exceptions':len(exact_exceptions),'fn_roots':report['final_fn_root_causes']},indent=2))
 return report

if __name__=='__main__':main()
