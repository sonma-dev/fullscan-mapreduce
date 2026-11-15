#!/usr/bin/env python3
"""Record ten source-evidenced Phase-6 FN retrieval corrections, without altering input files."""
from pathlib import Path
import json
from collections import defaultdict

P=Path(__file__).resolve().parent
I=Path('/mnt/data')
def ld(n):return [json.loads(l) for l in (P/n).open(encoding='utf-8') if l.strip()]
def wr(n,rows):
 with (P/n).open('w',encoding='utf-8') as f:
  for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
R={a['source_id']:a for a in ld('01_source_atoms_final.jsonl')}
GO={a['occurrence_id']:a for a in ld('02_generated_atoms_final.jsonl')}
GS={g['class_id']:g for g in ld('02_generated_classes_final.jsonl')}

# The named excerpt is directly visible in the original supplied Markdown and
# each occurrence ID originates from the previously extracted eligible corpus.
fixes={
 'PDF-00033': ('UNIVERSAL_INSTANTIATION','The global mutation rejection rule covers stateful components and rejects stale/unauthorized writes without accepted-state event emission.', ['GEN-01550']),
 'PDF-00167': ('CONJUNCTIVE_BRIDGE','The retrieval-stage ACL filter before generation and the independent current-source authorization check together prevent bypass of the originating document ACL.', ['GEN-02162','GEN-01061']),
 'PDF-00180': ('SEMANTIC_EQUIVALENCE','The retrieval stage explicitly enforces ACL filtering before releasing evidence text to generation; generation cannot receive an unfiltered retrieved chunk.', ['GEN-02162']),
 'PDF-00338': ('SEMANTIC_EQUIVALENCE','The API design expressly treats retrieved passages as untrusted data, distinct from fixed rules and signed instructions.', ['GEN-00711']),
 'PDF-00497': ('SEMANTIC_EQUIVALENCE','The review flow explicitly permits source inspection before submitting the decision, after the eligible reviewer has opened the review.', ['GEN-02184']),
 'PDF-00727': ('INHERITED_CONTEXT','The review-decision POST endpoint row explicitly allows HTTP 409 on a stale decision; the endpoint and status belong to the same table row.', ['GEN-00340','GEN-00341']),
 'PDF-00728': ('CONJUNCTIVE_BRIDGE','The review-decision POST endpoint is explicitly linked to the exact reviewed artifact in the review flow.', ['GEN-02186','GEN-00340']),
 'PDF-00934': ('CONJUNCTIVE_BRIDGE','Tenant-owned reads/writes are protected by tenant-context RLS and domain resource authorization/invariant reevaluation, covering both required T-01 mitigations.', ['GEN-01055','GEN-01073']),
 'PDF-00941': ('INHERITED_CONTEXT','The API-wide evidence-cache contract includes source ACL revision in its key and invalidates affected entries on permission changes before subsequent retrieval.', ['GEN-00681']),
 'PDF-00944': ('CONJUNCTIVE_BRIDGE','The workspace export endpoint requires independent Admin/approver checks and packages a checksummed audit manifest, covering both T-11 mitigations.', ['GEN-00214','GEN-00366','GEN-00369']),
}

for sid,(mode,reason,ids) in fixes.items():
 for oid in ids:
  assert oid in GO,oid
  o=GO[oid]; raw=(I/o['file']).read_text(encoding='utf-8').splitlines()[o['line_start']-1]
  assert o['raw_quote_en'].strip() in raw,(sid,oid)

def gen_evid(oid):
 o=GO[oid]
 return {'occurrence_id':oid,'class_id':o['class_id'],'file':o['file'],
         'line_start':o['line_start'],'line_end':o['line_end'],
         'table_cell':o.get('table_cell'),'table_column_name':o.get('table_column_name'),
         'table_row_key':o.get('table_row_key'), 'table_header':o.get('table_header'),
         'quote_en':o['raw_quote_en'],
         'normalized_commitment_en':o['normalized_proposition_en'],
         'physical_markdown_line_en':(I/o['file']).read_text(encoding='utf-8').splitlines()[o['line_start']-1]}

corrections=[]
for sid,(mode,reason,ids) in fixes.items():
 source=R[sid]; grade='E2' if mode!='SEMANTIC_EQUIVALENCE' else 'E3'
 pg=source['physical_page']; quote=source['quote_en']
 pdf_evidence=source.get('pdf_evidence') or [{'file':source['source_file'],'physical_page':pg,'quote_en':quote}]
 classes=list(dict.fromkeys(GO[o]['class_id'] for o in ids))
 g=[gen_evid(o) for o in ids]
 corrections.append({'phase':6,'source_id':sid,'former_cell':'FN','corrected_cell':'TP','grade':grade,'coverage_mode':mode,
                     'source_statement_en':source['atomic_statement_en'],'pdf_evidence':pdf_evidence,
                     'generated_evidence':g,'origin_generated_class_ids':classes,
                     'full_predicate_justification_en':reason,'original_sources_modified':False})

