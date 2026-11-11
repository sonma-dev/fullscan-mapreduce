#!/usr/bin/env python3
"""Evidence-context screening of partial source-cell fragments; final within Phase 4."""
import re,json,collections,unicodedata
from pathlib import Path
import fitz
P=Path('/mnt/data');O=P/'oriondesk_phase4_v61';G2=P/'oriondesk_phase2_current_scored_8';S3=P/'oriondesk_phase3_v61_redo'
rd=lambda f:[json.loads(l) for l in open(f) if l.strip()]
wr=lambda f,r:(O/f).write_text(''.join(json.dumps(a,ensure_ascii=False)+'\n' for a in r))
v=rd(O/'04_generated_claim_validity_final.jsonl');raw=rd(G2/'02_generated_atoms_final.jsonl');G=rd(G2/'02_generated_classes_final.jsonl');R=rd(S3/'01_source_atoms_final.jsonl');N=rd(S3/'01_source_negative_controls_final.jsonl');M=rd(S3/'03_evidence_matches_final.jsonl');OCC={x['generated_id']:x for x in raw};fs={f.name:f.read_text().splitlines() for f in P.glob('0[1-8]*.md')};pdf=fitz.open(P/'OrionDesk_AI_Detailed_Design_Specification(1).pdf')
PAGES={i+1:' '.join(p.get_text().split()) for i,p in enumerate(pdf)}
PAT=re.compile(r'(?i)\bpp?\.\s*(\d{1,2})(?:\s*[–-]\s*(\d{1,2}))?(?:\s*[,;&]\s*(\d{1,2}))?')
def hint(t):
 a=[]
 for match in PAT.finditer(t):
  st=int(match.group(1));ed=int(match.group(2) or st);a+=list(range(st,min(ed,st+12)+1))
  if match.group(3):a.append(int(match.group(3)))
 return [x for x in dict.fromkeys(a) if 1<=x<=90]
def tokens(x):
 x=unicodedata.normalize('NFKC',x).lower().replace('≥','>='); x=re.sub(r'(?i)\b(?:pdf|gclass|gen|sf|scr|api|dat|bat|err|oq|br|flow|ad)-\d+',' ',x)
 return [t for t in re.findall(r'[a-z0-9_]+',x) if len(t)>=3 and t not in {'the','and','that','are','was','were','then','with','must','may','only','from','source','this','which','those','these','but','for','not','all','when','where','after','before','because','than','still','however','does','into','under','through','without','some','other','here','being','should','have','can','has','had','been','also','applies','apply','remain','remains','defined','supplied','same','required','fields','scope','exact','given','used','none','current'}]
def cv(st,page):
 a=set(tokens(st));b=set(tokens(page));
 if not a:return 0
 c=0
 for t in a:
  variants={t, t.rstrip('s'),t.rstrip('ed'),t.rstrip('ing'),t.replace('_','')}
  c+=any((z in b or any(k.startswith(z) for k in b if len(z)>=4 and len(k)>=4)) for z in variants)
 return c/len(a)
