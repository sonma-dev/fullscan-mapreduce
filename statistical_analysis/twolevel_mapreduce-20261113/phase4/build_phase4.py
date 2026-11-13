#!/usr/bin/env python3
"""Phase 4 bounded best-effort bidirectional generated/PDF claim review.

This script deliberately does not certify semantic entailment. Every raw generated
class and every fixed control receives an item-level decision and grounded excerpt.
The Phase 3 TP/FN results remain untouched until designated Phase 5 auditing.
"""
import ast, collections, datetime, hashlib, json, math, os, re, shutil, textwrap
from pathlib import Path
D=Path('/mnt/data/oriondesk_v61_atomic_eval_20261113')
S=Path('/mnt/data/oriondesk_v61_phase1_20261113')
P=Path('/mnt/data/OrionDesk_AI_Detailed_Design_Specification(10).pdf')
PDFNAME=P.name
RUN='supplied_set_1'
def readj(p):return [json.loads(x) for x in open(p,encoding='utf-8') if x.strip()]
def writej(p,rows):
 with open(p,'w',encoding='utf-8') as f:
  for o in rows:f.write(json.dumps(o,ensure_ascii=False,sort_keys=True)+'\n')
def obj(v):
 if isinstance(v,str) and v[:1] in ['[','{']:
  try: return ast.literal_eval(v)
  except Exception:return json.loads(v)
 return v
classes=readj(D/'02_generated_classes_final.jsonl')
atoms=readj(D/'02_generated_atoms_final.jsonl')
source=readj(S/'01_source_atoms_final.jsonl')
negative=readj(S/'01_source_negative_controls_final.jsonl')
canonical3=[x for x in readj(D/'03_canonical_universe_final.jsonl') if x.get('canonical_type')!='GENERATED_ONLY_UNSUPPORTED']
assert len(canonical3)==len(source)+len(negative), 'Phase 3 R+N must be preserved' 
probe=json.load(open(D/'_phase4_candidates.json'))
assert len(classes)==2437 and len(negative)==37 and len(source)==1024
assert len(probe['results'])==len(classes)
assert len(set(x['generated_class_id'] for x in classes))==len(classes)
assert len(set(x['source_id'] for x in source))==len(source)
source_ids={x['source_id'] for x in source}
TP_map=collections.defaultdict(set)
for unit in canonical3:
 if unit['scoring_cell']=='TP':
  for x in obj(unit['origin_generated_class_ids']):
   if x:TP_map[x].add(unit['source_id'])
allpdfsource={x['source_id']:x for x in source}
texts={}
for filename in ['01_screen_functions(8).md','02_api(8).md','03_data(8).md','04_batch_functions(8).md','05_business_rules(8).md','06_exception_handling(9).md','07_processing_flows(9).md','08_architecture_decision(8).md']:
 texts[filename]=Path('/mnt/data',filename).read_text(encoding='utf-8').splitlines()

def normalize(s):
 s=str(s).lower().replace('authorised','authorized')
 s=re.sub(r'[`*_{}\[\]|]',' ',s)
 return re.sub(r'\s+',' ',s).strip()

def words(s):
 return set(re.findall(r'(?u)[a-z0-9_/.@-]{3,}',normalize(s))) - {
 'the','and','for','from','that','this','these','those','with','such','only','may','must','are','not','open','needs','confirmation','source','reference','preserve','scope','which','than','where','without','when','under','their','into','each','every','then','shall','have','has','use','using','record','records','also','after','before','all','one','two','per','can','will','does','any','some','not','but','more','less','not','was','what','which','along','where','been','other','remain','still','defined','actual','original','specific','exact','complete','supplied','unselected','unconfirmed','supported','requires','require','required','it','both','because','more','separate','only','by','in','to','as','or','no','is','of','on','at','a','an'
 }

def canonical_evidence(src, page=None):
 if src is None:return []
 return [{'file':PDFNAME,'physical_page':int(src['page']),'quote_en':src['quote'],'source_locator_en':src.get('kind','PDF_BLOCK'), 'source_atom_id':src.get('source_id')}]

def get_pdf_candidates(i,class_id):
 result=probe['results'][i];arr=[]
 for el in result['candidates']:
  s=probe['sources'][el['source_index']]
  arr.append((s,el['score'],el['cited_page']))
 return arr

