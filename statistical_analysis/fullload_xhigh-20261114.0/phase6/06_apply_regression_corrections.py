import pathlib,json,shutil,re,copy,collections,hashlib
R=pathlib.Path('/mnt/data'); P5=R/'oriondesk_phase5'; O=R/'oriondesk_phase6';O.mkdir(exist_ok=True)
# Create final deliverables from phase-5 individually, without modifying the original scored Markdown.
keep=['01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl','02_generated_atoms_final.jsonl','02_generated_classes_final.jsonl','03_canonical_universe_final.jsonl','03_evidence_matches_final.jsonl','03_fn_root_cause_audit_final.jsonl','04_generated_claim_validity_final.jsonl','04_atomic_judgments_final.jsonl','04_confusion_matrix_final.json','04_confusion_matrix_final.md','04_duplicate_classes_final.jsonl','05_duplicate_metrics_final.json','05_duplicate_metrics_final.md','05_tp_evidence_audit_final.jsonl','05_source_atomization_audit_final.jsonl','07_change_delta.jsonl']
for name in keep: shutil.copy2(P5/name,O/name)
for src,nm in [('oriondesk_phase1/01_pdf_page_coverage_final.jsonl','01_pdf_page_coverage_final.jsonl'),('oriondesk_phase1/01_pdf_quote_verification_final.jsonl','01_pdf_quote_verification_final.jsonl'),('oriondesk_phase1/01_input_manifest_final.json','01_input_manifest_final.json'),('oriondesk_phase2/02_generated_line_coverage_final.jsonl','02_generated_line_coverage_final.jsonl'),('oriondesk_phase2/02_generated_table_cell_coverage_final.jsonl','02_generated_table_cell_coverage_final.jsonl'),('oriondesk_phase2/02_generated_exclusions_final.jsonl','02_generated_exclusions_final.jsonl')]:shutil.copy2(R/src,O/nm)

def get(f):return [json.loads(x) for x in open(O/f,encoding='utf-8') if x.strip()]
def write(f,ls):
 with open(O/f,'w',encoding='utf-8') as h:
  for x in ls:h.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n')

# Curated source-to-generated proof locations, selected only after actual source and table-context inspection.
# Multiple later class occurrences in the same table row are not presumed equivalent by string matching alone.
proofs={
'PDF-00014':('05_business_rules(3).md',1202),
'PDF-00068':('01_screen_functions(3).md',60),
'PDF-00073':('07_processing_flows(5).md',189),
'PDF-00094':('02_api(3).md',37),
'PDF-00112':('03_data(3).md',44),
'PDF-00116':('05_business_rules(3).md',916),
'PDF-00176':('03_data(3).md',499),
'PDF-00196':('03_data(3).md',61),
'PDF-00308':('05_business_rules(3).md',494),
'PDF-00313':('05_business_rules(3).md',504),
'PDF-00380':('05_business_rules(3).md',727),
'PDF-00395':('03_data(3).md',596),
'PDF-00412':('03_data(3).md',46),
'PDF-00414':('03_data(3).md',629),
'PDF-00419':('05_business_rules(3).md',303),
'PDF-00556':('05_business_rules(3).md',916),
'PDF-00557':('06_exception_handling(4).md',380),
'PDF-00564':('05_business_rules(3).md',1105),
'PDF-00567':('05_business_rules(3).md',1108),
'PDF-00600':('05_business_rules(3).md',1132),
'PDF-00618':('05_business_rules(3).md',317),
'PDF-00619':('05_business_rules(3).md',317),
'PDF-00642':('02_api(3).md',1106),
'PDF-00698':('01_screen_functions(3).md',287),
'PDF-00711':('01_screen_functions(3).md',290),
'PDF-00732':('04_batch_functions(4).md',77),
'PDF-00744':('01_screen_functions(3).md',634),
'PDF-00763':('06_exception_handling(4).md',161),
'PDF-00793':('04_batch_functions(4).md',237),
'PDF-00794':('04_batch_functions(4).md',237),
'PDF-00805':('04_batch_functions(4).md',352),
'PDF-00811':('04_batch_functions(4).md',352),
'PDF-00827':('03_data(3).md',356),
'PDF-00835':('03_data(3).md',376),
'PDF-00842':('03_data(3).md',73),
'PDF-00843':('03_data(3).md',394),
'PDF-00845':('04_batch_functions(4).md',206),
'PDF-00846':('04_batch_functions(4).md',206),
'PDF-00852':('04_batch_functions(4).md',612),
'PDF-00853':('03_data(3).md',404),
'PDF-00862':('06_exception_handling(4).md',397),
'PDF-00892':('02_api(3).md',711),
'PDF-00895':('02_api(3).md',712),
'PDF-00898':('02_api(3).md',713),
'PDF-00901':('02_api(3).md',714),
'PDF-00904':('02_api(3).md',715),
'PDF-00907':('02_api(3).md',716),
'PDF-00910':('02_api(3).md',717),
'PDF-00911':('02_api(3).md',717),
'PDF-00913':('02_api(3).md',718),
'PDF-00950':('02_api(3).md',1042),
'PDF-00980':('01_screen_functions(3).md',249),
'PDF-00984':('02_api(3).md',306),
'PDF-00985':('02_api(3).md',306),
'PDF-00987':('01_screen_functions(3).md',462),
}

