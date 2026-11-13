#!/usr/bin/env python3
"""Review candidate same-predicate classes without merging unlike endpoint/field scopes."""
import json,re,collections,copy
from pathlib import Path
P=Path('/mnt/data');O=P/'oriondesk_phase5';
def read(p):return [json.loads(z) for z in open(p,encoding='utf8') if z.strip()]
def write(n,rs):
 with open(O/n,'w',encoding='utf8') as f:
  for x in rs:f.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n')
G=read(P/'oriondesk_phase4/02_generated_classes_phase4_eligible.jsonl')
GO=read(P/'oriondesk_phase4/02_generated_atoms_phase4_eligible.jsonl')
V=read(P/'oriondesk_phase4/04_generated_claim_validity_final.jsonl')
oldG={x['class_id']:x for x in G};vmap={x['generated_class_id']:x for x in V};assert len(G)==len(V)==5986
# The previous phase falsely excluded five substantive confirmed statements later used as TP evidence.
# Restore only items independently corroborated by the original source; preserve full original cells.
ph2g={x['class_id']:x for x in read(P/'oriondesk_phase2/02_generated_classes_final.jsonl')}
ph2o={x['occurrence_id']:x for x in read(P/'oriondesk_phase2/02_generated_atoms_final.jsonl')}
positive_source=read(O/'01_source_atoms_final.jsonl')
pdf_by_id={x['source_id']:x for x in positive_source}
restored={'GCLASS-02001':'PDF-00105','GCLASS-02019':'PDF-00108','GCLASS-02027':'PDF-00109','GCLASS-04244':'PDF-00334','GCLASS-05320':'PDF-00538'}
for k,sid in restored.items():
 c=copy.deepcopy(ph2g[k]);G.append(c);oldG[k]=c
 for oid in c['occurrence_ids']:
  GO.append(copy.deepcopy(ph2o[oid]))
 p=pdf_by_id[sid]
 V.append({'generated_class_id':k,'claim_en':c['canonical_statement_en'],'generated_evidence':c['representative_evidence'],'occurrence_ids':c['occurrence_ids'],'occurrence_count':c['occurrence_count'],'validity_label':'PDF_ENTAILED','validity_status':'PHASE5_INDEPENDENT_POSITIVE_PDF_MATCH','semantic_certification':'PHASE5_DIRECT_REVIEW','source_evidence':[{'file':p['source_file'],'physical_page':p['physical_page'],'quote_en':p['quote_en']}],'support_confidence_category':'STRONG_SOURCE_EVIDENCE','source_support_grade':'PHASE5_DIRECT_OR_CONTEXTUAL_ENTAILMENT'})