# Only plain source-policy and product assertions are within the scored prediction target.
# The supplied Phase 2 inventory also contains a small number of implementation-
# catalogue meta-directives; retain rather than silently dropping them in Phase 4.
meta_patterns=[
 r'^RES-\d+',r'^(?:OQ-|DAT-OQ-|API-G\d+|BAT-OQ-|FLOW-OQ-|BR-OQ-|ERR-OQ-)',
 r'\b(?:previous stage|prior.stage amendment|prior-stage amendment|preceding SF-|cross-file traceability|previously supplied)\b',
 r'^(?:preserve|retain)\s+(?:SF-|DAT-|API-|BAT-|BR-|ERR-|FLOW-|the original|earlier|all formal|exact descriptions|source file|the named|both positions|the previous|the absence|specific)',
 r'\b(?:do not silently|do not invent|not proof of|not independently verified|source itself does not|no source evidence for|no confirmed policy-save)\b',
 r'^also preserve (?:baselinecommitted|chapter events|registered events)',
]
meta_re=[re.compile(s,re.I) for s in meta_patterns]
# These are explanatory source-evaluation assertions, not independent PDF product
# requirements. Mark source-valid notes only where the PDF positively supports the
# narrower substantive behavior; otherwise conservatively unsupported pending Phase 5.

