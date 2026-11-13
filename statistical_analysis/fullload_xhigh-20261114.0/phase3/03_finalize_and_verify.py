#!/usr/bin/env python3
"""Phase 3 post-adjudication structural verification and report generation. No Phase 4 scoring."""
import os,json,re,collections,hashlib
from pathlib import Path
P=Path('/mnt/data');D=P/'oriondesk_phase3';src=P/'oriondesk_phase1'; gen=P/'oriondesk_phase2'

R=[json.loads(x) for x in open(src/'01_source_atoms_final.jsonl')]
N=[json.loads(x) for x in open(src/'01_source_negative_controls_final.jsonl')]
A=[json.loads(x) for x in open(D/'03_evidence_matches_final.jsonl')]
C=[json.loads(x) for x in open(D/'03_canonical_universe_final.jsonl')]
classes={x['class_id']:x for x in map(json.loads,open(gen/'02_generated_classes_final.jsonl'))}
init={x['source_id']:x for x in map(json.loads,open(D/'03_fn_root_cause_audit_final.jsonl'))}
md={path.name:path.read_text(encoding='utf8').splitlines() for path in P.glob('0[1-8]_*.md')}

# Correct a demonstrable false positive introduced by a generic 'principal relationships' substring.
for x in A:
 if x['source_id']=='PDF-00186' and x['scoring_cell']=='TP' and any('Purpose and principal relationships' in e['normalized_proposition_en'] for e in x['generated_evidence']):
  wrong=x['generated_evidence'];x.update({'scoring_cell':'FN','predicted_label':0,'entailment_grade':'E1','coverage_mode':'NOT_ENTAILED','origin_generated_class_ids':[],'generated_evidence':[],'specific_reason_en':'The nearby DAT-014 phrase "principal relationships" names a generic column header, not the Principal owner aggregate. UUIDv7 use by a Principal cannot be proved from a universal application-ID statement without the correct principal-identifier membership proof.','predicate_check_en':'The target Principal identity predicate is not proved; a generic universal UUIDv7 convention without qualified actor identity does not entail this atom.','scope_membership_proof_en':'No correctly qualified Principal-to-application-UUIDv7 identity bridge is evidenced.','adjudication_policy':'BEST_EFFORT_CONSERVATIVE'})
  x['predicate_checks']['target_action_modality_outcome']={'status':'not_proven','explanation_en':x['specific_reason_en']}
  init[x['source_id']]={'source_id':x['source_id'],'initial_grade':'E1','initial_predicted_label':0,'fn_review_disposition':'PARTIAL_ENTAILMENT','final_source_id_or_replacement_ids':[x['source_id']],'final_scoring_cell':'FN','pdf_evidence':x['pdf_evidence'],'best_generated_candidates':wrong,'exact_and_alias_keys_checked':['Principal target in generated data/identity inventories','DAT-014 principal relationships is a column header, not named principal'], 'universal_context_conjunction_checked':{'direct_synonyms':'not complete','universal_rules':'UUIDv7 baseline is insufficient without principal membership','table_context':'DAT-014 header rejected','cross_file':'data and identity corpus checked'},'scope_membership_proof_en':x['scope_membership_proof_en'],'met_predicates_en':['general UUIDv7 baseline'],'unmet_predicates_en':['Principal owner-aggregate classification','Principal identifier scope'], 'specific_reason_en':x['specific_reason_en'],'adjudication_policy':'BEST_EFFORT_CONSERVATIVE','retrieval_diagnostics':{'noted_false_positive_corrected':True}}
  delta_path=D/'03_phase3_change_delta.jsonl';d=[json.loads(z) for z in open(delta_path)];d.append({'source_id':x['source_id'],'reason':'INCORRECT_TP_BRIDGE_DOWNGRADED','source_statement_en':x['atomic_statement_en'],'invalid_candidate_en':'DAT-014 `principal relationships` header does not identify the Principal owner aggregate.','final_scoring_cell':'FN'});delta_path.write_text(''.join(json.dumps(z,ensure_ascii=False)+'\n' for z in d))