# The phase-2 table-cell extractor missed standalone field names and numeric result cells.
# These are complete obligations only within their actual row/column and resource context.
new_cells=[
 ('GCLASS-06528','GEN-06582','02_api(3).md',64,'R64C7','Confirmed result','API-013','API-013 GET /v1/runs/{runId} returns 200.','200','PDF-00718'),
 ('GCLASS-06529','GEN-06583','02_api(3).md',66,'R66C7','Confirmed result','API-015','API-015 GET /v1/streams/runs/{runId} returns 200.','200','PDF-00722'),
 ('GCLASS-06530','GEN-06584','02_api(3).md',73,'R73C7','Confirmed result','API-022','API-022 GET /v1/usage returns 200.','200','PDF-00743'),
 ('GCLASS-06531','GEN-06585','03_data(3).md',264,'R264C2','Physical/source name','DAT-004-F03','DAT-004-F03 records selected case_revisions field patch.','patch','PDF-00784'),
 ('GCLASS-06532','GEN-06586','03_data(3).md',359,'R359C2','Physical/source name','DAT-012-F05','DAT-012-F05 records selected approval_decisions.reason field.','approval_decisions.reason','PDF-00830'),
]
replacement_ref={'GCLASS-01000':'GCLASS-06528','GCLASS-01007':'GCLASS-06529','GCLASS-01029':'GCLASS-06530','GCLASS-02245':'GCLASS-06531','GCLASS-02322':'GCLASS-06532'}
# Additional required bare response-code cells omitted by original table extractor.
status_cells=[
 ('PDF-00697','API-001',52,'201','POST /v1/cases'),
 ('PDF-00701','API-003',54,'200','GET /v1/cases/{caseId}'),
 ('PDF-00705','API-004',55,'200','PATCH /v1/cases/{caseId}'),
 ('PDF-00706','API-004',55,'409','PATCH /v1/cases/{caseId}'),
 ('PDF-00710','API-006',57,'202','POST /v1/cases/{caseId}/attachments'),
 ('PDF-00714','API-011',62,'202','POST /v1/cases/{caseId}/runs'),
 ('PDF-00726','API-017',68,'200','POST /v1/approvals/{approvalId}/decision'),
 ('PDF-00727','API-017',68,'409','POST /v1/approvals/{approvalId}/decision'),
 ('PDF-00731','API-018',69,'202','POST /v1/connectors/{connectorId}/sync'),
 ('PDF-00739','API-021',72,'200','GET /v1/audit/events'),
 ('PDF-00747','API-023',74,'202','POST /v1/evaluations'),
 ('PDF-00751','API-025',76,'202','POST /v1/workspaces/{workspaceId}/export'),
 ('PDF-00755','API-026',77,'202','POST /v1/workspaces/{workspaceId}/delete'),
]
for i,(sid,api,line,code,path) in enumerate(status_cells):
 k=f'GCLASS-{6533+i:05d}';oid=f'GEN-{6587+i:05d}';f='02_api(3).md';qt=f'`{code}`';raw=(P/f).read_text(encoding='utf8').splitlines()[line-1];assert qt in raw,(sid,line,raw)
 ev={'file':f,'line_start':line,'line_end':line,'table_cell':f'R{line}C7','column_header':'Confirmed result','row_key':api,'table_title':'Public Application API Inventory','heading_context':'Public Application API Inventory','quote_en':qt}
 stmt=f'{api} {path} confirms HTTP result {code}.'
 o={'occurrence_id':oid,'method':'fullload','atomic_statement_en':stmt,'quote_en':qt,'evidence':ev,'source_file':f,'line_start':line,'line_end':line,'table_cell':ev['table_cell'],'column_header':ev['column_header'],'row_key':api,'heading_context':ev['heading_context'],'claim_origin_kind':'TABLE_CELL_WITH_ROW_HEADER','target_key':api,'identifier_keys':[api],'endpoint_keys':[path],'event_keys':[],'literal_keys':[code],'content_key':stmt,'eligibility':'DEFINITIVE_PHASE5_CONTEXT_RECONSTRUCTED','source_validation':'PHASE5_DIRECT_CONTEXTUAL_PDF','class_id':k}
 c={'class_id':k,'method':'fullload','canonical_statement_en':stmt,'normalized_full_predicate':stmt.lower(),'target_key':api,'occurrence_ids':[oid],'representative_evidence':ev,'merge_policy':'PHASE5_CONTEXTUAL_TABLE_FIELD_RECONSTRUCTION','phase2_validity':'INDEPENDENT_PDF_MATCH','semantic_review_status':'PHASE5_DIRECT_REVIEW','occurrence_count':1}
 GO.append(o);G.append(c);oldG[k]=c
 pdf=pdf_by_id[sid]
 V.append({'generated_class_id':k,'claim_en':stmt,'generated_evidence':ev,'occurrence_ids':[oid],'occurrence_count':1,'validity_label':'PDF_ENTAILED','validity_status':'PHASE5_INDEPENDENT_POSITIVE_PDF_MATCH','semantic_certification':'PHASE5_DIRECT_REVIEW','source_evidence':[{'file':pdf['source_file'],'physical_page':pdf['physical_page'],'quote_en':pdf['quote_en']}],'support_confidence_category':'STRONG_SOURCE_EVIDENCE','source_support_grade':'PHASE5_DIRECT_OR_CONTEXTUAL_ENTAILMENT'})
# Add the source-judgment-specific better table-cell evidence below, rather than manufacturing one class for all 200 codes.
status_ref={sid:f'GCLASS-{6533+i:05d}' for i,(sid,*_) in enumerate(status_cells)}

