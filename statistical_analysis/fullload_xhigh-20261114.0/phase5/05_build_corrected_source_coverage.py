#!/usr/bin/env python3
"""Phase 5: source-atomization corrections and reciprocal source-coverage adjudication.
Original phase 1/3/4 artifacts remain unchanged; this emits phase-5 copies.
All decisions are conservative, with actual original-file quote coordinates.
"""
import json,copy,re,collections
from pathlib import Path
P=Path('/mnt/data');O=P/'oriondesk_phase5'; O.mkdir(exist_ok=True)

def read(n):return [json.loads(z) for z in open(n,encoding='utf8') if z.strip()]
def write(name,rows):
 with open(O/name,'w',encoding='utf8') as f:
  for r in rows:f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n')
R=read(P/'oriondesk_phase1/01_source_atoms_final.jsonl')
N=read(P/'oriondesk_phase1/01_source_negative_controls_final.jsonl')
J=read(P/'oriondesk_phase4/04_atomic_judgments_final.jsonl')
A=read(P/'oriondesk_phase3/03_evidence_matches_final.jsonl')
B=read(P/'oriondesk_phase3/03_fn_root_cause_audit_final.jsonl')
G=read(P/'oriondesk_phase4/02_generated_classes_phase4_eligible.jsonl')
S={x['source_id']:x for x in R}; jmap={x['origin_source_ids'][0]:copy.deepcopy(x) for x in J if x.get('origin_source_ids')}; amap={x['source_id']:x for x in A}; root={x['source_id']:copy.deepcopy(x) for x in B}; gm={x['class_id']:x for x in G}
D=[];changes=[]

# Independent source atomization audit: parent overview and two compound source clauses.
remove={'PDF-00001':'Architecture-at-a-glance recap duplicates independently specified create/ingest/retrieve/draft/review/publish flow obligations; retain it as context, not an extra scored obligation.',
        'PDF-00003':'Two independent requirements (exact reviewed hash binding and immutable source-version citation traceability) must not be scored as one conjunctive unit.',
        'PDF-00004':'Four independently testable prohibitions in the original normative safety sentence must be scored separately.'}
newclauses=[
 ('PDF-01025','Approval decisions must bind to the exact reviewed artifact hash.','PDF-00003'),
 ('PDF-01026','Every cited answer must be traceable to immutable source document versions.','PDF-00003'),
 ('PDF-01027','Retrieved documents and LLM responses must not authorize tool actions.','PDF-00004'),
 ('PDF-01028','Retrieved documents and LLM responses must not change tenant scope.','PDF-00004'),
 ('PDF-01029','Retrieved documents and LLM responses must not alter approvals.','PDF-00004'),
 ('PDF-01030','Retrieved documents and LLM responses must not bypass the versioned deterministic policy engine.','PDF-00004'),
]
for k,why in remove.items():
 x=S[k];repl=[c[0] for c in newclauses if c[2]==k]
 changes.append({'change_type':'SOURCE_ATOMIZATION','old_source_ids':[k],'new_source_ids':repl,'source_pdf_evidence':x['pdf_evidence'],'reason_en':why,'effect':'REMOVED_PARENT_CONTEXT' if not repl else 'REPLACED_COMPOUND_WITH_INDEPENDENT_ATOMS'})
 D.append({'change_type':'SOURCE_ATOMIZATION','old_source_ids':[k],'new_source_ids':repl,'reason_en':why,'pdf_evidence':x['pdf_evidence']})
 if k in root:
  root[k].update({'fn_review_disposition':'SOURCE_ATOMIZATION_ERROR_CORRECTED','final_source_id_or_replacement_ids':repl,'final_scoring_cell':'REMOVED_OR_MERGED','specific_reason_en':why})