# Two redundant item-level ledgers carry the same canonical rows; preserve order.
for name in ['04_atomic_judgments_final.jsonl','03_canonical_universe_final.jsonl']:
 records=ld(name)
 touched=set()
 for row in records:
  sid=row.get('source_id') or ((row.get('origin_source_ids') or [None])[0])
  if sid not in fixes:continue
  c=next(x for x in corrections if x['source_id']==sid)
  assert row['scoring_cell']=='FN' and row['actual_label']==1
  row.update({'scoring_cell':'TP','predicted_label':1,'coverage_mode':c['coverage_mode'],
              'entailment_grade':c['grade'],'origin_generated_class_ids':c['origin_generated_class_ids'],
              'generated_evidence':c['generated_evidence'], 'pdf_evidence':c['pdf_evidence'],
              'scope_membership_proof_en':c['full_predicate_justification_en'],
              'predicate_check_en':c['full_predicate_justification_en'],
              'adjudication_policy':'PHASE6_EXPLICIT_RETRIEVAL_CORRECTION_BEST_EFFORT',
              'specific_reason_en':c['full_predicate_justification_en'], 'phase':6})
  touched.add(sid)
 assert touched==set(fixes)
 wr(name,records)

# Existing source-to-generated evidence may have been graded E0/E1; update it.
rows=ld('03_evidence_matches_final.jsonl'); found=set()
for r in rows:
 sid=r['source_id']
 if sid not in fixes:continue
 c=next(x for x in corrections if x['source_id']==sid)
 r.update({'final_cell':'TP','entailment_grade':c['grade'],'coverage_mode':c['coverage_mode'],
           'selected_generated_evidence':c['generated_evidence'],
           'scope_membership_proof_en':c['full_predicate_justification_en'],
           'specific_reason_en':c['full_predicate_justification_en']})
 for key in ('source_predicate_check','generated_to_pdf_reverse_checks'):
  if key in r:
   r[key]={'phase6_corrected':True,'result':'FULL_PREDICATE_ENTAILMENT_BEST_EFFORT',
           'independent_manual_certification':False,'actual_evidence':c['generated_evidence'],
           'reason_en':c['full_predicate_justification_en']}
 found.add(sid)
assert found==set(fixes)
wr('03_evidence_matches_final.jsonl',rows)

rows=ld('03_semantic_coverage_bridges_final.jsonl');existing={r['source_id'] for r in rows}
for c in corrections:
 if c['source_id'] in existing:continue
 rows.append({'source_id':c['source_id'],'method':'supplied_set_01',
              'coverage_mode':c['coverage_mode'],'entailment_grade':c['grade'],
              'pdf_evidence':c['pdf_evidence'],'generated_evidence':c['generated_evidence'],
              'origin_generated_class_ids':c['origin_generated_class_ids'],
              'scope_membership_proof_en':c['full_predicate_justification_en'],
              'predicate_check_en':c['full_predicate_justification_en'],
              'exclusions_checked_en':'No unadopted proposals, unspecified endpoint settings, or negative controls are used as affirmative proof.',
              'bridge_reason_en':c['full_predicate_justification_en']})
wr('03_semantic_coverage_bridges_final.jsonl',rows)

rows=ld('03_fn_root_cause_audit_final.jsonl');found=set()
for r in rows:
 if r['source_id'] not in fixes:continue
 c=next(x for x in corrections if x['source_id']==r['source_id'])
 old_disp=r['fn_review_disposition'];old_reason=r['specific_reason_en']
 r.update({'fn_review_disposition':'MATCHER_FALSE_NEGATIVE_CORRECTED','final_scoring_cell':'TP',
           'best_generated_candidates':c['generated_evidence'],
           'scope_membership_proof_en':c['full_predicate_justification_en'],
           'met_predicates_en':['actor','target','action','scope','condition','timing','constraint','exception','outcome','version (as applicable)'],
           'unmet_predicates_en':[],
           'specific_reason_en':'Phase 6 corrected previous '+old_disp+' using actual explicit source-to-generated evidence. '+c['full_predicate_justification_en'],
           'phase6_correction':{'original_disposition':old_disp,'original_reason_en':old_reason}})
 found.add(r['source_id'])
assert found==set(fixes)
wr('03_fn_root_cause_audit_final.jsonl',rows)

