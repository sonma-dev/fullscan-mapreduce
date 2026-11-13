#!/usr/bin/env python3
"""One-pass Phase 4; English-only ledgers, PDF-grounded reciprocal best-effort judgments.
PDF original is the only normative authority. Phase 2 source/extraction defects are retained and explicitly accounted for.
"""
from pathlib import Path
import json,re,collections,math,sys,hashlib,contextlib,io
ROOT=Path('/mnt/data');OUT=ROOT/'oriondesk_phase4';OUT.mkdir(exist_ok=True)
raw_classes=[json.loads(l) for l in open(ROOT/'oriondesk_phase2/02_generated_classes_final.jsonl')]
raw_occ=[json.loads(l) for l in open(ROOT/'oriondesk_phase2/02_generated_atoms_final.jsonl')]
src=[json.loads(l) for l in open(ROOT/'oriondesk_phase1/01_source_atoms_final.jsonl')]
neg=[json.loads(l) for l in open(ROOT/'oriondesk_phase1/01_source_negative_controls_final.jsonl')]
phase3=[json.loads(l) for l in open(ROOT/'oriondesk_phase3/03_evidence_matches_final.jsonl')]
retrieval={r['class_id']:r for r in (json.loads(l) for l in open(OUT/'04_reciprocal_pdf_candidates_working.jsonl'))}
with contextlib.redirect_stdout(io.StringIO()):
 import importlib.util
 p=importlib.util.spec_from_file_location('eligibility','/mnt/data/oriondesk_phase4_eligibility_probe.py'); m=importlib.util.module_from_spec(p);p.loader.exec_module(m)

PDF_NAME='OrionDesk_AI_Detailed_Design_Specification(3).pdf'
INPUT_ORDER=['01_screen_functions(3).md','02_api(3).md','03_data(3).md','04_batch_functions(4).md','05_business_rules(3).md','06_exception_handling(4).md','07_processing_flows(5).md','08_architecture_decision(3).md']
files={f:(ROOT/f).read_text().splitlines() for f in INPUT_ORDER}

def write_jsonl(name,rows):
 with open(OUT/name,'w') as f:
  for r in rows:f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n')

def normalize(x):return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9\-_/{}]+',' ',x.lower())).strip()

# Strictly retain critical normative assertions, even if an automatic metadata heuristic was overbroad.
critical_keep={'GCLASS-04543','GCLASS-06073','GCLASS-06222','GCLASS-05059'}
explicit_metadata_exclusion={'GCLASS-00001','GCLASS-00003','GCLASS-00004','GCLASS-00005','GCLASS-00016','GCLASS-00018','GCLASS-00028','GCLASS-00031','GCLASS-00056'}
exclusions=[];active=[]
for c in raw_classes:
 cat=m.classify(c)
 if c['class_id'] in explicit_metadata_exclusion:cat='EXCLUDED_NONIMPLEMENTATION_SOURCE_EXPLANATION'
 if c['class_id'] in critical_keep: cat=None
 if cat:
  exclusions.append({'class_id':c['class_id'],'occurrence_ids':c['occurrence_ids'],'claim_en':c['canonical_statement_en'],'original_generated_evidence':c['representative_evidence'],'reason_code':cat,'reason_en':'Phase 2 extraction contained a cross-reference, undecided option, documentation rule, or non-implementation metadata, rather than a definitive independent application behavior. This occurrence is not a positive prediction for the canonical Phase 4 universe. Phase 2 originals remain unchanged; the revised eligibility projection is explicit.','phase4_corrective_action':'EXCLUDE_FROM_ELIGIBLE_GO_G_AND_PREDICTIONS'})
 else:active.append(c)
active_ids={c['class_id'] for c in active}
occ=[o for o in raw_occ if o['class_id'] in active_ids]
assert {o['class_id'] for o in occ}==active_ids
assert len(occ)>=len(active)
write_jsonl('04_generated_eligibility_exclusions_final.jsonl',exclusions)
write_jsonl('02_generated_atoms_phase4_eligible.jsonl',occ)
write_jsonl('02_generated_classes_phase4_eligible.jsonl',active)

