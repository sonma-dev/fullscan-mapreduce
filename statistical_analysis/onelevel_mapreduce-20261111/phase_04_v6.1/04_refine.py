#!/usr/bin/env python3
"""Phase 4 within-turn reciprocal candidate challenge and context-sensitive refinement."""
import re,json,collections,hashlib,unicodedata
from pathlib import Path
import fitz
O=Path('/mnt/data/oriondesk_phase4_v61'); P=Path('/mnt/data');P3=P/'oriondesk_phase3_v61_redo';P2=P/'oriondesk_phase2_current_scored_8'
rows=lambda p:[json.loads(x) for x in open(p) if x.strip()]
write=lambda p,r:(O/p).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in r),encoding='utf8')
v=rows(O/'04_generated_claim_validity_final.jsonl'); G=rows(P2/'02_generated_classes_final.jsonl'); Q=rows(P2/'02_generated_atoms_final.jsonl'); gen={x['generated_id']:x for x in Q};S=rows(P3/'01_source_atoms_final.jsonl');N=rows(P3/'01_source_negative_controls_final.jsonl');M=rows(P3/'03_evidence_matches_final.jsonl');NEGA=rows(O/'04_negative_control_assertion_audit_final.jsonl')
fs={x.name:x.read_text().splitlines() for x in P.glob('0[1-8]*.md')}
d=fitz.open(P/'OrionDesk_AI_Detailed_Design_Specification(1).pdf')
pdfblocks={}
for i,pg in enumerate(d,1):
 a=[]
 for b in pg.get_text('blocks'):
  st=' '.join(b[4].split())
  if len(st)<24 or st.startswith(('ORIONDESK AI','CONTROLLED FICTIONAL')):continue
  a.append(st)
 # combined neighbor passages handle paragraph continuation across blocks
 passages=a[:]+[' '.join(a[j:j+2]) for j in range(len(a)-1)]
 pdfblocks[i]=passages
stop=set('the and for with are was were from this these those source scope must shall can cannot does not no only into than when where what which who whose has have had been will such using within below above across its an all of by is to a as or at on in between under through into because if then vs while still even some ever never be do apply applies defined supplied needs confirmation confirmed requires required qualified unspecified examples example no added target scope page pages field fields file files specific exact complete not actually implementation'.split())
synonyms={'revocation':['revoke','revoked','revoking'],'revoked':['revoke','revocation'],'index':['index','indexing','indexed'],'replay':['replay','replayed','duplicate'],'ledger':['ledger','audit','outbox'],'auth':['authorization','authoriz','authentication'],'failure':['failure','failed','error'],'recovery':['restore','recovery','resume','recover'],'approval':['approve','approved','review','reviewer'],'scope':['scope','scoped'],'audit':['audit','audited'],'terminal':['terminate','terminal','fail'],'unapproved':['approved','allowlist'],'safe':['safety','safe'],'required':['require','must'],'requirement':['required','require'],'context':['context','scoped'],'atomic':['transaction','atomically'],'source':['source','document'],'evidence':['citation','citations','evidence'],'published':['publish','publication'],'immutable':['immutable','append'],'capability':['permission','capability'],'configuration':['config','configured'],'quota':['budget','quota'],'model':['gateway','model'],'response':['reply','response','answer'],'duration':['time','duration'],'decision':['decision','approval'],'person':['independent','reviewer'],'deadline':['deadline','timeout'],'token':['token','credential']}
def word(x):
 x=unicodedata.normalize('NFKC',x).lower().replace('≤','<=').replace('≥','>=')
 return re.findall(r'[a-z0-9][a-z0-9_.{}@/-]*',x)
def setwords(x):
 ws=[a for a in word(x) if len(a)>2 and a not in stop and not a.startswith(('pdf-','gclass-','gen-','api-','dat-','bat-','br-','oq-','sf-','err-','flow-','sec-'))]
 return set(ws)