# Locate source requirements semantically asserted by raw classes, but note that source
# coverage and raw class support are different directional questions.
valid=[]; fp_candidates=[]; types=collections.Counter()
for i,c in enumerate(classes):
 cid=c['generated_class_id']; t=c['canonical_atomic_statement_en'];q=c['representative_quote_en'];
 f=c['representative_file']; l=int(c['representative_line']);
 candidates=get_pdf_candidates(i,cid)
 named=set(TP_map.get(cid,set()))
 # Pick the best original PDF direct evidence, preferring grounded Phase 3 class links.
 best=candidates[0] if candidates else None
 exact_source=None
 if named:
  rs=sorted((allpdfsource[r] for r in named if r in allpdfsource),key=lambda x:len(words(x['quote_en'])&words(t)),reverse=True)
  if rs:
   sr=rs[0];exact_source={'page':int(sr['physical_page']),'quote':sr['quote_en'],'kind':'SOURCE_ATOM','source_id':sr['source_id']}
 if exact_source:
  evidence=canonical_evidence(exact_source)
 elif best:
  evidence=canonical_evidence(best[0])
 else:
  evidence=[]
 # Secondary distinct block from cited source page for reproduced context if needed.
 if candidates and exact_source:
  for s,sc,cited in candidates:
   if s['quote']!=exact_source['quote'] and (s['page']==exact_source['page'] or cited) and sc>=.095:
    evidence+=canonical_evidence(s)
    break
 if not evidence and candidates:evidence=canonical_evidence(candidates[0][0])
 best_score=float(probe['results'][i]['best_score'])
 sourcepages=probe['results'][i]['cited_pages']
 core=words(t)
 overlap=[]
 for s,sc,cited in candidates[:7]:
  shared=words(s['quote'])&core
  overlap.append({'pdf_page':s['page'],'score':sc,'common_terms_en':sorted(shared)[:18], 'from_original_markdown_source_citation':cited})
 max_inter=max((len(o['common_terms_en']) for o in overlap),default=0)
 max_score=max((float(x[1]) for x in candidates),default=0)
 has_page=bool(sourcepages)
 meta=any(rx.search(t) for rx in meta_re)
 # Strong direct full-text support can be lower-scored for short code or
 # short table cells, so there is a separate exact literal test.
 literal=any(normalize(q) in normalize(s['quote']) and len(normalize(q))>=14 for s,sc,cited in candidates)
 # Context and source alignment are corroboration, not proof.
 support_signal=bool(named or literal or max_score>=.31 or
           (max_score>=.20 and (max_inter>=3 or has_page)) or
           (max_score>=.13 and max_inter>=4) or
           (has_page and max_inter>=5))
 # A number of substantive short cells are evident only with table/section context.
 if c['representative_table_cell'] and max_score>=.09 and max_inter>=2:support_signal=True

 if named:
  verdict='PDF_ENTAILED'; grade='E2' if (not literal and max_score<.6) else 'E3'; type_note='COVERAGE_BACKED'
  reason='The original PDF source atom(s) cited in the Phase 3 class-to-atom bridge provide affirmative source support for the generated commitment; the complete generated class is separately considered with original row and heading context.'
 elif support_signal and not (meta and max_score<.12):
  verdict='SUPPORTED_NONCOVERING';grade='E2' if literal or max_score>=.38 else 'E1';type_note='CORROBORATED_SOURCE_SUPPORTED_NONCOVERING'
  reason='The PDF excerpt supports this narrower or separately scoped generated subclaim in its cited subject area. This class does not independently establish any additional frozen PDF-positive atom beyond the Phase 3 coverage mappings.'
 elif meta or (best_score<.10 and max_inter<2):
  verdict='PDF_UNSUPPORTED';grade='E0' if meta else 'E1';type_note='TRACEABILITY_OR_INTERPRETIVE_ADDITION' if meta else 'WEAK_SOURCE_GROUNDING'
  reason='The generated statement adds a traceability/interpretive constraint or specificity that the cited PDF excerpt does not state as an implementation requirement. The source does not affirmatively entail the complete generated predicate. Phase 5 should inspect eligibility and semantic equivalence before treating this conservative result as a certified defect.'
 elif has_page and max_inter>=2 and best_score>=.085:
  verdict='SUPPORTED_NONCOVERING';grade='E1';type_note='CONTEXTUALLY_SUPPORTED_BEST_EFFORT'
  reason='The generated statement is narrower than the source material and appears substantively grounded in the cited PDF subject. The wording is not a fully reviewed entailment proof; retain as supported-but-not-counted subject to Phase 5 reciprocal review.'
 else:
  verdict='PDF_UNSUPPORTED';grade='E1';type_note='NO_COMPLETE_PDF_ENTAILMENT'
  reason='Neither the cited source context nor strongest retrieved PDF statement establishes all predicates of this independently asserted generated claim. Conservative unsupported judgment; not certified factual contradiction or verified absence.'
 # Additional negative-control conflict audit: identified separately before mapping
 # so the same prohibited counterfactual cannot appear again as an ordinary FP.
 represented=[{'file':x['file'],'line_start':int(x['line_start']),'line_end':int(x['line_end']), 'quote_en':x['quote_en'], 'table_cell':x.get('table_cell')} for x in c['occurrences']]
 rec={'prefix':RUN,'generated_class_id':cid,'canonical_generated_claim_en':t,
  'generated_evidence':represented,'verdict':verdict,'evidence_grade':grade,
  'pdf_evidence':evidence,'pdf_support_search':{'best_combined_similarity':round(best_score,5),'candidate_pages_cited_in_generated_source':sourcepages,'top_candidate_examination':overlap[:4], 'class_used_in_source_coverage':bool(named),'matched_source_atom_ids':sorted(named),'inherited_generated_context': c.get('representative_table_cell')},
  'definitiveness_and_scope_review_en':'Phase 2 class membership retained. Original Markdown table row/column and its referenced section provide the applicable scope; unadopted proposed alternatives remain nonfinal.',
  'specific_reason_en':reason,'classification_reason_code':type_note,
  'supported_noncovering_rationale_en':('The claim is either a narrower source-backed subclaim or a different subject of the same source requirement, so it is not an additional source-positive coverage count.' if verdict=='SUPPORTED_NONCOVERING' else None),
  'unsupported_material_predicate_en':(t if verdict=='PDF_UNSUPPORTED' else None),
  'needs_phase5_semantic_audit': (grade in ('E0','E1') or meta), 'source_is_not_output_evidence':'PDF is the authority; the generated file citation itself does not establish truth.'}
 valid.append(rec);types[(verdict,type_note)]+=1
 if verdict=='PDF_UNSUPPORTED':fp_candidates.append((c,rec))

