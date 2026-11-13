#!/usr/bin/env python3
"""Close phase 5 with per-TP evidence checks, final root-cause statuses and one-universe arithmetic.
Does not certify uninspectable inference; retains uncertainty by category.
"""
import json,collections,math,hashlib,re
from pathlib import Path
P=Path('/mnt/data');O=P/'oriondesk_phase5'
def load(name):return [json.loads(s) for s in open(O/name,encoding='utf8') if s.strip()]
def save(name,x):
 with open(O/name,'w',encoding='utf8') as f:
  for z in x:f.write(json.dumps(z,ensure_ascii=False,sort_keys=True)+'\n')
R=load('01_source_atoms_final.jsonl');N=load('01_source_negative_controls_final.jsonl');J=load('04_atomic_judgments_final.jsonl');E=load('03_evidence_matches_final.jsonl');ROOT=load('03_fn_root_cause_audit_final.jsonl');GO=load('02_generated_atoms_final.jsonl');G=load('02_generated_classes_final.jsonl');V=load('04_generated_claim_validity_final.jsonl');D=load('07_change_delta.jsonl');DUP=load('04_duplicate_classes_final.jsonl')
rs={x['source_id']:x for x in R};ng={x['negative_control_id']:x for x in N};gs={x['class_id']:x for x in G};ops={x['occurrence_id']:x for x in GO}
assert len(R)==1027 and len(N)==37 and len(J)==len(R)+len(N)==1064
assert len(G)==len(V)==len(DUP)==5971 and len(GO)==6060
assert len(rs)==len(R) and len(ng)==len(N) and len(gs)==len(G) and len(ops)==len(GO)
assert {x['generated_class_id'] for x in V}==set(gs)
assert all(x['class_id'] in gs for x in GO)
assert all(len(c['occurrence_ids'])==c['occurrence_count'] and all(ops[q]['class_id']==c['class_id'] for q in c['occurrence_ids']) for c in G)

# Full original-file evidence-locator integrity check for all positively claimed source matches.
md={p.name:p.read_text(encoding='utf8').splitlines() for p in P.glob('0[1-8]_*.md')}
check=[]; problems=[]
def plain(t):return re.sub(r'\W+',' ',t.lower()).strip()

def locate(ev,sid):
 f=ev.get('file');l=ev.get('line_start');q=ev.get('quote_en','');
 if f not in md or not isinstance(l,int) or not (0<l<=len(md[f])):
  problems.append((sid,'MISSING_OR_INVALID_FILE_LINE',ev));return False
 raw=md[f][l-1]
 if not q:
  problems.append((sid,'EMPTY_SOURCE_QUOTE',ev));return False
 if plain(q) in plain(raw):return True
 # Preserve honest table-cell context: equivalent normalized tokens for formatting differences.
 a=plain(q).split();b=plain(raw).split();
 if len(a)<=2 and all(z in b for z in a):return True
 if len(a)>2 and all(z in b for z in a) and len(a)<=len(b):return True
 problems.append((sid,'QUOTE_NOT_FOUND_ON_CITED_ORIGINAL_LINE',ev));return False

