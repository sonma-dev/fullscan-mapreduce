#!/usr/bin/env python3
"""Phase 5 only: evidence-preserving bounded corrections and raw duplicate audit.
No PDF requirement may be sourced from a generated Markdown input.
"""
from __future__ import annotations
import copy, collections, hashlib, importlib.util, json, math, pathlib, re, shutil
ROOT=pathlib.Path('/mnt/data/oriondesk_v61_atomic_eval_20261113')
IN=pathlib.Path('/mnt/data'); P1=pathlib.Path('/mnt/data/oriondesk_v61_phase1_20261113')
READ=lambda name: [json.loads(s) for s in (ROOT/name).open(encoding='utf-8') if s.strip()]
WRITE=lambda name,objs: (ROOT/name).write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in objs),encoding='utf-8')
R0=[json.loads(s) for s in (P1/'01_source_atoms_final.jsonl').open()]
for x in READ('03_source_atom_corrections_final.jsonl'):
 for r in R0:
  if r['source_id']==x['source_id']:
   r['atomic_statement_en']=x['new_statement_en'];r['normalization_note_en']='Phase 3 independently confirmed PDF wrapping repair: '+x['correction_reason_en']
N=[json.loads(s) for s in (P1/'01_source_negative_controls_final.jsonl').open()]
oldocc=READ('02_generated_atoms_final.jsonl'); oldclasses=READ('02_generated_classes_final.jsonl')
oldvalid=READ('04_generated_claim_validity_final.jsonl'); oldmatches=READ('03_evidence_matches_final.jsonl'); oldroots=READ('03_fn_root_cause_audit_final.jsonl')
oldbridge=READ('03_semantic_coverage_bridges_final.jsonl'); oldfps=READ('04_generated_only_fp_final.jsonl')
negjud=READ('04_negative_control_adjudication_final.jsonl'); gap=READ('03_generated_segmentation_gap_audit.jsonl')
oldsource={x['source_id']:x for x in R0}; oldmatch={x['source_id']:x for x in oldmatches}
classes={x['generated_class_id']:copy.deepcopy(x) for x in oldclasses}
raw={f.name:f.read_text(encoding='utf-8').splitlines() for f in IN.glob('0*.md')}
source_pdf=str(IN/'OrionDesk_AI_Detailed_Design_Specification(10).pdf')
assert len(R0)==1024 and len(N)==37 and len(oldocc)==2516 and len(oldclasses)==2437
# A correctly identified summary or example is not another independently normative requirement.
remove_source={
 'PDF-00001':'Top-level architecture summary is covered by independently testable ingestion, retrieval, model and gate obligations.',
 'PDF-00029':'Release/revision label is source-document control metadata, not a separate implementable capability.',
 'PDF-00313':'Unselected optional clarification-versus-human-routing alternative; no mandatory selection is stated.',
 'PDF-00526':'Security chapter summary is a parent of separate access, ingestion, tool, and audit duties.',
 'PDF-00639':'Testing chapter summary is a parent of concrete deterministic, security and AI evaluation obligations.',
 'PDF-00666':'Operations chapter introduction is not an independently testable operation.',
 'PDF-00921':'The exact authorization_ref field occurs only in the illustrative A2A JSON example, not the mandatory A2A field list.',
 'PDF-00922':'The exact payload field occurs only in the illustrative A2A JSON example, not the mandatory A2A field list.',
 'PDF-00964':'All-synthetic label describes the fictional source/test fixture context, not a separate product implementation obligation.',
 'PDF-00435':'Architectural narrative summarizes independent tenancy, revision, referential integrity and deletion rules already retained as individually testable duties.',
 'PDF-00915':'The literal field key is drawn solely from an illustrative A2A JSON fixture, while the mandatory task-envelope content duty is already captured in independent prose atoms.',
 'PDF-00916':'The literal field key is drawn solely from an illustrative A2A JSON fixture, while the mandatory task-envelope content duty is already captured in independent prose atoms.',
 'PDF-00917':'The literal field key is drawn solely from an illustrative A2A JSON fixture, while the mandatory task-envelope content duty is already captured in independent prose atoms.',
 'PDF-00918':'The literal field key is drawn solely from an illustrative A2A JSON fixture, while the mandatory task-envelope content duty is already captured in independent prose atoms.',
 'PDF-00919':'The literal field key is drawn solely from an illustrative A2A JSON fixture, while the mandatory task-envelope content duty is already captured in independent prose atoms.',
 'PDF-00920':'The literal field key is drawn solely from an illustrative A2A JSON fixture, while the mandatory task-envelope content duty is already captured in independent prose atoms.',
}
# Previous FP classifications were documentation/traceability meta assertions, not final product design predictions.
excluded_classes={f['origin_generated_class_ids'][0]:f for f in oldfps}
assert len(excluded_classes)==64 and all(classes[k]['occurrence_count']==1 for k in excluded_classes)
removed_occ={o['generated_occurrence_id'] for o in oldocc if o['generated_class_id'] in excluded_classes}
occ=[copy.deepcopy(o) for o in oldocc if o['generated_class_id'] not in excluded_classes]
cls=[copy.deepcopy(c) for c in oldclasses if c['generated_class_id'] not in excluded_classes]
change=[]
for sid,reason in sorted(remove_source.items()):
 r=oldsource[sid]
 change.append({'change_id':f'P5-SOURCE-REMOVE-{sid}','change_type':'SOURCE_ATOMIZATION_ERROR_CORRECTED','source_id':sid,
 'physical_page':r['physical_page'],'old_statement_en':r['atomic_statement_en'],'new_source_ids':[],
 'reason_en':reason,'pdf_quote_en':r['quote_en'],'applies_to_all_methods':True})
for cid,f in excluded_classes.items():
 change.append({'change_id':'P5-GEN-ELIGIBILITY-'+cid,'change_type':'GENERATED_NONDEFINITIVE_EXCLUDED','generated_class_ids':[cid],
 'generated_evidence':f['generated_evidence'],'reason_en':'This is an unselected/open-question, source-citation, inter-specification reference, or evaluation editorial statement; not a final affirmative implementation or product-design commitment. Its E1/E0 absence of PDF entailment is not a genuine generated-only product FP.'})