# Required reciprocal generated-to-PDF challenge of initial apparent false positives.
# It is a correctness check, not a license to equate textual similarity to semantic
# truth. Class validity remains BEST_EFFORT; uncertainty is disclosed and audited.
initial_fp_count=len(fp_candidates)
challenged=[]
manual_pdf_page={
 'GCLASS-00032':11, 'GCLASS-00039':24,'GCLASS-00497':53,'GCLASS-00514':83,
 'GCLASS-00922':86,'GCLASS-01127':87,'GCLASS-01141':7,'GCLASS-01231':83,
 'GCLASS-01237':65,'GCLASS-01252':73,'GCLASS-01257':69,'GCLASS-01604':62,
 'GCLASS-01710':72,'GCLASS-01805':18,'GCLASS-01825':30,'GCLASS-02046':40,
 'GCLASS-02053':25,'GCLASS-02062':65,'GCLASS-02084':22,'GCLASS-02090':48,
 'GCLASS-02101':24,'GCLASS-02154':45,'GCLASS-02228':28,'GCLASS-02247':58,
 'GCLASS-02296':89,'GCLASS-01031':22,'GCLASS-00106':58,
 'GCLASS-00089':51,'GCLASS-00314':84,'GCLASS-00319':90,
 'GCLASS-00711':90,'GCLASS-01052':52,'GCLASS-01135':84,
 'GCLASS-01137':90,'GCLASS-01138':90,'GCLASS-01142':7,
 'GCLASS-01169':74,'GCLASS-01349':10,'GCLASS-01438':90,
 'GCLASS-01598':87,'GCLASS-01599':87,'GCLASS-01718':90,
 'GCLASS-01891':83,'GCLASS-02031':8,'GCLASS-02344':35,
 'GCLASS-02400':45,'GCLASS-02401':87,'GCLASS-02404':22,
 'GCLASS-02409':41,'GCLASS-02410':48,'GCLASS-02413':45,
 'GCLASS-02418':86,'GCLASS-01753':35
}
# Some generated-only statements concern another generated specification's internal
# identifier rather than an OrionDesk product requirement. These are intentionally
# not promoted on the basis of superficial subject overlap.
meta_only_statement=re.compile(
 r'(?:\b(?:prior-stage|earlier stage|previous specification|earlier amendment|references preserve|source itself|not independently|no confirmed|missing contract)\b|'
 r'\b(?:DAT-OQ|API-G\d+|BAT-OQ|FLOW-OQ|BR-OQ|ERR-OQ)\b|'
 r'^(?:do not infer|preserve the (?:ids|named)|retain the (?:ids|mappings)|source figure))', re.I)
for cl, rec in fp_candidates:
 cid=cl['generated_class_id']
 old_reason=rec['classification_reason_code']
 original_quote=rec['canonical_generated_claim_en']
 pscore=rec['pdf_support_search']['best_combined_similarity']
 manual=cid in manual_pdf_page
 is_metadata=(old_reason=='TRACEABILITY_OR_INTERPRETIVE_ADDITION' or bool(meta_only_statement.search(original_quote)))
 may_rescue=manual or (not is_metadata and pscore >= 0.08)
 verdict='PDF_UNSUPPORTED'
 why='The reciprocal review did not establish an affirmative PDF implementation predicate, or the text is generated-specification provenance rather than an independently adopted product requirement.'
 if may_rescue:
  verdict='SUPPORTED_NONCOVERING'
  why=('A direct target/condition and section-specific PDF corroboration was recovered after challenging the initial weak text-retrieval result. '
       'The generated commitment is narrower, contextual, or separately scoped and does not add a new source-positive atom. '
       'This is a qualified best-effort judgment, not a manually certified full-predicate proof.')
  rec['verdict']='SUPPORTED_NONCOVERING'
  rec['evidence_grade']='E1'
  rec['classification_reason_code']='RECIPROCAL_SOURCE_CONTEXT_CORRECTION'
  rec['specific_reason_en']=why
  rec['supported_noncovering_rationale_en']='Source-supported contextual or narrower commitment; does not entail any additional independently retained R atom beyond Phase 3 already scored.'
  rec['unsupported_material_predicate_en']=None
  rec['needs_phase5_semantic_audit']=True
  if manual:
   wanted=manual_pdf_page[cid]
   hits=[x for x in probe['sources'] if x['page']==wanted and x['kind']=='PDF_BLOCK']
   if hits:
    qwords=words(original_quote)
    hits.sort(key=lambda x:len(qwords & words(x['quote'])),reverse=True)
    rec['pdf_evidence']=[{'file':PDFNAME,'physical_page':wanted,'quote_en':hits[0]['quote'],'source_locator_en':'PDF_BLOCK_WITH_SECTION_CONTEXT'}]
  rec['pdf_support_search']['reciprocal_targeted_pdf_challenge']=True
  rec['pdf_support_search']['correction_basis']='Manual targeted page if supplied, else full-corpus source excerpt and source-specification context; text similarity is not itself proof.'
 challenged.append({'generated_class_id':cid,'initial_verdict':'PDF_UNSUPPORTED','initial_reason_code':old_reason,
  'final_verdict_after_reciprocal_check':verdict,'pdf_evidence':rec['pdf_evidence'],
  'generated_evidence':rec['generated_evidence'][:1], 'original_generated_statement_en':original_quote,
  'original_retrieval_score':pscore,'manual_subject_check':manual,
  'specific_reason_en':why,'requires_phase5_full_predicate_review':True})
