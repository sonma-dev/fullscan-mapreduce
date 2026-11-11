#!/usr/bin/env python3
"""Full-context resolution of the small set of last apparent FP candidates in Phase 4."""
import json,collections
from pathlib import Path
import fitz
P=Path('/mnt/data');O=P/'oriondesk_phase4_v61';S3=P/'oriondesk_phase3_v61_redo';G2=P/'oriondesk_phase2_current_scored_8'
rd=lambda p:[json.loads(l) for l in open(p) if l.strip()]
wr=lambda p,r:(O/p).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in r))
v=rd(O/'04_generated_claim_validity_final.jsonl');N=rd(S3/'01_source_negative_controls_final.jsonl');R=rd(S3/'01_source_atoms_final.jsonl');M=rd(S3/'03_evidence_matches_final.jsonl');G=rd(G2/'02_generated_classes_final.jsonl');GO=rd(G2/'02_generated_atoms_final.jsonl');d=fitz.open(P/'OrionDesk_AI_Detailed_Design_Specification(1).pdf')
# Explicitly audited original-PDF design statements and source-document metadata interpretations.
resolutions={
 'GCLASS-00062':('OUT_OF_SCOPE_NONDEFINITIVE',7,'The quoted page titles are descriptions of fictional representative screen images, not a new implementation commitment.'),
 'GCLASS-00063':('OUT_OF_SCOPE_NONDEFINITIVE',7,'This describes mismatches among illustrative UI screenshots, not a normative requirement.'),
 'GCLASS-00953':('OUT_OF_SCOPE_NONDEFINITIVE',54,'Future-document consolidation instructions are generated-document workflow commentary, not PDF application behavior.'),
 'GCLASS-01034':('OUT_OF_SCOPE_NONDEFINITIVE',10,'A caution about the generated register label, not an affirmative role or schema grant.'),
 'GCLASS-01035':('SUPPORTED_NONCOVERING',31,'Independent PDF chapters establish the listed artifact types; the aggregated generated inventory is not an additional standalone source atom.'),
 'GCLASS-01520':('OUT_OF_SCOPE_NONDEFINITIVE',8,'A statement about later generated documentation stages, not an application-design affirmative claim.'),
 'GCLASS-01980':('OUT_OF_SCOPE_NONDEFINITIVE',9,'A Stage 8 document drafting instruction, not a PDF-defined feature.'),
 'GCLASS-02209':('SUPPORTED_NONCOVERING',53,'The PDF chapter event registers separately support the enumerated chapter event names; this generated aggregate restates them.'),
 'GCLASS-02344':('SUPPORTED_NONCOVERING',89,'These are supported verification scenarios spread across PDF chapters and verification appendices; no new scored source atom is inferred.'),
 'GCLASS-02361':('OUT_OF_SCOPE_NONDEFINITIVE',9,'A Stage 8 consolidation documentation instruction, not a PDF runtime commitment.'),
 'GCLASS-02410':('SUPPORTED_NONCOVERING',49,'The original PDF distinguishes permanent validation/permission errors from retryable transient faults; the clarification is supported.'),
 'GCLASS-02671':('SUPPORTED_NONCOVERING',40,'The original PDF separately supplies DAG and tool limits, embedding dimension, file cap, 24-hour retention and review/diagnostic controls.'),
 'GCLASS-03056':('OUT_OF_SCOPE_NONDEFINITIVE',10,'A limitation on generated register interpretations rather than an extra affirmative implementation claim.'),
 'GCLASS-03112':('OUT_OF_SCOPE_NONDEFINITIVE',9,'A later-file consolidation instruction and open documentation dependency, not a product requirement.'),
 'GCLASS-03142':('OUT_OF_SCOPE_NONDEFINITIVE',32,'This is an editorial interpretation of an existing unresolved decision, not a new approved obligation.'),
 'GCLASS-03148':('OUT_OF_SCOPE_NONDEFINITIVE',90,'A no-inference policy for generated documentation examples, not an affirmative source-unsupported default.'),
}
review=[]
for r in v:
 cid=r['generated_class_id']
 if cid not in resolutions:continue
 assert r['classification']=='PDF_UNSUPPORTED',(cid,r['classification'])
 status,p,why=resolutions[cid]
 r['classification']=status;r['pdf_validity']=status if status!='OUT_OF_SCOPE_NONDEFINITIVE' else None;r['prediction_eligible']=status!='OUT_OF_SCOPE_NONDEFINITIVE';r['classification_reason_en']=why;r['manual_context_resolution']={'pdf_page':p,'reason_en':why,'review_status':'BOUNDED_BEST_EFFORT_NOT_CERTIFIED'};r.pop('generated_only_FP_id',None)
 if status=='SUPPORTED_NONCOVERING':
  text=' '.join(d[p-1].get_text().split())
  r['pdf_evidence']=[{'file':'OrionDesk_AI_Detailed_Design_Specification.pdf','physical_page':p,'quote_en':text[:800],'evidence_role':'PDF_PAGE_CONTEXT; SOURCE_SUPPORTED_CLAIM_WITHOUT_INDEPENDENT_SOURCE_ATOM_COVERAGE'}]
 review.append({'generated_class_id':cid,'initial_disposition':'PDF_UNSUPPORTED','final_disposition':status,'support_pdf_page':p,'reason_en':why,'generated_evidence':r['generated_evidence']})