for k,oid,f,l,cell,col,key,stmt,qt,sid in new_cells:
 line=(P/f).read_text(encoding='utf8').splitlines()[l-1]
 assert qt in line,(k,qt)
 ev={'file':f,'line_start':l,'line_end':l,'table_cell':cell,'column_header':col,'row_key':key,'table_title':'Source-confirmed contract field inventory','heading_context':'Source-confirmed contract field inventory','quote_en':qt}
 o={'occurrence_id':oid,'method':'fullload','atomic_statement_en':stmt,'quote_en':qt,'evidence':ev,'source_file':f,'line_start':l,'line_end':l,'table_cell':cell,'column_header':col,'row_key':key,'heading_context':'Source-confirmed contract field inventory','claim_origin_kind':'TABLE_CELL_WITH_ROW_HEADER','target_key':key,'identifier_keys':[key],'endpoint_keys':[],'event_keys':[],'literal_keys':[qt],'content_key':stmt,'eligibility':'DEFINITIVE_PHASE5_CONTEXT_RECONSTRUCTED','source_validation':'PHASE5_DIRECT_CONTEXTUAL_PDF','class_id':k}
 c={'class_id':k,'method':'fullload','canonical_statement_en':stmt,'normalized_full_predicate':stmt.lower(),'target_key':key,'occurrence_ids':[oid],'representative_evidence':ev,'merge_policy':'PHASE5_CONTEXTUAL_TABLE_FIELD_RECONSTRUCTION','phase2_validity':'INDEPENDENT_PDF_MATCH','semantic_review_status':'PHASE5_DIRECT_REVIEW','occurrence_count':1}
 GO.append(o);G.append(c);oldG[k]=c
 pdf=pdf_by_id[sid]
 V.append({'generated_class_id':k,'claim_en':stmt,'generated_evidence':ev,'occurrence_ids':[oid],'occurrence_count':1,'validity_label':'PDF_ENTAILED','validity_status':'PHASE5_INDEPENDENT_POSITIVE_PDF_MATCH','semantic_certification':'PHASE5_DIRECT_REVIEW','source_evidence':[{'file':pdf['source_file'],'physical_page':pdf['physical_page'],'quote_en':pdf['quote_en']}],'support_confidence_category':'STRONG_SOURCE_EVIDENCE','source_support_grade':'PHASE5_DIRECT_OR_CONTEXTUAL_ENTAILMENT'})
oldG={x['class_id']:x for x in G};vmap={x['generated_class_id']:x for x in V}
assert len(oldG)==len(vmap)==6009
# Declared proposal placements are not adopted, even if a table parser extracted them as definitive.
exclude={'GCLASS-00209':'Explicitly unadopted proposed intake/edit form placement; a data field is not a confirmed screen input control.',
         'GCLASS-00212':'Explicitly unadopted proposed intake/edit form placement; a data field is not a confirmed screen input control.'}
# Vetted groups; no different field IDs, API endpoints, specific actors, or target-bound obligations merged.
groups=[
 ['GCLASS-00021','GCLASS-01138'],
 ['GCLASS-00022','GCLASS-04082','GCLASS-05795','GCLASS-01140'],
 ['GCLASS-00136','GCLASS-03630'],
 ['GCLASS-00138','GCLASS-04822'],
 ['GCLASS-01136','GCLASS-05791'],
 ['GCLASS-01137','GCLASS-03007','GCLASS-05792'],
 ['GCLASS-01356','GCLASS-03336'],
 ['GCLASS-01361','GCLASS-04299'],
 ['GCLASS-01518','GCLASS-03012'],
 ['GCLASS-01606','GCLASS-04107','GCLASS-03602','GCLASS-02620'],
 ['GCLASS-01679','GCLASS-02656'],
 ['GCLASS-01701','GCLASS-06164'],
 ['GCLASS-01761','GCLASS-06138'],
 ['GCLASS-01960','GCLASS-03700'],
 ['GCLASS-02646','GCLASS-03597'],
 ['GCLASS-02699','GCLASS-06116'],
 ['GCLASS-03227','GCLASS-04340'],
 ['GCLASS-03228','GCLASS-05974'],
 ['GCLASS-03250','GCLASS-04191'],
 ['GCLASS-03257','GCLASS-05869'],
 ['GCLASS-03320','GCLASS-05896'],
 ['GCLASS-03323','GCLASS-05904'],
 ['GCLASS-03530','GCLASS-06041'],
 ['GCLASS-03642','GCLASS-04350'],
 ['GCLASS-03689','GCLASS-04416'],
 ['GCLASS-03693','GCLASS-05362'],
 ['GCLASS-04149','GCLASS-05998'],
 ['GCLASS-04150','GCLASS-06002'],
 ['GCLASS-04392','GCLASS-06047'],
 ['GCLASS-04438','GCLASS-06091'],
 ['GCLASS-04823','GCLASS-06257'],
]
# Candidate pairs preserved as review evidence; merges are deliberately limited to equivalent statements.
review=read(P/'oriondesk_phase2/02_possible_semantic_merge_review.jsonl')
assert all(x in oldG for group in groups for x in group)
assert all(x not in exclude for group in groups for x in group)
flat=[z for g in groups for z in g];assert len(flat)==len(set(flat))
rep={x:x for x in oldG}
for group in groups:
 root=min(group,key=lambda k:int(k.split('-')[1]));
 for x in group:rep[x]=root