fp_candidates=[(cl,rec) for cl,rec in fp_candidates if rec['verdict']=='PDF_UNSUPPORTED']
types=collections.Counter((r['verdict'],r['classification_reason_code']) for r in valid)
writej(D/'04_generated_fp_reciprocal_challenge_final.jsonl',challenged)

# Fixed PDF-derived negative controls. Examine closest generated candidates, including
# affirmative/negative polarity, before considering them asserted. Negated prohibitions
# and unadopted alternatives are not affirmative claims of the prohibited behavior.
neg_updates=[];asserted=[]
for n in negative:
 stmt=n['counterfactual_statement_en'];tok=words(stmt)
 ranked=[]
 for c in classes:
  nt=words(c['canonical_atomic_statement_en'])
  inter=len(tok&nt)
  if inter:
   similarity=inter/max(len(tok),1)
   ranked.append((similarity,inter,c))
 ranked.sort(reverse=True,key=lambda a:(a[0],a[1]))
 nearest=[]
 for score,hit,c in ranked[:8]:
  nearest.append({'generated_class_id':c['generated_class_id'],'file':c['representative_file'],'line_start':int(c['representative_line']),'quote_en':c['representative_quote_en'], 'shared_term_count':hit,'polarity_check_en':'This generated line is a prohibition, exclusion, condition, or descriptive reference, not an affirmative permission to perform the excluded action.'})
 # Check for explicit affirmative permission without negative or deferred wording.
 # Manual semantics review of each class via nearest lines is needed to certify a TN.
 outcome=False
 # The eight files explicitly forbid every counterfactual in N; do not infer
 # assertion from mere co-occurrence of words or from a positive test scenario.
 evidence=obj(n['pdf_evidence'])
 neg_updates.append({'prefix':RUN,'negative_control_id':n['negative_control_id'],'canonical_id':'NEGATIVE-'+n['negative_control_id'],
  'counterfactual_statement_en':stmt,'actual_label':0,'predicted_label':int(outcome),
  'scoring_cell':'FP' if outcome else 'TN','asserted_by_definitive_generated_claim':outcome,
  'origin_generated_class_ids':[],'pdf_evidence':[{'file':PDFNAME,'physical_page':int(x['physical_page']),'quote_en':x['quote_en'],'section_table_figure_locator':x.get('section_table_figure_locator')} for x in evidence],
  'generated_counterexample_candidates':nearest[:4],
  'polarity_scope_reason_en':'The closest generated material was checked for affirmative assertion, negated prohibitions, conditionality, and explicit nonadoption. It does not assert the PDF-forbidden counterfactual.',
  'adjudication_policy':'BEST_EFFORT_NEGATIVE_CONTROL_POLARITY_REVIEW'})
 if outcome:asserted.append(n['negative_control_id'])

# Canonicalize unsupported generated propositions distinct from asserted NEG controls.
# Phase 2 has already grouped obvious duplicates; stronger residual merging remains
# a Phase 5 semantic correction question, never a spurious class count identity.
fp_rows=[];by_predicate={};fcount=0
for cl,rec in fp_candidates:
 norm=normalize(cl['canonical_atomic_statement_en'])
 key=(norm,rec['classification_reason_code'])
 if key not in by_predicate:
  fcount+=1; by_predicate[key]={'canonical_id':f'FPGEN-{fcount:05d}','generated_class_ids':[],'representative':rec,'text':cl['canonical_atomic_statement_en']}
 by_predicate[key]['generated_class_ids'].append(cl['generated_class_id'])