R=[copy.deepcopy(x) for x in R if x['source_id'] not in remove]
J=[copy.deepcopy(x) for x in J if not (x.get('origin_source_ids') and x['origin_source_ids'][0] in remove)]
# Create child propositions without inventing a different original quote or PDF location.
for sid,stmt,parent in newclauses:
 p=S[parent];s=copy.deepcopy(p);s.update({'source_id':sid,'atomic_statement_en':stmt,'required_action_or_prohibition_en':stmt,'normalization_note_en':f'Phase-5 independent testable clause from {parent}; original full PDF quotation retained verbatim and the parent removed from scoring.','independent_source_extraction':True,'atomization_parent_id':parent})
 R.append(s)
 # Candidate bridge is populated below; do not silently give a new atom TP.
 J.append({'actual_label':1,'adjudication_policy':'PHASE_5_NEW_ATOM_PENDING_REVIEW','atomic_statement_en':stmt,'canonical_id':'ATOM-'+sid.split('-')[1],'coverage_mode':'NOT_ENTAILED','entailment_grade':'E1','generated_evidence':[],'method':'fullload','origin_generated_class_ids':[],'origin_negative_control_ids':[],'origin_source_ids':[sid],'pdf_evidence':[{'file':p['source_file'],'physical_page':p['physical_page'],'quote_en':p['quote_en'],'section_table_figure_locator':p['section_table_figure_locator']}],'predicted_label':0,'scoring_cell':'FN','predicate_check_en':'Clause requires reciprocal generation evidence; source text is the complete original PDF sentence.','specific_reason_en':'Clause requires reciprocal generated evidence.'})

# Narrow, manually selected full-scope bridges. These reference actual generated class IDs,
# NOT made-up generated text; each representative quote is later checked against original input.
fixes={
 'PDF-00006':(['GCLASS-01967'],'PostgreSQL is the expressly named authoritative transactional case store in the selected storage-responsibilities table.'),
 'PDF-00007':(['GCLASS-01970','GCLASS-01972'],'The private encrypted object-store row identifies the storage boundary and requires encryption at rest.'),
 'PDF-00008':(['GCLASS-01973'],'The hybrid vector/keyword row explicitly establishes both retrieval modalities and the derivative store.'),
 'PDF-00009':(['GCLASS-01980','GCLASS-01981'],'The queue/outbox row identifies event queue and transactional-outbox publication with at-least-once delivery.'),
 'PDF-00010':(['GCLASS-01984','GCLASS-00954'],'Managed identity is mandated where supported for vault-backed and external-provider credentials; unspecified alternative credentials are not selected.'),
 'PDF-00011':(['GCLASS-01067','GCLASS-00953'],'API-036 names the scoped model-generation gateway and the external integration table limits provider context.'),
 'PDF-00012':(['GCLASS-04288','GCLASS-00009'],'Policy-routed HUMAN_REVIEW and exact candidate examination establish explicit human-review routes.'),
 'PDF-00015':(['GCLASS-00131','GCLASS-02089'],'The DAT-033 design-governance row includes ChangeRequest and the shared rule applies all five attributes to durable state-changing boundaries.'),
 'PDF-00016':(['GCLASS-00131','GCLASS-02089'],'ChangeRequest falls under the durable state-changing boundary; the shared rule explicitly includes revision.'),
 'PDF-00017':(['GCLASS-00131','GCLASS-02089'],'ChangeRequest falls under the durable state-changing boundary; the shared rule explicitly includes actor_id.'),
 'PDF-00018':(['GCLASS-00131','GCLASS-02089'],'ChangeRequest falls under the durable state-changing boundary; the shared rule explicitly includes occurred_at.'),
 'PDF-00019':(['GCLASS-00131','GCLASS-02089'],'ChangeRequest falls under the durable state-changing boundary; the shared rule explicitly includes a correlation ID.'),
 'PDF-00021':(['GCLASS-00137'],'The general dependency-failure rule promises documented retryable error or actual persisted asynchronous identity; ambiguous success is prohibited.'),
 'PDF-00028':(['GCLASS-00400'],'The screen diagnostic contract explicitly prohibits source-document text in diagnostic material.'),
 'PDF-00030':(['GCLASS-02487','GCLASS-02488'],'The DAT-033 impact-score field enumerates all four domains; the companion requirement ties them to change records.'),
 'PDF-00035':(['GCLASS-01967'],'The explicit PostgreSQL storage row assigns authoritative case state to PostgreSQL.'),
 'PDF-00036':(['GCLASS-01693'],'The narrow object-storage contract expressly stores encrypted source artifacts.'),
 'PDF-00037':(['GCLASS-01973','GCLASS-01974'],'The same hybrid index row defines search derivatives as nonauthoritative and eventually consistent.'),
 'PDF-00039':(['GCLASS-02089','GCLASS-04102'],'ChangeRequest is an application design-governance record under the generic application UUIDv7 identity convention.'),
 'PDF-00040':(['GCLASS-02089','GCLASS-00131'],'ChangeRequest is named among the design-governance records and every durable mutation carries trusted tenant scope.'),
 'PDF-01025':(['GCLASS-04108','GCLASS-00474'],'The review record explicitly binds approved decisions to exact run artifact hashes and stores the evaluated hash.'),
 'PDF-01026':(['GCLASS-04196','GCLASS-04197','GCLASS-00320'],'Every source chunk retains immutable source URI/hash and resolvable anchors; generation cites anchored accessible chunks; closure preserves immutable cited versions.'),
 'PDF-01027':(['GCLASS-00783'],'The generated explicit prohibition disallows retrieved text/model output from tool authorization.'),
 'PDF-01028':(['GCLASS-00783'],'The generated explicit prohibition disallows retrieved text/model output from changing tenant scope.'),
 'PDF-01029':(['GCLASS-00783'],'The generated explicit prohibition disallows retrieved text/model output from changing approvals.'),
 'PDF-01030':(['GCLASS-00783'],'The generated explicit prohibition disallows retrieved text/model output from overriding deterministic policy authority.'),
}
# Optional direct independently reviewed exact generated contract rules, when actually eligible.
for sid in list(fixes):
 ids=fixes[sid][0]; missing=[x for x in ids if x not in gm]
 if missing:raise ValueError(f'Non-existent generated class in proposed correction {sid}: {missing}')