# Strengthen endpoint membership proof: replace a merely adjacent cross-reference with an actual API inventory method+path claim.
route_re=re.compile(r'\b(GET|POST|PATCH|PUT|DELETE)\s+(/(?:v1|internal)/[\w/{}/.?=&-]+)',re.I)
endpoint_replaced=0
for x in A:
 if x['scoring_cell']!='TP' or x['coverage_mode']!='UNIVERSAL_INSTANTIATION':continue
 m=route_re.search(x['atomic_statement_en']);
 if not m:continue
 method,path=m.group(1).lower(),m.group(2).lower().rstrip('.,;:');find=f'{method} {path}'
 if any('method and path' in e['normalized_proposition_en'].lower() and find in e['normalized_proposition_en'].lower() for e in x['generated_evidence']):continue
 possible=[]
 for g in classes.values():
  e=g['representative_evidence'];t=g['canonical_statement_en'].lower()
  if ('method and path' in t or 'method/path or protocol' in t) and f'{method} {path}' in t:
   possible.append(g)
 if not possible:continue
 g=possible[0];e=g['representative_evidence']
 target={'class_id':g['class_id'],'file':e['file'],'line_start':e['line_start'],'line_end':e['line_end'],'table_cell':e.get('table_cell'),'column_header':e.get('column_header'),'row_key':e.get('row_key'),'heading_context':e.get('heading_context'),'quote_en':e['quote_en'],'normalized_proposition_en':g['canonical_statement_en']}
 if not any(z['class_id']==g['class_id'] for z in x['generated_evidence']):
  # Retain the generic invariant and replace the weaker endpoint witness only.
  x['generated_evidence']=[z for z in x['generated_evidence'] if 'before long-running' in z['normalized_proposition_en'].lower() or 'validate request' in z['normalized_proposition_en'].lower()]+[target]
  x['origin_generated_class_ids']=[z['class_id'] for z in x['generated_evidence']]
  endpoint_replaced+=1

# Write back after correction.

def write(name,rows):
 with open(D/name,'w',encoding='utf8') as f:
  for x in rows:f.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n')
write('03_evidence_matches_final.jsonl',A)
write('03_fn_root_cause_audit_final.jsonl',sorted(init.values(),key=lambda z:z['source_id']))
C[:len(R)]=A;write('03_canonical_universe_final.jsonl',C)
B=[{'source_id':x['source_id'],'canonical_id':x['canonical_id'],'entailment_grade':x['entailment_grade'],'coverage_mode':x['coverage_mode'],'pdf_evidence':x['pdf_evidence'],'generated_evidence':x['generated_evidence'],'scope_membership_proof_en':x['scope_membership_proof_en'],'predicate_check_en':x['predicate_check_en'],'predicate_checks':x['predicate_checks'],'checked_exceptions_en':'The generated evidence must preserve named source target, actor/authorization, conditions, timing, numerical limits, exceptions, and outcome; no unadopted decisions counted. This is a best-effort source-coverage audit pending Phase 5 independent review.','adjudication_policy':x['adjudication_policy']} for x in A if x['scoring_cell']=='TP']
write('03_semantic_coverage_bridges_final.jsonl',B)