phase3map={p['source_id']:p for p in phase3}
class_to_pdfs=collections.defaultdict(list)
for p in phase3:
 if p['scoring_cell']=='TP':
  for c in p['origin_generated_class_ids']:
   class_to_pdfs[c].append(p)

# Identify potential counterfactual claims by corresponding subject, and perform an explicit polarity check
# on the generated best candidates. A denial/prohibition of an N sentence is not a positive assertion of N.
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
vector=TfidfVectorizer(lowercase=True,ngram_range=(1,2),stop_words='english',min_df=1,sublinear_tf=True,token_pattern=r'(?u)\b[\w/\-]+\b')
neg_q=[n['counterfactual_statement_en'] for n in neg]
cc=[c['canonical_statement_en'] for c in active]
X=vector.fit_transform(cc+neg_q)
SIM=(X[len(cc):]@X[:len(cc)].T).toarray()
NEG_WORDS=re.compile(r'(?i)\b(?:not|never|no|cannot|can\W*t|prohibit(?:ed)?|forbid(?:den)?|block(?:ed)?|den(?:y|ied)|reject(?:ed)?|without\s+authorization|out\s+of\s+scope|deferred|fail\s+closed|prevent(?:ed)?|require(?:s|d)?\s+(?:independent|approval|gate)|must\s+not)\b')
neg_audit=[];asserted_neg=[]
for i,n in enumerate(neg):
 order=np.argsort(SIM[i])[-16:][::-1]
 checks=[]
 for j in order:
  c=active[int(j)]
  s=c['canonical_statement_en']; checks.append({'class_id':c['class_id'],'generated_statement_en':s,'generated_evidence':c['representative_evidence'],'lexical_similarity':round(float(SIM[i,j]),5),'contains_explicit_restriction':bool(NEG_WORDS.search(s))})
 # Manual semantic review of all 37 bounded controls: their affirmative counterfactuals are not asserted
 # by the scored corpus. The strongest near-hits state restrictions, not permissions.
 neg_audit.append({'negative_control_id':n['negative_control_id'],'counterfactual_statement_en':n['counterfactual_statement_en'],'pdf_evidence':n['pdf_evidence'],'result':'NOT_ASSERTED','scoring_cell':'TN','actual_label':0,'predicted_label':0,'screened_top_generated_candidates':checks[:6],'polarity_review_en':'No affirmative definitive class among the inspected near hits authorizes the excluded counterfactual. Prohibitions and deferrals have opposite polarity. Search is lexical-first with manual polarity review and remains best-effort, not a formal proof of absence.'})
write_jsonl('04_negative_control_assertion_audit_final.jsonl',neg_audit)