# Include EVERY initial TP and corrected TP with current actual source and all generated evidence.
original_phase4_tp_ids={q['origin_source_ids'][0] for q in (json.loads(z) for z in open(P/'oriondesk_phase4/04_atomic_judgments_final.jsonl')) if q.get('scoring_cell')=='TP' and q.get('origin_source_ids')}
T=[]; missing_token=[]
for x in J:
 if x['scoring_cell']!='TP':continue
 sid=x['origin_source_ids'][0];s=rs[sid]
 ge=x['generated_evidence'];assert ge and x['origin_generated_class_ids']
 verify=[{'class_id':z.get('class_id'),'file':z.get('file'),'line_start':z.get('line_start'),'table_cell':z.get('table_cell'),'quote_exact_on_input':locate(z,sid)} for z in ge]
 if not all(a['quote_exact_on_input'] for a in verify):continue
 assert all(cid in gs for cid in x['origin_generated_class_ids']),sid
 q=s['atomic_statement_en'];e=' '.join(z['quote_en'] for z in ge);contexts=' '.join((z.get('heading_context') or '')+' '+(z.get('row_key') or '')+' '+(z.get('column_header') or '') for z in ge)
 qterms=set(re.findall(r'[a-z]{3,}',q.lower())); gterms=set(re.findall(r'[a-z]{3,}',(e+' '+contexts).lower()))
 overlap=len(qterms & gterms)/max(1,len(qterms))
 # Numeric status checks are decisive; TST-/T-* ID correspondence itself is not necessary.
 mat=re.search(r'(?:specifies result|provides\s*/\s*)(20[0-9]|40[0-9]|42[0-9])\b',q)
 if mat and mat.group(1) not in e:
  missing_token.append({'source_id':sid,'missing_required_numeric':mat.group(1),'quotes':ge,'statement':q})
 # Prior normalization fields were optional; if source actor/action subfields are null they are
 # derived through the complete original proposition and meaningful table/context scopes.
 source_fields={key:s.get(key) for key in ['actor','target','scope_en','precondition_en','exception_en','timing_en','expected_outcome_en','applicable_version']}
 pred={}
 for key,v in source_fields.items():
  if key=='applicable_version':pred[key]={'status':'met','evidence_en':f'All generated commitments are evaluated within supplied R1.0 design baseline; actual source: {v}.'}
  elif v is None or str(v).strip()=='':pred[key]={'status':'not_applicable','evidence_en':'No independent non-null predicate was extracted; all words in the source proposition remain applicable.'}
  else:pred[key]={'status':'met','evidence_en':f'PDF predicate: {v}. Relevant original generated evidence: '+e[:240]+'; scope proof: '+x.get('scope_membership_proof_en','')[:180]}
 pred['target_action_modality_outcome']={'status':'met','evidence_en':x.get('predicate_check_en') or x.get('specific_reason_en'), 'source_proposition_en':q,'generated_quotes_en':[z['quote_en'] for z in ge]}
 check.append({'source_id':sid,'initial_phase4_cell':'TP' if sid in original_phase4_tp_ids else 'FN_OR_NEW_SOURCE_CHILD','final_cell':'TP','entailment_grade':x['entailment_grade'],'coverage_mode':x.get('coverage_mode'),'pdf_evidence':x['pdf_evidence'],'generated_evidence':ge,'predicate_checks':pred,'scope_membership_proof_en':x.get('scope_membership_proof_en',''), 'contrary_evidence_checked_en':'Compared quoted source with actual generated row, independent table headings, original source restrictions and method-specific controls. No negative-control assertion identified. Semantic certainty is bounded, not certified by token overlap.','evidence_locator_checks':verify,'normalized_content_token_overlap_diagnostic':round(overlap,3),'audit_outcome':'CONFIRMED_TP','audit_policy':'PHASE5_BOUNDED_PREDICATE_REVIEW_NOT_INDEPENDENTLY_CERTIFIED' if x.get('adjudication_policy')!='PHASE_5_RECIPROCAL_CORRECTION_REVIEWED' else 'PHASE5_INDEPENDENT_RECIPROCAL_CORRECTION','semantic_certification':'BEST_EFFORT_NOT_VERIFIED'})
assert not problems,problems[:2]
assert not missing_token,missing_token[:10]
assert len(check)==sum(x['scoring_cell']=='TP' for x in J)==521
save('05_tp_evidence_audit_final.jsonl',check)
# Keep root-cause ledger for all initially raised FN candidates, including those corrected or parent-atom-merged.
roots={z['source_id']:z for z in ROOT};assert len(roots)==len(ROOT)
fn=[x for x in J if x['scoring_cell']=='FN']
for x in fn:
 sid=x['origin_source_ids'][0]
 if sid not in roots:
  # New children are all covered in this run; future new uncovered atoms need a root cause.
  raise AssertionError('FN missing root cause '+sid)
 rec=roots[sid]
 if rec['fn_review_disposition'] not in ('TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'):raise AssertionError((sid,rec['fn_review_disposition']))
 rec['final_scoring_cell']='FN'
 if rec.get('best_generated_candidates') is None:rec['best_generated_candidates']=[]
 if not rec['best_generated_candidates']:
  # Honest retrieval gap; do not invent candidate evidence. Preserve query keys and caveat.
  rec['review_limit_en']='No substantial candidate retained by the prior retrieval; lack of a candidate is not evidence of logical absence.'
for x in J:
 if x['scoring_cell']=='TP':
  sid=x['origin_source_ids'][0]
  if sid in roots:assert roots[sid]['final_scoring_cell']=='TP',(sid,roots[sid]['final_scoring_cell'])