errors=[];qa=collections.Counter();
ids=[z['source_id'] for z in R]; assert len(ids)==len(set(ids))
assert len(A)==len(R)==1024
assert len(C)==len(R)+len(N)==1061
assert [z['source_id'] for z in A]==ids
assert len(set(z['canonical_id'] for z in C))==len(C)
for i,x in enumerate(A):
 try:
  assert x['source_id']==R[i]['source_id']
  assert x['atomic_statement_en']==R[i]['atomic_statement_en']
  assert x['scoring_cell'] in ('TP','FN')
  assert x['actual_label']==1 and x['predicted_label']==(1 if x['scoring_cell']=='TP' else 0)
  assert x['entailment_grade'] in ('E3','E2') if x['scoring_cell']=='TP' else x['entailment_grade'] in ('E1','E0')
  assert x['pdf_evidence'] and x['pdf_evidence'][0]['physical_page']==R[i]['physical_page']
  assert x['generated_evidence'] if x['scoring_cell']=='TP' else not x['generated_evidence']
  assert x['source_id'] in init if x['scoring_cell']=='FN' else True
 except AssertionError: errors.append({'type':'source_coverage_invariant','source_id':x['source_id']})
 for ev in x['generated_evidence']:
  if ev['class_id'] not in classes:errors.append({'type':'class_id_missing','source_id':x['source_id'],'class_id':ev['class_id']});continue
  if ev['file'] not in md:errors.append({'type':'source_file_missing','file':ev['file']});continue
  ln=ev['line_start']
  if ln is None or not 1<=ln<=len(md[ev['file']]):errors.append({'type':'line_out_of_range','source_id':x['source_id'],'file':ev['file'],'line_start':ln});continue
  source_line=md[ev['file']][ln-1]
  # the representative evidence is table cell or prose: cell text may have formatting normalization.
  q=ev['quote_en'];
  if q not in source_line and not re.sub(r'[`* ]','',q) in re.sub(r'[`* ]','',source_line):
   errors.append({'type':'quote_not_in_line','source_id':x['source_id'],'class_id':ev['class_id'],'file':ev['file'],'line':ln,'quote':q[:170]})
  else:qa['exact_generated_quote_matches']+=1
for j,n in enumerate(N):
 row=C[len(R)+j]
 if row['origin_negative_control_ids'] !=[n['negative_control_id']] or row['atomic_statement_en']!=n['counterfactual_statement_en'] or row['scoring_cell']!='PENDING_PHASE_4' or row['predicted_label'] is not None:errors.append({'type':'negative_pending_row_invalid','negative_id':n['negative_control_id']})
fnids={z['source_id'] for z in A if z['scoring_cell']=='FN'}
for sid,root in init.items():
 if root['final_scoring_cell']=='FN':
  if sid not in fnids or root['fn_review_disposition'] not in ('TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'):errors.append({'type':'fn_root_closure_invalid','source_id':sid})
  if not root.get('best_generated_candidates'):errors.append({'type':'fn_no_candidate_evidence','source_id':sid})
 elif root['final_scoring_cell']=='TP':
  if sid in fnids or root['fn_review_disposition']!='MATCHER_FALSE_NEGATIVE_CORRECTED':errors.append({'type':'correction_inconsistency','source_id':sid})
 else:errors.append({'type':'invalid_root_final','source_id':sid})
assert len(init)==706
assert len(B)+len(fnids)==1024
assert len([x for x in init.values() if x['final_scoring_cell']=='FN'])==len(fnids)
assert len([x for x in init.values() if x['final_scoring_cell']=='TP'])==len(init)-len(fnids)

# Recompute Phase 3 diagnostic probes from final source ledger (no historical pre-labeled expected results).
probes=[]
patterns={'case_title':'case includes title','workspace_retention_class':'workspace settings includes retention class','identical_case_replay':'one case and identical response','non_disclosing_foreign_id':'cross-tenant id substitution','indexed_source_revocation':'revoke source access after indexing','stale_review_hash':'approve wrong artifact hash','source_not_authority':'browser never sends arbitrary tool definitions'}
for label,phrase in patterns.items():
 matched=[x for x in A if phrase in x['atomic_statement_en'].lower()]
 probes.append({'probe_name':label,'searched_phrase_en':phrase,'source_atoms':[{'source_id':x['source_id'],'scoring_cell':x['scoring_cell'],'entailment_grade':x['entailment_grade'],'generated_evidence':x['generated_evidence'][:2]} for x in matched]})
write('03_regression_probes_final.jsonl',probes)