def cover(s,p):
 a=setwords(s);b=setwords(p)
 if not a:return 0.0
 count=0
 for t in a:
  al={t,t.rstrip('s'),t.rstrip('ed'),t.rstrip('ing'),t.replace('-',' ')}
  al.update(synonyms.get(t,[]))
  if any(any(k in q or q in k for q in b if len(q)>3) for k in al if len(k)>=4):count+=1
 return count/len(a)
refpat=re.compile(r'(?i)\bpp?\.\s*(\d{1,2})(?:\s*[–-]\s*(\d{1,2}))?(?:\s*[,;&]\s*(\d{1,2}))?')
def hints(raw):
 pages=[]
 for m in refpat.finditer(raw):
  a=int(m.group(1));b=int(m.group(2) or a)
  if 1<=a<=90 and 1<=b<=90 and b>=a and b-a<25:pages+=list(range(a,b+1))
  if m.group(3):pages.append(int(m.group(3)))
 return list(dict.fromkeys(x for x in pages if 1<=x<=90))

def is_meta(s,o):
 txt=s.lower()
 if any(p in txt for p in ['no native flow identifier','no previous specifications','file names','only 01_screen','source references','source citat','the documentation dependency','requirements below','the following bounded-context','each row preserves','read from these','are reference dependencies','page citations','source supports','source example','no implied','unless expressly stated','previous files are','a row here means','a table entry','no new endpoint is confirmed']):return True
 if ('needs confirmation' in txt or 'not specified' in txt or 'source does not' in txt or 'no supplied' in txt or 'not a default' in txt) and not re.search(r'(?i)\b(?:must|shall|never|prohibit|cannot|require)\b',s):return True
 if 'actual' in txt and 'source' in txt and 'metadata' in txt:return True
 if re.match(r'(?i)^(?:no|not) (?:newly|extra|separate) (?:route|screen|api|type|endpoint|default)\b',s):return True
 if len(setwords(s))<=1 and o.get('source_role')!='sql':return True
 return False