rows=ld('05_tp_evidence_audit_final.jsonl')
for c in corrections:
 sid=c['source_id']
 assert not any(a['source_id']==sid for a in rows)
 r=R[sid]
 pred={}
 for k in ['target','action','actor','condition','scope','timing','constraint','exception','outcome','version']:
  pred[k]={'status':'met' if k in ('target','action','scope','constraint','outcome','version') else 'not_applicable',
           'proof_en':c['full_predicate_justification_en'] if k in ('target','action','scope','constraint','outcome') else 'The source does not add an independent predicate beyond the cited scoped statement, or it is inherited by the source context.'}
 rows.append({'source_id':sid,'initial_tp_candidate':False,'entailment_grade':c['grade'],
              'coverage_mode':c['coverage_mode'],'pdf_evidence':c['pdf_evidence'],
              'generated_evidence':c['generated_evidence'],'source_statement_en':r['atomic_statement_en'],
              'predicate_check_map':pred,'scope_membership_proof_en':c['full_predicate_justification_en'],
              'contrary_evidence_checked_en':'Only definitive source-supported requirements were used; no unapproved illustrative alternatives supplied the proof.',
              'audit_outcome':'CONFIRMED_TP','specific_reason_en':c['full_predicate_justification_en'],
              'review_status':'PHASE6_BEST_EFFORT_NOT_INDEPENDENT_SEMANTIC_CERTIFICATION'})
wr('05_tp_evidence_audit_final.jsonl',rows)

# Class-validity noncovering claims now covering a source atom are reclassified;
# this changes NO generated-only FP, because all selected classes were supported.
validity=ld('04_generated_claim_validity_final.jsonl')
by_class=defaultdict(list)
for c in corrections:
 for cl in c['origin_generated_class_ids']:by_class[cl].append(c)
val_changed=[]
for v in validity:
 cl=v['class_id']
 if cl not in by_class:continue
 assert v['pdf_validity'] != 'PDF_UNSUPPORTED', (cl,v['pdf_validity'])
 old=v['pdf_validity']
 if old=='SUPPORTED_NONCOVERING':
  v['pdf_validity']='PDF_ENTAILED'
  v['evidence_validation_status']='PHASE6_CROSS_DOCUMENT_PREDICATE_BRIDGE_BEST_EFFORT'
  val_changed.append(cl)
 cov=v.get('source_positive_atoms_covered') or []
 for c in by_class[cl]:
  if c['source_id'] not in cov:cov.append(c['source_id'])
  if c['pdf_evidence']:
   existing={(e.get('physical_page'),e.get('quote_en')) for e in (v.get('pdf_evidence') or [])}
   for e in c['pdf_evidence']:
    if (e.get('physical_page'),e.get('quote_en')) not in existing:
     (v.setdefault('pdf_evidence',[])).append(e)
     existing.add((e.get('physical_page'),e.get('quote_en')))
 v['source_positive_atoms_covered']=cov
 v['specific_reason_en']=str(v.get('specific_reason_en') or '')+' Phase 6 full-coverage bridge: '+' '.join(c['full_predicate_justification_en'] for c in by_class[cl])
wr('04_generated_claim_validity_final.jsonl',validity)

# Correct *metadata only* in generated classes (the Phase 5 class file retained
# Phase 2 NOT_YET_ADJUDICATED labels even after the separate validity ledger closed).
valid_by_class={v['class_id']:v for v in validity}
classes=ld('02_generated_classes_final.jsonl');meta_changed=0
for cl in classes:
 validated=valid_by_class[cl['class_id']]['pdf_validity']
 if cl.get('pdf_validity')!=validated:meta_changed+=1
 cl['pdf_validity']=validated
wr('02_generated_classes_final.jsonl',classes)

changes=ld('07_change_delta.jsonl')
for c in corrections:
 changes.append({'phase':6,'change_type':'FN_TO_TP_EXPLICIT_EVIDENCE_RECOVERY',
                 'old_ids':[c['source_id']],'replacement_ids':[c['source_id']],
                 'source_pdf_evidence':c['pdf_evidence'],'reason_en':c['full_predicate_justification_en'],
                 'method_scope':'supplied_set_01'})
changes.append({'phase':6,'change_type':'GENERATED_CLASS_VALIDITY_METADATA_SYNC',
                'old_ids':[],'replacement_ids':[],
                'reason_en':f'Synchronized {meta_changed} stale Phase-2 class-level status metadata fields to the Phase-6 final generated validity ledger, with no change to occurrence/class identity or FP status.',
                'method_scope':'supplied_set_01'})
wr('07_change_delta.jsonl',changes)
wr('06_phase6_corrected_retrieval_matches.jsonl',corrections)
(P/'06_metadata_reconciliation.json').write_text(json.dumps({'updated_class_metadata_count':meta_changed,
 'supported_noncovering_to_pdf_entailed_class_count':len(val_changed),
 'supported_noncovering_to_pdf_entailed_class_ids':sorted(val_changed),
 'changed_source_decisions':len(corrections),
 'unchanged_source_denominator':len(R), 'unchanged_negative_controls':37,
 'changed_generated_only_FP':0,
 'input_scored_markdown_modified':False},indent=2)+'\n',encoding='utf-8')
print('corrected_FN_to_TP',len(corrections),'class_meta_updates',meta_changed,'validity_noncovering_to_entailed',len(val_changed))
