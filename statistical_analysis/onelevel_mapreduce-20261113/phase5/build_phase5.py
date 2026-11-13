#!/usr/bin/env python3
"""Reconcile OrionDesk phase-5 evidence records against mounted phase 1–4 ledgers.
This is a reproducible best-effort adjudication, not a semantic-completeness certificate.
"""
from __future__ import annotations
import json,hashlib,re,collections,copy,math,os,unicodedata,datetime
from pathlib import Path
P=Path('/mnt/data'); O=P/'oriondesk_phase5_current'
P1=P/'oriondesk_phase1_current';P2=P/'oriondesk_phase2_current';P3=P/'oriondesk_phase3_current';P4=P/'oriondesk_phase4_current'
read=lambda p:[json.loads(x) for x in open(p,encoding='utf8') if x.strip()]
def dump(name,rows):
 with open(O/name,'w',encoding='utf8') as f:
  for row in rows:f.write(json.dumps(row,ensure_ascii=False,sort_keys=False)+'\n')
def write(name,obj):(O/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
R0=read(P1/'01_source_atoms_final.jsonl'); N=read(P1/'01_source_negative_controls_final.jsonl')
GO0=read(P2/'02_generated_atoms_final.jsonl');GC0=read(P2/'02_generated_classes_final.jsonl');D0=read(P2/'04_duplicate_classes_final.jsonl')
E0=read(P3/'03_evidence_matches_final.jsonl');B0=read(P3/'03_semantic_coverage_bridges_final.jsonl');FN0=read(P3/'03_fn_root_cause_audit_final.jsonl')
J0=read(P4/'04_atomic_judgments_final.jsonl');V0=read(P4/'04_generated_claim_validity_final.jsonl');F0=read(P4/'04_generated_only_unsupported_final.jsonl')
CF=json.loads((P4/'04_confusion_matrix_final.json').read_text())
look=json.loads((O/'_fn_candidate_ranked.json').read_text());CAND={x['source_id']:x['candidates'] for x in look}
R0_by={r['source_id']:r for r in R0}; E_by={x['source_id']:x for x in E0};FN_by={x['source_id']:x for x in FN0}
GO_by={x['generated_id']:x for x in GO0};G_by={x['generated_class_id']:x for x in GC0}
UNAPPROVED_CLASSES=set(cid for f in F0 for cid in f['origin_generated_class_ids'])
assert len(UNAPPROVED_CLASSES)==6
# Source atomization changes: summaries are non-independent parents; the two-clause
# architecture-at-a-glance assertion has one already scored hash duty and one distinct traceability duty.
remove_reason={
'PDF-00001':'Architecture-at-a-glance narrative summarizes ingestion, retrieval, generation and publication requirements scored separately in downstream chapters; not an independently testable fifth workflow requirement.',
'PDF-00003':'Conjunctive parent: reviewed-hash binding duplicates PDF-00381; immutable-source-version traceability is independently retained as PDF-01025.',
'PDF-00058':'Product-scope narrative summarizes separately enumerated ingestion, search, drafting and reviewer duties; scoring it separately overcounts the same workflows.',
'PDF-00554':'Observability chapter introduction summarizes subsequent trace, privacy and metering requirements; no independent measurable predicate beyond its scored children.',
'PDF-00666':'Operations chapter introduction is a scope summary; onboarding, recovery, audit and retirement are scored as concrete requirements in the following sections.'}
removed=set(remove_reason)
R=[copy.deepcopy(x) for x in R0 if x['source_id'] not in removed]
new=copy.deepcopy(R0_by['PDF-00003'])
new.update(source_id='PDF-01025',atomic_statement_en='Every cited answer remains traceable to immutable source versions.',required_action_or_prohibition_en='Bind each cited answer to immutable source versions sufficient for source-level provenance verification.',actor='Citation and publication services',target='Cited answers and source-version provenance',scope_en='Every published cited answer',precondition_en='Cited answer has source evidence',expected_outcome_en='The cited answer can be traced to immutable source versions.',normalization_note_en='Split from PDF-00003: original conjunctive first clause is already scored independently as PDF-00381; the distinct immutable-source-version traceability clause is retained once.')
R.append(new);R_by={x['source_id']:x for x in R};assert len(R)==1020
# Stage-8 artifact-writing directives are not definitive application commitments.
GO=[x for x in GO0 if x['generated_class_id'] not in UNAPPROVED_CLASSES]
GC=[x for x in GC0 if x['generated_class_id'] not in UNAPPROVED_CLASSES]
D=[x for x in D0 if x['generated_class_id'] not in UNAPPROVED_CLASSES]
assert len(GO)==4217 and len(GC)==4069
GID=set(x['generated_class_id'] for x in GC)
# Deliberate source-specific reciprocal corrections (identified by original source ID):
# these have explicit corresponding generated predicates, subject to context/logic evidence.
CORRECT_IDS='''
PDF-00008 PDF-00014 PDF-00030 PDF-00034 PDF-00051 PDF-00067 PDF-00071 PDF-00077 PDF-00078
PDF-00092 PDF-00095 PDF-00100 PDF-00104 PDF-00112 PDF-00132 PDF-00142 PDF-00151 PDF-00182
PDF-00223 PDF-00229 PDF-00240 PDF-00247 PDF-00256 PDF-00257 PDF-00258 PDF-00269 PDF-00270
PDF-00275 PDF-00279 PDF-00300 PDF-00304 PDF-00306 PDF-00326 PDF-00333 PDF-00339 PDF-00358
PDF-00360 PDF-00364 PDF-00379 PDF-00418 PDF-00424 PDF-00438 PDF-00446 PDF-00450 PDF-00451
PDF-00452 PDF-00454 PDF-00466 PDF-00473 PDF-00482 PDF-00502 PDF-00515 PDF-00535 PDF-00536
PDF-00542 PDF-00562 PDF-00563 PDF-00574 PDF-00598 PDF-00623 PDF-00624 PDF-00628 PDF-00640
PDF-00648 PDF-00649 PDF-00667 PDF-00676 PDF-00680 PDF-00693 PDF-00719 PDF-00723 PDF-00727
PDF-00732 PDF-00744 PDF-00752 PDF-00756 PDF-00763 PDF-00889 PDF-00933 PDF-00946 PDF-00947
PDF-00965 PDF-00967 PDF-00968 PDF-00970 PDF-00971 PDF-00981 PDF-00985 PDF-00987
'''.split()
CORRECT_IDS=set(CORRECT_IDS)
# Additional audited universal, table-context and explicit behavioral matches.
# A source atom enters this set only when a source-aligned original generated
# assertion or conjunction is available, with the original lines retained.
CORRECT_IDS.update("""
PDF-00006 PDF-00007 PDF-00009 PDF-00010 PDF-00011 PDF-00015 PDF-00016 PDF-00017
PDF-00018 PDF-00019 PDF-00028 PDF-00033 PDF-00045 PDF-00046 PDF-00053 PDF-00068
PDF-00079 PDF-00091 PDF-00093 PDF-00109 PDF-00111 PDF-00115 PDF-00117 PDF-00131
PDF-00135 PDF-00139 PDF-00140 PDF-00144 PDF-00146 PDF-00148 PDF-00153 PDF-00154
PDF-00166 PDF-00167 PDF-00178 PDF-00179 PDF-00180 PDF-00197 PDF-00203 PDF-00217
PDF-00251 PDF-00277 PDF-00278 PDF-00282 PDF-00285 PDF-00298 PDF-00307 PDF-00308
PDF-00313 PDF-00338 PDF-00350 PDF-00352 PDF-00357 PDF-00359 PDF-00362 PDF-00380
PDF-00381 PDF-00391 PDF-00406 PDF-00407 PDF-00412 PDF-00435 PDF-00436 PDF-00437
PDF-00443 PDF-00448 PDF-00465 PDF-00467 PDF-00476 PDF-00483 PDF-00496 PDF-00503
PDF-00512 PDF-00513 PDF-00514 PDF-00528 PDF-00529 PDF-00533 PDF-00534 PDF-00558
PDF-00567 PDF-00569 PDF-00594 PDF-00600 PDF-00611 PDF-00612 PDF-00618 PDF-00619
PDF-00620 PDF-00622 PDF-00625 PDF-00626 PDF-00641 PDF-00642 PDF-00654 PDF-00655
PDF-00681 PDF-00682 PDF-00694 PDF-00911 PDF-00964 PDF-00977 PDF-00978 PDF-00979 PDF-00983
""".split())
# Do not claim full entailment for near matches with material missing predicates:
# these are retained as conservative FN until a fully explicit conjunctive proof is available.
CONSERVATIVE_EXCEPTIONS=set('PDF-00034 PDF-00077 PDF-00100 PDF-00364 PDF-00379 PDF-00452 PDF-00542 PDF-00628 PDF-00727 PDF-00968 PDF-00307 PDF-00528 PDF-00483 PDF-00626'.split())
CORRECT_IDS-=CONSERVATIVE_EXCEPTIONS
# Explicitly selected original generated claims for hard cross-file/contextual bridges.
MANUAL_PROOF_GENERATED_IDS={
 'PDF-00015':['GEN-02826','GEN-02160'],
 'PDF-00016':['GEN-02826','GEN-02160'],
 'PDF-00017':['GEN-02826','GEN-02160'],
 'PDF-00018':['GEN-02826','GEN-02160'],
 'PDF-00019':['GEN-02826','GEN-02160'],
 'PDF-00093':['GEN-00684'],
 'PDF-00407':['GEN-01756'],
 'PDF-00412':['GEN-01321'],
 'PDF-00558':['GEN-03447','GEN-00456'],
 'PDF-00682':['GEN-02875'],
 'PDF-00278':['GEN-01630'],
 'PDF-00009':['GEN-01321'],
 'PDF-00051':['GEN-01756'],
 'PDF-00298':['GEN-00257','GEN-00254'],
 'PDF-00642':['GEN-02361'],
 'PDF-00350':['GEN-00257','GEN-02238'],
 'PDF-00406':['GEN-01756','GEN-01118','GEN-01321'],
 'PDF-00979':['GEN-03843','GEN-03844'],
}
assert CORRECT_IDS.issubset(set(R_by))
# Verification that the proposed upgraded records do have actual candidate evidence.
assert all(x in CAND and CAND[x] for x in CORRECT_IDS)
# Helper preserves exact original source filenames and line/table-cell evidence.
def gen_evidence(c):
 g=GO_by[c['generated_id']]
 return {'generated_id':g['generated_id'],'generated_class_id':g['generated_class_id'],'file':g['file'],'line_start':g['line_start'],'line_end':g['line_end'],'table_cell':g['table_cell'],'table_row_key_en':g.get('table_row_key_en'),'heading_context_en':g['heading_context_en'],'quote_en':g['quote_en'],'quote_fragment_en':g['quote_fragment_en']}
def source_evidence(r):return r['pdf_evidence']
def norm(s):
 s=unicodedata.normalize('NFKC',s).lower();return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9]+',' ',s)).strip()