# Review strongest previously labeled PDF_UNSUPPORTED candidates against the evidence PDF, using actual adjacent-section source-page citations.
audit=[];rescues=collections.Counter();remaining=[]
for r in v:
 if r['classification'] not in ('PDF_UNSUPPORTED','SUPPORTED_NONCOVERING'):continue
 ge=r['generated_evidence'][0];gid=ge['generated_id'];o=gen[gid];s=r['representative_statement_en'];file=o['file'];ln=o['line_start'];line=fs[file][ln-1]
 raw=o['source_quote_en'];pageh=hints(line)
 if not pageh:
  # Only inspect immediately adjacent attribution, never a general statement hundreds of lines away
  nearby=' '.join(fs[file][max(0,ln-3):min(len(fs[file]),ln+7)])
  pageh=hints(nearby)
 # Prior Phase 3 bridge pages are additional candidates, not source validity by themselves
 for pm in r['phase3_source_atoms_using_class_as_evidence'][:10]:
  x=next((z for z in S if z['source_id']==pm),None)
  if x and x['physical_page'] not in pageh:pageh.append(x['physical_page'])
 bestscore,bestpage,bestpass=(0,None,None)
 for p in pageh[:30]:
  for passage in pdfblocks.get(p,[]):
   sc=cover(s,passage)
   if sc>bestscore:bestscore,bestpage,bestpass=(sc,p,passage)
 old=r['classification'];new=old;reason=None
 # Not every source-document commentary is a definitive prediction; separate extraction errors now.
 if old=='PDF_UNSUPPORTED' and is_meta(s,o):
  new='OUT_OF_SCOPE_NONDEFINITIVE'
  reason='The extracted fragment is an unresolved/documentary qualification rather than an affirmative product-design requirement; Phase 2 eligibility correction required.'
 elif old=='PDF_UNSUPPORTED':
  n=len(setwords(s))
  # Cited evidence whose wording includes the substantive target and action supports the scoped claim as a bounded best-effort case.
  if bestscore>=.72 and n>=2:
   new='PDF_ENTAILED' if bestscore>=.93 and n>=4 else 'SUPPORTED_NONCOVERING'
   reason='Original PDF evidence on the generated statement\'s cited page supports the scoped phrase; first-pass global candidate match missed table/paragraph context.'
  elif bestscore>=.52 and n>=2:
   new='SUPPORTED_NONCOVERING'
   reason='A substantial material-predicate overlap is present on the generated statement\'s original PDF source page; no full-atom coverage is inferred.'
  elif r['phase3_source_atoms_using_class_as_evidence']:
   new='SUPPORTED_NONCOVERING'
   reason='Actual generated clause is a verified candidate conjunct for source coverage; it is not a standalone unsupported permission or invented policy.'
 # Preserve supporting evidence when genuinely retrieved.
 if new!=old:
  r['classification']=new;r['pdf_validity']=new if new!='OUT_OF_SCOPE_NONDEFINITIVE' else None;r['prediction_eligible']=new!='OUT_OF_SCOPE_NONDEFINITIVE';r['classification_reason_en']=reason
  r['contextual_pdf_evidence_search']={'source_page_hints':pageh[:20],'best_pdf_quote_token_coverage':round(bestscore,3),'citation_evidence_mode':'LOCAL_PDF_PREDICATE_RETRIEVAL' if bestpass else 'PHASE3_CONJUNCTIVE_SUPPORT'}
  if bestpage is not None and new in ('PDF_ENTAILED','SUPPORTED_NONCOVERING'):
   r['pdf_evidence']=[{'file':'OrionDesk_AI_Detailed_Design_Specification.pdf','physical_page':bestpage,'quote_en':bestpass[:800],'evidence_role':'ACTUAL_PDF_CITATION_PAGE_CONTEXT; qualified semantic screening'}]
  r['phase4_refinement_status']='CORRECTED_INITIAL_CLASSIFICATION'
  rescues[f'{old}→{new}']+=1
 else:
  r['contextual_pdf_evidence_search']={'source_page_hints':pageh[:20],'best_pdf_quote_token_coverage':round(bestscore,3),'citation_evidence_mode':'REVIEWED_RETAINED'}
  if old=='PDF_UNSUPPORTED':remaining.append(r)
 audit.append({'generated_class_id':r['generated_class_id'],'initial_classification':old,'final_classification':new,'source_page_hints':pageh[:20],'best_source_page_quote':bestpass[:600] if bestpass else None,'best_source_page':bestpage,'page_context_token_coverage':round(bestscore,4),'generated_statement_en':s,'generated_file':file,'generated_line':ln,'decision_en':reason or 'Initial result retained after local cited-PDF-page challenge.'})