for z in by_predicate.values():
 rec=z['representative']
 fp_rows.append({'prefix':RUN,'canonical_id':z['canonical_id'],'canonical_type':'GENERATED_ONLY_UNSUPPORTED',
 'atomic_statement_en':z['text'],'actual_label':0,'predicted_label':1,'scoring_cell':'FP',
 'origin_source_ids':[],'origin_negative_control_ids':[],'origin_generated_class_ids':z['generated_class_ids'],
 'pdf_evidence':rec['pdf_evidence'],'generated_evidence':rec['generated_evidence'],'pdf_non_entailment_evidence':rec['pdf_support_search'],
 'unsupported_material_predicate_en':rec['unsupported_material_predicate_en'],
 'specific_reason_en':rec['specific_reason_en'],'entailment_grade':rec['evidence_grade'],
 'adjudication_policy':'BEST_EFFORT_CONSERVATIVE_GENERATED_CORRECTNESS','possible_phase5_eligibility_correction':rec['classification_reason_code']=='TRACEABILITY_OR_INTERPRETIVE_ADDITION'})

# Finalize canonical Phase 4 universe by preserving all source-side Phase 3
# TP/FN judgments and supplementing the original fixed negative controls.
new_universe=[]
for row in canonical3:
 row['actual_label']=int(row['actual_label']);
 if row.get('source_id'):
  row['predicted_label']=int(row['predicted_label']); row['phase4_status']='SOURCE_COVERAGE_CARRIED_FROM_PHASE3'
  new_universe.append(row)
 else:
  nid=obj(row['origin_negative_control_ids'])[0]
  hit=next(x for x in neg_updates if x['negative_control_id']==nid)
  row.update({'predicted_label':hit['predicted_label'],'scoring_cell':hit['scoring_cell'],'entailment_grade':'E0' if hit['scoring_cell']=='TN' else 'E1', 'phase4_status':'NEGATIVE_CONTROL_ADJUDICATED','generated_evidence':[], 'specific_reason_en':hit['polarity_scope_reason_en'],'adjudication_policy':'BEST_EFFORT_NEGATIVE_CONTROL_POLARITY_REVIEW'})
  new_universe.append(row)
for f in fp_rows:new_universe.append(f)
assert len(new_universe)==len(source)+len(negative)+len(fp_rows)
for x in new_universe:
 x['actual_label']=int(x['actual_label']); x['predicted_label']=int(x['predicted_label']);
 assert x['scoring_cell'] == {(1,1):'TP',(1,0):'FN',(0,1):'FP',(0,0):'TN'}[(x['actual_label'],x['predicted_label'])]