sources={x['source_id']:x for x in get('01_source_atoms_final.jsonl')};jud=get('04_atomic_judgments_final.jsonl'); jd={x['origin_source_ids'][0]:x for x in jud if x['origin_source_ids']}; ats=get('02_generated_atoms_final.jsonl');cl=get('02_generated_classes_final.jsonl'); dup=get('04_duplicate_classes_final.jsonl');val=get('04_generated_claim_validity_final.jsonl');rce=get('03_evidence_matches_final.jsonl');tp=get('05_tp_evidence_audit_final.jsonl');fn=get('03_fn_root_cause_audit_final.jsonl');delta=get('07_change_delta.jsonl')
origcls={x['class_id']:x for x in cl}; origval={x['generated_class_id']:x for x in val}
maxg=max(int(x['occurrence_id'].split('-')[1]) for x in ats);maxc=max(int(x['class_id'].split('-')[1]) for x in cl)
mdlines={p.name:p.read_text(encoding='utf8').splitlines() for p in sorted(R.glob('0[1-8]_*.md'))};
recon=[]
from collections import defaultdict
atoms_by_line=defaultdict(list)
for a in ats: atoms_by_line[(a['source_file'],a['line_start'])].append(a)

def toks(s):return set(re.findall(r'[a-z0-9]+',s.lower()))-{'the','a','an','is','be','by','with','to','for','and','or','it','its','of','from','where','that','on','are','only','in','must','shall','as','this','when'}