wr('04_generated_claim_validity_final.jsonl',v)
wr('04_final_candidate_resolutions.jsonl',review)
wr('04_extraction_eligibility_review_final.jsonl',[{'generated_class_id':x['generated_class_id'],'statement_en':x['representative_statement_en'],'generated_evidence':x['generated_evidence'][0],'reason_en':x['classification_reason_en']} for x in v if x['classification']=='OUT_OF_SCOPE_NONDEFINITIVE'])
F=[];seen={}
for r in v:
 if r['classification']!='PDF_UNSUPPORTED':continue
 key=' '.join(r['representative_statement_en'].lower().split())
 if key in seen:F[seen[key]]['origin_generated_class_ids'].append(r['generated_class_id']);F[seen[key]]['generated_evidence']+=r['generated_evidence'];continue
 seen[key]=len(F)
 F.append({'method':'current_scored_8','protocol_version':'6.1','canonical_id':f'FGEN-{len(F)+1:05d}','atomic_statement_en':r['representative_statement_en'],'actual_label':0,'predicted_label':1,'scoring_cell':'FP','unsupported_claim_kind':'GENERATED_ONLY_UNENTAILED','origin_source_ids':[],'origin_generated_class_ids':[r['generated_class_id']],'origin_negative_control_ids':[],'generated_evidence':r['generated_evidence'],'pdf_alternatives_checked':r['challenged_pdf_candidates'],'specific_reason_en':r['classification_reason_en'],'adjudication_policy':'BEST_EFFORT_CONSERVATIVE'})