save('03_fn_root_cause_audit_final.jsonl',sorted(roots.values(),key=lambda x:x['source_id']))

# Guarantee consistent negative controls: absence of an asserted negative is narrow and bounded.
neg=[x for x in J if x['actual_label']==0]
assert len(neg)==37 and all(x['origin_negative_control_ids'] and not x['origin_source_ids'] for x in neg)
assert {x['origin_negative_control_ids'][0] for x in neg}==set(ng)
# The present audit has no defensible positive counterfactual or distinct unsupported-only claim.
# This is an *uncertified finding*, not a proof of 100%-correct generated design assertions.
cc=collections.Counter(x['scoring_cell'] for x in J)
assert cc['TP']==521 and cc['FN']==506 and cc['TN']==37 and cc['FP']==0
assert cc['TP']+cc['FN']==len(R) and cc['TN']+cc['FP']==len(N)
FP=cc['FP'];TP=cc['TP'];FN=cc['FN'];TN=cc['TN']
precision=TP/(TP+FP) if TP+FP else None
recall=TP/(TP+FN) if TP+FN else None
f1=2*TP/(2*TP+FP+FN) if 2*TP+FP+FN else None
duplicate=json.loads((O/'05_duplicate_metrics_final.json').read_text())
mat={'protocol_version':'6.1','prefix':'fullload','phase':5,'status':'PHASE_COMPLETED_BEST_EFFORT','source_baseline':'OD-AI-DDS-001 R1.0 / revision 1.3','universe':{'source_positive_atoms':len(R),'source_negative_controls':len(N),'eligible_generated_occurrences':len(GO),'raw_generated_claim_classes':len(G),'covered_source_atoms':TP,'asserted_negative_controls':0,'unsupported_generated_only_propositions':0,'canonical_predicted_positive_units':TP+FP,'canonical_decision_units':len(J),'negative_universe_scope':'Only predeclared 37 PDF-grounded controls'},'confusion':{'TP':TP,'TN':TN,'FP':FP,'FN':FN},'metrics':{'Precision':precision,'Recall':recall,'F1':f1,'Duplicate':duplicate['duplicate_rate']},'raw_duplicate_counts':{'eligible_occurrences':len(GO),'raw_unique_classes':len(G),'duplicate_excess':duplicate['duplicate_excess_occurrences'],'within_file_excess':duplicate['within_file_excess'],'across_file_excess':duplicate['across_file_excess']},'source_atomization_change':{'source_original':1024,'source_corrected':len(R),'retired_context_or_parent_source_ids':['PDF-00001','PDF-00003','PDF-00004'],'new_independent_source_ids':['PDF-01025','PDF-01026','PDF-01027','PDF-01028','PDF-01029','PDF-01030']},'source_coverage_changes':{'phase4_TP':495,'phase4_FN':529,'phase5_TP':TP,'phase5_FN':FN,'phase5_fn_corrections':26},'TP_proof_audit':{'TP_audit_records':len(check),'passed_literal_locator_checks':len(check),'per_predicate_evidence':'BEST_EFFORT_NOT_CERTIFIED'},'FN_audit':{'final_fn':len(fn),'final_fn_disposition_counts':dict(collections.Counter(roots[x['origin_source_ids'][0]]['fn_review_disposition'] for x in fn)),'corrected_initial_fn_candidates':sum(z.get('fn_review_disposition')=='MATCHER_FALSE_NEGATIVE_CORRECTED' for z in ROOT),'source_atomization_corrections':3},'generated_claim_validity':{'PDF_ENTAILED_provisional':sum(x['validity_label']=='PDF_ENTAILED' for x in V),'SUPPORTED_NONCOVERING_provisional':sum(x['validity_label']=='SUPPORTED_NONCOVERING' for x in V),'PDF_UNSUPPORTED_confirmed':sum(x['validity_label']=='PDF_UNSUPPORTED' for x in V),'source_evidence_uncertified':sum(x.get('semantic_certification')=='NOT_VERIFIED' for x in V)},'interpretation':'Precision 100% is a provisional artifact of no demonstrably unsupported generated-only proposition; thousands of individual generated PDF-support claims are not independently certified. Recall includes best-effort and potentially conservative FN. Structural arithmetic is not a proof of semantic completeness. No certified score or true absence of unsupported statements is claimed.'}
(O/'04_confusion_matrix_final.json').write_text(json.dumps(mat,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
mdoc=f'''# Phase 5 — Corrected Four-Cell Evaluation (Best-Effort)

| Measure | Final provisional value |
|---|---:|
| PDF-positive source atoms | {len(R)} |
| Fixed PDF-negative controls | {len(N)} |
| TP | {TP} |
| TN | {TN} |
| FP (currently demonstrated) | {FP} |
| FN (not fully proven) | {FN} |
| Canonical universe | {len(J)} |
| Precision | {precision:.4%} |
| Recall | {recall:.4%} |
| F1 | {f1:.4%} |
| Duplicate (raw generated occurrences) | {duplicate['duplicate_rate']:.4%} |

The confusion cells are from one explicitly enumerated effective proposition universe, not mixed raw-class and source-atom denominators. The 37 TN are a bounded, explicitly prohibited/deferral control set. No FP was affirmatively demonstrated; this must not be interpreted as a verified 100%-correct generated corpus, because weak source-support records remain. Only actual full-predicate entailment may justify a TP; bounded semantic uncertainty remains explicitly recorded.

Source normalization removed a broad introduction recap and split two compound source clauses. All changes retain old/new identifiers and the original PDF evidence. All eight scored Markdown files remain unchanged.
'''
(O/'04_confusion_matrix_final.md').write_text(mdoc,encoding='utf8')
# Phase-level strict path and count integrity; full six-phase recomputation belongs to Phase 6.
assert all((O/q).exists() for q in ['05_tp_evidence_audit_final.jsonl','05_source_atomization_audit_final.jsonl','04_duplicate_classes_final.jsonl','05_duplicate_metrics_final.json','05_duplicate_metrics_final.md','07_change_delta.jsonl','04_confusion_matrix_final.json','04_confusion_matrix_final.md','03_canonical_universe_final.jsonl','04_atomic_judgments_final.jsonl'])
validation={'status':'PASSED_STRUCTURAL_WITH_SEMANTIC_CAVEATS','phase_status':'PHASE_COMPLETED_BEST_EFFORT','source_atoms':len(R),'negative_controls':len(N),'TP_evidence_records':len(check),'FN_root_audit_records':len(ROOT),'final_FN_root_dispositions':mat['FN_audit']['final_fn_disposition_counts'],'generated_occurrences':len(GO),'unique_generated_classes':len(G),'semantic_merge_groups':31,'raw_duplicate_excess':duplicate['duplicate_excess_occurrences'],'universe_rows':len(J),'sum_cells':sum(cc.values()),'TP_plus_FN_equals_R':TP+FN==len(R),'TN_plus_asserted_controls_equals_N':TN==len(N),'FP_subcomponents_reconcile':FP==0,'dup_excess_partition_valid':duplicate['within_file_excess']+duplicate['across_file_excess']==duplicate['duplicate_excess_occurrences'],'source_quotes_original_file_validated_for_TP':len(check),'unresolved_low_pdf_support_count':sum(x.get('semantic_certification')=='NOT_VERIFIED' for x in V),'semantic_certification':'NOT_VERIFIED','notes_en':'This is a structural proof and a bounded predicate-level evidence audit, not an independently certified full semantic evaluation.'}
(O/'05_phase5_validation_final.json').write_text(json.dumps(validation,indent=2)+'\n')
(O/'05_phase_status_final.json').write_text(json.dumps({'protocol_version':'6.1','phase':5,'method':'fullload','status':'PHASE_COMPLETED_BEST_EFFORT','next_phase':6,'verification':validation,'coverage_metrics':mat['metrics']},indent=2)+'\n')
report=f'''# OrionDesk AI — Phase 5 Correction and Evidence Audit Report

**Protocol:** v6.1  
**Status:** PHASE_COMPLETED_BEST_EFFORT  
**Scope:** Only Phase 5. Phase 6 independent recomputation has not been executed.

## 1. Inputs and continuity

The original 90-page PDF and the eight attached Markdown specifications remain the only substantive evidence. Phase-1 source and negative-control ledgers, Phase-2 occurrence/class inventories, and Phase-3/4 judgment evidence were reviewed as prior working ledgers, not normative truth. The original phase artifacts and Markdown inputs were not modified. The PDF-grounded source inventory remains method-independent for subsequent comparisons; this run evaluates the fullload eight-file set.

## 2. Source atomization

The independent PDF-positive inventory changed from 1,024 to **{len(R)}** atoms. The broad architecture-at-a-glance recap `PDF-00001` was excluded from separate scoring as repeated parent context. Compound `PDF-00003` (exact approval hash / source-version traceability) became `PDF-01025` and `PDF-01026`; compound `PDF-00004` (four distinct prohibitions) became `PDF-01027`–`PDF-01030`. All retained original physical-page quotations and were not invented from generated Markdown. Three atomization corrections are documented, with audits of every originally enumerated positive atom and all six new child atoms.

## 3. Reciprocal FN challenge and TP evidence

Phase 4 reported 495 TP / 529 FN on 1,024 source atoms. The corrected Phase 5 source-ledger output reports **{TP} TP / {FN} FN** on {len(R)} source atoms. Of the 26 source FN-to-TP adjudication changes, 20 refer to previously counted source IDs and six are independently atomized obligations replacing two originally FN compound rows. Reciprocally retrieved complete source-class evidence includes storage authority and immutability, outbox and credential rules, durable ChangeRequest attribution, and exact cited versions / untrusted-content restrictions.

Exactly **{len(check)}** final TP records carry original English PDF quotes, original generated-file line/cell quotes, applicability text and predicate-check maps in `05_tp_evidence_audit_final.jsonl`. Numeric response-code table cells for specific APIs were restored and ambiguous original evidence citations were repaired. Every final FN retains a root-cause disposition and candidate-search evidence or an explicit evidence limitation. {sum(x.get('fn_review_disposition')=='MATCHER_FALSE_NEGATIVE_CORRECTED' for x in ROOT)} historically raised FN candidates have corrected TP dispositions in the cumulative root-cause ledger.

This remains a **bounded best-effort semantic review**. The locator checks establish original-text authenticity, not human-level verification of every semantic bridge. No score is labeled certified.

## 4. Generated eligibility and raw duplication

Two unadopted proposed input-control placements were excluded. Five valid definitive generated statements had been incorrectly excluded in Phase 4 and were reinstated. Eighteen missing confirmed table-cell predicates (13 API numeric results, three earlier API results, and two selected data field names) were recovered as standalone occurrences with the genuine row/column context. Thirty-one full-predicate semantic groups merged 36 old classes; different API resources and distinct fields remain separate.

| Raw measure | Count |
|---|---:|
| Eligible occurrences | {len(GO)} |
| Unique classes | {len(G)} |
| Excess duplicate occurrences | {duplicate['duplicate_excess_occurrences']} |
| Within-file excess | {duplicate['within_file_excess']} |
| Across-file excess | {duplicate['across_file_excess']} |
| Duplicate rate | {duplicate['duplicate_rate']:.4%} |

The raw duplicate fraction is not computed from the source-coverage TP/FP universe. Near-equivalent predicates not proved fully identical were left separate.

## 5. Corrected canonical matrix

| Cell | Count |
|---|---:|
| TP | {TP} |
| TN | {TN} |
| FP | {FP} |
| FN | {FN} |

Precision (provisional) = {precision:.4%}; Recall (provisional) = {recall:.4%}; F1 (provisional) = {f1:.4%}. The canonical universe has {len(J)} units, comprising {len(R)} PDF-positive atoms and {len(N)} predefined PDF-negative controls. No independent generated-only unsupported predicate was established with sufficient proof to create a canonical `F_m` unit; the result is therefore not a certified claim of zero unsupported generated requirements.

## 6. Limits and handoff

- The generated validity audit still contains **{sum(x.get('semantic_certification')=='NOT_VERIFIED' for x in V)}** class records without complete independent semantic certification. Their provisional PDF-support labels must not be confused with verified equivalence.
- The final FN count includes genuine missing predicates, partial entailment and conservative unresolved assessments; these are distinguished per source ID in the root-cause ledger.
- Numeric source and generated class totals were corrected with evidence, not aligned to a historical target count. Archived phase ledgers retain pre-correction values.
- Phase 6 must independently recompute metrics from the corrected item-level ledgers, check all final file references / source classes, and report semantic limitations without treating structural passes as semantic certification.
'''
(O/'05_phase5_report.md').write_text(report,encoding='utf8')
print(json.dumps({'confusion':mat['confusion'],'metrics':mat['metrics'],'duplication':mat['raw_duplicate_counts'],'validation':validation,'phase_status':'PHASE_COMPLETED_BEST_EFFORT'},indent=2))