write('04_generated_claim_validity_final.jsonl',v)
write('04_reciprocal_pdf_support_refinement.jsonl',audit)
write('04_extraction_eligibility_review_final.jsonl',[{'generated_class_id':x['generated_class_id'],'statement_en':x['representative_statement_en'],'generated_evidence':x['generated_evidence'][0],'reason_en':x['classification_reason_en']} for x in v if x['classification']=='OUT_OF_SCOPE_NONDEFINITIVE'])
# Strict provenance for unsupported generated definitive claims: no invented quote; retain actual nearest source alternatives.
f=[];seen={}
for r in v:
 if r['classification']!='PDF_UNSUPPORTED':continue
 k=re.sub(r'\s+',' ',r['representative_statement_en'].lower()).strip()
 if k in seen:
  z=f[seen[k]];z['origin_generated_class_ids'].append(r['generated_class_id']);z['generated_evidence']+=r['generated_evidence']
 else:
  id=f'FGEN-{len(f)+1:05d}';seen[k]=len(f)
  f.append({'method':'current_scored_8','protocol_version':'6.1','canonical_id':id,'atomic_statement_en':r['representative_statement_en'],'actual_label':0,'predicted_label':1,'scoring_cell':'FP','unsupported_claim_kind':'GENERATED_ONLY_NOT_ENTAILED','origin_source_ids':[],'origin_generated_class_ids':[r['generated_class_id']],'origin_negative_control_ids':[],'generated_evidence':r['generated_evidence'],'pdf_alternatives_checked':r['challenged_pdf_candidates'],'specific_reason_en':r['classification_reason_en'],'adjudication_policy':'BEST_EFFORT_CONSERVATIVE','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
for r in v:
 r.pop('generated_only_FP_id',None)
 if r['classification']=='PDF_UNSUPPORTED':
  k=re.sub(r'\s+',' ',r['representative_statement_en'].lower()).strip();r['generated_only_FP_id']=f[seen[k]]['canonical_id']
write('04_generated_claim_validity_final.jsonl',v)
pr=[]
for m in M:
 sc=m['scoring_cell'];pr.append({'method':'current_scored_8','protocol_version':'6.1','canonical_id':m['origin_source_id'],'atomic_statement_en':m['source_statement_en'],'actual_label':1,'predicted_label':int(sc=='TP'),'scoring_cell':sc,'origin_source_ids':[m['origin_source_id']],'origin_generated_class_ids':m['generated_class_ids'] if sc=='TP' else [],'origin_negative_control_ids':[],'pdf_evidence':m['pdf_evidence'],'generated_evidence':m['generated_evidence'],'entailment_grade':m['entailment_grade'],'coverage_mode':m['coverage_mode'],'specific_reason_en':m['specific_reason_en'],'predicate_check_en':m['predicate_check_en'],'adjudication_policy':m['adjudication_policy'],'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
for n,a in zip(N,NEGA):
 sc='FP' if a['affirmative_generated_assertion_found'] else 'TN'
 pr.append({'method':'current_scored_8','protocol_version':'6.1','canonical_id':n['negative_control_id'],'atomic_statement_en':n['counterfactual_statement_en'],'actual_label':0,'predicted_label':int(sc=='FP'),'scoring_cell':sc,'origin_source_ids':[],'origin_generated_class_ids':[],'origin_negative_control_ids':[n['negative_control_id']],'pdf_evidence':n['pdf_evidence'],'generated_evidence':[],'specific_reason_en':a['specific_reason_en'],'adjudication_policy':'PDF_BOUND_NEGATIVE_CONTROL','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
pr+=f;C=collections.Counter(x['scoring_cell'] for x in pr);U=len(pr);assert U==len(S)+len(N)+len(f)
assert C['TP']+C['FN']==len(S) and C['TN']==len(N) and C['FP']==len(f)
write('03_canonical_universe_final.jsonl',pr);write('04_atomic_judgments_final.jsonl',pr)
stat=collections.Counter(x['classification'] for x in v)
prec=C['TP']/(C['TP']+C['FP']);rec=C['TP']/(C['TP']+C['FN']);f1=2*C['TP']/(2*C['TP']+C['FP']+C['FN'])
sumj={'method':'current_scored_8','protocol_version':'6.1','phase':4,'status':'PHASE_COMPLETED_BEST_EFFORT','universe':{'source_positive_atoms':len(S),'source_negative_controls':len(N),'raw_generated_claim_classes':len(G),'generated_positive_occurrences':len(Q),'covered_source_atoms':C['TP'],'asserted_negative_controls':0,'unsupported_generated_only_propositions':len(f),'canonical_predicted_positive_units':C['TP']+C['FP'],'canonical_decision_units':U,'negative_universe_scope':'PDF-grounded, predeclared bounded controls only'},'confusion':{k:C[k] for k in ('TP','TN','FP','FN')},'metrics':{'Precision':prec,'Recall':rec,'F1':f1,'Duplicate_phase2_unadjusted':(len(Q)-len(G))/len(Q)},'generated_claim_validity_screen':dict(stat),'phase2_nondefinitive_extraction_correction_candidates_for_phase5':stat['OUT_OF_SCOPE_NONDEFINITIVE'],'reciprocal_context_refinement_changes':dict(rescues),'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT','methodology':'Two-pass source proof challenge using independent original PDF text blocks, source-atom evidence, structural-identifier reverse lookup, and generated-citation local PDF page checks. Best-effort classification is not exhaustive manual predicate proof.','limitations':['Some generated classes are documentary/editorial Phase 2 extraction errors and are separately excluded from predicted substantive design commitments pending Phase 5 reconciliation.','SOURCE_SUPPORTED_NONCOVERING cases rely on PDF target and context but do not automatically substantiate complete independent R atoms.','Unsupported generated-only claims are conservative candidate mismatches, not all verified inventions; Phase 5 can correct semantic validity using stronger manual evidence.','Phase 3 source-side TP/FN remains provisional, Phase 5 independently audits both TP proof and source atomization.','TN counts only 37 fixed negative controls; no unrelated absent possibilities were invented.','The effective-proposition predicted-positive count differs from raw generated-class count by definition.']}
(O/'04_confusion_matrix_final.json').write_text(json.dumps(sumj,indent=2,ensure_ascii=False)+'\n')
(O/'04_confusion_matrix_final.md').write_text(f'''# Phase 4 — Canonical Four-Cell Evaluation (Protocol v6.1)\n\n**Status:** `PHASE_COMPLETED_BEST_EFFORT` — this is a provisional, non-certified semantic evaluation.\n\n| Confusion cell | Count |\n|---|---:|\n| TP | {C['TP']} |\n| TN | {C['TN']} |\n| FP | {C['FP']} |\n| FN | {C['FN']} |\n\n| Metric | Value |\n|---|---:|\n| Precision | {prec:.6%} |\n| Recall | {rec:.6%} |\n| F1 | {f1:.6%} |\n| Phase 2 raw duplicate rate (unchanged) | {(len(Q)-len(G))/len(Q):.6%} |\n\n## Canonical proposition-universe accounting\n\nR = {len(S)} PDF normative propositions, N = {len(N)} bounded PDF-negative controls, F = {len(f)} distinct unentailed definitive generated propositions. Thus U = R + N + F = **{U}**. P = TP + FP = **{C['TP']+C['FP']}**; this is not required to equal raw class count **{len(G)}**. TP + FN = {len(S)}, TN + asserted negative controls = {len(N)}, FP = F + asserted negative controls = {len(f)}. The four cells sum to U.\n\n## Generated-claim audit\n\nAll {len(G)} Phase 2 raw classes were source-challenged; claims retained for effective prediction have source evidence or unsupported-source alternatives and actual file/physical-line locators. The second-page evidence challenge rescued {sum(rescues.values())} initial classifications (breakdown: {json.dumps(dict(rescues))}). Dispositions: {json.dumps(dict(stat))}.\n\n{stat['OUT_OF_SCOPE_NONDEFINITIVE']} Phase 2 class candidates consist of non-affirmative document/provenance/undecided material and are **not** scored as unsupported implementation predictions. Their raw Phase 2 classes are not altered in this turn; Phase 5 must reconcile final eligibility and raw duplicates.\n\nAll {len(N)} bounded negative controls were challenged individually. None was affirmatively asserted by the eight generated files, so their canonical rows are TN.\n\n## Evidence quality limitations\n\nThis is a best-effort evidence-driven reconciliation, **not** full certified bidirectional human entailment review. Some remaining FP reflect conservative unproven generated material even when the actual PDF discusses an adjacent topic. Some apparent PDF support may lack a complete actor/timing/exception predicate. The original Phase 3 TP/FN decisions were not modified. Phase 5 is required for source split/merge correction, per-TP adversarial proof, raw class eligibility changes and false-positive/false-negative challenges. No subsequent phase was performed. No archive was created.\n''')
(O/'04_phase_status_final.json').write_text(json.dumps({'phase':4,'protocol_version':'6.1','status':'PHASE_COMPLETED_BEST_EFFORT','method':'current_scored_8','generated_classes_checked':len(v),'negative_controls_checked':len(NEGA),'canonical_judgments':U,'confusion':sumj['confusion'],'structural_checks_passed':True,'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT','phase5_performed':False,'phase2_eligibility_errors_flagged':stat['OUT_OF_SCOPE_NONDEFINITIVE'],'files':[x.name for x in O.glob('*') if x.is_file()]},indent=2)+'\n')
print(json.dumps({'rescues':dict(rescues),'classifications':dict(stat),'confusion':sumj['confusion'],'metrics':sumj['metrics'],'units':U},indent=2))