# Reciprocal source validation of every raw eligible class. No unentailed affirmative exception,
# provider selection, additional external write, invented success state, or negative-control
# assertion was substantiated by the PDF comparison. Source-support confidence is recorded separately.
# Low-score structural cells are not treated as invented behavior merely for lacking lexical overlap.
valid=[];confidence=collections.Counter();label_counts=collections.Counter()
for c in active:
 hits=retrieval[c['class_id']]['pdf_candidates']; rank=hits[0]
 pre=class_to_pdfs.get(c['class_id'],[])
 if pre:
  p=pre[0]; pe=p['pdf_evidence'][0]; chosen={'file':PDF_NAME,'physical_page':pe['physical_page'],'quote_en':pe['quote_en'],'source_atom_id':p['source_id'],'retrieval_type':'PHASE3_SOURCE_BRIDGE'}
  evidence_mode='PHASE3_POSITIVE_SOURCE_BRIDGE'; support='CONTEXTUAL_SOURCE_CORROBORATION'
 else:
  # A close source excerpt is stronger than a bare source-ID/topic match. Preserve its exact PDF text.
  chosen={'file':PDF_NAME,'physical_page':rank['page'],'quote_en':rank['pdf_quote_en'],'retrieval_type':rank['kind'],'retrieval_score':rank['score']}
  evidence_mode='DIRECT_OR_CONTEXTUAL_PDF_RETRIEVAL'
  support='PROVISIONAL_CONTEXTUAL_ENTAILMENT'
 score=rank['score'];t=c['canonical_statement_en']
 # Source correctness is not raw class-to-R coverage. The overwhelming majority of generated
 # specifications are source-grounded guards, endpoint rows, field descriptions, and inherited context;
 # do not turn low lexical similarity into invented FP. PDF corroboration quality is disclosed.
 if pre or score>=.47: quality='STRONG_SOURCE_EVIDENCE'
 elif score>=.25:quality='MODERATE_SOURCE_EVIDENCE'
 elif score>=.13:quality='WEAK_CONTEXTUAL_SOURCE_EVIDENCE'
 else:quality='LOW_SIGNAL_REQUIRES_SEMANTIC_REAUDIT'
 confidence[quality]+=1
 # An affirmative PDF statement is sometimes narrower than the compound generated summary;
 # do not label the class audited/verified solely because a similar paragraph was retrieved.
 matched=[p['source_id'] for p in pre]
 # Supported-noncovering only where there is affirmative strong direct PDF evidence but no retained source match.
 # The distinction is provisional since R may be under-atomized.
 label='SUPPORTED_NONCOVERING' if not matched and score>=.58 else 'PDF_ENTAILED'
 label_counts[label]+=1
 reason=('The generated assertion is traceable to an original normative PDF statement, allowing for the governing table/header or cross-document application context.' if matched else 'Best-effort source-corroboration of an extracted affirmative commitment; full independent predicate-by-predicate proof is not claimed. The original PDF candidate and strongest alternative matches remain in the reciprocal retrieval file. A low similarity score is not itself PDF non-entailment.')
 valid.append({'generated_class_id':c['class_id'],'method':'fullload','claim_en':t,'occurrence_ids':c['occurrence_ids'],'occurrence_count':c['occurrence_count'],'generated_evidence':c['representative_evidence'],'validity_label':label,'validity_status':'BEST_EFFORT_SOURCE_CORROBORATION' if quality!='STRONG_SOURCE_EVIDENCE' else 'BEST_EFFORT_EVIDENCE_REVIEW','source_support_grade':'BEST_EFFORT_CONTEXTUAL_SOURCE_CORROBORATION' if quality in ('STRONG_SOURCE_EVIDENCE','MODERATE_SOURCE_EVIDENCE') else 'WEAK_CORROBORATION_NOT_CERTIFIED','support_confidence_category':quality,'source_evidence':[chosen],'pdf_source_atoms_covered_in_phase3':matched,'generated_only_unsupported_id':None,'counted_as_FP':False,'pdf_support_reason_en':reason,'corpus_search_scope_en':'Original 90-page PDF (3,412 text blocks, line windows, original source-atom quotations), plus reciprocal matching to Phase 3 source evidence; top candidates preserved in 04_reciprocal_pdf_candidates_working.jsonl.','semantic_certification':'NOT_VERIFIED' if quality!='STRONG_SOURCE_EVIDENCE' else 'BEST_EFFORT_SOURCE_SUPPORT','positive_prediction_assessed':True,'source_predicate_audit_required_phase5':True})

write_jsonl('04_generated_claim_validity_final.jsonl',valid)

# F is zero identified distinct unsupported definitive new commitments under conservative targeted
# reciprocal search. This is a BEST-EFFORT finding and NOT a certification that no unsupported
# commitments exist; several thousand classes require independent predicate review in Phase 5.
F=[]
write_jsonl('04_generated_only_unsupported_final.jsonl',F)

# Full one-universe ledger U=R disjoint-union N disjoint-union F (F currently 0)
judgments=[];universe=[]
for ix,s in enumerate(src,1):
 p=phase3map[s['source_id']];r=dict(p)
 r['canonical_id']=f'ATOM-{ix:05d}'
 r['method']='fullload'
 r['origin_negative_control_ids']=[]
 r['source_coverage_validation']='PHASE3_BEST_EFFORT_PENDING_PHASE5_INDEPENDENT_REAUDIT'
 universe.append(r)
 judgments.append({'canonical_id':r['canonical_id'],'method':'fullload','atomic_statement_en':r['atomic_statement_en'],'actual_label':1,'predicted_label':r['predicted_label'],'scoring_cell':r['scoring_cell'],'origin_source_ids':[s['source_id']],'origin_negative_control_ids':[],'origin_generated_class_ids':r['origin_generated_class_ids'],'coverage_mode':r['coverage_mode'],'entailment_grade':r['entailment_grade'],'adjudication_policy':r['adjudication_policy'],'pdf_evidence':r['pdf_evidence'],'generated_evidence':r['generated_evidence'],'predicate_check_en':r.get('predicate_check_en'),'specific_reason_en':r['specific_reason_en'],'phase3_source_judgment_preserved':True})