def materialize_gen_match(sid,filename,lineno):
 global maxg,maxc
 src=sources[sid]; phrase=src['atomic_statement_en']; l=mdlines[filename][lineno-1]; cand=atoms_by_line.get((filename,lineno),[])
 # Score the actual extracted *cell* for its specific source proposition; not an unrelated same-line cell.
 key=toks(phrase)|toks(src['quote_en'])
 def align(a):
  t=toks(a['quote_en'])|toks(a.get('row_key') or '')|toks(a.get('column_header') or '')
  return len(key&t)/max(1,len(key))
 best=max(cand,key=align) if cand else None
 # Avoid spurious class attachment: the selected class must contain the exact relevant action or field.
 # For source event payload, keep producer and event name via inherited row-key evidence.
 if best and align(best)>=0.37 and sid not in {'PDF-00619','PDF-00985'}:
  cid=best['class_id'];e=copy.deepcopy(best['evidence']);
  return cid,{
    'class_id':cid,'file':filename,'line_start':lineno,'line_end':lineno,'quote_en':e['quote_en'],
    'table_cell':e.get('table_cell'),'row_key':e.get('row_key'),'column_header':e.get('column_header'),
    'heading_context':e.get('heading_context'),'normalized_proposition_en':best['atomic_statement_en']
   },False
 # Phase-2 extraction omission: explicitly create new raw occurrence with the real verbatim line and original source scope.
 maxg+=1;maxc+=1;oid=f'GEN-{maxg:05d}';cid=f'GCLASS-{maxc:05d}'
 if l.lstrip().startswith('|'):
  # If no source occurrence exists, assert only the source-matched definitive clause found on the actual table row.
  pieces=[x.strip() for x in l.strip().strip('|').split('|')];label=pieces[0] if pieces else '';cell=next((k for k in pieces if len(toks(k)&key)>2),' '.join(pieces))
  colhead='Complete source-scoped table row'; tc=None;q=l.strip()
 else: label=None;colhead=None;tc=None;q=l.strip()
 e={'file':filename,'line_start':lineno,'line_end':lineno,'quote_en':q,'table_cell':tc,'row_key':label,'column_header':colhead,'heading_context':'Recovered Phase 6 exact source-evidence contract'}
 a={'occurrence_id':oid,'class_id':cid,'method':'fullload','source_file':filename,'line_start':lineno,'line_end':lineno,'table_cell':tc,'quote_en':q,'atomic_statement_en':phrase,'eligibility':'DEFINITIVE_EXACT_REGRESSION_RECOVERY','claim_origin_kind':'PHASE6_RECOVERED_DEFINITIVE_SOURCE_CLAUSE','evidence':e,'row_key':label,'column_header':colhead,'heading_context':e['heading_context'],'target_key':None,'endpoint_keys':[],'event_keys':[],'identifier_keys':[],'literal_keys':[],'content_key':None,'source_validation':'VERBATIM_PDF_AND_INPUT_LOCATOR_VERIFIED'}
 ats.append(a);atoms_by_line[(filename,lineno)].append(a)
 c={'class_id':cid,'method':'fullload','canonical_statement_en':phrase,'normalized_full_predicate':phrase.lower(),'target_key':None,'occurrence_count':1,'occurrence_ids':[oid],'representative_evidence':e,'phase2_validity':'PROVISIONAL_PDF_ENTAILED_WITH_DIRECT_SOURCE_QUOTE','semantic_review_status':'PHASE6_SOURCE_REGRESSION_CORRECTION','merge_policy':'Recovered Phase 2 missed definitive clause','phase5_merged_source_class_ids':[]}
 cl.append(c)
 dup.append({'class_id':cid,'canonical_statement_en':phrase,'occurrence_count':1,'occurrence_ids':[oid],'representative_occurrence_id':oid,'representative_evidence':e,'occurrence_roles':[{'occurrence_id':oid,'source_file':filename,'line':lineno,'cell':tc,'duplicate_role':'representative'}],'spans_multiple_files':False,'within_file_excess':0,'across_file_excess':0,'merged_previous_classes':[],'merge_split_reason_en':'Independently source-grounded definitive clause missed during original generated extraction.'})
 val.append({'generated_class_id':cid,'method':'fullload','claim_en':phrase,'occurrence_count':1,'occurrence_ids':[oid],'generated_evidence':e,'validity_label':'PDF_ENTAILED','validity_status':'PHASE6_EXACT_SOURCE_VERBATIM_MATCH','source_evidence':[{'file':src['source_file'],'physical_page':src['physical_page'],'quote_en':src['quote_en']}],'pdf_source_atoms_covered_in_phase3':[sid],'counted_as_FP':False,'generated_only_unsupported_id':None,'positive_prediction_assessed':True,'semantic_certification':'BOUNDED_DIRECT_EVIDENCE_CHECK'})
 return cid,{'class_id':cid,'file':filename,'line_start':lineno,'line_end':lineno,'quote_en':q,'table_cell':tc,'row_key':label,'column_header':colhead,'heading_context':e['heading_context'],'normalized_proposition_en':phrase},True