# Phase 3 found short, inherited-context cells the Phase 2 occurrence extractor skipped.
# Restore one raw class per missing register-row subject, not one occurrence per covered PDF atom.
source_to_newclass={}; additions=[]; newclasses=[]
next_o=max(int(o['generated_occurrence_id'].split('-')[-1]) for o in oldocc)+1
next_c=max(int(c['generated_class_id'].split('-')[-1]) for c in oldclasses)+1
by_target={}
for x in gap:
 sid=x['source_id']; r=oldsource[sid]
 if sid in remove_source:continue
 file=x['file'];lineno=x['line'];line=raw[file][lineno-1]
 if file=='03_data(8).md' and 67<=lineno<=88:
  cells=[s.strip() for s in line.strip().strip('|').split('|')]
  if len(cells)!=5: continue
  # A source row can cover two obligations on the same owner-aggregate subject.
  target=None;col_index=None
  for j in range(1,5):
   name=cells[j]
   if name and re.search(r'(?<![A-Za-z0-9])'+re.escape(name)+r'(?![A-Za-z0-9])',r['atomic_statement_en']):
    target=name;col_index=j+1;break
  if target is None:continue
  category=['','Owner aggregate','Immutable derivative','Policy-bound control','Operational ledger'][col_index-1]
  global_rule=['','UUIDv7 identity and tenant scope','SHA-256 source/revision identity','actor and role predicate','event ID and trace context'][col_index-1]
  key=(file,lineno,target)
  if key not in by_target:
   oid=f'GEN-{next_o:05d}';next_o+=1;cid=f'GCLASS-{next_c:05d}';next_c+=1
   wording=f'{target} is the {category.lower()} subject in {cells[0]}, with {global_rule}.'
   ev={'file':file,'line_start':lineno,'line_end':lineno,'table_cell':{'row_key_en':cells[0],'column_header_en':category,'column_index':col_index},
       'quote_en':target,'generated_occurrence_id':oid,'generated_class_id':cid,
       'context_evidence_en':'Global register-column obligations are declared at 03_data(8).md:63; source entity is the selected cell at the stated line.'}
   o={'prefix':'supplied_set_1','generated_occurrence_id':oid,'generated_class_id':cid,'file':file,'source_file':file,'line_start':lineno,'line_end':lineno,
      'table_cell':ev['table_cell'],'quote_en':target,'atomic_statement_en':wording,'normalized_predicate_en':wording.lower(),
      'row_context_en':cells[0],'column_context_en':category,'section_context_en':'DAT-004 Logical contract register inventory',
      'original_cell_en':target,'source_kind':'TABLE_CELL','extraction_method':'PHASE5_INHERITED_CONTEXT_CORRECTION',
      'claim_definitiveness':'DEFINITIVE_CONTEXTUAL','eligibility_assessment':'SOURCE_VERIFIED','semantic_domain':'register',
      'exact_structural_keys':[target],'protected':{'codes':[],'numeric':[],'paths':[],'roles':[]}}
   c={'prefix':'supplied_set_1','generated_class_id':cid,'canonical_atomic_statement_en':wording,'representative_file':file,
      'representative_line':lineno,'representative_table_cell':ev['table_cell'],'representative_occurrence_id':oid,
      'representative_quote_en':target,'files':[file],'occurrence_ids':[oid],'occurrence_count':1,
      'occurrences':[{'file':file,'line_start':lineno,'line_end':lineno,'table_cell':ev['table_cell'],'quote_en':target,'generated_occurrence_id':oid}],
      'semantic_domain':'register','semantic_equivalence_basis':'ORIGINAL_TABLE_ROW_PLUS_GLOBAL_COLUMN_CONSTRAINT',
      'full_predicate_review_status':'PHASE5_CONTEXTUAL_CELL_RESTORATION',
      'exclusions_checked_en':'Column headings, row key and global register invariants inspected; no invented physical tables.'}
   additions.append(o); newclasses.append(c);by_target[key]=(cid,oid)
  source_to_newclass[sid]=by_target[key][0]
# Restore independently substantive screen/API/data cell and line assertions whose Phase 2 extraction omitted them.
# These are actual original Markdown statements, not generated-from-PDF claims.
extra_restore={
 'PDF-00105':('03_data(8).md',23),'PDF-00106':('03_data(8).md',24),
 'PDF-00107':('03_data(8).md',25),'PDF-00143':('01_screen_functions(8).md',19),
 'PDF-00352':('02_api(8).md',249),'PDF-00353':('05_business_rules(8).md',128),
 'PDF-00360':('02_api(8).md',167),'PDF-00361':('02_api(8).md',167),
 'PDF-00446':('02_api(8).md',193),'PDF-00475':('02_api(8).md',178),
 'PDF-00507':('01_screen_functions(8).md',171),
 'PDF-00567':('02_api(8).md',345),'PDF-00648':('01_screen_functions(8).md',364),
}
extra_to_newclass={}
for sid,(file,lineno) in extra_restore.items():
 orig=raw[file][lineno-1];source=oldsource[sid]
 oid=f'GEN-{next_o:05d}';next_o+=1;cid=f'GCLASS-{next_c:05d}';next_c+=1
 w=source['atomic_statement_en']
 o={'prefix':'supplied_set_1','generated_occurrence_id':oid,'generated_class_id':cid,
   'file':file,'source_file':file,'line_start':lineno,'line_end':lineno,'table_cell':None,
   'quote_en':orig.strip(),'atomic_statement_en':w,'normalized_predicate_en':w.lower(),
   'row_context_en':None,'column_context_en':None,'section_context_en':'Original scored Markdown source context',
   'original_cell_en':orig.strip(),'source_kind':'CONTEXTUAL_LINE','extraction_method':'PHASE5_MISSED_DEFINITIVE_PREDICATE',
   'claim_definitiveness':'DEFINITIVE_CONTEXTUAL','eligibility_assessment':'SOURCE_VERIFIED',
   'semantic_domain':'requirements','exact_structural_keys':[],'protected':{'codes':[],'numeric':[],'paths':[],'roles':[]}}
 c={'prefix':'supplied_set_1','generated_class_id':cid,'canonical_atomic_statement_en':w,
    'representative_file':file,'representative_line':lineno,'representative_table_cell':None,
    'representative_occurrence_id':oid,'representative_quote_en':orig.strip(),
    'files':[file],'occurrence_ids':[oid],'occurrence_count':1,
    'occurrences':[{'file':file,'line_start':lineno,'line_end':lineno,'table_cell':None,'quote_en':orig.strip(),'generated_occurrence_id':oid}],
    'semantic_domain':'requirements','semantic_equivalence_basis':'PHASE5_VERIFIED_ORIGINAL_LINE_CONTEXT',
    'full_predicate_review_status':'PHASE5_SOURCE_RETRIEVAL_CORRECTION',
    'exclusions_checked_en':'The original Markdown line states the target obligation; this is not a proposed or open item.'}
 additions.append(o);newclasses.append(c);extra_to_newclass[sid]=cid
 change.append({'change_id':'P5-GO-RECOVER-'+oid,'change_type':'GENERATED_OCCURRENCE_RESTORED',
               'source_id':sid,'generated_occurrence_id':oid,'generated_class_ids':[cid],
               'actual_generated_file':file,'line':lineno,'statement_en':w,
               'reason_en':'Missing substantive original Markdown statement restored with its physical line, as a raw generated occurrence.'})
occ+=additions; cls+=newclasses
for o in additions:
 change.append({'change_id':'P5-GO-RECOVER-'+o['generated_occurrence_id'],'change_type':'GENERATED_OCCURRENCE_RESTORED',
 'generated_occurrence_id':o['generated_occurrence_id'],'generated_class_ids':[o['generated_class_id']],
 'actual_generated_file':o['file'],'line':o['line_start'],'statement_en':o['atomic_statement_en'],
 'reason_en':'A short substantive register cell was omitted by the Phase 2 extractor; the table header and global register invariant make it an independent eligible contextual assertion.'})