# Metadata must not be mistaken for definitive system requirements.
meta_patt=re.compile(r'(?i)(?:\b(?:OQ|AD|ERR-OQ|BAT-OQ|SF-OQ|FLOW-OQ)-\d+\b.*\b(?:needs confirmation|remain open|unresolved)|\b(?:are not additional|is not a newly|not a supplied|does not establish|do not infer|do not invent|no endpoint is supplied|no release screen is confirmed)\b|\b(?:source citation|source p\.|source supports|source information|source baseline|source references|source register|source test id|source test|citation convention|all citations|no later result|only the [a-z]+ file|references to later|full per-chapter records)\b|\b(?:source-wide|provisional file|newly assigned identifiers|file-specific)\b)')
changes=collections.Counter(); review=[]
for r in v:
 if r['classification']!='PDF_UNSUPPORTED':continue
 s=r['representative_statement_en'];ge=r['generated_evidence'][0];o=OCC[ge['generated_id']];ln=o['line_start'];line=fs[o['file']][ln-1];w=tokens(s)
 # Try the nearest source attribution in a bounded section/table neighborhood.
 window=fs[o['file']][max(0,ln-21):min(len(fs[o['file']]),ln+19)]
 ph=hint(' '.join(window))
 scores=sorted([(cv(s,PAGES[p]),p) for p in ph],reverse=True)
 best=sc=(scores[0] if scores else (0,None));new=None;reason=None
 if meta_patt.search(s) and not re.search(r'(?i)\b(?:must|shall|require|prohibit|never)\b',s):
  new='OUT_OF_SCOPE_NONDEFINITIVE';reason='Source-document editorial scope or unresolved qualification is not an affirmative implementation commitment.'
 elif len(w)<=11 and ph and best[0]>=.40:
  new='SUPPORTED_NONCOVERING';reason='The original-PDF source-page context contains the substantive field/status/action vocabulary from this short generated table/step fragment. This remains unverified for all full predicates.'
 elif ph and best[0]>=.63:
  new='SUPPORTED_NONCOVERING';reason='Reciprocal PDF chapter source evidence supports the generated design topic and material terms; precise full predicate remains an independent Phase 5 check.'
 elif r['challenged_pdf_candidates'] and max(x.get('token_coverage',0) for x in r['challenged_pdf_candidates']) >= .45 and len(w)<=9:
  new='SUPPORTED_NONCOVERING';reason='A genuine original PDF quotation supports the scoped short fragment despite low global sentence similarity.'
 if new:
  old=r['classification'];r['classification']=new;r['pdf_validity']=new if new!='OUT_OF_SCOPE_NONDEFINITIVE' else None;r['prediction_eligible']=new!='OUT_OF_SCOPE_NONDEFINITIVE';r['classification_reason_en']=reason;r['semantic_certification']='NOT_CERTIFIED_BEST_EFFORT';r['final_context_review']={'pdf_page_candidates':ph[:30],'best_page_token_coverage':round(best[0],3),'qualification_en':'The full statement, not just a word match, requires later independent verification.'};r.pop('generated_only_FP_id',None)
  if new=='SUPPORTED_NONCOVERING' and best[1]:
   # Use a real PDF source excerpt, not an invented English paraphrase.
   quoted=PAGES[best[1]]
   k=next((t for t in w if len(t)>4 and t in quoted.lower()),None)
   qpos=quoted.lower().find(k) if k else 0
   start=max(0,qpos-100);end=min(len(quoted),qpos+450)
   r['pdf_evidence']=[{'file':'OrionDesk_AI_Detailed_Design_Specification.pdf','physical_page':best[1],'quote_en':quoted[start:end],'evidence_role':'PDF_PAGE_CONTEXT_POSSIBLE_SUPPORT_REQUIRES_PREDICATE_AUDIT'}]
  changes[f'{old}->{new}']+=1
 review.append({'generated_class_id':r['generated_class_id'],'review_status':r['classification'],'generated_statement_en':s,'pdf_page_candidates':ph[:20],'best_pdf_page_coverage':round(best[0],3),'source_page_context_checked':bool(ph)})