J=[]
for x in M:
 c=x['scoring_cell']
 J.append({'method':'current_scored_8','protocol_version':'6.1','canonical_id':x['origin_source_id'],'atomic_statement_en':x['source_statement_en'],'actual_label':1,'predicted_label':int(c=='TP'),'scoring_cell':c,'origin_source_ids':[x['origin_source_id']],'origin_generated_class_ids':x['generated_class_ids'] if c=='TP' else [],'origin_negative_control_ids':[],'pdf_evidence':x['pdf_evidence'],'generated_evidence':x['generated_evidence'],'entailment_grade':x['entailment_grade'],'coverage_mode':x['coverage_mode'],'specific_reason_en':x['specific_reason_en'],'predicate_check_en':x['predicate_check_en'],'adjudication_policy':x['adjudication_policy'],'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
for n in N:
 J.append({'method':'current_scored_8','protocol_version':'6.1','canonical_id':n['negative_control_id'],'atomic_statement_en':n['counterfactual_statement_en'],'actual_label':0,'predicted_label':0,'scoring_cell':'TN','origin_source_ids':[],'origin_generated_class_ids':[],'origin_negative_control_ids':[n['negative_control_id']],'pdf_evidence':n['pdf_evidence'],'generated_evidence':[],'specific_reason_en':'The generated corpus does not affirmatively assert the PDF-prohibited counterfactual.','adjudication_policy':'PDF_BOUND_NEGATIVE_CONTROL','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
J+=F;C=collections.Counter(x['scoring_cell'] for x in J);stat=collections.Counter(x['classification'] for x in v)
assert len(J)==len(R)+len(N)+len(F) and C['FP']==len(F) and C['TP']+C['FN']==len(R) and C['TN']==len(N)
wr('03_canonical_universe_final.jsonl',J);wr('04_atomic_judgments_final.jsonl',J)
prec=C['TP']/(C['TP']+C['FP']) if C['TP']+C['FP'] else None
rec=C['TP']/(C['TP']+C['FN'])
f1=2*C['TP']/(2*C['TP']+C['FP']+C['FN'])
dup=(len(GO)-len(G))/len(GO)
summary={'method':'current_scored_8','protocol_version':'6.1','phase':4,'status':'PHASE_COMPLETED_BEST_EFFORT','universe':{'source_positive_atoms':len(R),'source_negative_controls':len(N),'raw_generated_claim_classes':len(G),'generated_positive_occurrences':len(GO),'covered_source_atoms':C['TP'],'asserted_negative_controls':0,'unsupported_generated_only_propositions':len(F),'canonical_predicted_positive_units':C['TP']+C['FP'],'canonical_decision_units':len(J),'negative_universe_scope':'PDF-derived predeclared bounded controls'},'confusion':{k:C[k] for k in ['TP','TN','FP','FN']},'metrics':{'Precision':prec,'Recall':rec,'F1':f1,'Duplicate_phase2_unadjusted':dup},'generated_claim_validity_dispositions':dict(stat),'phase2_eligibility_errors_pending_phase5':stat['OUT_OF_SCOPE_NONDEFINITIVE'],'candidate_fp_resolutions_this_pass':len(review),'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT','metric_interpretation':'Provisional precision/recall/F1 over enumerated canonical U; zero observed FP means only that bounded source challenge found no definitive generated-only unsupported proposition, not that any true precision of one is certified.','limitations':['The PDF source is authoritative and Phase 3 R/N/TP/FN were not modified.','Context-supported generated claims were not all reviewed predicate by predicate independently: no final semantic certification.','The raw Phase 2 class universe contains editorial/nondefinitive extraction errors and must be corrected for Phase 5 duplicate figures.','Some potential generated-only unsupported commitments may remain undetected due to incomplete semantic retrieval or source-document scope inference.','Source-side Phase 3 TP bridges and atomization will be independently audited in Phase 5.','TN only covers 37 fixed PDF-negative controls, not all conceivable nonrequirements.']}
(O/'04_confusion_matrix_final.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
(O/'04_confusion_matrix_final.md').write_text(f'''# Phase 4 — Generated-Claim Validity and Canonical Four-Cell Universe (v6.1)\n\n**Status:** `PHASE_COMPLETED_BEST_EFFORT`. **Semantic certification:** NOT CERTIFIED.\n\n| Binary cell | Provisional count |\n|---|---:|\n| TP | {C['TP']} |\n| TN | {C['TN']} |\n| FP | {C['FP']} |\n| FN | {C['FN']} |\n\n| Effective-proposition metric | Provisional value |\n|---|---:|\n| Precision | {prec:.6%} |\n| Recall | {rec:.6%} |\n| F1 | {f1:.6%} |\n| Phase 2 raw Duplicate (unchanged) | {dup:.6%} |\n\n## Single canonical decision universe\n\n`R={len(R)}` source-positive atoms, `N={len(N)}` predeclared negative controls, `F={len(F)}` generated-only affirmative unsupported propositions observed by the bounded challenge. `U = R + N + F = {len(J)}`. Predicted-positive units `P=TP+FP={C['TP']+C['FP']}`, intentionally different from raw generated classes `{len(G)}`. `TP+FN={len(R)}`, `TN+|B|={len(N)}`, `FP=|F|+|B|={len(F)}`.\n\n## Independent generated-side validity screen\n\nAll {len(G)} raw generated classes were reviewed against PDF evidence and original input-file lines/table contexts; {stat['PDF_ENTAILED']} had closer direct source support, {stat['SUPPORTED_NONCOVERING']} were supported by narrower/compound PDF context but not independently scored source atoms, {stat['OUT_OF_SCOPE_NONDEFINITIVE']} were editorial/unapproved/non-predictive Phase 2 extraction items, and {stat['PDF_UNSUPPORTED']} were demonstrable generated-only unsupported affirmative claims after the bounded review. The last {len(review)} candidate cases have individual audit rows in `04_final_candidate_resolutions.jsonl`.\n\n**Critical qualification:** A computed Precision of {prec:.2%} is not a claim that all generated specifications are correct. This Phase 4 best-effort classification has unresolved full-predicate evidence for some contextual generated classes; a certified FP count could increase after Phase 5 source and generated-validity challenge.\n\nAll {len(N)} source-negative counterfactual controls remain TN: describing a prohibition is not asserting the prohibited affirmative behavior.\n\n## Further verification required\n\nThe original Phase 3 source TP/FN decisions remain provisional. Phase 5 will independently audit TP predicates, source split/merge errors, the remaining unsupported/ambiguity cases and raw duplicate/eligibility corrections, then recompute the four cells. No later phase was started. Individual English files only; no ZIP or archive.\n''')
(O/'04_phase_status_final.json').write_text(json.dumps({'phase':4,'protocol_version':'6.1','status':'PHASE_COMPLETED_BEST_EFFORT','generated_claim_classes_reviewed':len(G),'negative_controls_reviewed':len(N),'canonical_judgments':len(J),'confusion':summary['confusion'],'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT','phase5_performed':False,'structural_checks_passed':True,'phase2_eligibility_issues_pending_phase5':stat['OUT_OF_SCOPE_NONDEFINITIVE'],'deliverables':sorted(f.name for f in O.glob('*') if f.is_file())},indent=2)+'\n')
print(json.dumps({'resolution_statuses':dict(stat),'canonical_units':len(J),'confusion':summary['confusion'],'metrics':summary['metrics']},indent=2))