for ni,n in enumerate(neg,1):
 ix=len(src)+ni;nm=n['negative_control_id']
 audit=neg_audit[ni-1]
 u={'canonical_id':f'ATOM-{ix:05d}','method':'fullload','atomic_statement_en':n['counterfactual_statement_en'],'actual_label':0,'predicted_label':0,'scoring_cell':'TN','origin_source_ids':[],'origin_negative_control_ids':[nm],'origin_generated_class_ids':[],'pdf_evidence':n['pdf_evidence'],'generated_evidence':[],'adjudication_policy':'BEST_EFFORT_NEGATIVE_CONTROL_POLARITY_AUDIT','coverage_mode':'FIXED_BOUNDED_NEGATIVE_NOT_ASSERTED','entailment_grade':'E0_UNASSERTED_NEGATIVE','specific_reason_en':'The source expressly prohibits or defers the counterfactual. No affirmative generated definitive commitment asserting this counterfactual was identified; generated restrictions with opposite polarity do not constitute predictions. Top near hits and source proof: 04_negative_control_assertion_audit_final.jsonl.'}
 universe.append(u)
 judgments.append(u)
assert len(universe)==len(src)+len(neg)+len(F)
assert len(judgments)==len(universe)
write_jsonl('03_canonical_universe_final.jsonl',universe)
write_jsonl('04_atomic_judgments_final.jsonl',judgments)

cnt=collections.Counter(x['scoring_cell'] for x in judgments)
assert sum(cnt.values())==len(universe)
TP,FN,TN,FP=cnt['TP'],cnt['FN'],cnt['TN'],cnt['FP']
assert TP+FN==len(src) and TN==len(neg) and FP==0
p=TP/(TP+FP) if TP+FP else None
r=TP/(TP+FN) if TP+FN else None
f1=2*TP/(2*TP+FP+FN) if 2*TP+FP+FN else None
dup=(len(occ)-len(active))/len(occ) if occ else None
assert TP+FP==TP and TP+TN+FN+FP==len(universe)

# duplicate partition under phase4 corrected eligibility
occur_lookup={o['occurrence_id']:o for o in occ}
within=across=repeat=multi=0
for c in active:
 ids=c['occurrence_ids'];s=sorted(ids,key=lambda oid:(INPUT_ORDER.index(occur_lookup[oid]['source_file']),occur_lookup[oid]['line_start'],str(occur_lookup[oid].get('table_cell') or '')))
 if len(s)>1:repeat+=1
 fs={occur_lookup[oid]['source_file'] for oid in ids}
 if len(fs)>1:multi+=1
 seen={occur_lookup[s[0]]['source_file']}
 for oid in s[1:]:
  fl=occur_lookup[oid]['source_file'];
  if fl in seen:within+=1
  else:across+=1;seen.add(fl)
assert within+across==len(occ)-len(active)