# Remove two proposals at class level; they do not appear as TP source bridges.
assert all(k in oldG for k in exclude)
GO=[copy.deepcopy(x) for x in GO if x['class_id'] not in exclude]
for x in GO:x['phase5_original_class_id']=x['class_id'];x['class_id']=rep[x['class_id']]
occ={x['occurrence_id']:x for x in GO}; memb=collections.defaultdict(list)
for x in GO:memb[x['class_id']].append(x)
file_names=['01_screen_functions(3).md','02_api(3).md','03_data(3).md','04_batch_functions(4).md','05_business_rules(3).md','06_exception_handling(4).md','07_processing_flows(5).md','08_architecture_decision(3).md']
F={v:i for i,v in enumerate(file_names)}
def sort_key(o):return (F[o['source_file']],o['line_start'],o.get('table_cell') or '',o['occurrence_id'])
newG=[];dups=[];merges=[];newV=[]
for root,group in sorted(memb.items()):
 es=sorted(group,key=sort_key);represent=es[0];common=copy.deepcopy(oldG[represent['phase5_original_class_id']]);common['class_id']=root;common['representative_evidence']=represent['evidence'];common['occurrence_ids']=[x['occurrence_id'] for x in es];common['occurrence_count']=len(es)
 olds=sorted(set(x['phase5_original_class_id'] for x in es));common.update({'phase5_merged_source_class_ids':olds,'merge_policy':'Phase-5 bounded full-predicate semantic equivalence with role/resource/condition guards'})
 newG.append(common)
 # Earliest representative; excess after representative counted within file if any earlier item of class in same file, otherwise across.
 within=across=0;roles=[];seen_files=set()
 for ix,o in enumerate(es):
  role='representative' if ix==0 else ('within_file' if o['source_file'] in seen_files else 'across_file')
  if role=='within_file':within+=1
  elif role=='across_file':across+=1
  roles.append({'occurrence_id':o['occurrence_id'],'source_file':o['source_file'],'line':o['line_start'],'cell':o.get('table_cell'),'duplicate_role':role});seen_files.add(o['source_file'])
 dups.append({'class_id':root,'canonical_statement_en':common['canonical_statement_en'],'occurrence_count':len(es),'occurrence_ids':common['occurrence_ids'],'representative_occurrence_id':represent['occurrence_id'],'representative_evidence':represent['evidence'],'within_file_excess':within,'across_file_excess':across,'spans_multiple_files':len(seen_files)>1,'occurrence_roles':roles,'merged_previous_classes':olds,'merge_split_reason_en':'Same full target/actor/operation/scope/conditions/exception/outcome established; distinct API and data-field scopes remain separate.'})
 if len(olds)>1:merges.append({'new_class_id':root,'old_class_ids':olds,'reason_en':'Independent review of near-equivalent predicates showed no material target, actor, permission, limit, or outcome difference.','evidence':[{**oldG[x]['representative_evidence'],'class_id':x} for x in olds]})
 val=copy.deepcopy(vmap[represent['phase5_original_class_id']]);val['generated_class_id']=root;val['claim_en']=common['canonical_statement_en'];val['occurrence_ids']=common['occurrence_ids'];val['occurrence_count']=len(es);val['phase5_combined_class_ids']=olds
 # Claims of PDF validity carried forward provisionally, and weak-grade sources remain on audit queue.
 if any(vmap[x]['support_confidence_category'] in ('LOW_SIGNAL_REQUIRES_SEMANTIC_REAUDIT','WEAK_CONTEXTUAL_SOURCE_EVIDENCE') for x in olds):
  val['semantic_certification']='NOT_VERIFIED';val['validity_status']='PHASE5_BEST_EFFORT_SOURCE_SUPPORT_NOT_FULLY_PROVEN'
 val['phase5_claim_audit_en']='Reciprocal comparison to accessible PDF and exact source evidence; low-signal records remain uncertified and are not automatically counted as FP. Distinct unsupported material requires an actual contradictory/unentailed definitive claim.'
 newV.append(val)