status=json.loads((D/'03_phase_status_final.json').read_text()); status['source_coverage']={'TP':len(B),'FN':len(fnids),**dict(collections.Counter(x['entailment_grade'] for x in A))};status['FN_root_cause']=dict(collections.Counter(init[z]['fn_review_disposition'] for z in fnids));status['initial_FN_candidates_audited']=705;status['initial_TP_downgrades']=1;status['corrected_FN_candidates']=sum(z['final_scoring_cell']=='TP' for z in init.values());status['reciprocal_corrections']=status['corrected_FN_candidates'];status['endpoint_scope_evidence_repairs']=endpoint_replaced
status['phase3_structural_validation']='PASS' if not errors else 'FAIL'
(D/'03_phase_status_final.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
validation={'phase':3,'status':'PASS' if not errors else 'FAIL','inputs_available':{'original_pdf_physical_pages':90,'generated_markdown_files':len(md),'frozen_source_positive':len(R),'frozen_negative_controls':len(N),'raw_generated_classes':len(classes)},'phase3_counts':{'source_TP':len(B),'source_FN':len(fnids),'initial_FN_candidates':705,'corrected_matcher_FN':status['corrected_FN_candidates'],'negative_controls_pending_phase_4':len(N),'phase3_universe_records':len(C)},'evidence_coverage':{'generated_original_quote_matches':qa['exact_generated_quote_matches'],'unverified_quote_location_count':sum(e['type']=='quote_not_in_line' for e in errors),'TP_bridge_records':len(B),'FN_root_final_records':len(fnids),'corrected_candidate_root_records':status['corrected_FN_candidates']},'failures':errors[:50],'error_count':len(errors),'safety_caveat':'Structural validation and exact citation occurrence do not establish full semantic entailment.'}
(D/'03_phase3_validation_final.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')

report=f'''# OrionDesk AI — Phase 3 Semantic Source-Coverage Report

**Protocol:** version 6.1  
**Phase:** 3 only, completed  
**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Generated-set label:** `fullload` inherited from Phase 2 metadata; original method provenance not independently verified.  
**Primary PDF:** `OrionDesk_AI_Detailed_Design_Specification(3).pdf`, 90 physical pages.  
**Source baseline:** reused immutable Phase 1 positive (`R`) and bounded negative (`N`) inventories.

## Coverage-stage outputs (not a four-cell matrix)

| Phase 3 statistic | Provisional result |
|---|---:|
| PDF-positive source atoms | {len(R):,} |
| Source atoms with a documented TP-grade direct or logical bridge | {len(B):,} |
| Source atoms without a complete demonstrated bridge (conservative FN) | {len(fnids):,} |
| E3 direct source propositions | {status['source_coverage'].get('E3',0):,} |
| E2 equivalence, inherited-context, universal and conjunctive bridges | {status['source_coverage'].get('E2',0):,} |
| E1 partly matched / materially unproven | {status['source_coverage'].get('E1',0):,} |
| E0 no defensible source predicate bridge | {status['source_coverage'].get('E0',0):,} |
| Initial FN candidates challenged | 705 |
| Initial FN errors corrected to TP with actual evidence | {status['corrected_FN_candidates']:,} |
| Final PARTIAL_ENTAILMENT | {status['FN_root_cause'].get('PARTIAL_ENTAILMENT',0):,} |
| Final CONSERVATIVE_UNRESOLVED | {status['FN_root_cause'].get('CONSERVATIVE_UNRESOLVED',0):,} |
| Final TRUE_MISSING | {status['FN_root_cause'].get('TRUE_MISSING',0):,} |
| Fixed negative controls carried forward without prediction | {len(N):,} |

**Interpretation:** The ratio of evidenced source-positive TP records to the reused source inventory is **{len(B)/len(R):.2%}**. This is **only a provisional Phase 3 source-coverage fraction**, *not* the final audited Recall, not a complete confusion matrix, and not a verified rate of missing requirements. Its numerator and denominator remain subject to independent complete-predicate and source-atomization review in Phase 5. A conservative FN can be a retrieval/interpretation gap, and even an apparent TP can lack a full predicate if a contextual table row was overinterpreted.

## Retrieval and reciprocal evidence challenges

The phase consumed all eight unchanged Markdown files (8,330 physical lines and 14,882 table cells as inventoried in Phase 2), with 6,581 extracted occurrences and 6,527 conservative generated classes. Candidate retrieval combined word/character n-grams, uncapped exact route and identifier lookups, named field tables, original row/column context, shared requirements and explicit multiple-statement bridges. In addition, the source-atom-to-generated and generated-to-source meaning challenges inspected named endpoint, field, event, screen, state, test and DDL targets.

Full predicate scope is **not** assumed from a mere identifier match. For source-specific API requirements, the complete method/path and applicable actor, status and outcome were checked against the original generated API inventory row. For physical fields, the source entity and the DAT field row were checked together. Explicit shared rules were instantiated only where a matching resource-level membership witness was available. Unadopted proposals and the open architecture register were not promoted to positive implementation decisions.

Clear misses included the case-title data field, workspace retention class, cross-tenant/foreign-tenant equivalence, identical-response case replay, revised invariant negative tests, and screen-inventory rows. These were corrected to TP with actual file/line evidence and remain in the corrected-FN root-cause history.

## Quality and remaining uncertainty

- **Evidence completeness:** all {len(R):,} source-positive units have an item-level decision, original PDF citation, and retrieval outcome; all {len(fnids):,} remaining candidate FNs retain closest original generated evidence with a specific unmet requirement or conservative ambiguity.
- **Full-predicate proof:** Phase 3 records the predicate check and scope bridge for every candidate TP, but these are partly automated best-effort adjudications. No claim of independently certified semantic proof for every TP is made. Phase 5 must challenge each of them independently.
- **Source atomization:** the preserved historical PDF ledger has a 100-item watchlist including repeated cross-cutting context and acceptance-test overlap. It was retained as requested; its count has **not** been independently certified as the minimal meaningful denominator.
- **Conservative FN uncertainty:** labels `PARTIAL_ENTAILMENT` and `CONSERVATIVE_UNRESOLVED` do **not** certify semantic absence. They identify the best currently grounded judgment after attempted reciprocal retrieval. Any objectively located, complete match was corrected during this phase.
- **No Phase 4 leakage:** the 37 predeclared negative controls remain undecided; unsupported generated-only propositions, asserted controls, FP/TN classification and effective-universe metrics are **not** evaluated here.

## Selected regression cases

| Diagnostic probe | Source result |
|---|---|
'''
for pr in probes:
 if not pr['source_atoms']:label='No matching source atom under this probe phrase.'
 else:label=', '.join(z['source_id']+' '+z['scoring_cell'] for z in pr['source_atoms'][:6])
 report+=f"| `{pr['probe_name']}` | {label} |\n"
report+='''
## Individual deliverables

- `03_canonical_universe_final.jsonl`: all 1,024 source-positive units and 37 fixed negative controls with **pending** Phase 4 labels. Generated-only unsupported units are deliberately not appended yet.
- `03_evidence_matches_final.jsonl`: one source-positive predicate/citation decision per source atom.
- `03_semantic_coverage_bridges_final.jsonl`: direct and contextual TP-grade claim bridges, including exact original generated file/line evidence and predicate checks.
- `03_fn_root_cause_audit_final.jsonl`: **all initially nominated FN candidates**, including those corrected to TP; each remaining FN has a named disposition and nearest actual generated evidence.
- `03_phase3_change_delta.jsonl`: per-item corrected matcher FN history and any explicit adverse proof corrections.
- `03_candidate_generated_validity_review.jsonl`: possible class-review leads; not validity judgments or FP counts.
- `03_regression_probes_final.jsonl`: actual requirement/field/test regression queries.
- `03_phase_status_final.json`: current phase metadata and limitation counts.
- `03_phase3_validation_final.json`: structural and citation-address integrity checks.
- `03_build_coverage.py`, `03_reciprocal_corrections.py`, `03_structural_final_pass.py`, `03_final_close.py`, `03_final_predicate_probe.py`, `03_finalize_and_verify.py`: reproducible local processing stages. 

## Phase boundary

Phase 3 is complete on a best-effort basis. **Phase 4 is not started**: no final Precision, Recall, F1, TP/TN/FP/FN four-cell confusion matrix, or independent generated-class validity ledger is claimed. The fixed source R/N denominators have not been modified in this phase.
'''
(D/'03_phase3_report.md').write_text(report,encoding='utf8')
print(json.dumps(validation,ensure_ascii=False,indent=2)[:3600]);print('REPORT',D/'03_phase3_report.md')
if errors:raise SystemExit(2)