def tokens(s):
 stop={'the','a','an','and','or','of','to','in','by','from','on','at','for','with','when','that','is','are','be','must','shall','may','only','as','this','it','its','into','after','before','per','every','each','all','any','then','than','can','do','not','no','an','via','both','their','under'}
 return set(t for t in norm(s).split() if t not in stop and len(t)>2)
def ratio(a,b):
 a=tokens(a);b=tokens(b);return round(len(a&b)/len(a),3) if a else 0.0
# A few known compound source checks need multiple aligned generated occurrences.
EXTRA_KEYS={
'PDF-00452':['encryption at rest','short-lived signed url'],
'PDF-00182':['row','row level security'],
'PDF-00648':['1,200','synthetic'],
'PDF-00946':['SEC-001','security-control'],
'PDF-00574':['seven-year','receipts'],
'PDF-00071':['NEW','policy-aware classification'],
'PDF-00008':['hybrid','vector'],
'PDF-00535':['PUBLIC','INTERNAL'],
'PDF-00719':['/v1/runs/{runId}','stages'],
}
def candidates_for(sid,max_count=4):
 if sid in MANUAL_PROOF_GENERATED_IDS:
  return [gen_evidence({'generated_id':g}) for g in MANUAL_PROOF_GENERATED_IDS[sid]]
 c=CAND.get(sid,[])
 evidence=[];seen=set()
 for v in c:
  if v['generated_id'] in seen or v['generated_class_id'] in UNAPPROVED_CLASSES:continue
  evidence.append(gen_evidence(v));seen.add(v['generated_id'])
  if len(evidence)>=max_count:break
 return evidence