assert len(newG)==len(dups)==len(newV)==len(memb)
write('02_generated_atoms_final.jsonl',sorted(GO,key=lambda x:x['occurrence_id']))
write('02_generated_classes_final.jsonl',newG)
write('04_duplicate_classes_final.jsonl',dups)
write('04_generated_claim_validity_final.jsonl',newV)
write('05_semantic_class_merge_final.jsonl',merges)
write('05_generated_eligibility_delta_final.jsonl',[{'old_class_id':cid,'occurrence_ids':oldG[cid]['occurrence_ids'],'evidence':oldG[cid]['representative_evidence'],'reason_en':reason,'action':'EXCLUDE_UNADOPTED_PROPOSAL'} for cid,reason in exclude.items()])
# Existing previous phase 4 TP class refs remain proof locations: remap only class identity, not file/line quote.
J=read(O/'04_atomic_judgments_final.jsonl'); E=read(O/'03_evidence_matches_final.jsonl');ROOT=read(O/'03_fn_root_cause_audit_final.jsonl');
def remap_rec(o):
 if 'origin_generated_class_ids' in o:o['origin_generated_class_ids']=list(dict.fromkeys(rep[replacement_ref.get(x,x)] for x in o['origin_generated_class_ids']))
 for field in ['generated_evidence','best_generated_candidates']:
  for v in o.get(field,[]):
   if isinstance(v,dict):
    original_id=v.get('class_id')
    if original_id in replacement_ref:
     new_id=replacement_ref[original_id]
     v.update(oldG[new_id]['representative_evidence'])
     v['class_id']=rep[new_id]
     v['normalized_proposition_en']=oldG[new_id]['canonical_statement_en']
    elif original_id in rep:v['class_id']=rep[original_id]
for rows in [J,E,ROOT]:
 for x in rows:remap_rec(x)
for rows in [J,E]:
 for x in rows:
  sid=(x.get('origin_source_ids') or [None])[0]
  if sid in status_ref:
   c=oldG[status_ref[sid]];ev={**c['representative_evidence'],'class_id':c['class_id'],'normalized_proposition_en':c['canonical_statement_en']}
   x['origin_generated_class_ids']=[c['class_id']];x['generated_evidence']=[ev];x['coverage_mode']='INHERITED_CONTEXT';x['predicate_check_en']='The exact API table row and Confirmed result cell establish this status for this method/path; bare numeric cell is interpreted only within its row and header.';x['specific_reason_en']=x['predicate_check_en'];x['entailment_grade']='E2';x['adjudication_policy']='PHASE5_TABLE_CELL_RECOVERY_REVIEWED'
# Acceptance tests are evaluated by their trigger and actual result; literal TST identifier spelling is not itself an independent predicate.
extra_test_proof={'PDF-00949':'GCLASS-05399','PDF-00951':'GCLASS-05535','PDF-00953':'GCLASS-00864','PDF-00962':'GCLASS-05471'}
for rows in [J,E]:
 for x in rows:
  sid=(x.get('origin_source_ids') or [None])[0]
  if sid in extra_test_proof:
   c=oldG[extra_test_proof[sid]];ev={**c['representative_evidence'],'class_id':rep[c['class_id']],'normalized_proposition_en':c['canonical_statement_en']}
   ids=x['origin_generated_class_ids'];
   if ev['class_id'] not in ids:ids.append(ev['class_id']);x['generated_evidence'].append(ev)
   x['predicate_check_en']='Both test trigger and exact expected outcome are retained in original source-defined acceptance rows; a full outcome is not inferred from the trigger alone.';x['specific_reason_en']=x['predicate_check_en'];x['coverage_mode']='CONJUNCTIVE_BRIDGE';x['entailment_grade']='E2'