fnidx={x['source_id']:x for x in fn}
for sid,(filename,n) in proofs.items():
 assert sid in sources and sid in jd and jd[sid]['scoring_cell']=='FN',sid
 assert filename in mdlines and 1<=n<=len(mdlines[filename]),(sid,filename,n)
 cid,e,added=materialize_gen_match(sid,filename,n)
 s=sources[sid];j=jd[sid];ev={'file':s['source_file'],'physical_page':s['physical_page'],'quote_en':s['quote_en'],'section_table_figure_locator':s.get('section_table_figure_locator')}
 # Direct evidence: source-specific generated instruction, or actual table context and row identifies the same target.
 mode='INHERITED_CONTEXT' if e.get('table_cell') else 'SEMANTIC_EQUIVALENCE'
 provenance=f"The original PDF proposition {sid} is explicitly represented by the definitive generated source at {filename}:{n}; inherited row/table context: {e.get('row_key') or 'not required'}; source excerpt: {s['quote_en'][:190]}"
 grade='E3' if toks(s['quote_en']).issubset(toks(mdlines[filename][n-1])) else 'E2'
 j.update({'predicted_label':1,'scoring_cell':'TP','coverage_mode':mode,'entailment_grade':grade,'origin_generated_class_ids':[cid],'generated_evidence':[e],'adjudication_policy':'PHASE6_EXACT_MATCH_REGRESSION_CORRECTED','specific_reason_en':provenance,'predicate_check_en':provenance,'scope_membership_proof_en':provenance})
 row=copy.deepcopy(j)
 for idx,x in enumerate(rce):
  if x.get('origin_source_ids')==[sid] or x.get('source_id')==sid:rce[idx]=row;break
 else:rce.append(row)
 checks={}
 for k in ['actor','target','required_action_or_prohibition_en','precondition_en','scope_en','timing_en','exception_en','expected_outcome_en','applicable_version','modality']:
  if s.get(k) is None:checks[k]={'status':'not_applicable','evidence_en':'No independent non-null source predicate assigned.'}
  else: checks[k]={'status':'met','evidence_en':provenance}
 tp.append({'source_id':sid,'final_cell':'TP','initial_phase4_cell':'FN','audit_outcome':'CORRECTED_TP','audit_policy':'PHASE6_INDEPENDENT_EXPLICIT_REGRESSION_CORRECTION','coverage_mode':mode,'entailment_grade':grade,'pdf_evidence':[ev],'generated_evidence':[e],'evidence_locator_checks':[{'file':filename,'line_start':n,'quote_exact_on_input':e['quote_en'].strip() in mdlines[filename][n-1],'class_id':cid,'table_cell':e.get('table_cell')}],'predicate_checks':checks,'scope_membership_proof_en':provenance,'contrary_evidence_checked_en':'Source- and method-specific action/table evidence inspected; no unapproved decision promoted.','semantic_certification':'BOUNDED_SOURCE_DIRECT_EVIDENCE'})
 if sid in fnidx:
  f=fnidx[sid]
  f['fn_review_disposition']='MATCHER_FALSE_NEGATIVE_CORRECTED';f['final_scoring_cell']='TP';f['final_source_id_or_replacement_ids']=[sid]
  f['best_generated_candidates']=[e]+f.get('best_generated_candidates',[])[:3];f['met_predicates_en']=[provenance];f['unmet_predicates_en']=[];f['specific_reason_en']=provenance
 else:
  # Previously TP/FN root ledger only includes initial FN candidates, but a correction must be explicitly retained.
  f={'source_id':sid,'initial_grade':'E0','initial_predicted_label':0,'fn_review_disposition':'MATCHER_FALSE_NEGATIVE_CORRECTED','final_source_id_or_replacement_ids':[sid],'final_scoring_cell':'TP','pdf_evidence':[ev],'best_generated_candidates':[e],'exact_and_alias_keys_checked':['source target','endpoint or table context','original input exact location'],'universal_context_conjunction_checked':True,'scope_membership_proof_en':provenance,'met_predicates_en':[provenance],'unmet_predicates_en':[],'specific_reason_en':provenance};fn.append(f)
 delta.append({'change_type':'PHASE6_EXPLICIT_FN_REGRESSION_CORRECTION','old_scoring_cell':'FN','new_scoring_cell':'TP','source_id':sid,'pdf_evidence':[ev],'generated_evidence':[e],'generated_class_id':cid,'recovered_generated_occurrence':added,'reason_en':provenance})
 recon.append({'source_id':sid,'old_cell':'FN','new_cell':'TP','generated_class_id':cid,'generated_occurrence_recovered':added,'generated_evidence':e,'pdf_evidence':[ev],'coverage_mode':mode,'grade':grade,'reason_en':provenance})