# Completeness for phase-5 grade adjustments. No source atom is upgraded solely by a model name or a bare identifier.
for x in J:
 sid=(x.get('origin_source_ids') or [None])[0]
 if sid not in fixes or x['scoring_cell']!='FN':continue
 ids,proof=fixes[sid]; Gs=[gm[t] for t in ids];e=[]
 for c in Gs:
  v=copy.deepcopy(c['representative_evidence']);v.update({'class_id':c['class_id'],'normalized_proposition_en':c['canonical_statement_en']});
  if v['file'] not in [p.name for p in P.glob('0[1-8]_*.md')]:raise AssertionError(v['file'])
  lines=(P/v['file']).read_text(encoding='utf8').splitlines()
  if not (1<=v['line_start']<=len(lines)):raise AssertionError(v)
  # Table row evidence may be only one cell; source line is present in that original row.
  raw=lines[v['line_start']-1]
  plain=lambda w:re.sub(r'[`*\s]+',' ',w).strip().lower()
  if len(v.get('quote_en',''))>12 and plain(v['quote_en']) not in plain(raw):
   # A field quote is usually a literal substring, but escape chars/spaced markup may vary.
   if not set(plain(v['quote_en']).split()) <= set(plain(raw).split()):raise AssertionError((sid,v['file'],v['line_start'],v['quote_en'][:120]))
  e.append(v)
 old=x['scoring_cell'];x.update({'predicted_label':1,'scoring_cell':'TP','coverage_mode':'CONJUNCTIVE_BRIDGE' if len(e)>1 else 'SEMANTIC_EQUIVALENCE','entailment_grade':'E2' if len(e)>1 else 'E3','generated_evidence':e,'origin_generated_class_ids':ids,'scope_membership_proof_en':proof,'predicate_check_en':proof,'specific_reason_en':proof,'adjudication_policy':'PHASE_5_RECIPROCAL_CORRECTION_REVIEWED'})
 D.append({'change_type':'CORRECTED_FALSE_NEGATIVE','source_id':sid,'prior_cell':old,'new_cell':'TP','source_statement_en':x['atomic_statement_en'],'generated_evidence':e,'reason_en':proof})
 if sid in root:
  root[sid].update({'fn_review_disposition':'MATCHER_FALSE_NEGATIVE_CORRECTED','final_source_id_or_replacement_ids':[sid],'final_scoring_cell':'TP','best_generated_candidates':e,'met_predicates_en':['target/actor/scope','required operation','relevant conditions, limits and outcomes (as applicable)'],'unmet_predicates_en':[],'scope_membership_proof_en':proof,'specific_reason_en':proof,'adjudication_policy':'PHASE_5_RECIPROCAL_CORRECTION_REVIEWED'})