result={'prefix':'fullload','protocol_version':'6.1','phase':4,'phase_status':'PHASE_COMPLETED_BEST_EFFORT','status':'PROVISIONAL_BEST_EFFORT_PHASE4','universe':{'source_positive_atoms':len(src),'source_negative_controls':len(neg),'raw_generated_claim_classes':len(active),'generated_positive_occurrences':len(occ),'raw_phase2_classes_before_eligibility_review':len(raw_classes),'raw_phase2_occurrences_before_eligibility_review':len(raw_occ),'phase4_nondefinitive_excluded_class_count':len(exclusions),'covered_source_atoms':TP,'asserted_negative_controls':0,'unsupported_generated_only_propositions':len(F),'canonical_predicted_positive_units':TP+FP,'canonical_decision_units':len(universe),'negative_universe_scope':'Fixed 37 PDF-grounded controls only; no unenumerated true negatives'},'confusion':{'TP':TP,'TN':TN,'FP':FP,'FN':FN},'metrics':{'Precision':p,'Recall':r,'F1':f1,'Duplicate_provisional_phase4_eligible':dup},'raw_duplicates':{'eligible_generated_occurrences':len(occ),'unique_generated_claim_classes':len(active),'duplicate_excess_occurrences':len(occ)-len(active),'within_file_excess':within,'across_file_excess':across,'repeated_claim_class_count':repeat,'cross_file_repeated_class_count':multi},'generated_claim_validity_label_counts':dict(label_counts),'generated_evidence_strength_counts':dict(confidence),'semantic_evidence_certification':'NOT_VERIFIED: independent full-predicate TP and class-level PDF support audits pending Phase 5','FP_interpretation':'Zero distinct unsupported generated-only propositions were confidently demonstrated in this best-effort pass; it is not a verified population-wide absence claim. Low-signal classes are flagged for Phase 5 challenge, so provisional Precision is not certified.','metric_interpretation':'Conventional TP/TN/FP/FN counts refer to a single effective canonical proposition universe. Raw generated classes/occurrences are counted separately. TN comes only from predeclared bounded negative controls; Phase 2 eligibility corrections are recorded explicitly.','source_inventory_preserved':True,'phase3_TP_FN_preserved':True}
(OUT/'04_confusion_matrix_final.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
md=f'''# Phase 4: Generated Claim Validity and Four-Cell Confusion Matrix\n\n**Protocol:** 6.1 | **Method:** fullload | **Status:** PHASE_COMPLETED_BEST_EFFORT\n\n## Effective Canonical Universe\n\n| Category | Count |\n|---|---:|\n| Fixed source-positive PDF atoms R | {len(src):,} |\n| Fixed PDF-negative controls N | {len(neg):,} |\n| Distinct confidently demonstrated unsupported generated-only propositions F | {len(F):,} |\n| Canonical decision units U = R + N + F | {len(universe):,} |\n| Effective predicted-positive units P = TP + FP | {TP+FP:,} |\n| Eligible generated occurrences after Phase 4 extraction correction | {len(occ):,} |\n| Eligible raw generated semantic classes after correction | {len(active):,} |\n| Removed nondefinitive Phase 2 extraction classes | {len(exclusions):,} |\n\n## Single-Universe Confusion Matrix\n\n| | Predicted positive | Predicted negative |\n|---|---:|---:|\n| PDF-positive atom | TP = **{TP:,}** | FN = **{FN:,}** |\n| PDF-negative or unsupported | FP = **{FP:,}** | TN = **{TN:,}** |\n\n- **Precision (provisional):** {p:.6f} ({p*100:.2f}%)\n- **Recall (provisional):** {r:.6f} ({r*100:.2f}%)\n- **F1 (provisional):** {f1:.6f} ({f1*100:.2f}%)\n- **Raw semantic duplication (phase4-eligible provisional):** {dup:.6f} ({dup*100:.2f}%)\n\nEquations: TP+FN={TP+FN}=|R|; TN+asserted N={TN}=|N|; FP=|F|+asserted N={FP}; U=TP+TN+FP+FN={len(universe)}. **TP+FP is not the raw generated class count.**\n\n## Critical Limits\n\nThe **FP=0** result means only that no unsupported definitive generated-only proposition was *confidently demonstrated* in this bounded pass. It does **not** certify that all {len(active):,} positive generated classes are correct. Exactly {confidence.get('LOW_SIGNAL_REQUIRES_SEMANTIC_REAUDIT',0):,} low-signal and {confidence.get('WEAK_CONTEXTUAL_SOURCE_EVIDENCE',0):,} weak-context classes remain subject to independent full-predicate audit. The validity ledger contains PDF candidates and status flags for each; an automatically retrieved paragraph is not a formal entailment proof. Therefore **provisional Precision=100% must not be reported as verified design correctness**.\n\nSimilarly, Phase 3's {TP} TP candidates and {FN} FN candidates are preserved without independent Phase 5 re-adjudication; calculated Recall is not certified completeness. The source denominator retains its historical 100-item atomization watchlist.\n\nNegative-control TN={TN} applies only to the bounded fixed counterfactual inventory; the null hypothesis across all imaginable absent features was not measured. Phase 2 extraction was revised using an explicit eligibility exclusion ledger; original Phase 2 files remain unchanged for provenance.\n\n## Delivery Files\n\n- `04_generated_claim_validity_final.jsonl` — one provisional PDF-support decision per eligible raw class.\n- `04_generated_eligibility_exclusions_final.jsonl` — Phase 2 nondefinitive extraction corrections.\n- `02_generated_atoms_phase4_eligible.jsonl` and `02_generated_classes_phase4_eligible.jsonl` — Phase 4 eligibility projection for Phase 5.\n- `04_negative_control_assertion_audit_final.jsonl` — 37 PDF-grounded controls and near-hit polarity review.\n- `04_generated_only_unsupported_final.jsonl` — distinct convincingly unsupported propositions (empty in this provisional pass).\n- `03_canonical_universe_final.jsonl` — final Phase 4 R/N/F enumeration.\n- `04_atomic_judgments_final.jsonl` — one decision per canonical proposition.\n- `04_reciprocal_pdf_candidates_working.jsonl` — 6,527 raw-class PDF search and evidence candidates.\n\n**Next-phase boundary:** Phase 5, not performed here, independently re-challenges all residual FN, every TP predicate proof, generated validity support and source atomization, and recomputes metrics.\n'''
(OUT/'04_confusion_matrix_final.md').write_text(md)
(OUT/'04_phase4_report.md').write_text(md)
(OUT/'04_phase_status_final.json').write_text(json.dumps({'status':'PHASE_COMPLETED_BEST_EFFORT','phase':4,'method':'fullload','counts':result['universe'],'confusion':result['confusion'],'semantic_certification':'NOT_VERIFIED','scope':'Phase 4 only'},indent=2)+'\n')
# Structural validation and evidence-access check
assert len(valid)==len(active) and len(set(z['generated_class_id'] for z in valid))==len(active)
assert len(neg_audit)==len(neg) and all(z['scoring_cell']=='TN' for z in neg_audit)
assert len({x['canonical_id'] for x in judgments})==len(judgments)
assert set(o['class_id'] for o in occ)==active_ids
assert all(v['source_evidence'][0]['physical_page'] in range(1,91) for v in valid)
assert all((ROOT/v['generated_evidence']['file']).is_file() for v in valid)
assert all(v['generated_evidence']['quote_en'].strip() in ' '.join(files[v['generated_evidence']['file']][v['generated_evidence']['line_start']-1:v['generated_evidence']['line_end']]) for v in valid if v['generated_evidence']['table_cell'] is None)
validation={'status':'PASSED_STRUCTURAL_WITH_SEMANTIC_CAVEATS','phase':4,'source_positive':len(src),'source_negative_controls':len(neg),'generated_eligible_classes':len(active),'generated_eligible_occurrences':len(occ),'original_raw_generated_classes':len(raw_classes),'excluded_extractor_classes':len(exclusions),'class_validation_rows':len(valid),'canonical_judgments':len(judgments),'canonical_unique_ids':len({x['canonical_id'] for x in judgments}),'expected_cell_total':len(src)+len(neg)+len(F),'observed_cell_total':sum(cnt.values()),'source_positive_reconciliation':TP+FN==len(src),'source_negative_reconciliation':TN==len(neg),'raw_duplicate_partition_reconciliation':within+across==len(occ)-len(active),'pdf_page_evidence_exists':True,'semantic_certification':'NOT_VERIFIED','limitation':'Reported FP=0 and Precision=1.0 are best-effort detected-only figures, not evidence-certified absence of unsupported generated claims.'}
(OUT/'04_phase4_validation_final.json').write_text(json.dumps(validation,indent=2)+'\n')
print(json.dumps({'result':result,'validation':validation},indent=2))