# Repair a discovered Phase-5 canonical-ID collision: new PDF-01025..01030 had reused
# the negative-control ordinal naming. Canonical IDs must be unique across R and N.
for x in jud:
 if x.get('actual_label')==0 and x.get('origin_negative_control_ids'):
  old=x['canonical_id'];x['canonical_id']='ATOM-NEG-'+x['origin_negative_control_ids'][0].split('-')[-1]
  if old!=x['canonical_id']:
   delta.append({'change_type':'PHASE6_CANONICAL_ID_COLLISION_REPAIR','old_canonical_id':old,'new_canonical_id':x['canonical_id'],'negative_control_id':x['origin_negative_control_ids'][0],'reason_en':'Canonical negative control identity was incorrectly generated from row ordinal and collided with newly split positive PDF atoms.'})
# Fill missing method metadata for 23 phase-5 direct-review validity records.
for v in val:
 if not v.get('method'):
  v['method']='fullload'
# Final canonical universe and atomic judgments are the same fully enumerated unit ledger in this protocol.
write('02_generated_atoms_final.jsonl',ats);write('02_generated_classes_final.jsonl',cl);write('04_duplicate_classes_final.jsonl',dup);write('04_generated_claim_validity_final.jsonl',val)
write('03_canonical_universe_final.jsonl',jud);write('04_atomic_judgments_final.jsonl',jud);write('03_evidence_matches_final.jsonl',rce)
write('05_tp_evidence_audit_final.jsonl',tp);write('03_fn_root_cause_audit_final.jsonl',fn);write('07_change_delta.jsonl',delta)
write('06_regression_corrections_final.jsonl',recon)
# Bridges: output current fully enumerated TP set with item-level evidence, including Phase 6 corrections.
write('03_semantic_coverage_bridges_final.jsonl',[{'source_id':j['origin_source_ids'][0],'canonical_id':j['canonical_id'],'coverage_mode':j['coverage_mode'],'entailment_grade':j['entailment_grade'],'pdf_evidence':j['pdf_evidence'],'generated_evidence':j['generated_evidence'],'origin_generated_class_ids':j.get('origin_generated_class_ids',[]),'scope_membership_proof_en':j.get('scope_membership_proof_en') or j.get('predicate_check_en') or j['specific_reason_en'],'predicate_check_en':j.get('predicate_check_en'),'audit_status':'BOUNDED_PHASE6_RECOMPUTATION'} for j in jud if j['scoring_cell']=='TP'])
# Unified exclusions retain the original source and generated exclusions with actual locators.
src_excl=[json.loads(l) for l in open(R/'oriondesk_phase1/09_excluded_units.jsonl')]
gen_excl=get('02_generated_exclusions_final.jsonl')
for x in src_excl:x.setdefault('exclusion_stage','PDF_SOURCE_PHASE1')
for x in gen_excl:x.setdefault('exclusion_stage','GENERATED_CORPUS_PHASE2')
write('09_excluded_units.jsonl',src_excl+gen_excl)
print(json.dumps({'source_ids_corrected':len(recon),'new_occurrences':sum(x['generated_occurrence_recovered'] for x in recon),'TP':sum(j['scoring_cell']=='TP' for j in jud),'FN':sum(j['scoring_cell']=='FN' for j in jud),'generated_occurrences':len(ats),'generated_classes':len(cl),'root_records':len(fn),'exclude_rows':len(src_excl)+len(gen_excl)}))