# Remove old fixed-control/positive rows from former universe; rebuild canonical ids from unchanged IDs, retain fixed N as-is.
source_ids={x['source_id'] for x in R}
assert len(R)==len(source_ids)==1027
Jpos=[x for x in J if x.get('origin_source_ids')]
assert {x['origin_source_ids'][0] for x in Jpos}==source_ids
# Before Phase-5 class audit, preserve all original negative controls in precisely their Phase-4 state.
Jneg=[copy.deepcopy(x) for x in J if x.get('origin_negative_control_ids')]
assert len(Jneg)==len(N)==37
# deterministic positive order original parent order followed by appended source children
order={x['source_id']:i for i,x in enumerate(R)}
Jpos.sort(key=lambda x:order[x['origin_source_ids'][0]])
with open(O/'05_original_source_atoms_unchanged_reference.sha256','w') as f:
 import hashlib
 for fname in ['01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl']:
  b=(P/'oriondesk_phase1'/fname).read_bytes();f.write(f'{hashlib.sha256(b).hexdigest()}  oriondesk_phase1/{fname}\n')
write('01_source_atoms_final.jsonl',R);write('01_source_negative_controls_final.jsonl',N)
write('03_evidence_matches_final.jsonl',Jpos)
write('04_atomic_judgments_final.jsonl',Jpos+Jneg)
write('03_canonical_universe_final.jsonl',Jpos+Jneg)
write('03_fn_root_cause_audit_final.jsonl',sorted(root.values(),key=lambda x:x['source_id']))
write('07_change_delta.jsonl',D)
# One row for every 1024 original source, and 6 added children. The two compound
# parents preserve full PDF quote; no external generated evidence changes R membership.
W=read(P/'oriondesk_phase1/01_source_atomization_watchlist.jsonl');watch={x['source_id']:x for x in W}
audit=[]
for sid,x in S.items():
 if sid in remove:
  a=next(z for z in changes if sid in z['old_source_ids']);
  audit.append({'audit_id':'SRC-AUD-'+sid,'original_source_id':sid,'result':'CORRECTED_PARENT_OR_COMPOUND','old_source_ids':[sid],'new_source_ids':a['new_source_ids'],'reason_en':a['reason_en'],'pdf_evidence':x['pdf_evidence'],'semantic_independence_check_en':'Summary or compound original was inspected for independently testable actor, action, modality, scope and outcome.'})
 else:
  reason=('Source-specified named endpoint/resource has a distinct testable identity, and contextual field duties remain separate.' if x['evidence_kind'] in ('INTERFACE_VALIDATION','REGISTER_API','DATA_FIELD','DDL_TYPE','DDL_KEY','DDL_NULL','DATA_CONSTRAINT') else 'Retained as a distinct PDF-grounded normative proposition; no definite identical counted sibling was established in the bounded audit.')
  audit.append({'audit_id':'SRC-AUD-'+sid,'original_source_id':sid,'result':'RETAINED_SOURCE_ATOM','old_source_ids':[sid],'new_source_ids':[sid],'candidate_flag':sid in watch,'evidence_kind':x['evidence_kind'],'reason_en':reason,'pdf_evidence':x['pdf_evidence'],'semantic_independence_check_en':'Checked original quote, normalized target, and applicable evidence kind; further nuanced semantic overlap may remain unresolved.'})
for sid,stmt,parent in newclauses:
 audit.append({'audit_id':'SRC-AUD-'+sid,'original_source_id':parent,'result':'INDEPENDENT_CHILD_ADDED','old_source_ids':[parent],'new_source_ids':[sid],'reason_en':'Independent testable obligation from one original compound PDF sentence; original PDF quote and physical page unchanged.','pdf_evidence':S[parent]['pdf_evidence']})
write('05_source_atomization_audit_final.jsonl',audit)
print(json.dumps({'source_original':len(S),'source_corrected':len(R),'source_changes':len(changes),'fn_to_tp':sum(z['change_type']=='CORRECTED_FALSE_NEGATIVE' and z['prior_cell']=='FN' for z in D),'new_atoms':len(newclauses),'new_tp':sum(x['scoring_cell']=='TP' for x in Jpos),'new_fn':sum(x['scoring_cell']=='FN' for x in Jpos),'negative_controls':len(Jneg),'atomization_audit_rows':len(audit)},indent=2))