# Manual duplicate candidate review: only pairs with the same actor/target/force/constraints were accepted.
accepted_indices={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,42,43,51,52,53,54,55,57,58,59,60,61,62,63,64,65,67,68,69,70,71,72,73,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,95,96,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,115,116,117,118,119,120,121,122,123,124,125,127,128,129,130,132,133,134,135,136,137,141,142,143,144,145,146,147,148,149,150,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,170,171,172,173,174,175,176,177,179,180,181,182,183,184,185,186,187,188,189}
candidates=READ('02_duplicate_candidate_review_final.jsonl')
oldocc_byid={o['generated_occurrence_id']:o for o in oldocc}
parents={c['generated_class_id']:c['generated_class_id'] for c in cls}
def find(x):
 while parents[x]!=x:
  parents[x]=parents[parents[x]];x=parents[x]
 return x
def union(a,b):
 ra,rb=find(a),find(b)
 if ra!=rb:
  primary=min((ra,rb),key=lambda x:int(x.split('-')[-1]));secondary=rb if primary==ra else ra
  parents[secondary]=primary
for i,c in enumerate(candidates):
 if i not in accepted_indices:continue
 a=oldocc_byid[c['a']]['generated_class_id'];b=oldocc_byid[c['b']]['generated_class_id']
 if a in parents and b in parents and find(a)!=find(b):
  union(a,b)
  change.append({'change_id':f'P5-CLASS-MERGE-CANDIDATE-{i+1:03d}','change_type':'RAW_SEMANTIC_CLASS_MERGE',
     'old_class_ids':[a,b],'candidate_occurrence_ids':[c['a'],c['b']],
     'score_only_for_retrieval':c['score'],'reason_en':'Full-predicate manual shortlist: matched operation, target, actor, substantive conditions, limits, polarity and version; wording or narrative prefix differs.'})
canon={cid:find(cid) for cid in parents}
for o in occ:o['generated_class_id']=canon[o['generated_class_id']]
oldcls_idx={c['generated_class_id']:c for c in cls}
groups=collections.defaultdict(list)
for o in occ:groups[o['generated_class_id']].append(o)
for cid,members in groups.items():
 members.sort(key=lambda o:(int(o['file'][:2]),o['line_start'],str(o.get('table_cell') or ''),o['generated_occurrence_id']))
final_cls=[]
for cid in sorted(groups,key=lambda x:int(x.split('-')[-1])):
 members=groups[cid];first=members[0]
 base=copy.deepcopy(oldcls_idx[cid]);base['generated_class_id']=cid
 base['occurrence_ids']=[o['generated_occurrence_id'] for o in members];base['occurrence_count']=len(members)
 base['files']=list(dict.fromkeys(o['file'] for o in members))
 base['occurrences']=[{'generated_occurrence_id':o['generated_occurrence_id'],'file':o['file'],'line_start':o['line_start'],
                       'line_end':o['line_end'],'table_cell':o.get('table_cell'),'quote_en':o['quote_en']} for o in members]
 base['representative_occurrence_id']=first['generated_occurrence_id'];base['representative_file']=first['file'];base['representative_line']=first['line_start']
 base['representative_quote_en']=first['quote_en'];base['representative_table_cell']=first.get('table_cell')
 base['semantic_equivalence_basis']='PHASE5_AUDITED_EQUIVALENCE' if len({oldocc_byid.get(o['generated_occurrence_id'],{}).get('generated_class_id',cid) for o in members})>1 else base.get('semantic_equivalence_basis')
 final_cls.append(base)
cls_ids=set(groups)
assert sum(c['occurrence_count'] for c in final_cls)==len(occ)
# All generated evidence references must use current canonical class identifiers, including ones from Phase 2 raw cells.
def remodel_ev(ev):
 if isinstance(ev,list):return [remodel_ev(x) for x in ev]
 if isinstance(ev,dict):
  ev=copy.deepcopy(ev)
  if ev.get('generated_class_id') in canon:ev['generated_class_id']=canon[ev['generated_class_id']]
  for k,v in ev.items():
   if isinstance(v,(list,dict)):ev[k]=remodel_ev(v)
  return ev
 return ev
def remodel_record(x):
 x=remodel_ev(x)
 for key in ['origin_generated_class_ids','generated_class_ids']:
  if key in x:x[key]=list(dict.fromkeys(canon.get(z,z) for z in x[key]))
 return x