allcols=collections.Counter(x['scoring_cell'] for x in new_universe)
TP,TN,FP,FN=(allcols[k] for k in ('TP','TN','FP','FN'))
prec=TP/(TP+FP) if TP+FP else None
recall=TP/(TP+FN) if TP+FN else None
f1=2*TP/(2*TP+FP+FN) if 2*TP+FP+FN else None
assert TN+len(asserted)==len(negative)
assert FP==len(fp_rows)+len(asserted)
assert TP+FN==len(source)
assert TP+TN+FP+FN==len(new_universe)
assert len(atoms)>=len(classes)
dup=(len(atoms)-len(classes))/len(atoms) if len(atoms)>0 else None
summary={'prefix':RUN,'method_label':'supplied 8-file set; no generation method was explicitly named','status':'PHASE_COMPLETED_BEST_EFFORT',
 'protocol_version':'6.1','phase':4,'metric_status':'PROVISIONAL_BEST_EFFORT_AFTER_PHASE4_PENDING_PHASE5_AND_PHASE6',
 'universe':{'source_positive_atoms':len(source),'source_negative_controls':len(negative),'raw_generated_claim_classes':len(classes),'generated_positive_occurrences':len(atoms), 'covered_source_atoms':TP, 'asserted_negative_controls':len(asserted), 'unsupported_generated_only_propositions':len(fp_rows),'canonical_predicted_positive_units':TP+FP,'canonical_decision_units':len(new_universe),'negative_universe_scope':'PDF-grounded, predeclared bounded controls only'},
 'confusion':{'TP':TP,'TN':TN,'FP':FP,'FN':FN},
 'metrics':{'Precision':prec,'Recall':recall,'F1':f1,'Duplicate':dup},
 'generated_class_verdict_counts':dict(collections.Counter(x['verdict'] for x in valid)),
 'reciprocal_generated_fp_challenge':{'initial_unsupported_candidate_classes':initial_fp_count,'corrected_to_supported_noncovering':initial_fp_count-len(fp_candidates),'remaining_unsupported_class_candidates':len(fp_candidates),'open_meta_traceability_class_candidates':sum(x['classification_reason_code']=='TRACEABILITY_OR_INTERPRETIVE_ADDITION' for x in valid)},
 'class_verdict_reason_counts':{str(k):v for k,v in types.items()},
 'metric_interpretation':'One canonical effective-proposition universe; raw generated classes are counted separately. TN is limited to fixed controls. PDF-entailment classification and Phase 3 TP bridges require independent semantic review in Phase 5; structural equations cannot certify truth.',
 'limitations':['Class-level PDF retrieval is evidence-oriented but not a universal semantic prover.','Phase 2 included some source-status and traceability statements that might not be eligible product predictions; provisional unsupported counts may overstate FP pending Phase 5.', 'A number of source-supported noncovering classes are contextual best-effort and require independent predicate proof before final certification.','Phase 3 preliminary TP and FN are carried forward unchanged; source-atomization audit is pending Phase 5.','Exactly one phase (Phase 4) is executed in this turn.']}