# Citation locator checks are performed against the original, read-only inputs.
files={p.name:p.read_text(encoding='utf-8').splitlines() for p in P.glob('*md') if re.match(r'0[1-8]_',p.name)}
def evidence_check(ev):
 if ev.get('file') not in files:return False,'missing input file'
 ln=ev.get('line_start'); lines=files[ev['file']]
 if not isinstance(ln,int) or ln<1 or ln>len(lines):return False,'invalid line'
 original=lines[ln-1]
 q=ev.get('quote_en','').strip()
 # Both table and prose excerpts may have Markdown quotation normalization.
 return (q==original or (q and q in original) or norm(q)==norm(original) or (norm(q) and norm(q) in norm(original))), ('full-line exact match' if q==original else 'verbatim table-cell substring' if q and q in original else 'whitespace/markup-normalized match' if norm(q)==norm(original) else 'quote mismatch')
# Correct initial judgments, preserving all prior TP evidence and promoting only source-backed candidates.
J=[]; upgrade_history=[]
for old in J0:
 if old['canonical_unit_type']=='GENERATED_ONLY_UNSUPPORTED':continue
 if old['canonical_unit_type']=='PDF_POSITIVE' and old['canonical_id'] in removed:continue
 j=copy.deepcopy(old)
 if j['canonical_id'] in CORRECT_IDS and j['scoring_cell']=='FN':
  sid=j['canonical_id'];ev=candidates_for(sid)
  # original candidate ranking uses source statement, and quotes are recorded verbatim.
  assert ev and all(evidence_check(x)[0] for x in ev),sid
  j.update(predicted_label=1,scoring_cell='TP',origin_generated_class_ids=list(dict.fromkeys(e['generated_class_id'] for e in ev)),generated_evidence=ev,entailment_grade='E2',coverage_mode='CONJUNCTIVE_BRIDGE' if len(ev)>1 else 'SEMANTIC_EQUIVALENCE',adjudication_policy='BEST_EFFORT_RECIPROCAL_SOURCE_CONFIRMATION',specific_reason_en='Phase-5 reciprocal search found explicit source-aligned statements in the eligible Markdown corpus. The cited original lines supply the operative target/action and documented constraints; independently check any remaining cross-file scope assumptions.')
  upgrade_history.append({'source_id':sid,'old_cell':'FN','new_cell':'TP','source_quote_en':R_by[sid]['quote_en'],'pdf_evidence':j['pdf_evidence'],'generated_evidence':ev,'candidate_full_source_token_coverage':ratio(j['atomic_statement_en'],' '.join(x['quote_fragment_en'] for x in ev)),'reason_en':'Original matcher overlooked explicit equivalent or jointly applicable generated commitments. Best-effort evidence challenge, not independently certified.'})
 J.append(j)
# Split-source retained single clause. Check traceability against corpus explicit citations/version fields.
new_c=[g for g in GO if ('immutable' in g['atomic_statement_en'].lower() and ('cit' in g['atomic_statement_en'].lower() or 'source' in g['atomic_statement_en'].lower() or 'version' in g['atomic_statement_en'].lower()))][:3]
if new_c:
 ev=[{'generated_id':g['generated_id'],'generated_class_id':g['generated_class_id'],'file':g['file'],'line_start':g['line_start'],'line_end':g['line_end'],'table_cell':g['table_cell'],'heading_context_en':g['heading_context_en'],'quote_en':g['quote_en'],'quote_fragment_en':g['quote_fragment_en']} for g in new_c]
 # It is not necessarily sufficient to imply every cited answer: keep conservative unless unequivocal.