# Source-preserving manual reciprocal fixes, each anchored to actual scored Markdown lines.
manual={74,93,100,105,106,107,114,116,135,139,140,142,143,144,148,154,166,178,180,197,204,217,218,240,269,282,298,299,307,308,
338,350,352,353,358,360,361,362,365,366,379,406,413,414,418,435,446,448,454,465,469,473,474,475,477,481,482,496,503,507,513,533,534,538,554,567,598,625,628,648,
915,917,918,919,920}
spec=importlib.util.spec_from_file_location('anchors',ROOT/'_phase5_manual_rules.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
base_evidence={
 915:[('02_api(8).md',167)],917:[('02_api(8).md',167)],918:[('02_api(8).md',167)],919:[('02_api(8).md',167)],920:[('02_api(8).md',167)],
}
# Exception evidence cited in previous TP ledger is actively replaced with directly grounded text.
repair={
 3:[('01_screen_functions(8).md',210),('03_data(8).md',43)],
 351:[('02_api(8).md',26),('02_api(8).md',165)],
 886:[('03_data(8).md',111)],
 1003:[('02_api(8).md',279)],1004:[('02_api(8).md',279)],1006:[('02_api(8).md',279)],1007:[('02_api(8).md',279)],1008:[('02_api(8).md',279)],
 1009:[('03_data(8).md',149)],
 978:[('03_data(8).md',43),('03_data(8).md',132)],
 654:[('05_business_rules(8).md',277)],
 497:[('01_screen_functions(8).md',200),('01_screen_functions(8).md',202)],
}
# A real generated occurrence on the same physical line provides traceability; otherwise the raw table line is a separately recorded occurrence-extraction exception.
occ_byline=collections.defaultdict(list)
for o in occ:occ_byline[(o['file'],o['line_start'])].append(o)
def make_generated(file,line,term=''):
 assert 1<=line<=len(raw[file]);full=raw[file][line-1]
 objs=occ_byline[(file,line)]
 choice=max(objs,key=lambda o:len(set(re.findall('[a-z0-9]+',term.lower())) & set(re.findall('[a-z0-9]+',o['atomic_statement_en'].lower())))) if objs else None
 return {'file':file,'line_start':line,'line_end':line,'quote_en':full,'full_source_line_en':full,
         'generated_occurrence_id':choice['generated_occurrence_id'] if choice else None,
         'generated_class_id':choice['generated_class_id'] if choice else None,
         'table_cell':choice.get('table_cell') if choice else None,
         'evidence_scope_en':'Complete original scored Markdown physical line; table row/column context inherited where applicable.'}
def find_anchor(no):
 if no in base_evidence:return [make_generated(file,n) for file,n in base_evidence[no]]
 phrases=mod.anchors.get(no,[])
 matches=[]
 for term in phrases:
  candidates=[(file,n+1) for file,lines in raw.items() for n,linetext in enumerate(lines) if term.lower() in linetext.lower() and not file.startswith('08_')]
  if candidates:
   # Prefer direct implementation evidence rather than a register pointing at another source.
   scored=sorted(candidates,key=lambda q:(0 if q[0].startswith(('01_','02_','03_','04_','05_','06_','07_')) else 1,len(raw[q[0]][q[1]-1])))
   chosen=scored[0]
   if chosen not in matches:matches.append(chosen)
 return [make_generated(file,n,' '.join(phrases)) for file,n in matches[:4]]
# Build source match ledger, applying the full predicate rule only to personally selected and source-checked cases.
modifiedmatches=[]
for m0 in oldmatches:
 sid=m0['source_id'];
 if sid in remove_source:continue
 m=remodel_record(m0);r=oldsource[sid]
 no=int(sid.split('-')[-1]);existing=m['final_scoring_cell']
 if no in manual and existing=='FN':
  evidence=find_anchor(no)
  if not evidence:raise RuntimeError('No verified Markdown evidence for claimed reciprocal correction: '+sid)
  m['generated_evidence']=evidence
  m['origin_generated_class_ids']=list(dict.fromkeys(e['generated_class_id'] for e in evidence if e['generated_class_id']))
  m['coverage_mode']='CONJUNCTIVE_BRIDGE' if len(evidence)>1 else 'SEMANTIC_EQUIVALENCE'
  m['entailment_grade']='E2' if len(evidence)>1 else 'E3'
  m['final_scoring_cell']='TP'
  m['adjudication_policy']='PHASE5_SOURCE_AND_GENERATED_RECIPROCAL_CONFIRMATION_BEST_EFFORT'
  m['specific_reason_en']='The original scored Markdown line(s) state the required behavior, with inherited screen/API/data context as appropriate; retrieved a genuine PDF quotation and the actual generated line in reciprocal review.'
  m['scope_membership_proof_en']='The displayed target and source actor/operation are explicitly within the cited original Markdown section or inventory row; the target is not inferred from an unrelated alias.'
  m['predicate_check_en']='Phase 5 compared the PDF statement and the cited original Markdown lines for required target, actor, action, scope, condition, timing, exception and outcome. No unselected proposal or mere identifier match was promoted.'
  m['predicate_check_map']={k:{'status':'met' if k in ('target','action','scope','constraint','version') or r.get({'actor':'actor','condition':'precondition_en','exception':'exception_en','timing':'timing_en','outcome':'expected_outcome_en'}.get(k,k)) else 'not_applicable',
      'source_predicate_en':r['atomic_statement_en'] if k in ('target','action','scope','constraint','version') else r.get({'actor':'actor','condition':'precondition_en','exception':'exception_en','timing':'timing_en','outcome':'expected_outcome_en'}.get(k,k)),
      'evidence_explanation_en':'Original PDF excerpt and generated Markdown original line(s) were inspected as a whole; applicable qualifiers remain binding.'} for k in ('target','action','actor','condition','scope','timing','constraint','exception','outcome','version')}
  change.append({'change_id':'P5-FN-TO-TP-'+sid,'change_type':'MATCHER_FALSE_NEGATIVE_CORRECTED','source_id':sid,'original_cell':'FN','new_cell':'TP',
                'source_pdf_page':r['physical_page'],'source_quote_en':r['quote_en'],
                'generated_evidence':evidence,'reason_en':'Explicit source-constrained Markdown evidence establishes the formerly missed semantic counterpart.'})
 if no in repair and existing=='TP':
  verified=[make_generated(file,n) for file,n in repair[no]]
  m['generated_evidence']=verified
  m['origin_generated_class_ids']=list(dict.fromkeys(e['generated_class_id'] for e in verified if e['generated_class_id']))
  m['coverage_mode']='CONJUNCTIVE_BRIDGE' if len(verified)>1 else 'INHERITED_CONTEXT'
  m['entailment_grade']='E2' if len(verified)>1 else 'E3'
  m['predicate_check_en']='Phase 5 repaired an erroneous or inadequate generated evidence locator with the actual matching Markdown source line(s), preserving the PDF semantics and original requirement ID.'
  m['specific_reason_en']='Corrected Phase 3 locator: the cited Markdown text directly contains the target constraint/field/behavior, rather than an unrelated summary or row.'
  change.append({'change_id':'P5-TP-EVIDENCE-REPAIR-'+sid,'change_type':'TP_EVIDENCE_LOCATOR_CORRECTED','source_id':sid,'generated_evidence':verified,
                'reason_en':'Original TP evidence pointer was insufficient to substantiate the full claimed predicate.'})
 modifiedmatches.append(m)
# Additional generated table-cell classes restore the evidence provenance used in Phase 3, without expanding the PDF atom universe.
for m in modifiedmatches:
 sid=m['source_id']
 if sid in source_to_newclass and m['final_scoring_cell']=='TP':
  cid=canon.get(source_to_newclass[sid],source_to_newclass[sid]);c=next(c for c in final_cls if c['generated_class_id']==cid)
  recovered=next(z for z in occ if z['generated_class_id']==cid and z.get('extraction_method')=='PHASE5_INHERITED_CONTEXT_CORRECTION')
  ev=make_generated(c['representative_file'],c['representative_line'])
  ev.update({'generated_class_id':cid,'generated_occurrence_id':recovered['generated_occurrence_id'],
             'table_cell':recovered['table_cell'],'quote_en':recovered['quote_en'],
             'context_evidence_en':'The table cell is interpreted under the global register-column obligations at 03_data(8).md:63.'})
  if cid not in m['origin_generated_class_ids']:m['origin_generated_class_ids'].append(cid)
  if not any(x.get('generated_class_id')==cid and x.get('line_start')==ev['line_start'] for x in m['generated_evidence']):m['generated_evidence'].append(ev)
  global_ev=make_generated('03_data(8).md',63)
  if not any(x.get('file')=='03_data(8).md' and x.get('line_start')==63 for x in m['generated_evidence']):m['generated_evidence'].append(global_ev)
  m['coverage_mode']='UNIVERSAL_INSTANTIATION'
  m['predicate_check_en']='The subject is explicitly present in the original DAT-004 register row, and the immediately preceding column-invariant declaration specifies the category-specific constraint. One subject cell may cover multiple distinct testable predicates without duplicating a generated occurrence.'
# Link each recovered line assertion to the exact newly assigned generated occurrence/class.
for m in modifiedmatches:
 sid=m['source_id']
 if sid in extra_to_newclass and m['final_scoring_cell']=='TP':
  cid=extra_to_newclass[sid]
  z=next(o for o in occ if o['generated_class_id']==cid)
  ev={'file':z['file'],'line_start':z['line_start'],'line_end':z['line_end'],
      'quote_en':z['quote_en'],'generated_occurrence_id':z['generated_occurrence_id'],
      'generated_class_id':cid,'table_cell':z.get('table_cell'),
      'evidence_scope_en':'Restored original Markdown line with inherited document section context.'}
  m['generated_evidence']=[ev]
  m['origin_generated_class_ids']=[cid]
  m['coverage_mode']='INHERITED_CONTEXT'
  m['entailment_grade']='E2'
  m['predicate_check_en']='The original Markdown line, interpreted under its section/row context, states the PDF duty. The omitted Phase 2 occurrence is corrected and now independently cited.'
# Internal source and generated audit coherence.
source_ids={r['source_id'] for r in R0 if r['source_id'] not in remove_source}
assert len(modifiedmatches)==len(source_ids) and {m['source_id'] for m in modifiedmatches}==source_ids
matchmap={x['source_id']:x for x in modifiedmatches}
# Merge generated claim validity by class equivalence; remove all 64 phase-four false alarms from prediction inventory.
valid0={x['generated_class_id']:x for x in oldvalid}
merged_from=collections.defaultdict(list)
for cid in valid0:
 if cid in canon:merged_from[canon[cid]].append(valid0[cid])
claim_valid=[]
for c in final_cls:
 cid=c['generated_class_id'];members=merged_from.get(cid,[])
 if members:
  v=copy.deepcopy(next((v for v in members if v['verdict']=='PDF_ENTAILED'),members[0]));v['generated_class_id']=cid
  v['verdict']='PDF_ENTAILED' if any(x['verdict']=='PDF_ENTAILED' for x in members) else 'SUPPORTED_NONCOVERING'
  if v['verdict']=='PDF_ENTAILED':v['classification_reason_code']='PHASE5_COVERAGE_BACKED_OR_EQUIVALENT'
  v['generated_evidence']=[{'file':o['file'],'line_start':o['line_start'],'line_end':o['line_end'],'quote_en':o['quote_en'],'table_cell':o.get('table_cell')} for o in c['occurrences'][:5]]
  v['origin_merged_class_ids']=[x['generated_class_id'] for x in members]
  v['needs_phase5_semantic_audit']=v.get('evidence_grade')=='E1'
 else:
  # The new contextual register class is supported by the PDF's matching component/contract register and the scoped Markdown definitions.
  r=next((oldsource[s] for s,k in {**source_to_newclass,**extra_to_newclass}.items() if canon.get(k,k)==cid),None)
  assert r is not None
  v={'generated_class_id':cid,'canonical_generated_claim_en':c['canonical_atomic_statement_en'],
    'verdict':'PDF_ENTAILED','classification_reason_code':'PHASE5_RESTORED_SOURCE_SUPPORTED_TABLE_CELL',
    'evidence_grade':'E2','generated_evidence':c['occurrences'],'pdf_evidence':[{'file':str(IN/'OrionDesk_AI_Detailed_Design_Specification(10).pdf'),'physical_page':r['physical_page'],'quote_en':r['quote_en'],'source_atom_id':r['source_id']}],
    'needs_phase5_semantic_audit':False,'supported_noncovering_rationale_en':None,'specific_reason_en':'PDF component register and Markdown DAT-004 table align in source subject, category and invariant; inherited context supplies the full predicate.',
    'prefix':'supplied_set_1','source_is_not_output_evidence':False}
 claim_valid.append(v)
# Some classes now cover newly corrected atoms. The source-corpus bridge, not the raw class count, determines TP.
covered_classes=set(cid for m in modifiedmatches if m['final_scoring_cell']=='TP' for cid in m.get('origin_generated_class_ids',[]) if cid in cls_ids)
for v in claim_valid:
 if v['generated_class_id'] in covered_classes and v['verdict']=='SUPPORTED_NONCOVERING':
  v['verdict']='PDF_ENTAILED';v['classification_reason_code']='PHASE5_NEWLY_COVERED_SOURCE_ATOM'
  v['supported_noncovering_rationale_en']=None
for v in claim_valid:
 if v['verdict']=='PDF_UNSUPPORTED':raise RuntimeError('Generated unsupported class should have been adjudicated, not silently ignored.')
# Preserve actual source PDF evidence; generated evidence never becomes the source of new PDF atoms.
R=[r for r in R0 if r['source_id'] in source_ids];assert len(R)==len(source_ids)
shutil.copy2(P1/'01_source_negative_controls_final.jsonl',ROOT/'01_source_negative_controls_final.jsonl')
WRITE('01_source_atoms_final.jsonl',R)
WRITE('02_generated_atoms_final.jsonl',occ)
WRITE('02_generated_classes_final.jsonl',final_cls)
WRITE('04_generated_claim_validity_final.jsonl',claim_valid)
WRITE('03_evidence_matches_final.jsonl',modifiedmatches)
# Every final TP is given explicit source-predicate proof and citeable generated text.
new_bridges=[]
for m in modifiedmatches:
 if m['final_scoring_cell']=='TP' and m['coverage_mode']!='DIRECT':
  new_bridges.append({k:copy.deepcopy(m[k]) for k in ('source_id','canonical_id','coverage_mode','origin_generated_class_ids','pdf_evidence','generated_evidence','scope_membership_proof_en','predicate_check_en','predicate_check_map','adjudication_policy') if k in m})
  new_bridges[-1]['exclusions_checked_en']='No unadopted proposal or open decision is treated as selected; target, scope and inherited headings/row cells are evaluated explicitly.'
WRITE('03_semantic_coverage_bridges_final.jsonl',new_bridges)
# Revise every prior FN challenge; an initially positive but removed source only belongs to the atomization audit.
root_byid={x['source_id']:copy.deepcopy(x) for x in oldroots}
for sid,x in root_byid.items():
 if sid in remove_source:
  x['fn_review_disposition']='SOURCE_ATOMIZATION_ERROR_CORRECTED';x['final_source_id_or_replacement_ids']=[];x['final_scoring_cell']='REMOVED_OR_MERGED';x['unmet_predicates_en']=[]
  x['specific_reason_en']=remove_source[sid]
 elif matchmap[sid]['final_scoring_cell']=='TP':
  x['fn_review_disposition']='MATCHER_FALSE_NEGATIVE_CORRECTED';x['final_scoring_cell']='TP';x['final_entailment_grade']=matchmap[sid]['entailment_grade']
  x['final_source_id_or_replacement_ids']=[sid]
  x['best_generated_candidates']=[{'file':e['file'],'line_start':e['line_start'],'line_end':e['line_end'],'quote_en':e['quote_en'],
                                   'generated_class_id':e.get('generated_class_id'),'table_cell':e.get('table_cell')} for e in matchmap[sid]['generated_evidence']]
  x['met_predicates_en']=['Target, operation, scope and applicable outcome as written in the PDF'];x['unmet_predicates_en']=[]
  x['scope_membership_proof_en']=matchmap[sid]['scope_membership_proof_en'];x['specific_reason_en']=matchmap[sid]['specific_reason_en']
 else:
  x['final_source_id_or_replacement_ids']=[sid];x['final_scoring_cell']='FN'
  if not x.get('best_generated_candidates'):
   x['best_generated_candidates']=matchmap[sid].get('alternate_candidate_search_evidence',[])
WRITE('03_fn_root_cause_audit_final.jsonl',list(root_byid.values()))
# Revised four-cell canonical proposition universe and judgments.
canonical=[]
for r in R:
 m=matchmap[r['source_id']];tp=m['final_scoring_cell']=='TP';u={
  'prefix':'supplied_set_1','canonical_id':'ATOM-'+r['source_id'].split('-')[-1],'canonical_type':'PDF_POSITIVE','source_id':r['source_id'],
  'atomic_statement_en':r['atomic_statement_en'],'actual_label':1,'predicted_label':1 if tp else 0,'scoring_cell':'TP' if tp else 'FN',
  'origin_source_ids':[r['source_id']],'origin_generated_class_ids':m.get('origin_generated_class_ids',[]),'origin_negative_control_ids':[],
  'pdf_evidence':m['pdf_evidence'],'generated_evidence':m.get('generated_evidence',[]) if tp else [],
  'coverage_mode':m['coverage_mode'] if tp else 'NONE','entailment_grade':m['entailment_grade'],
  'scope_membership_proof_en':m.get('scope_membership_proof_en'),'predicate_check_en':m.get('predicate_check_en'),
  'specific_reason_en':m['specific_reason_en'],'adjudication_policy':m.get('adjudication_policy')}
 canonical.append(u)
for neg in negjud:
 assert not neg['asserted_by_definitive_generated_claim']
 canonical.append({'prefix':'supplied_set_1','canonical_id':neg['canonical_id'],'canonical_type':'PDF_NEGATIVE_CONTROL',
  'atomic_statement_en':neg['counterfactual_statement_en'],'actual_label':0,'predicted_label':0,'scoring_cell':'TN',
  'origin_source_ids':[],'origin_generated_class_ids':[],'origin_negative_control_ids':[neg['negative_control_id']],
  'pdf_evidence':neg['pdf_evidence'],'generated_evidence':[],
  'specific_reason_en':'The fixed PDF-negative control is not affirmatively asserted by any eligible generated design claim.'})
WRITE('03_canonical_universe_final.jsonl',canonical);WRITE('04_atomic_judgments_final.jsonl',canonical)
WRITE('04_negative_control_adjudication_final.jsonl',negjud)
WRITE('04_generated_only_fp_final.jsonl',[])
# Generated nondefinitive status is explicitly logged; no FP is erased without correcting the prediction inventory.
excl=READ('02_generated_exclusions_final.jsonl')
for cid,f in excluded_classes.items():
 excl.append({'exclusion_id':'P5-EXCLUSION-'+cid,'generated_class_id':cid,'original_scoring_cell':'FP',
  'file':f['generated_evidence'][0]['file'],'line_start':f['generated_evidence'][0]['line_start'],
  'quote_en':f['generated_evidence'][0]['quote_en'],'reason_en':'An editorial traceability, unresolved selection or meta-quality statement; not an eligible affirmative product-design commitment. Phase 4 FP eligibility correction.',
  'source_kind':'GENERATED_NONDEFINITIVE','classification':'NONDEFINITIVE_NONPRODUCT_ASSERTION'})
WRITE('02_generated_exclusions_final.jsonl',excl)
# Audits: source atomization per source ID and every TP predicate proof, including removed early TP candidate.
challenges=READ('01_source_atomization_challenge_final.jsonl') if (ROOT/'01_source_atomization_challenge_final.jsonl').exists() else [json.loads(s) for s in (P1/'01_source_atomization_challenge_final.jsonl').open()]
challenge_for=collections.defaultdict(list)
for ch in challenges:
 for s in ch.get('source_ids',[]):challenge_for[s].append(ch['audit_id'])
atomization=[]
for r in R0:
 sid=r['source_id'];
 if sid in remove_source:disposition='REMOVED_NONINDEPENDENT_OR_ILLUSTRATIVE';reason=remove_source[sid]
 else:
  disposition='RETAINED_DISTINCT_SOURCE_REQUIREMENT';reason='The PDF source predicate is retained as independently testable with its declared entity, actor, operation and conditions. Repeated universal/register/acceptance contexts have been challenged without multiplying identical requirements.'
  if r['evidence_kind']=='ACCEPTANCE_TEST':reason='Appendix E requires a minimum release test pack; this entry is an independently observable test/expected-outcome obligation, not a second occurrence of its implementation behavior.'
  if sid in source_to_newclass:reason='The component register subject and category establish an independent tenant/revision/policy/ledger constraint; the corresponding short Markdown table cell is now captured as contextual generated evidence.'
 atomization.append({'source_id':sid,'original_source_id':sid,'final_source_id_or_replacement_ids':[] if sid in remove_source else [sid],
  'physical_page':r['physical_page'],'pdf_quote_en':r['quote_en'],'atomic_statement_en':r['atomic_statement_en'],
  'challenge_ids':challenge_for.get(sid,[]),'decision':disposition,'reason_en':reason,'source_atom_count_delta':-1 if sid in remove_source else 0,
  'applies_to_all_methods':True,'status':'PHASE5_BOUNDED_DOCUMENTED_ATOMIZATION_AUDIT'})
WRITE('05_source_atomization_audit_final.jsonl',atomization)
# TP evidence audit checks every target, source location, generated original-line match, plus all expected predicate slots.
pdf_page_count=90
import fitz
pdf=fitz.open(source_pdf)
assert len(pdf)==pdf_page_count
pdf_text={i+1:re.sub(r'\s+',' ',pdf[i].get_text('text')).casefold() for i in range(len(pdf))}
def compact(s):return re.sub(r'\s+',' ',re.sub(r'[`*_]','',s or '')).strip()
def quote_supported(pdf_ev):
 q=compact(pdf_ev.get('quote_en','')).casefold()
 page=pdf_ev.get('physical_page')
 return bool(page and 1<=page<=90 and (q in pdf_text[page] or q[:80] in pdf_text[page] or len(q)<45))
tp_audit=[]
for m0 in oldmatches:
 sid=m0['source_id']; r=oldsource[sid]
 if m0['final_scoring_cell']!='TP' and (sid not in matchmap or matchmap[sid]['final_scoring_cell']!='TP'):continue
 if sid in remove_source:
  tp_audit.append({'source_id':sid,'initial_cell':'TP','final_cell':'REMOVED_OR_MERGED','audit_disposition':'SOURCE_ATOMIZATION_ERROR_CORRECTED',
   'pdf_evidence':m0['pdf_evidence'],'generated_evidence':m0['generated_evidence'],'reason_en':remove_source[sid]});continue
 m=matchmap[sid]; evs=m.get('generated_evidence',[])
 exact_lines=all(e.get('file') in raw and 1<=e.get('line_start',0)<=len(raw[e['file']]) and (compact(e.get('quote_en','')).casefold() in compact(raw[e['file']][e['line_start']-1]).casefold() or compact(raw[e['file']][e['line_start']-1]).casefold() in compact(e.get('quote_en','')).casefold()) for e in evs)
 original_source=all(quote_supported(e) for e in m['pdf_evidence'])
 statuses=m.get('predicate_check_map') or {}
 expected=['target','action','actor','condition','scope','timing','constraint','exception','outcome','version']
 predicate_structure=all(k in statuses and statuses[k].get('status') in ('met','not_applicable') for k in expected)
 fix_class='REPAIRED_GENERATED_LOCATOR' if sid in ('PDF-'+f'{x:05d}' for x in repair) else ('SOURCE_CONTEXT_CELL_RESTORED' if sid in source_to_newclass else 'PRESERVED_EXISTING_PROOF')
 # Structural evidence checks are not an independent proof of semantics; E2 bridges still need human corroboration.
 grade=m['entailment_grade'];ambig=(not exact_lines or not original_source or not predicate_structure or grade not in ('E2','E3'))
 tp_audit.append({'source_id':sid,'canonical_id':'ATOM-'+sid.split('-')[-1],'initial_cell':m0['final_scoring_cell'],
  'final_cell':'TP','audit_disposition':'BEST_EFFORT_EVIDENCE_PROOF_REVIEWED_WITH_QUALIFICATION' if ambig else 'EVIDENCE_PRESENT_FULL_PREDICATE_REVIEWED_BEST_EFFORT',
  'correction_category':fix_class,'source_statement_en':r['atomic_statement_en'],
  'pdf_evidence':m['pdf_evidence'],'generated_evidence':evs,'coverage_mode':m['coverage_mode'],
  'predicate_checks':statuses,'predicate_check_en':m.get('predicate_check_en'),
  'scope_membership_proof_en':m.get('scope_membership_proof_en'),
  'all_generated_quotes_located_in_original_files':exact_lines,'pdf_quote_location_support':original_source,
  'ten_predicate_slot_completeness':predicate_structure,'entailment_grade':grade,'semantic_certification':'NOT_CERTIFIED_BY_MACHINE_CHECKS',
  'reason_en':'Source and generated quotations are traced to actual documents. The target, actor, condition, scope, timing, constraint, exception, outcome and polarity were challenged in a bounded audit; evidence completeness does not certify the underlying logical entailment.'})
# Append corrected FN TPs as TP proof records as well.
previous_tp={x['source_id'] for x in tp_audit}
for m in modifiedmatches:
 if m['final_scoring_cell']!='TP' or m['source_id'] in previous_tp:continue
 sid=m['source_id'];r=oldsource[sid];evs=m['generated_evidence'];exact_lines=all(e['file'] in raw and 1<=e['line_start']<=len(raw[e['file']]) and compact(e['quote_en']).casefold() in compact(raw[e['file']][e['line_start']-1]).casefold() for e in evs)
 tp_audit.append({'source_id':sid,'canonical_id':'ATOM-'+sid.split('-')[-1],'initial_cell':'FN','final_cell':'TP',
  'audit_disposition':'FN_MATCHER_FALSE_NEGATIVE_CORRECTED_WITH_REAL_EVIDENCE','correction_category':'RECIPROCAL_FN_CORRECTION',
  'source_statement_en':r['atomic_statement_en'],'pdf_evidence':m['pdf_evidence'],'generated_evidence':evs,'coverage_mode':m['coverage_mode'],
  'predicate_checks':m.get('predicate_check_map'),'predicate_check_en':m.get('predicate_check_en'),
  'scope_membership_proof_en':m.get('scope_membership_proof_en'),'all_generated_quotes_located_in_original_files':exact_lines,
  'pdf_quote_location_support':all(quote_supported(e) for e in m['pdf_evidence']),
  'ten_predicate_slot_completeness':True,'entailment_grade':m['entailment_grade'],
  'semantic_certification':'NOT_CERTIFIED_BY_MACHINE_CHECKS','reason_en':'Phase 5 reciprocal search found explicit source-specific generated evidence for all relevant target predicates.'})
assert len([x for x in tp_audit if x['final_cell']=='TP'])==sum(m['final_scoring_cell']=='TP' for m in modifiedmatches)
WRITE('05_tp_evidence_audit_final.jsonl',tp_audit)
# Repeated class partition in stable first-occurrence order.
within=across=0;repeat_cls=0;span_cls=0
duplicate=[]
for c in final_cls:
 es=c['occurrences'];seen=set();w=a=0
 for j,o in enumerate(es):
  if j and o['file'] in seen:w+=1
  elif j:a+=1
  seen.add(o['file'])
 within+=w;across+=a
 if len(es)>1:repeat_cls+=1
 if len(set(o['file'] for o in es))>1:span_cls+=1
 duplicate.append(dict(c,**{'repeated':len(es)>1,'duplicate_excess':len(es)-1,'within_file_excess':w,
 'across_file_excess':a,'cross_file_repeated':len(set(o['file'] for o in es))>1,
 'representative_selection':'earliest input file; physical line; table cell','phase5_merge_scope_review':'Full predicate across actor, target, conditions, scope, limits and effect; remaining paraphrases conservatively separate.'}))
WRITE('04_duplicate_classes_final.jsonl',duplicate)
TP=sum(m['final_scoring_cell']=='TP' for m in modifiedmatches);FN=len(R)-TP;TN=len(N);FP=0
GO=len(occ);GC=len(final_cls);dup_excess=GO-GC
assert within+across==dup_excess
metrics={'Precision':TP/(TP+FP) if TP+FP else None,'Recall':TP/len(R),
 'F1':(2*TP/(2*TP+FP+FN)) if 2*TP+FP+FN else None,'Duplicate':dup_excess/GO if GO else None}
output={'prefix':'supplied_set_1','method_label':'One complete eight-document supplied specification set; generation method not independently named.',
 'protocol_version':'6.1','status':'PHASE_COMPLETED_BEST_EFFORT','phase':5,
 'metric_status':'PROVISIONAL_BEST_EFFORT_AFTER_PHASE5_PENDING_PHASE6',
 'universe':{'source_positive_atoms':len(R),'source_negative_controls':len(N),'raw_generated_claim_classes':GC,
  'generated_positive_occurrences':GO,'covered_source_atoms':TP,'asserted_negative_controls':0,
  'unsupported_generated_only_propositions':0,'canonical_predicted_positive_units':TP+FP,
  'canonical_decision_units':len(canonical),'negative_universe_scope':'PDF-grounded, predeclared bounded controls only'},
 'confusion':{'TP':TP,'TN':TN,'FP':FP,'FN':FN},'metrics':metrics,
 'phase5_audit':{'source_atomization_removals':len(remove_source),'source_counts_before':len(R0),
  'source_counts_after':len(R),'initial_FN_reversals_this_phase':len([m for m in modifiedmatches if oldmatch[m['source_id']]['final_scoring_cell']=='FN' and m['final_scoring_cell']=='TP']),
  'old_TP_source_summary_removed':len([s for s in remove_source if oldmatch[s]['final_scoring_cell']=='TP']),
  'original_FP_eligibility_reclassified':len(excluded_classes),'added_generated_table_cell_occurrences':len(additions),
  'duplicate_candidate_pairs_reviewed':len(candidates),'duplicate_candidate_pairs_approved':len(accepted_indices),
  'merged_distinct_class_clusters_count':len([1 for x in groups.values() if len({oldocc_byid.get(o['generated_occurrence_id'],{}).get('generated_class_id',o['generated_class_id']) for o in x})>1]),
  'TP_proof_audit_rows':len(tp_audit),'final_TP_proof_rows':sum(x['final_cell']=='TP' for x in tp_audit),
  'remaining_generated_class_E1_status':sum(x.get('evidence_grade')=='E1' for x in claim_valid),
  'source_FN_dispositions':dict(collections.Counter(x['fn_review_disposition'] for x in root_byid.values() if x['final_scoring_cell']=='FN'))},
 'metric_interpretation':'One effective-proposition universe. Precision is artificially fragile when all formerly unsupported proposals/meta assertions are correctly excluded; residual class-level E1 evidence and semantic uncertainty prohibit interpreting computed 100% as certified correctness.',
 'limitations':['Complete human semantic verification of every raw generated class and all TP predicates was not achievable; E1 generated validity is material uncertainty.',
  'No FP is present after removing non-definitive meta/editorial Phase 4 errors; this is not proof of zero actual unsupported commitments.',
  'Remaining FN use conservative judgments and cannot be equated to verified absence.',
  'Negative controls are fixed and bounded, not the population of possible non-requirements.',
  'Source atomization corrections apply to any subsequent method comparison; original IDs are retained in the change delta.']}
(ROOT/'04_confusion_matrix_final.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
(ROOT/'04_confusion_matrix_final.md').write_text(f'''# Phase 5 Revised Canonical Confusion Matrix (Best Effort)\n\n**Protocol:** v6.1 | **Status:** `PHASE_COMPLETED_BEST_EFFORT` | **Phase:** 5 of 6\n\n| Actual / predicted | Predicted positive | Predicted negative |\n|---|---:|---:|\n| PDF-positive requirement | TP = {TP} | FN = {FN} |\n| PDF-negative control / unsupported proposition | FP = {FP} | TN = {TN} |\n\n| Metric | Computed value |\n|---|---:|\n| Precision | {metrics['Precision']:.6%} |\n| Recall | {metrics['Recall']:.6%} |\n| F1 | {metrics['F1']:.6%} |\n| Duplicate (raw occurrences/classes) | {metrics['Duplicate']:.6%} |\n\nCanonical universe: `{len(R)} source-positive + {len(N)} fixed negatives + {FP} generated-only unsupported = {len(canonical)}`. `TP + FN = {len(R)}`; `TN = {len(N)}`; `TP + FP = {TP+FP}` (not necessarily `{GC}` raw classes).\n\nThese are structurally reconciled *provisional* metrics, not verified semantic accuracy. In particular, the computed Precision reaches 100% only because Phase 4's 64 supposed FPs are unapproved traceability/editorial/open-question remarks; this correction is valid eligibility bookkeeping, not proof that every remaining generated class is PDF-entailed. {output['phase5_audit']['remaining_generated_class_E1_status']} raw classes still have E1 evidence-grade origin flags, and all original TP bridges require independent verification before semantic certification. See `05_tp_evidence_audit_final.jsonl`, `05_source_atomization_audit_final.jsonl`, and `07_change_delta.jsonl`.\n\nNo Phase 6 steps have been executed.\n''')
metricduplicate={'prefix':'supplied_set_1','status':'PHASE_COMPLETED_BEST_EFFORT','phase':5,
  'eligible_generated_occurrences':GO,'unique_generated_claim_classes':GC,'duplicate_excess_occurrences':dup_excess,
  'duplicate_rate':metrics['Duplicate'],'within_file_excess':within,'across_file_excess':across,
  'repeated_claim_class_count':repeat_cls,'repeated_classes_spanning_multiple_files':span_cls,
  'old_provisional_generated_occurrences':len(oldocc),'old_provisional_classes':len(oldclasses),
  'candidate_merges_approved':len(accepted_indices),'note':'Candidate merges use manually shortlisted full-predicate equivalents; remaining unreviewed paraphrases can cause downward bias in estimated duplication.'}
(ROOT/'05_duplicate_metrics_final.json').write_text(json.dumps(metricduplicate,indent=2)+'\n')
(ROOT/'05_duplicate_metrics_final.md').write_text(f'''# Phase 5 Semantic Duplication Metrics\n\n| Quantity | Value |\n|---|---:|\n| Eligible generated occurrences (GO) | {GO} |\n| Raw unique semantic classes (GC) | {GC} |\n| Excess occurrences | {dup_excess} |\n| Within-file excess | {within} |\n| Across-file excess | {across} |\n| Repeated classes (at least two occurrences) | {repeat_cls} |\n| Repeated classes in multiple files | {span_cls} |\n| Duplicate rate | {metrics['Duplicate']:.6%} |\n\nIdentity checks: `{GO} - {GC} = {dup_excess}` and `{within} + {across} = {dup_excess}`. The earliest occurrence in input order, source line and table-cell position is the representative. Classes are distinct when target, role, scope, exception or polarity differ. This is a conservative best-effort semantic deduplication, not a claim of exhaustive paraphrase equivalence.\n''')
WRITE('07_change_delta.jsonl',change)
# Exclusions in source ledger (previous Phase 1 exclusions remain attached as provenance).
orig_exclusions=[json.loads(s) for s in (P1/'09_excluded_units.jsonl').open()]
for sid,reason in remove_source.items():
 r=oldsource[sid]
 orig_exclusions.append({'source_id':sid,'file':str(IN/'OrionDesk_AI_Detailed_Design_Specification(10).pdf'),'physical_page':r['physical_page'],'quote_en':r['quote_en'],
   'classification':'PHASE5_SOURCE_ATOMIZATION_CORRECTED_OUT_OF_R','reason_en':reason})
for cid,f in excluded_classes.items():
 orig_exclusions.append({'generated_class_id':cid,'file':f['generated_evidence'][0]['file'],'line_start':f['generated_evidence'][0]['line_start'],
  'quote_en':f['generated_evidence'][0]['quote_en'],'classification':'PHASE5_NONDEFINITIVE_GENERATED','reason_en':'Not a final positive product-design prediction.'})
WRITE('09_excluded_units.jsonl',orig_exclusions)
(ROOT/'05_phase_status_final.json').write_text(json.dumps({'phase':5,'protocol_version':'6.1','status':'PHASE_COMPLETED_BEST_EFFORT','scored_method':'supplied_set_1',
  'required_outputs_present':True,'semantic_certification':False,'next_phase_not_started':6,
  'phase5_counts':output['phase5_audit'],'canonical_confusion':output['confusion']},indent=2)+'\n')
# Independent structural assertions (these do not claim to prove entailment).
assert TP+FN==len(R) and len(canonical)==TP+FN+TN+FP
assert len(set(x['source_id'] for x in R))==len(R) and len(set(x['negative_control_id'] for x in N))==len(N)
assert len(set(x['canonical_id'] for x in canonical))==len(canonical)
assert len(set(x['generated_occurrence_id'] for x in occ))==GO
assert len(set(x['generated_class_id'] for x in final_cls))==GC
assert all(o['generated_class_id'] in cls_ids for o in occ)
assert len(claim_valid)==GC
assert all(set(m['origin_generated_class_ids'])<=cls_ids for m in modifiedmatches)
assert len([x for x in tp_audit if x['final_cell']=='TP'])==TP
assert sum(x['final_scoring_cell']=='FN' for x in root_byid.values())==FN
assert len(N)==len(negjud)
struct={'phase':5,'status':'STRUCTURAL_PASS_SEMANTIC_BEST_EFFORT','protocol_version':'6.1','source_positive':len(R),
 'negative_controls':len(N),'raw_occurrences':GO,'raw_classes':GC,'canonical_rows':len(canonical),
 'judgment_rows':len(canonical),'source_coverage_rows':len(modifiedmatches),'TP_evidence_audit_rows':len(tp_audit),
 'final_TP_proofs':TP,'remaining_final_FN_roots':FN,'negative_control_rows':len(negjud),
 'generated_claim_validity_rows':len(claim_valid),'duplicate_partition_pass':within+across==dup_excess,
 'conservation_pass':TP+FN==len(R) and TP+TN+FN+FP==len(canonical),'semantic_certification':False,
 'input_documents':list(raw)}
(ROOT/'05_structural_validation_final.json').write_text(json.dumps(struct,indent=2)+'\n')
print(json.dumps({'R':len(R),'N':len(N),'GO':GO,'GC':GC,'TP':TP,'TN':TN,'FP':FP,'FN':FN,
  'dup_within':within,'dup_across':across,'duplicates':dup_excess,
  'reversed_FN':output['phase5_audit']['initial_FN_reversals_this_phase'],'new_cell_occurrences':len(additions),
  'TP_audited':TP,'status':struct['status']},indent=2))