write('04_atomic_judgments_final.jsonl',J);write('03_canonical_universe_final.jsonl',J);write('03_evidence_matches_final.jsonl',E);write('03_fn_root_cause_audit_final.jsonl',ROOT)
# New phase5 corrections are additive to the existing atomization/source coverage deltas.
D=read(O/'07_change_delta.jsonl');
for a in merges:D.append({'change_type':'RAW_GENERATED_CLASS_MERGE','old_class_ids':a['old_class_ids'],'new_class_id':a['new_class_id'],'reason_en':a['reason_en'],'generated_evidence':a['evidence']})
for k,sid in restored.items():D.append({'change_type':'GENERATED_ELIGIBILITY_REINSTATED','generated_class_id':k,'source_id':sid,'reason_en':'An original-file definitive commitment was erroneously excluded while being used as TP evidence. Restored after PDF verification.','generated_evidence':oldG[k]['representative_evidence']})
for k,oid,f,l,cell,col,key,stmt,qt,sid in new_cells:D.append({'change_type':'GENERATED_TABLE_CELL_ATOM_ADDED','generated_class_id':k,'generated_occurrence_id':oid,'source_id':sid,'reason_en':'A confirmed field/status in a headed table row was omitted by Phase-2 extraction; contextual table-cell reconstruction.','generated_evidence':oldG[k]['representative_evidence']})
for i,(sid,api,line,code,path) in enumerate(status_cells):D.append({'change_type':'GENERATED_TABLE_CELL_ATOM_ADDED','generated_class_id':f'GCLASS-{6533+i:05d}','source_id':sid,'reason_en':'Confirmed API HTTP result recovered from original headed table cell; corrected prior TP evidence which lacked numeric outcome.','generated_evidence':oldG[f'GCLASS-{6533+i:05d}']['representative_evidence']})
for cid,reason in exclude.items():D.append({'change_type':'GENERATED_ELIGIBILITY_REVIEW','old_class_id':cid,'new_class_ids':[],'reason_en':reason,'generated_evidence':[oldG[cid]['representative_evidence']]})
write('07_change_delta.jsonl',D)
# Rich individual raw class audit, including unchanged and still-low-signal classes.
audit=[]
for v in newV:
 ev=v['generated_evidence'];qt=v.get('source_evidence',[])
 audit.append({'generated_class_id':v['generated_class_id'],'validity_label':v['validity_label'],'support_confidence_category':v['support_confidence_category'],'generated_evidence':ev,'best_pdf_source_evidence':qt[:2], 'pdf_evidence_complete_predicate_review':'NOT_CERTIFIED' if v['semantic_certification']=='NOT_VERIFIED' else 'BEST_EFFORT','review_disposition':'MAINTAIN_PHASE4_WITH_UNCERTAINTY','reason_en':v['phase5_claim_audit_en']})
write('05_generated_class_reaudit_final.jsonl',audit)
count=sum(x['occurrence_count'] for x in newG);dup=count-len(newG);w=sum(x['within_file_excess'] for x in dups);b=sum(x['across_file_excess'] for x in dups)
metrics={'protocol_version':'6.1','prefix':'fullload','phase':5,'status':'PHASE_COMPLETED_BEST_EFFORT','eligible_generated_occurrences':count,'unique_generated_claim_classes':len(newG),'duplicate_excess_occurrences':dup,'duplicate_rate':dup/count,'within_file_excess':w,'across_file_excess':b,'repeated_claim_class_count':sum(x['occurrence_count']>=2 for x in dups),'cross_file_repeated_class_count':sum(x['spans_multiple_files'] for x in dups if x['occurrence_count']>=2),'phase4_generated_occurrences':len(read(P/'oriondesk_phase4/02_generated_atoms_phase4_eligible.jsonl')),'phase4_generated_classes':5986,'additional_nondefinitive_exclusions':len(exclude),'erroneous_phase4_exclusions_reinstated':len(restored),'missing_table_cells_recovered':len(new_cells)+len(status_cells),'reviewed_semantic_merge_groups':len(groups),'class_identity_merges':sum(len(g)-1 for g in groups),'structural_consistency':dup==w+b,'precision_note':'Raw class duplication only, never the canonical TP+FP denominator.'}
assert metrics['structural_consistency'];(O/'05_duplicate_metrics_final.json').write_text(json.dumps(metrics,indent=2)+'\n')
(O/'05_duplicate_metrics_final.md').write_text('# Phase 5 — Semantic Duplication (Best-Effort)\n\n| Measure | Result |\n|---|---:|\n'+ '\n'.join(f'| {k} | {v} |' for k,v in metrics.items() if isinstance(v,(int,float)))+ '\n\nOnly the same full-predicate claim was merged. Similar API paths or distinct data field targets were not merged. The class inventory remains conservatively under-merged; this is not a certified semantic-duplication rate.\n')
print(json.dumps(metrics,indent=2))