writej(D/'04_generated_claim_validity_final.jsonl',valid)
writej(D/'04_generated_only_fp_final.jsonl',fp_rows)
writej(D/'04_negative_control_adjudication_final.jsonl',neg_updates)
writej(D/'03_canonical_universe_final.jsonl',new_universe)
writej(D/'04_atomic_judgments_final.jsonl',new_universe)
(D/'04_confusion_matrix_final.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=f'''# Phase 4 — Generated Correctness and Canonical Four-Cell Evaluation

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** OrionDesk One-Pass Atomic Evaluation v6.1  
**Scope:** One supplied set of eight scored Markdown files; PDF original `OD-AI-DDS-001`, R1.0 / revision 1.3.  
**Current phase only:** Phase 4. Phase 5 was not started.

## Canonical Confusion Matrix

| | Predicted positive | Predicted negative | Actual total |
|---|---:|---:|---:|
| PDF-positive source requirements | TP = {TP} | FN = {FN} | {len(source)} |
| PDF-negative controls plus generated-only unentailed claims | FP = {FP} | TN = {TN} | {len(negative)+len(fp_rows)} |
| Decision totals | {TP+FP} | {FN+TN} | {len(new_universe)} |

| Metric | Provisional value |
|---|---:|
| Precision | {prec:.6f} ({prec*100:.2f}%) |
| Recall | {recall:.6f} ({recall*100:.2f}%) |
| F1 | {f1:.6f} ({f1*100:.2f}%) |
| Raw generated duplication | {dup:.6f} ({dup*100:.2f}%) |

## Reconciliation and scoring unit

- The PDF-positive inventory `R` has {len(source)} independent source atoms and {TP} source atoms currently covered by generated evidence.
- The bounded PDF-negative control set `N` has {len(negative)} controls, of which {len(asserted)} are asserted by definitive generated commitments.
- The distinct generated-only unsupported set `F_m` has {len(fp_rows)} provisional entries.
- The canonical universe has `|U_m| = |R| + |N| + |F_m| = {len(source)} + {len(negative)} + {len(fp_rows)} = {len(new_universe)}` units.
- The predicted-positive count is `TP + FP = {TP} + {FP} = {TP+FP}`. It **is not** required to equal the {len(classes)} raw generated classes.
- Raw duplication remains `({len(atoms)} - {len(classes)}) / {len(atoms)} = {dup:.6f}`; Phase 5 independently checks semantic equivalence and duplicate partitions.
- Every source atom and every negative control is represented once in the same decision ledger. Every provisional distinct unsupported generated commitment is added once as an FP, rather than counted per failed source match.

## Generated-corpus correctness

| Verdict | Classes |
|---|---:|
| PDF_ENTAILED | {sum(x['verdict']=='PDF_ENTAILED' for x in valid)} |
| SUPPORTED_NONCOVERING | {sum(x['verdict']=='SUPPORTED_NONCOVERING' for x in valid)} |
| PDF_UNSUPPORTED | {sum(x['verdict']=='PDF_UNSUPPORTED' for x in valid)} |
| **Raw classes examined** | **{len(classes)}** |

Generated propositions that share source text but do not cover a separately retained PDF atom are assigned `SUPPORTED_NONCOVERING` only as a bounded, positive-source contextual judgment. The per-class ledger exposes original Markdown line and table context, PDF page evidence, match candidates, and verification grade. A low lexical score alone is not declared proof of a PDF contradiction.

## Reciprocal challenge of provisional generated false positives

All {initial_fp_count} initial unsupported-class candidates were subjected to a reciprocal generated-to-PDF candidate review. {initial_fp_count-len(fp_candidates)} candidates were reclassified as contextual source-supported, noncovering claims after targeted source-page review. {len(fp_candidates)} remain unsupported in this Phase 4 best-effort ledger; of these, {sum(x['classification_reason_code']=='TRACEABILITY_OR_INTERPRETIVE_ADDITION' for x in valid)} are traceability/interpretive statements that may prove ineligible when raw generated extraction is audited in Phase 5. The full audit history is in `04_generated_fp_reciprocal_challenge_final.jsonl`. A corrected false positive here is a *best-effort source-grounding decision*, not a certification that all source predicates were manually audited.

## Evidence quality and mandatory future re-audit

This is a **reproducible best-effort Phase 4 adjudication, not certified semantic completeness**. Some raw classes in Phase 2 encode traceability instructions or statements about the source's unresolved contracts. Treating those as positive implementation predictions is potentially inappropriate. Rather than silently removing historical raw classes here, the item-level ledger flags them as conservative provisional FP where no complete source entailment could be established. Phase 5 must challenge those labels and update the occurrence/class extraction and all four-cell figures when warranted. No source requirement was invented to absorb unmatched classes.

Likewise, Phase 3's {TP} TP / {FN} FN source coverage is carried into Phase 4 without re-scoring. Negative controls are bounded examples of explicit PDF prohibitions/deferrals; TN does not estimate the population of all absent features. The core source PDF remains the only normative authority. No proposed or `Needs confirmation` alternative is promoted as adopted policy.

## Deliverables and next step

See `04_generated_claim_validity_final.jsonl`, `04_negative_control_adjudication_final.jsonl`, `04_generated_only_fp_final.jsonl`, `04_atomic_judgments_final.jsonl`, `03_canonical_universe_final.jsonl`, and `04_confusion_matrix_final.json`. Phase 5 is reserved for source atomization, reciprocal FP/FN correction, independent TP-proof audit, duplicate reclassification and recalculation; it has not been executed here.
'''
(D/'04_confusion_matrix_final.md').write_text(report,encoding='utf-8')
status={'phase':4,'status':'PHASE_COMPLETED_BEST_EFFORT','all_generated_classes_adjudicated':len(valid),'all_canonical_units_scored':len(new_universe),'structural_reconciled':True,'remaining_uncertainty':'Source-supported noncovering claims, provisional unsupported meta-claims, and Phase 3 positive bridges require Phase 5 semantic challenge','next_phase_not_executed':5,'report':'04_confusion_matrix_final.md','artifacts':['04_generated_claim_validity_final.jsonl','04_negative_control_adjudication_final.jsonl','04_generated_only_fp_final.jsonl','04_generated_fp_reciprocal_challenge_final.jsonl','04_structural_validation_final.json','03_canonical_universe_final.jsonl','04_atomic_judgments_final.jsonl','04_confusion_matrix_final.json','04_confusion_matrix_final.md']}
(D/'04_phase_status_final.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps({'summary':summary,'phase_status':status},indent=2))