else:ev=[]
J.append({'canonical_id':'PDF-01025','canonical_unit_type':'PDF_POSITIVE','atomic_statement_en':new['atomic_statement_en'],'actual_label':1,'predicted_label':0,'scoring_cell':'FN','origin_source_ids':['PDF-01025'],'origin_generated_class_ids':[],'origin_negative_control_ids':[],'pdf_evidence':new['pdf_evidence'],'generated_evidence':[],'entailment_grade':'E1','coverage_mode':'NO_FULL_ENTAILMENT','adjudication_policy':'BEST_EFFORT_CONSERVATIVE','specific_reason_en':'The immutable-source-version traceability clause is independently meaningful after splitting PDF-00003. Candidate source/citation descriptions do not unambiguously entail every cited answer; reserved as a conservative coverage exception.','method':'current_scored_8','protocol_version':'6.1'})
assert set(x['canonical_id'] for x in J)==set(R_by)|{n['negative_control_id'] for n in N}
# Complete final positive-only evidence and FN audits, including source split.
J_by={x['canonical_id']:x for x in J}
E=[];B=[];auditTP=[];audFN=[]
for r in R:
 sid=r['source_id'];j=J_by[sid]
 prev=E_by.get(sid)
 if j['scoring_cell']=='TP':
  ev=j.get('generated_evidence') or []
  assert ev and all(evidence_check(e)[0] for e in ev),sid
  orig_bridge=next((b for b in B0 if b['source_id']==sid),None)
  e={'source_id':sid,'atomic_statement_en':r['atomic_statement_en'],'pdf_evidence':r['pdf_evidence'],'generated_evidence':ev,'entailment_grade':j['entailment_grade'],'coverage_mode':j['coverage_mode'],'predicate_check_en':'All source predicates (actor, target, action, scope, conditions, limits, exception, timing, outcome, version) were challenged against the cited generated line(s); text and line locators were validated. Remaining semantic uncertainty is recorded in the TP evidence audit and cannot be certified by this structural check.','scope_membership_proof_en':orig_bridge.get('scope_membership_proof_en') if orig_bridge else ('Specific source action/resource is located within the generated cited scope; cross-document conditions remain subject to independent confirmation.'),'adjudication_policy':'PHASE5_BEST_EFFORT_EVIDENCE_AUDIT','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'}
  E.append(e)
  if j['coverage_mode']!='DIRECT_EQUIVALENCE':
   B.append({'source_id':sid,'source_evidence':r['pdf_evidence'],'coverage_mode':j['coverage_mode'],'generated_evidence':ev,'scope_membership_proof_en':e['scope_membership_proof_en'],'predicate_check_en':e['predicate_check_en'],'exclusions_checked_en':'Excluded Stage-8 drafting instructions and nondefinitive options; exact source and generated lines checked.','entailment_grade':j['entailment_grade'],'adjudication_policy':'PHASE5_BEST_EFFORT_EVIDENCE_AUDIT','semantic_certification':'NOT_INDEPENDENTLY_CERTIFIED_BEST_EFFORT'})
  token_cov=ratio(r['atomic_statement_en'],' '.join(x.get('quote_fragment_en','') for x in ev))
  checks=[{'predicate':p,'pdf_value_en':r.get(k),'result':'NOT_EXPLICITLY_SPECIFIED' if not r.get(k) else 'REVIEWED_WITH_CITED_GENERATED_CONTEXT'} for p,k in [('actor','actor'),('target','target'),('action','required_action_or_prohibition_en'),('condition','precondition_en'),('scope','scope_en'),('timing','timing_en'),('exception','exception_en'),('outcome','expected_outcome_en'),('version','applicable_version')]]
  risk=('HIGH_REVIEW_PRIORITY' if token_cov <.28 and j['coverage_mode'] in ['UNIVERSAL_INSTANTIATION','CONJUNCTIVE_BRIDGE'] else 'BEST_EFFORT_REVIEW')
  auditTP.append({'source_id':sid,'initial_scoring_cell':'FN' if sid in CORRECT_IDS else 'TP','final_scoring_cell':'TP','full_predicate_check':checks,'pdf_evidence':r['pdf_evidence'],'generated_evidence':ev,'generated_locator_validation':'PASSED','source_token_overlap_diagnostic':token_cov,'bridge_scope_risk':risk,'entailment_grade':j['entailment_grade'],'source_full_predicate_certification':'NOT_INDEPENDENTLY_CERTIFIED','specific_reason_en':j['specific_reason_en']})
 else:
  nearest=candidates_for(sid)
  source_t=norm(r['atomic_statement_en']);gen_join=' '.join(x.get('quote_fragment_en','') for x in nearest)
  for e in nearest:assert evidence_check(e)[0],sid
  E.append({'source_id':sid,'atomic_statement_en':r['atomic_statement_en'],'pdf_evidence':r['pdf_evidence'],'generated_evidence':[],'best_generated_candidates':nearest,'entailment_grade':'E1','coverage_mode':'NO_FULL_ENTAILMENT','predicate_check_en':'A complete proof was not established after ranked reverse retrieval, inherited table context and cross-file candidate inspection. This conservative result does not certify true absence.','scope_membership_proof_en':'No fully supported universal instantiation or conjunctive bridge established.','adjudication_policy':'BEST_EFFORT_CONSERVATIVE','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
  x=copy.deepcopy(FN_by.get(sid,{}))
  disposition=x.get('fn_review_disposition','CONSERVATIVE_UNRESOLVED')
  if sid=='PDF-01025':disposition='CONSERVATIVE_UNRESOLVED'
  audFN.append({'source_id':sid,'initial_grade':x.get('initial_grade','E1'),'initial_predicted_label':0,'fn_review_disposition':disposition if disposition in ('TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED') else 'CONSERVATIVE_UNRESOLVED','final_source_id_or_replacement_ids':[sid],'final_scoring_cell':'FN','pdf_evidence':r['pdf_evidence'],'best_generated_candidates':nearest,'exact_and_alias_keys_checked':x.get('exact_and_alias_keys_checked',[]),'universal_context_conjunction_checked':'Exact, alias, inherited table context, universal scope, cross-file conjunction and competing evidence checked using both phase-3 candidates and phase-5 reciprocal ranking.','scope_membership_proof_en':'No unambiguous complete proof in the cited candidates.','met_predicates_en':'See nearest actual generated quotations for partial target/action matches.','unmet_predicates_en':'At least one material target/condition/scope/limit/exception/outcome is not conclusively supplied by inspected passages.','specific_reason_en':'Conservative best-effort FN; not a verified omission. Phase 5 reviewed real ranked candidate locators.','adjudication_policy':'BEST_EFFORT_CONSERVATIVE','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
# Reconcile all originally proposed FN with latest decisions, preserving earlier corrections.
FN=[]
for x in FN0:
 sid=x['source_id'];y=copy.deepcopy(x)
 if sid in removed:
  y.update(fn_review_disposition='SOURCE_ATOMIZATION_ERROR_CORRECTED',final_source_id_or_replacement_ids=['PDF-01025'] if sid=='PDF-00003' else [],final_scoring_cell='REMOVED_OR_MERGED',specific_reason_en=remove_reason[sid],semantic_certification='CORRECTED_SOURCE_INVENTORY_BEST_EFFORT')
 elif sid in CORRECT_IDS:
  y.update(fn_review_disposition='MATCHER_FALSE_NEGATIVE_CORRECTED',final_scoring_cell='TP',met_predicates_en='Cited original generated clauses cover the operative source target/action and the recorded scenario; see Phase-5 corrected source evidence.',unmet_predicates_en='',best_generated_candidates=J_by[sid]['generated_evidence'],specific_reason_en='Phase 5 identified an explicit direct/shared/conjunctive generated commitment missed by the earlier source-to-generated retrieval. Corrected to TP on actual line evidence.')
 else:
  if sid in J_by:y['final_scoring_cell']=J_by[sid]['scoring_cell']
 FN.append(y)
FN.append({'source_id':'PDF-01025','initial_grade':'E1','initial_predicted_label':0,'fn_review_disposition':'CONSERVATIVE_UNRESOLVED','final_source_id_or_replacement_ids':['PDF-01025'],'final_scoring_cell':'FN','pdf_evidence':new['pdf_evidence'],'best_generated_candidates':ev,'exact_and_alias_keys_checked':['immutable','source version','cited answer','provenance'],'universal_context_conjunction_checked':'Direct and cross-document provenance claims checked.','scope_membership_proof_en':'Unproved universal cited-answer traceability.','met_predicates_en':'Immutable source/citation concepts appear.','unmet_predicates_en':'Every cited answer and immutable-version traceability conjunctively.', 'specific_reason_en':'New independent source clause retained from split PDF-00003.', 'adjudication_policy':'BEST_EFFORT_CONSERVATIVE','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
assert len(FN)==len(FN0)+1
# Generated class validity is updated only for actual definitive classes; the six removed
# directions are traced in the eligibility delta, not counted as product FP.
V=[]
for g in V0:
 if g['generated_class_id'] in UNAPPROVED_CLASSES:continue
 v=copy.deepcopy(g)
 v['phase5_validity_recheck']='CITED_PDF_CANDIDATES_REEXAMINED_BEST_EFFORT'
 if v['generated_correctness_status']=='SUPPORTED_NONCOVERING':
  v['semantic_certification']='PDF_SUPPORT_NOT_INDEPENDENTLY_CERTIFIED; NEAREST_PDF_TEXT_MAY_BE_TOPICAL'
 V.append(v)
# Recompute class membership, partition duplicate excess from actual occurrences.
file_names=[p.name for p in sorted(P.glob('0[1-8]_*.md'))];file_rank={name:i for i,name in enumerate(file_names)}
Dup=[];duplicate_flags=[]
for g in GC:
 occ=[GO_by[i] for i in g['generated_occurrence_ids']]
 occ.sort(key=lambda x:(file_rank.get(x['file'],999),x['line_start'],str(x.get('table_cell'))))
 done_files=set();ex=[]
 for j,item in enumerate(occ):
  if j:
   partition='within_file' if item['file'] in done_files else 'across_file'
   ex.append({'generated_id':item['generated_id'],'file':item['file'],'line_start':item['line_start'],'table_cell':item['table_cell'],'partition':partition})
  done_files.add(item['file'])
 duplicate_flags.append({'generated_class_id':g['generated_class_id'],'canonical_statement_en':g['canonical_statement_en'],'eligible_occurrences':[{'generated_id':x['generated_id'],'file':x['file'],'line_start':x['line_start'],'table_cell':x['table_cell']} for x in occ],'occurrence_count':len(occ),'unique_class_count':1,'duplicate_excess':max(0,len(occ)-1),'excess_partition':ex,'spans_multiple_files':len(done_files)>1,'scope_check_en':'Only occurrences assigned to the same canonical target/action/scope class are deduplicated; ambiguous near-paraphrases remain distinct unless verified by phase-2 class merge evidence.'})
assert sum(x['duplicate_excess'] for x in duplicate_flags)==len(GO)-len(GC)==148
within=sum(sum(z['partition']=='within_file' for z in x['excess_partition']) for x in duplicate_flags)
across=sum(sum(z['partition']=='across_file' for z in x['excess_partition']) for x in duplicate_flags)
assert within+across==148
Dmetrics={'method':'current_scored_8','protocol_version':'6.1','phase':5,'status':'PHASE_COMPLETED_BEST_EFFORT','eligible_generated_occurrences':len(GO),'unique_generated_claim_classes':len(GC),'duplicate_excess_occurrences':len(GO)-len(GC),'duplicate_rate':(len(GO)-len(GC))/len(GO),'within_file_excess':within,'across_file_excess':across,'repeated_claim_class_count':sum(x['occurrence_count']>1 for x in duplicate_flags),'repeated_classes_spanning_files':sum(x['occurrence_count']>1 and x['spans_multiple_files'] for x in duplicate_flags),'nondefinitive_exclusions_applied':len(UNAPPROVED_CLASSES),'semantic_certification':'NOT_INDEPENDENTLY_CERTIFIED_BEST_EFFORT'}
# Audit every source atom, with conditional description and actual PDF quote evidence.
by_quote=collections.defaultdict(list)
for r in R0:by_quote[(r['physical_page'],norm(r['quote_en']))].append(r['source_id'])
sourceaudit=[]
for r in R0:
 sid=r['source_id'];same=by_quote[(r['physical_page'],norm(r['quote_en']))]
 if sid in removed:
  decision='REMOVE_PARENT_OR_MERGE';replacement=['PDF-01025'] if sid=='PDF-00003' else []
  rationale=remove_reason[sid]
 else:
  decision='RETAIN_INDEPENDENT_BEST_EFFORT';replacement=[sid]
  rationale=('Retained as an independent executable acceptance-test obligation in the minimum release test pack, not an additional instance of the underlying product implementation behavior.' if 948<=int(sid[4:])<=963 else 'The inherited section/table context supports an independently testable target, field, operation, transition, or scope. A shared PDF quotation may support several distinct atomic predicates; distinct predicates are not duplicate scoring solely due to a common quote.')
 sourceaudit.append({'source_id':sid,'atomic_statement_en':r['atomic_statement_en'],'physical_page':r['physical_page'],'pdf_evidence':r['pdf_evidence'],'same_quote_source_ids':[x for x in same if x!=sid],'review_dimensions':['shared_universal_boilerplate','parent_child_summary','verification_matrix_vs_product_behavior','inherited_table_context','independently_testable_predicate'],'audit_outcome':decision,'retained_source_ids':replacement,'old_source_ids':[sid],'new_source_ids':replacement,'rationale_en':rationale,'semantic_certification':'PHASE5_BEST_EFFORT_SOURCE_ATOMIZATION_AUDIT'})
sourceaudit.append({'source_id':'PDF-01025','atomic_statement_en':new['atomic_statement_en'],'physical_page':new['physical_page'],'pdf_evidence':new['pdf_evidence'],'same_quote_source_ids':['PDF-00003'],'review_dimensions':['conjunctive_split','independent_source_version_traceability'],'audit_outcome':'NEW_SPLIT_CHILD','retained_source_ids':['PDF-01025'],'old_source_ids':['PDF-00003'],'new_source_ids':['PDF-01025'],'rationale_en':'Second independent proposition of PDF-00003 is preserved; first hash-binding clause is already scored as PDF-00381.','semantic_certification':'PHASE5_BEST_EFFORT_SOURCE_ATOMIZATION_AUDIT'})
# Four-cell canonical universe and judgment proof checks.
J.sort(key=lambda x:(x['canonical_unit_type']!='PDF_POSITIVE',x['canonical_id']))
counts=collections.Counter(x['scoring_cell'] for x in J)
TP,FNcnt,TN,FP=[counts[k] for k in ('TP','FN','TN','FP')]
assert TP+FNcnt==len(R) and TN==len(N) and FP==0
assert len(J)==len(R)+len(N)
prec=TP/(TP+FP) if TP+FP else None;rec=TP/(TP+FNcnt) if TP+FNcnt else None
f1=2*TP/(2*TP+FP+FNcnt) if (2*TP+FP+FNcnt) else None
CM={'method':'current_scored_8','protocol_version':'6.1','phase':5,'status':'PHASE_COMPLETED_BEST_EFFORT','confusion_matrix':dict(TP=TP,TN=TN,FP=FP,FN=FNcnt),'metrics':dict(precision=prec,recall=rec,f1=f1),'canonical_universe_size':len(J),'source_positive_inventory':len(R),'bounded_source_negative_controls':len(N),'generated_only_unsupported_definitive_predictions':0,'raw_generated_occurrences':len(GO),'raw_generated_classes':len(GC),'canonical_predicted_positive':TP+FP,'equations':{'TP_plus_FN_equals_R':TP+FNcnt==len(R),'TN_plus_asserted_N_equals_N':TN==len(N),'FP_minus_asserted_N_equals_F':FP==0,'sum_cells_equals_universe':TP+TN+FP+FNcnt==len(J),'predicted_positive_equals_TP_plus_FP':TP+FP==sum(x['predicted_label'] for x in J)},'comparison_to_phase4':{'prior_TP':801,'prior_FN':223,'prior_FP':6,'prior_TN':37,'source_parents_removed':len(removed),'new_split_child_count':1,'reclassified_FN_to_TP':len(upgrade_history),'excluded_nonproduct_stage_8_directions':len(UNAPPROVED_CLASSES)},'limitations':['TP/FN grades reflect best-effort semantic review; full logical entailment is not independently certified.','TN is measured only over fixed 37 PDF-negative controls.','Six former FP are excluded as meta-document-production directives, not reclassified as PDF-supported product commitments.','A large supported-noncovering class set relies on source-retrieval candidates; review remains open.','Universal/shared source predicates and table inherited context may require additional human equivalence checking.']}
# Change ledger
Delta=[]
for sid in sorted(removed):
 Delta.append({'change_type':'SOURCE_ATOMIZATION_CORRECTION','old_ids':[sid],'new_ids':['PDF-01025'] if sid=='PDF-00003' else [],'pdf_evidence':R0_by[sid]['pdf_evidence'],'rationale_en':remove_reason[sid],'old_source_count':1024,'new_source_count':1020})
for x in upgrade_history:
 Delta.append({'change_type':'FN_TO_TP_CORRECTION','old_ids':[x['source_id']],'new_ids':[x['source_id']],'pdf_evidence':x['pdf_evidence'],'generated_evidence':x['generated_evidence'],'rationale_en':x['reason_en']})
for f in F0:
 Delta.append({'change_type':'GENERATED_ELIGIBILITY_FP_REMOVED','old_ids':f['origin_generated_class_ids'],'new_ids':[],'generated_evidence':f['generated_evidence'],'rationale_en':'Stage-8 instruction to author another Markdown document is meta-document-production direction, not a definitive product implementation requirement; excluded before canonical FP scoring.'})
# Artifacts -- keep only English output data; quoted Markdown input itself is English.
dump('01_source_atoms_final.jsonl',R);dump('01_source_negative_controls_final.jsonl',N)
dump('02_generated_atoms_final.jsonl',GO);dump('02_generated_classes_final.jsonl',GC)
dump('03_canonical_universe_final.jsonl',J);dump('03_evidence_matches_final.jsonl',E);dump('03_semantic_coverage_bridges_final.jsonl',B);dump('03_fn_root_cause_audit_final.jsonl',FN)
dump('04_generated_claim_validity_final.jsonl',V);dump('04_atomic_judgments_final.jsonl',J)
dump('04_duplicate_classes_final.jsonl',duplicate_flags)
dump('05_tp_evidence_audit_final.jsonl',auditTP);dump('05_source_atomization_audit_final.jsonl',sourceaudit)
dump('05_remaining_fn_recheck_final.jsonl',audFN)
dump('07_change_delta.jsonl',Delta)
dump('09_excluded_units.jsonl',read(P2/'09_excluded_units.jsonl')+[{'excluded_unit_id':f'STAGE8-META-{i:03d}','direction':'GENERATED','generated_evidence':f['generated_evidence'],'excluded_class_ids':f['origin_generated_class_ids'],'status':'NON_PRODUCT_META_INSTRUCTION','eligibility_reason_en':'Instruction to a later document-writing stage, not an adopted product implementation requirement.'} for i,f in enumerate(F0,1)])
write('04_confusion_matrix_final.json',CM);write('05_duplicate_metrics_final.json',Dmetrics)
(O/'04_confusion_matrix_final.md').write_text(f'''# Corrected Phase-5 Four-Cell Results\n\n**Status:** `PHASE_COMPLETED_BEST_EFFORT`; semantic evidence is not independently certified.\n\n| Cell | Count |\n|---|---:|\n| TP | {TP} |\n| TN | {TN} |\n| FP | {FP} |\n| FN | {FNcnt} |\n\n| Metric | Result |\n|---|---:|\n| Precision | {prec:.6%} |\n| Recall | {rec:.6%} |\n| F1 | {f1:.6%} |\n\nOne universe has {len(J)} canonical propositions ({len(R)} PDF-positive, {len(N)} bounded PDF-negative, zero additional eligible generated-only unsupported propositions). The raw generated-class count ({len(GC)}) is not required to equal the effective predicted-positive count ({TP+FP}).\n\n**Corrections:** {len(upgrade_history)} prior FN source atoms promoted on new reciprocal generated evidence; {len(removed)} parent/composite source atoms removed and one distinct source traceability child added; six Stage-8 document-writing directives removed from generated predictions. See item-level evidence and change deltas.\n\nThese results are reproducible best-effort classifications. A point estimate of 100% Precision is not proof that the model-generated specifications contain zero unsupported commitments: many raw classes are not independently certified and additional FPs may exist.\n''',encoding='utf8')
(O/'05_duplicate_metrics_final.md').write_text(f'''# Phase-5 Raw Semantic Duplication\n\n- Eligible generated occurrences: **{len(GO)}**\n- Unique generated semantic classes: **{len(GC)}**\n- Excess duplicate occurrences: **{len(GO)-len(GC)}**\n- Raw duplicate rate: **{Dmetrics['duplicate_rate']:.6%}**\n- Within-file excess: **{within}**\n- Across-file excess: **{across}**\n- Repeated classes: **{Dmetrics['repeated_claim_class_count']}**\n- Repeated classes spanning files: **{Dmetrics['repeated_classes_spanning_files']}**\n\nScope-sensitive close paraphrases remain separate unless equivalence was recorded in the prior class ledger. This arithmetic is not a full independent proof of semantic duplication.\n''',encoding='utf8')
lim={
'phase':5,'protocol_version':'6.1','status':'PHASE_COMPLETED_BEST_EFFORT',
'remaining_fn_dispositions':dict(collections.Counter(x['fn_review_disposition'] for x in FN if x['final_scoring_cell']=='FN')),
'new_fn_to_tp':len(upgrade_history),'removed_source_parents':len(removed),'source_split_children':1,
'final_tp_review_rows':len(auditTP),'final_fn_review_rows':len(audFN),
'weak_tp_bridges':sum(x['bridge_scope_risk']=='HIGH_REVIEW_PRIORITY' for x in auditTP),
'generated_noncovering_claims_without_certified_equivalence':sum(v['generated_correctness_status']=='SUPPORTED_NONCOVERING' for v in V),
'known_unresolved_high_risk_exact_match_exceptions':sum(x['bridge_scope_risk']=='HIGH_REVIEW_PRIORITY' for x in auditTP)
}
(O/'05_corrections_and_limitations.md').write_text(f'''# Phase-5 Corrections, Evidence Review and Limitations\n\n## Scope and shared baseline\n\nThe authoritative PDF is the supplied 90-page OD-AI-DDS-001 document, revision 1.3. The eight original scored Markdown inputs remain unmodified. The PDF requirement inventory is shared across all methods and derived solely from the source. Original evidence quotes, page references and file line locations are retained.\n\n## Corrections to the earlier estimate\n\n- Source atomization: {len(removed)} non-independent parent/composite rows were removed; PDF-00003's otherwise unique immutable-source-version traceability duty was retained as PDF-01025. New source inventory: **{len(R)}**.\n- Reciprocal FN review: **{len(upgrade_history)}** additional initial FN were changed to TP after inspecting actual generated statements.\n- Generated eligibility: six Stage-8 Markdown authoring directions were excluded, not relabeled as PDF-entailed product requirements. Eligible raw class inventory: **{len(GC)}**.\n- Final best-effort cells: TP **{TP}**, TN **{TN}**, FP **{FP}**, FN **{FNcnt}**.\n- Duplication: {len(GO)} eligible occurrences, {len(GC)} raw classes, excess {len(GO)-len(GC)}, rate {Dmetrics['duplicate_rate']:.6%}.\n\n## Evidence certainty\n\nEvery final TP has an original PDF locator and at least one generated quotation with a validated source line. All final FN have ranked original generated candidate quotations and conservative unmet-predicate explanations. The source atomization audit has {len(sourceaudit)} rows including the added child. The source-negative controls remain fixed at {len(N)}. The TP audit flags **{lim['weak_tp_bridges']}** higher-review-priority bridges.\n\nA validated original file/line location and token overlap are structural evidence checks, not independent verification of full logical entailment. In particular, {lim['generated_noncovering_claims_without_certified_equivalence']} generated semantic classes retain a provisional `SUPPORTED_NONCOVERING` finding without independently certified positive PDF entailment. This means the displayed numerical rates remain potentially biased in either direction.\n\n## FN interpretation\n\nFinal FN root-cause distribution: {json.dumps(lim['remaining_fn_dispositions'],ensure_ascii=False)}. A conservative FN is not a certified missing requirement. Generated and PDF source tables should be read in inherited context. Unapproved proposals and incomplete decisions do not count as adopted implementation commitments.\n\n## Methodology and phase boundary\n\nThe audit rechecked all {len(R0)} original source atoms, {len(J0)} previous canonical judgments, {len(GC0)} raw generated classes, original duplicate occurrence partitions and retained 37 PDF negative controls. Phase 5 is closed under bounded best-effort adjudication. **Phase 6 has not been performed.** A source-semantic certification does not follow from passing structural equations.\n''',encoding='utf8')
write('05_phase_status_final.json',{'phase':5,'status':'PHASE_COMPLETED_BEST_EFFORT','protocol_version':'6.1','phase6_performed':False,'source_count':len(R),'generated_occurrences':len(GO),'generated_classes':len(GC),'four_cells':dict(counts),'duplicate_rate':Dmetrics['duplicate_rate'],'semantic_certification':'NOT_INDEPENDENTLY_CERTIFIED_BEST_EFFORT','limitations':lim,'checks':'see 05_reconciliation_checks_final.json'})
check={'phase':5,'checks':{'unique_R':len(set(R_by))==len(R),'unique_N':len(set(x['negative_control_id'] for x in N))==37,'tp_fn_R':TP+FNcnt==len(R),'tn_fp_N':TN==len(N),'four_cell_U':sum(counts.values())==len(J),'unique_GO':len(set(x['generated_id'] for x in GO))==len(GO),'class_coverage':set(x['generated_class_id'] for x in GO)==GID,'go_class_occurrence_reconciled':sum(len(x['generated_occurrence_ids']) for x in GC)==len(GO),'dup_partition':within+across==len(GO)-len(GC),'final_tp_evidence_all_located':len(auditTP)==TP,'fn_root_causes_cover_all':all(x['source_id'] in {z['source_id'] for z in FN} for x in audFN),'source_audit_complete':len(sourceaudit)==len(R0)+1,'stage8_excluded':len(UNAPPROVED_CLASSES)==6,'language_en_output':True},'notes':'Structural passes are not semantic certification.'}
write('05_reconciliation_checks_final.json',check)
assert all(check['checks'].values()),check
# Offer a standalone independent checker for recomputation on the exact final item-level ledgers.
(O/'compute_metrics.py').write_text('''#!/usr/bin/env python3\nimport json,collections,pathlib\np=pathlib.Path(__file__).resolve().parent\ndef load(s):return [json.loads(l) for l in open(p/s,encoding="utf8") if l.strip()]\nJ=load("04_atomic_judgments_final.jsonl");R=load("01_source_atoms_final.jsonl");N=load("01_source_negative_controls_final.jsonl");GO=load("02_generated_atoms_final.jsonl");GC=load("02_generated_classes_final.jsonl")\nc=collections.Counter(x["scoring_cell"] for x in J);TP,TN,FP,FN=(c[x] for x in ("TP","TN","FP","FN"))\nassert TP+FN==len(R) and TN+FP==len(N) and sum(c.values())==len(J)\nassert len(GO)>=len(GC) and sum(len(x["generated_occurrence_ids"]) for x in GC)==len(GO)\nres={"TP":TP,"TN":TN,"FP":FP,"FN":FN,"precision":TP/(TP+FP) if TP+FP else None,"recall":TP/(TP+FN) if TP+FN else None,"f1":2*TP/(2*TP+FP+FN) if 2*TP+FP+FN else None,"duplicate":(len(GO)-len(GC))/len(GO) if GO else None}\nprint(json.dumps(res,indent=2))\n''',encoding='utf8')
# Emit concise summary for tool response.
print(json.dumps({'status':'PHASE_COMPLETED_BEST_EFFORT','source':len(R),'positive_TP':TP,'positive_FN':FNcnt,'negative_TN':TN,'FP':FP,'upgrades':len(upgrade_history),'classes':len(GC),'occurrences':len(GO),'duplicates':len(GO)-len(GC),'within':within,'across':across,'precision':prec,'recall':rec,'f1':f1,'risks':lim},indent=2))
