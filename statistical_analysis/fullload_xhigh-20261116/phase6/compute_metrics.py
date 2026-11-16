#!/usr/bin/env python3
"""Independently recompute OrionDesk v6.1 canonical scores from item-level ledgers.

No expected counts, scores, or historical labels are hardcoded. Run:
    python compute_metrics.py [--root DIRECTORY] [--write]
The checker validates structural invariants; it cannot certify semantic entailment.
"""
import argparse,collections,json,pathlib,math,re,sys

def main(root,write=False):
 root=pathlib.Path(root).resolve(); workspace=root.parent
 def records(name):
  with (root/name).open(encoding='utf8') as f:return [json.loads(s) for s in f if s.strip()]
 def unique(items,k):
  d={}
  for x in items:
   i=x[k];assert i not in d,('duplicate ID',k,i);d[i]=x
  return d
 R=unique(records('01_source_atoms_final.jsonl'),'source_id')
 N=unique(records('01_source_negative_controls_final.jsonl'),'negative_control_id')
 GO=unique(records('02_generated_atoms_final.jsonl'),'occurrence_id')
 G=unique(records('02_generated_classes_final.jsonl'),'class_id')
 DUP=unique(records('04_duplicate_classes_final.jsonl'),'class_id')
 U=unique(records('03_canonical_universe_final.jsonl'),'canonical_id')
 J=unique(records('04_atomic_judgments_final.jsonl'),'canonical_id')
 BR=records('03_semantic_coverage_bridges_final.jsonl')
 FN=records('03_fn_root_cause_audit_final.jsonl')
 TP=records('05_tp_evidence_audit_final.jsonl')
 GA=unique(records('04_generated_claim_validity_final.jsonl'),'class_id')
 NA=unique(records('04_negative_control_challenge_final.jsonl'),'negative_control_id')
 SO=records('05_source_atomization_audit_final.jsonl')
 DELTA=records('07_change_delta.jsonl')
 LINES=records('02_line_cell_coverage_final.jsonl')
 assert set(R).isdisjoint(N) and set(G)==set(DUP)==set(GA)
 assert set(U)==set(J) and set(U)==(set(R)|set(N)|set(U)-set(R)-set(N))
 assert all(x.get('method')=='supplied_eight_file_set' for x in GO.values())
 assert all(x.get('method')=='supplied_eight_file_set' for x in G.values())
 assert all(x.get('method')=='supplied_eight_file_set' for x in J.values())
 occ_links=collections.Counter()
 for cid,c in G.items():
  assert len(c['occurrence_ids'])==c['occurrence_count']
  for oid in c['occurrence_ids']:
   assert oid in GO and GO[oid]['class_id']==cid,(cid,oid)
   occ_links[oid]+=1
 assert set(occ_links)==set(GO) and set(occ_links.values())=={1}
 extra=[];conf=collections.Counter();A=set();B=set();F=set();pos=set();neg=set()
 for uid,u in J.items():
  assert u==U[uid],('judgment/universe mismatch',uid)
  actual=u['actual_label'];pred=u['predicted_label'];cell=u['scoring_cell']
  assert actual in (0,1) and pred in (0,1)
  assert cell=={(1,1):'TP',(1,0):'FN',(0,1):'FP',(0,0):'TN'}[(actual,pred)],(uid,cell)
  conf[cell]+=1
  if uid in R:
   assert actual==1 and u.get('source_id')==uid;pos.add(uid)
   if cell=='TP':A.add(uid)
  elif uid in N:
   assert actual==0 and uid in u.get('origin_negative_control_ids',[]);neg.add(uid)
   if cell=='FP':B.add(uid)
  else:
   assert actual==0 and cell=='FP' and u.get('origin_generated_class_ids'),uid
   F.add(uid)
  for gc in u.get('origin_generated_class_ids') or []:assert gc in G,('invalid class link',uid,gc)
 assert pos==set(R) and neg==set(N)
 assert len(J)==len(R)+len(N)+len(F)
 assert conf['TP']==len(A)
 assert conf['FN']==len(R)-len(A)
 assert conf['TN']==len(N)-len(B)
 assert conf['FP']==len(F)+len(B)
 assert sum(conf.values())==len(U)
 assert conf['TP']+conf['FP']==len(A)+len(B)+len(F)
 assert len(GO)>=len(G)
 assert all((u.get('origin_negative_control_ids') or [uid])[0]==uid for uid,u in J.items() if uid in N)
 # The full TP audit and every E2 proof bridge must be uniquely linked.
 TPby=unique([x for x in TP if x.get('audit_outcome')=='CONFIRMED_TP'],'source_id')
 assert set(TPby)==A
 bridges=collections.defaultdict(list)
 for b in BR:bridges[b['source_id']].append(b)
 strong={'E2','E3'}
 incomplete=[]
 for sid in A:
  j=J[sid]; t=TPby[sid]
  assert j['entailment_grade'] in strong and j.get('pdf_evidence') and j.get('generated_evidence')
  assert t.get('pdf_evidence') and t.get('generated_evidence') and t['entailment_grade'] in strong
  if j['entailment_grade']=='E2':assert bridges.get(sid),('missing E2 bridge',sid)
  p=t.get('full_predicate_check') or {}
  if set(p)!={'target','action','actor','scope','condition','timing','constraint','exception','outcome','version'}:incomplete.append(sid)
  elif any((e.get('status') not in ('met','not_applicable') or not e.get('proof_en')) for e in p.values()):incomplete.append(sid)
 assert not incomplete,('missing predicate-proof structures',incomplete[:10])
 # Every current FN has a source-ID-matched candidate search record and final disposition.
 fn_by={x['source_id']:x for x in FN if x.get('final_scoring_cell')=='FN'}
 assert len(fn_by)==sum(1 for x in FN if x.get('final_scoring_cell')=='FN') and set(fn_by)==(set(R)-A)
 fn_d=collections.Counter()
 fn_weak_alias=0; fn_weak_reverse=0
 for sid,x in fn_by.items():
  assert x['fn_review_disposition'] in ('TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED')
  assert x.get('pdf_evidence') and x.get('best_generated_candidates') and x.get('specific_reason_en')
  fn_d[x['fn_review_disposition']]+=1
  if not x.get('exact_and_alias_keys_checked'):fn_weak_alias+=1
  if not x.get('retrieval_reversed_source_links'):fn_weak_reverse+=1
 assert sum(fn_d.values())==conf['FN']
 final_fn_history={x['source_id']:x for x in FN if x.get('final_scoring_cell')=='TP'}
 for sid,x in final_fn_history.items():
  assert sid in A and x['fn_review_disposition']=='MATCHER_FALSE_NEGATIVE_CORRECTED'
  assert J[sid].get('fn_review_disposition')=='MATCHER_FALSE_NEGATIVE_CORRECTED'
 src_removed={x['source_id'] for x in SO if x.get('audit_disposition') in ['REMOVE','REMOVED','MERGED','REMOVE_DUPLICATE_OR_NONNORMATIVE'] or x.get('source_denominator_delta')==-1}
 assert src_removed.isdisjoint(R)
 # A negative control is either asserted in both ledgers or unasserted in both.
 for nid,a in NA.items():
  assert nid in N
  assert bool(a['asserted_by_eligible_generated_corpus'])==(nid in B)
 # Raw duplicate class partition.
 assert set(DUP)==set(G)
 within=across=repeat=spans=0
 for cid,c in DUP.items():
  assert c['occurrence_count']==G[cid]['occurrence_count']
  w=c['excess_within_file'];a=c['excess_across_file']
  assert w+a==c['occurrence_count']-1
  within+=w;across+=a
  repeat+=(c['occurrence_count']>=2);spans+=(len(set(c['files']))>=2)
 assert within+across==len(GO)-len(G)
 # Real input files and cited line positions.
 file_names=set(x['file'] for x in GO.values());expected={'01_screen_functions','02_api','03_data','04_batch_functions','05_business_rules','06_exception_handling','07_processing_flows','08_architecture_decision'}
 assert len(file_names)==8
 assert {re.match(r'^\d\d_[^(.]+',f).group() for f in file_names}==expected
 rows={}
 for name in file_names:
  src=workspace/name;assert src.exists(),src
  rows[name]=src.read_text(encoding='utf8').splitlines()
 errors=[]
 for oid,x in GO.items():
  fn=x['file'];ln=x['line_start'];assert 1<=ln<=x['line_end']<=len(rows[fn]),(oid,fn,ln)
  raw='\n'.join(rows[fn][ln-1:x['line_end']])
  if x['exact_quote_en'].strip() not in raw and x['selected_clause_en'].strip() not in raw:
   errors.append((oid,fn,ln))
 assert not errors,('invalid original generated quote',errors[:10],len(errors))
 for sid in A:
  for ev in J[sid]['generated_evidence']:
   assert ev['file'] in rows and 1<=ev['line_start']<=len(rows[ev['file']]),(sid,ev)
 # Cover all lines and table cells, not simply unique generated occurrences.
 coverage=collections.Counter(x['file'] for x in LINES)
 for fn,lines in rows.items():
  assert fn in coverage and coverage[fn]>=len(lines),(fn,coverage[fn],len(lines))
 # Original PDF physical page extent and previously rendered page-wise audit.
 pg=json.load(open(root/'01_pdf_page_coverage.json',encoding='utf8'))
 assert pg['total_physical_pages']==90 and len(pg['page_records'])==90
 assert set(x['physical_page'] for x in pg['page_records'])==set(range(1,91))
 assert all(x.get('page_content_inspected') is True for x in pg['page_records'])
 for r in R.values():assert 1<=r['physical_page']<=90 and r.get('pdf_evidence')
 for n in N.values():assert n.get('pdf_evidence')
 # Each raw class receives one validity label. Labels can be provisional, not certified.
 assert all(v['validity_label'] in ('PDF_ENTAILED','PDF_UNSUPPORTED','SUPPORTED_NONCOVERING') for v in GA.values())
 uncertified=sum(v.get('semantic_certification')!='INDEPENDENTLY_CERTIFIED' for v in GA.values())
 gap=sum('LOW_CONFIDENCE' in str(v.get('phase4_evidence_caveat','')) for v in GA.values())
 count_nc=sum(v['validity_label']=='SUPPORTED_NONCOVERING' for v in GA.values())
 div=lambda a,b:None if b==0 else a/b
 tp=conf['TP'];fp=conf['FP'];fn=conf['FN'];precision=div(tp,tp+fp);recall=div(tp,tp+fn);f1=div(2*tp,2*tp+fp+fn)
 dup=div(len(GO)-len(G),len(GO))
 metrics={'protocol_version':'6.1','method':'supplied_eight_file_set','status':'FINAL_BEST_EFFORT','semantic_certification':'NOT_CERTIFIED','universe':{'source_positive_atoms':len(R),'source_negative_controls':len(N),'raw_generated_claim_classes':len(G),'generated_positive_occurrences':len(GO),'covered_source_atoms':len(A),'asserted_negative_controls':len(B),'unsupported_generated_only_propositions':len(F),'canonical_predicted_positive_units':len(A)+len(B)+len(F),'canonical_decision_units':len(U),'negative_universe_scope':'PDF-grounded, predeclared bounded controls only'},'confusion':dict((k,conf[k]) for k in ['TP','TN','FP','FN']),'metrics':{'Precision':precision,'Recall':recall,'F1':f1,'Duplicate':dup},'duplicates':{'duplicate_excess_occurrences':len(GO)-len(G),'within_file_excess':within,'across_file_excess':across,'repeated_claim_class_count':repeat,'classes_spanning_multiple_files':spans},'audits':{'fn_dispositions':dict(fn_d),'final_FN_with_empty_exact_alias_key_lists':fn_weak_alias,'final_FN_without_reverse_link_count':fn_weak_reverse,'final_TP_with_itemized_proof':len(TPby),'final_TP_E2_bridges':sum(J[s]['entailment_grade']=='E2' for s in A),'final_TP_E3_direct_matches':sum(J[s]['entailment_grade']=='E3' for s in A),'corrected_candidate_FNs_total':len(final_fn_history),'source_atomization_removals':len(src_removed),'uncertified_raw_class_validity':uncertified,'weak_PDF_reverse_support_class_count':gap,'provisionally_supported_noncovering_classes':count_nc,'source_page_inspection_count':len(pg['page_records']),'generated_scored_file_count':len(file_names),'generated_scored_physical_line_count':sum(len(v) for v in rows.values()),'line_and_cell_inspection_units':len(LINES)},'metric_interpretation':'Canonical effective-proposition universe U=R union N union F; raw generated class counting is separate. Precision 100% and FP=0 remain unverified because thousands of generated-class validity decisions lack complete predicate audit. TN is bounded to fixed PDF-negative controls. Semantic entailment is not certified by structural assertions.'}
 qc={'status':'PASS_STRUCTURE_WITH_SEMANTIC_LIMITATIONS','structural_checks_passed':True,'semantic_certification':'NOT_CERTIFIED','source_count':len(R),'negative_controls_count':len(N),'canonical_units':len(U),'TP_proof_records':len(TPby),'FN_root_cause_records':len(fn_by),'FN_with_empty_alias_search_key_lists':fn_weak_alias,'FN_with_no_reported_reverse_links':fn_weak_reverse,'class_support_unverified':uncertified,'weak_support_classes':gap,'remarks_en':['This script performs complete structural and original-line checks, not exhaustive human equivalence judgments.','No semantic certification is inferred from a passing numerical invariant.','The generated claim-validity labels SUPPORTED_NONCOVERING and PDF_ENTAILED remain provisional for the reported uncertified set.']}
 if write:
  (root/'06_metrics_final.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
  (root/'06_phase6_validation.json').write_text(json.dumps(qc,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps({'confusion':metrics['confusion'],'metrics':metrics['metrics'],'duplicate':metrics['duplicates'],'audits':metrics['audits'],'qc':qc['status']},indent=2))
 return metrics,qc
if __name__=='__main__':
 pa=argparse.ArgumentParser();pa.add_argument('--root',default=pathlib.Path(__file__).resolve().parent);pa.add_argument('--write',action='store_true');ar=pa.parse_args()
 try:main(ar.root,ar.write)
 except (Exception,AssertionError) as e:
  print('STRUCTURAL_VALIDATION_FAILED',str(e),file=sys.stderr);raise