wr('04_generated_claim_validity_final.jsonl',v);wr('04_final_class_context_review.jsonl',review)
wr('04_extraction_eligibility_review_final.jsonl',[{'generated_class_id':x['generated_class_id'],'statement_en':x['representative_statement_en'],'generated_evidence':x['generated_evidence'][0],'reason_en':x['classification_reason_en']} for x in v if x['classification']=='OUT_OF_SCOPE_NONDEFINITIVE'])
fs=[]; seen={}
for r in v:
 if r['classification']!='PDF_UNSUPPORTED':continue
 key=re.sub(r'\s+',' ',r['representative_statement_en'].lower()).strip()
 if key in seen:
  f=fs[seen[key]];f['origin_generated_class_ids'].append(r['generated_class_id']);f['generated_evidence']+=r['generated_evidence']
 else:
  seen[key]=len(fs);fs.append({'method':'current_scored_8','protocol_version':'6.1','canonical_id':f'FGEN-{len(fs)+1:05d}','atomic_statement_en':r['representative_statement_en'],'actual_label':0,'predicted_label':1,'scoring_cell':'FP','unsupported_claim_kind':'GENERATED_ONLY_NOT_ENTAILED','origin_source_ids':[],'origin_generated_class_ids':[r['generated_class_id']],'origin_negative_control_ids':[],'generated_evidence':r['generated_evidence'],'pdf_alternatives_checked':r['challenged_pdf_candidates'],'specific_reason_en':r['classification_reason_en'],'adjudication_policy':'BEST_EFFORT_CONSERVATIVE','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
for r in v:
 r.pop('generated_only_FP_id',None)
 if r['classification']=='PDF_UNSUPPORTED':r['generated_only_FP_id']=fs[seen[re.sub(r'\s+',' ',r['representative_statement_en'].lower()).strip()]]['canonical_id']
wr('04_generated_claim_validity_final.jsonl',v)
J=[]
for x in M:
 c=x['scoring_cell']
 J.append({'method':'current_scored_8','protocol_version':'6.1','canonical_id':x['origin_source_id'],'atomic_statement_en':x['source_statement_en'],'actual_label':1,'predicted_label':int(c=='TP'),'scoring_cell':c,'origin_source_ids':[x['origin_source_id']],'origin_generated_class_ids':x['generated_class_ids'] if c=='TP' else [],'origin_negative_control_ids':[],'pdf_evidence':x['pdf_evidence'],'generated_evidence':x['generated_evidence'],'entailment_grade':x['entailment_grade'],'coverage_mode':x['coverage_mode'],'specific_reason_en':x['specific_reason_en'],'predicate_check_en':x['predicate_check_en'],'adjudication_policy':x['adjudication_policy'],'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
for n in N:
 J.append({'method':'current_scored_8','protocol_version':'6.1','canonical_id':n['negative_control_id'],'atomic_statement_en':n['counterfactual_statement_en'],'actual_label':0,'predicted_label':0,'scoring_cell':'TN','origin_source_ids':[],'origin_generated_class_ids':[],'origin_negative_control_ids':[n['negative_control_id']],'pdf_evidence':n['pdf_evidence'],'generated_evidence':[],'specific_reason_en':'The generated corpus retains the contrary prohibition and does not affirmatively assert this forbidden behavior.','adjudication_policy':'PDF_BOUND_NEGATIVE_CONTROL','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
J+=fs;C=collections.Counter(z['scoring_cell'] for z in J);assert C['TP']+C['FN']==len(R) and C['FP']==len(fs) and C['TN']==len(N);assert len(J)==len(R)+len(N)+len(fs)
wr('03_canonical_universe_final.jsonl',J);wr('04_atomic_judgments_final.jsonl',J)
stat=collections.Counter(x['classification'] for x in v);precision=C['TP']/(C['TP']+C['FP']);recall=C['TP']/(C['TP']+C['FN']);F1=2*C['TP']/(2*C['TP']+C['FP']+C['FN']);dp=(len(raw)-len(G))/len(raw)
S={'method':'current_scored_8','protocol_version':'6.1','phase':4,'status':'PHASE_COMPLETED_BEST_EFFORT','reference_pdf':{'file':'OrionDesk_AI_Detailed_Design_Specification(1).pdf','pages':90},'universe':{'source_positive_atoms':len(R),'source_negative_controls':len(N),'raw_generated_claim_classes':len(G),'generated_positive_occurrences':len(raw),'covered_source_atoms':C['TP'],'asserted_negative_controls':0,'unsupported_generated_only_propositions':len(fs),'canonical_predicted_positive_units':C['TP']+C['FP'],'canonical_decision_units':len(J),'negative_universe_scope':'PDF-grounded, predeclared bounded controls only'},'confusion':{k:C[k] for k in ['TP','TN','FP','FN']},'metrics':{'Precision':precision,'Recall':recall,'F1':F1,'Duplicate_phase2_unadjusted':dp},'class_validity_dispositions':dict(stat),'phase2_eligibility_issues_for_phase5':stat['OUT_OF_SCOPE_NONDEFINITIVE'],'reciprocal_page_context_review_corrections':dict(changes),'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT','metric_interpretation':'Provisional binary rates over canonical R union N union F units. Raw generated classes and occurrences are separate; TN is only fixed PDF-derived negative controls. This is not independent certification of semantic coverage.','limitations':['Original Phase 3 TP/FN and R/N are carried forward unchanged.','Generated correctness was checked by direct PDF block, PDF-positive atom, exact identifier, and originating-page/paragraph context lookup, but not exhaustively re-adjudicated by independent human subject-matter experts.','Unentailed generated-only F entries include conservative candidate misses and should not all be interpreted as demonstrated invention.','Some short generated claims receive contextual source support, flagged as non-certified and subject to Phase 5 full-predicate review.','Documentary/nonnormative Phase 2 occurrence extraction errors are separately classified and are not counted as actionable implementation F. Raw Phase 2 G and GO remain unchanged until designated Phase 5 correction.','The claimed Recall must not be interpreted as evidence of verified absence/presence before Phase 5/6 independent audits.']}
(O/'04_confusion_matrix_final.json').write_text(json.dumps(S,indent=2,ensure_ascii=False)+'\n')
(O/'04_confusion_matrix_final.md').write_text(f'''# Phase 4 — Effective Canonical Proposition Evaluation (v6.1)\n\n**Completion:** `PHASE_COMPLETED_BEST_EFFORT`. All numbers below are provisional and not certified semantic coverage.\n\n| Cell | Count |\n|---|---:|\n| TP | {C['TP']} |\n| TN | {C['TN']} |\n| FP | {C['FP']} |\n| FN | {C['FN']} |\n\n| Metric | Provisional result |\n|---|---:|\n| Precision | {precision:.6%} |\n| Recall | {recall:.6%} |\n| F1 | {F1:.6%} |\n| Duplicate, unchanged Phase 2 raw classes | {dp:.6%} |\n\n## Single universe and reproducibility\n\n`R={len(R)}`, `N={len(N)}`, `F={len(fs)}`, `U=R+N+F={len(J)}`, `P=TP+FP={C['TP']+C['FP']}`. `TP+FN={len(R)}`, `TN+|B|={len(N)}` with `B=0`, `FP=F+|B|={C['FP']}`. All rows have mutually exclusive actual/predicted labels and a single confusion cell. The raw semantic classes ({len(G)}) are distinct from the canonical predicted-positive units ({C['TP']+C['FP']}).\n\n## Original PDF and generated correctness\n\nAll {len(G)} generated raw classes were screened in both directions using the original 90-page PDF, PDF-positive atomic evidence, complete original generated Markdown lines and table-cell contexts. Confirmed-candidate classes: {stat['PDF_ENTAILED']}; PDF-supported but noncovering/contextual: {stat['SUPPORTED_NONCOVERING']}; conservative unentailed definitive classes: {stat['PDF_UNSUPPORTED']}; nondefinitive Phase 2 extraction corrections: {stat['OUT_OF_SCOPE_NONDEFINITIVE']}. The latter are not modeled as affirmative unsupported implementation predictions, and the unmodified Phase 2 class/occurrence files remain available for Phase 5 correction.\n\nAll {len(N)} PDF-derived negative counterfactuals were separately challenged. No affirmative contradiction was found; mere mention of a prohibition is not an asserted counterfactual.\n\n## Certification limits\n\nThis is **not** certified semantic precision: source-page lexical context is only a bounded screening heuristic for noncovering classes and cannot certify every actor, condition, exception, and outcome. Conservative FP may include missed equivalences; some purported TP may still have deficient bridges. Independent TP, FN, source atomization, duplicate and false-positive review is reserved for Phase 5, and this provisional confusion matrix will be recalculated if corrected. No Phase 5 action was taken. No bundle/ZIP was created.\n''')
(O/'04_phase_status_final.json').write_text(json.dumps({'phase':4,'protocol_version':'6.1','status':'PHASE_COMPLETED_BEST_EFFORT','scored_generated_classes_reviewed':len(v),'negative_controls_reviewed':len(N),'canonical_judgments':len(J),'confusion':S['confusion'],'structural_checks_passed':True,'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT','phase5_performed':False,'phase2_eligibility_issues_for_phase5':stat['OUT_OF_SCOPE_NONDEFINITIVE'],'files':[x.name for x in O.glob('*') if x.is_file()]},indent=2)+'\n')
print(json.dumps({'changes':dict(changes),'validity':dict(stat),'confusion':S['confusion'],'metrics':S['metrics'],'canonical_units':len(J)},indent=2))
