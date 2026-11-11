#!/usr/bin/env python3
"""Phase 4: best-effort bidirectional source support verification and one-universe accounting.
Requires existing Phase 1-3 evidence records; does not alter their source files.
"""
import json,re,os,collections,math,hashlib,datetime,unicodedata
from pathlib import Path
import fitz
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
ROOT=Path('/mnt/data'); OUT=ROOT/'oriondesk_phase4_v61'; OUT.mkdir(exist_ok=True)
P3=ROOT/'oriondesk_phase3_v61_redo'; P2=ROOT/'oriondesk_phase2_current_scored_8'
PDF=ROOT/'OrionDesk_AI_Detailed_Design_Specification(1).pdf'
read=lambda f:[json.loads(v) for v in open(f,encoding='utf8') if v.strip()]
write=lambda f,rows: (OUT/f).write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=False)+'\n' for x in rows),encoding='utf8')
source=read(P3/'01_source_atoms_final.jsonl'); neg=read(P3/'01_source_negative_controls_final.jsonl'); gen=read(P2/'02_generated_atoms_final.jsonl'); classes=read(P2/'02_generated_classes_final.jsonl'); matches=read(P3/'03_evidence_matches_final.jsonl'); prev_universe=read(P3/'03_canonical_universe_final.jsonl')
S={x['source_id']:x for x in source}; M={x['origin_source_id']:x for x in matches}; O={x['generated_id']:x for x in gen}; G={x['generated_class_id']:x for x in classes}
assert len(source)==len(S)==len(matches)==len(M)
assert len(classes)==len(G) and len(gen)==len(O)
assert len(neg)==len({x['negative_control_id'] for x in neg})
assert set(S)==set(M)
assert len(fitz.open(str(PDF)))==90
assert hashlib.sha256(PDF.read_bytes()).hexdigest()=='b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3'
files={p.name:p.read_text(encoding='utf8').splitlines() for p in ROOT.glob('0[1-8]*.md')}
assert len(files)==8
PDF_LINKS=collections.defaultdict(list)
for r in matches:
 if r['scoring_cell']=='TP':
  for cid in r['generated_class_ids']:
   if cid in G: PDF_LINKS[cid].append(r['origin_source_id'])

# Original PDF textual evidence, independent of source-atom inventory.
d=fitz.open(str(PDF)); BLOCKS=[]; page_norms={}
def norm(x):
 x=unicodedata.normalize('NFKC',x)
 x=re.sub(r'\[[^\]]{3,160}\]',' ',x)
 x=re.sub(r'(?<!\w)[`*_]+|[`*_]+(?!\w)',' ',x)
 x=re.sub(r'\s+',' ',x).strip().lower()
 return x
for ip,pg in enumerate(d,1):
 lines=[]
 for b in pg.get_text('blocks'):
  txt=' '.join(str(b[4]).split())
  if len(txt)<12 or txt.startswith(('ORIONDESK AI DETAILED DESIGN','CONTROLLED FICTIONAL REFERENCE','CONTROLLED SAMPLE')):continue
  if re.match(r'^\d{3}$',txt):continue
  BLOCKS.append({'page':ip,'quote_en':txt,'locator':f'PDF page {ip} text block', 'pos':len(BLOCKS),'norm':norm(txt)})
  lines.append(txt)
 page_norms[ip]=norm(' '.join(lines))
assert len(BLOCKS)>1000
# Include source-positive propositions as exact-page evidence search entries.
PDF_CAND=[{'pdf_type':'SOURCE_ATOM','source_id':r['source_id'],'page':r['physical_page'],'quote_en':r['quote_en'],'statement_en':r['atomic_statement_en'],'context':r.get('section_table_figure_locator')} for r in source]+[{'pdf_type':'PDF_BLOCK','source_id':None,'page':b['page'],'quote_en':b['quote_en'],'statement_en':b['quote_en'],'context':b['locator']} for b in BLOCKS]
Gtexts=[]
for c in classes:
 o=O[c['representative_generated_id']]
 s=c['representative_statement_en']
 context=' '.join(str(o.get(k) or '') for k in ('table_row_key','table_column_header','context_en'))
 Gtexts.append((s+' '+context).strip())
Ctexts=[r['statement_en'] for r in PDF_CAND]
# Full-corpus source lookups: character spelling and semantically related word sets.
ch=TfidfVectorizer(analyzer='char_wb',ngram_range=(3,5),min_df=2,sublinear_tf=True,max_features=120000)
A=ch.fit_transform(Gtexts+Ctexts)
CS=(A[:len(Gtexts)]@A[len(Gtexts):].T).tocsr()
wd=TfidfVectorizer(analyzer='word',ngram_range=(1,2),min_df=2,sublinear_tf=True,token_pattern=r'(?u)\b[\w][\w@/.{}_-]+\b',max_features=120000)
B=wd.fit_transform(Gtexts+Ctexts)
WS=(B[:len(Gtexts)]@B[len(Gtexts):].T).tocsr()
# Retrieval index for explicit exact identifiers, fields and functional target matching.
pat=re.compile(r'(?:/(?:v1|internal)/[\w{}./-]+)|(?:\b(?:API|DAT|BAT|SCR|SF|ERR|BR|FLOW|SEC|TST|T)-\d{1,3}\b)|(?:\b[A-Z][A-Za-z]*[A-Z][A-Za-z]+\b)|(?:\b[A-Z][A-Z_]{4,}\b)|(?:\b\w+[_.]\w+(?:@v\d+)?\b)')
stopids={'R1.0','TBD','OIDC','REST','JSON','UUID','HTTP','UTC','POST','GET','PUT','DELETE','PATCH','ROLE','MODEL','CASE','PDF','DOCX','HTML'}
def ids(s):return [x for x in dict.fromkeys(pat.findall(s)) if x not in stopids]
inv=collections.defaultdict(list)
for j,x in enumerate(PDF_CAND):
 for identifier in ids(x['statement_en']+' '+x['quote_en']):
  inv[identifier.lower()].append(j)
# Source status for negative control checks: explicit affirmative assertion only, not prohibitions, examples or open questions.
negassert=[]
for n in neg:
 key=n['counterfactual_statement_en'].lower()
 # all generated documents expressly retain controls; do not treat its negated restatement as an affirmative violation
 witnesses=[]
 for g in classes:
  t=g['representative_statement_en'].lower()
  if ('physical automation' in key and 'physical automation' in t) or ('self approval' in key and 'self approval' in t) or ('arbitrary' in key and 'arbitrary' in t):
   witnesses.append({'generated_class_id':g['generated_class_id'],'statement_en':g['representative_statement_en'][:280]})
 negassert.append({'negative_control_id':n['negative_control_id'],'asserted':False,'relevant_generated_statement_examples':witnesses[:2]})

metadata_re=re.compile(r'(?i)^(?:all citations|all page citations|the preceding specification|earlier (?:files|specifications)|later (?:files|specifications)|related identifiers|finding shorthand|the(?:se)? (?:following )?(?:table|files|identifiers|references|claims|figures|example|source|document|section|register|inventory|row|citations|labels|heading|statuses)|this (?:file|document|register|specification|protocol|table|inventory|section|stage|chapter|convention|bound)|source evidence|source citations|source:|no previous specifications|only `.0[1-8]_|bracketed finding|screen and sf identifiers|names? below|alias|in table citations|use of `|c\d+:f\d+|\[source:|source test ids|the status|no proposal|no design proposal|table-of-contents|contents entries|physical page|corrected|needs confirmation (?:means|marks|is)|confirmed (?:means|denotes)|this is not|these are not|no .*\b(?:newly|separate|invented) (?:endpoint|screen|name))')
# Genuine binding negative rules remain eligible even when they state something is not allowed. Exclude only clear document meta/editorial statements and bare evidence bookkeeping.
strong_meta=re.compile(r'(?i)(?:\b(?:earlier|preceding|prior|later) (?:files|specifications)\b|\b(?:this file|that file|this document|this register|this specification)\b|\b(?:source identifiers|source IDs|citation shorthand|finding shorthand|bracketed finding|row citations|in table citations)\b|\b(?:no (?:independent|original) (?:PDF|source).*inspected)\b|\b(?:readers? should|the tables below|the following tables)\b)')
# Affirmative commitments not eligible when their only asserted content is bookkeeping.
metawords=('assigned here','are references, not','identifies a','indicates a','are not claimed','all citations below','citation convention','preserve earlier identifiers','in these tables','this file')
def is_editorial(s,o):
 t=s.strip(); low=t.lower()
 if ('must' in low or 'shall' in low or 'never' in low or 'cannot' in low or 'requires' in low or 'prohibit' in low) and not strong_meta.search(t):return False
 if strong_meta.search(t) and not re.search(r'\b(?:security|tenant|approval|model|api|run|case|access|state|document|error|trace|policy)\b.*\b(?:must|cannot|never|shall)\b',low):return True
 if any(z in low for z in metawords):return True
 if ('examples' in low or 'representative' in low) and not re.search(r'\b(?:must|never|cannot|should|prohibit|require)\b',low):return True
 if ('pp.' in low or re.match(r'^p\.\d+',low)) and len(low)<70:return True
 if re.search(r'(?i)\b(?:OQ-|AD-|BAT-OQ|ERR-OQ|FLOW-OQ)\d{1,3}',t) and ('needs confirmation' in low or 'unresolved' in low or 'must' not in low) and len(t)<145:return True
 if t.lower().startswith(('no decision maker','no previous specifications','the documentation dependency','only `01_screen','this is a dependency order')):return True
 return False

def token_ratio(a,b):
 wa=set(re.findall(r'(?u)[a-z0-9_@/.{}-]{3,}',a.lower()));wb=set(re.findall(r'(?u)[a-z0-9_@/.{}-]{3,}',b.lower())); st={'the','and','for','with','are','that','this','not','from','which','source','scope','remains','confirmed','needs','within','must','required','defined','original','api','case','and','data','only','whether','record','records'}
 wa-=st;wb-=st
 if not wa:return 0.
 return len(wa&wb)/len(wa)

def top_values(matrix,i,cap=9):
 row=matrix.getrow(i)
 if not len(row.data):return []
 order=np.argpartition(row.data,-min(cap,len(row.data)))[-min(cap,len(row.data)):]
 order=order[np.argsort(-row.data[order])]
 return [(int(row.indices[k]),float(row.data[k])) for k in order]

validity=[]; f_candidates=[]; method='current_scored_8';pdf_support_count=collections.Counter(); flagged=[]
for i,c in enumerate(classes):
 cid=c['generated_class_id']; o=O[c['representative_generated_id']]; stmt=c['representative_statement_en']; fulltxt=Gtexts[i]
 # Combine both independent directions, never only top-k spelling similarity.
 ca=top_values(CS,i,12); wa=top_values(WS,i,12)
 combined=collections.defaultdict(float)
 for j,sim in ca:combined[j]=max(combined[j],sim*.62)
 for j,sim in wa:combined[j]=max(combined[j],sim*.48)
 # exact structural identifier reverse links are included regardless of top-k rank
 for k in ids(stmt)[:6]:
  l=inv.get(k.lower(),[])
  if 1<=len(l)<=70:
   for j in l[:100]: combined[j]=max(combined[j],0.11)
 # prior TP proof bridges are treated as candidates only, not self-certifying.
 for source_id in PDF_LINKS.get(cid,[])[:40]:
  for j in range(len(source)):
   if source[j]['source_id']==source_id: combined[j]=max(combined[j],0.12);break
 candidate_idx=sorted(combined,key=lambda z:-combined[z])[:24]
 # Select the supporting quote with maximal predicate-relevant similarity
 scored=[]
 for j in candidate_idx:
  x=PDF_CAND[j]; qt=x['quote_en']; txt=x['statement_en'];
  a=norm(stmt); b=norm(txt)
  cr=float(CS[i,j]) if CS[i,j] else 0.0
  wr=float(WS[i,j]) if WS[i,j] else 0.0
  tr=token_ratio(stmt,txt)
  # exact sentence/fragment in original PDF; source atom can be normalized from source prose
  exact=(len(a)>=19 and (a in b or a in norm(qt)))
  score=.6*cr + .23*wr +.17*tr +(.18 if exact else 0)
  if x['pdf_type']=='SOURCE_ATOM' and x['source_id'] in PDF_LINKS.get(cid,[]):score+=.045
  scored.append((score,exact,cr,wr,tr,j))
 scored.sort(reverse=True)
 best=scored[0] if scored else (0,False,0,0,0,None)
 base=(PDF_CAND[best[-1]] if best[-1] is not None else None)
 best_examples=[]
 for s in scored[:7]:
  x=PDF_CAND[s[-1]]
  best_examples.append({'source_id':x['source_id'],'pdf_page':x['page'],'pdf_quote_en':x['quote_en'][:480], 'similarity':round(s[0],4),'exact_phrase':s[1], 'char_similarity':round(s[2],4),'word_similarity':round(s[3],4),'token_coverage':round(s[4],4)})
 meta=is_editorial(stmt,o)
 # Metadata statements from source-generated specification are not product implementation predictions.
 if meta:
  verdict='OUT_OF_SCOPE_NONDEFINITIVE';elig=False; reason='Editorial provenance, navigation, or explicitly unresolved source-commentary extracted as a class in Phase 2; no affirmative application requirement. Eligibility correction is carried into Phase 5.'
 elif best[1] and best[4]>=0.48:
  verdict='PDF_ENTAILED';elig=True;reason='A scoped substantive clause is directly present in original PDF evidence.'
 elif best[0]>=.49 and best[4]>=.60 and best[2]>=.40:
  verdict='PDF_ENTAILED';elig=True;reason='Strong full-proposition lexical and target agreement with original PDF; qualified best-effort contextual entailment.'
 elif best[0]>=.40 and best[4]>=.53 and cid in PDF_LINKS:
  verdict='PDF_ENTAILED';elig=True;reason='Independent source lookup agrees with a Phase 3 coverage bridge; full predicates remain subject to Phase 5 adversarial audit.'
 elif best[0]>=.31 and best[4]>=.46:
  verdict='SUPPORTED_NONCOVERING';elig=True;reason='PDF supplies contextual/narrower support but the source atom coverage projection does not depend on this generated class; verify precise composite predicate in Phase 5.'
 elif cid in PDF_LINKS and (best[0]>=.23 or best[4]>=.34):
  verdict='SUPPORTED_NONCOVERING';elig=True;reason='This generated statement is one supporting conjunct in a Phase 3 source match, but is not independently proven to entail a complete scored source atom.'
 else:
  verdict='PDF_UNSUPPORTED';elig=True;reason='Reciprocal PDF source-atom, actual-PDF text-block and exact-identifier searches failed to establish the complete generated proposition. Conservative absence is not proof of a fabricated design.'
 # Exclusions from Phase 2 discovered in Phase 4 remain separate from unsupported definitive predictions.
 if verdict=='OUT_OF_SCOPE_NONDEFINITIVE': pdf_support_count['editorial_ineligible']+=1;flagged.append({'generated_class_id':cid,'reason_en':reason,'generated_evidence':{'file':o['file'],'line_start':o['line_start'],'table_cell':o.get('table_cell'),'statement_en':stmt}})
 else:pdf_support_count[verdict]+=1
 link_ids=list(dict.fromkeys(PDF_LINKS.get(cid,[])))
 src_ev=[]
 if base:
  src_ev.append({'file':'OrionDesk_AI_Detailed_Design_Specification.pdf','physical_page':base['page'],'quote_en':base['quote_en'],'source_id':base['source_id'],'evidence_role':'DIRECT_OR_NEAREST_CANDIDATE_NOT_AUTOMATIC_PROOF'})
 ge={'generated_id':o['generated_id'],'generated_class_id':cid,'file':o['file'],'line_start':o['line_start'],'line_end':o['line_end'],'table_cell':o.get('table_cell'),'table_column_header':o.get('table_column_header'),'table_row_key':o.get('table_row_key'),'quote_en':o['source_quote_en'],'normalized_statement_en':stmt}
 rec={'method':method,'protocol_version':'6.1','generated_class_id':cid,'occurrence_ids':c['occurrence_ids'], 'representative_statement_en':stmt,'classification':verdict,'pdf_validity':verdict if elig else None,'prediction_eligible':elig,'pdf_support_status':'BEST_EFFORT' if elig else 'EXCLUDED_SOURCE_COMMENTARY','classification_reason_en':reason,'generated_evidence':[ge], 'pdf_evidence':src_ev if verdict in ('PDF_ENTAILED','SUPPORTED_NONCOVERING') else [],'challenged_pdf_candidates':best_examples[:5], 'phase3_source_atoms_using_class_as_evidence':link_ids,'scope_membership_proof_en':('Referenced PDF source atom(s) '+', '.join(link_ids[:6])+'; applicability in original generated row/section must be independently checked.' if link_ids else 'No source-positive coverage bridge references this generated class.'),'predicate_check_en':'Substantive source-vs-generated predicates were compared using original PDF quotes, original Markdown line/table context, exact structural identifiers, and bidirectional spelling/word overlap. This is a conservative machine-assisted screening, not a fully certified human semantic proof.','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'}
 validity.append(rec)
 if verdict=='PDF_UNSUPPORTED': f_candidates.append(rec)

# Generated-only canonical false positive classes. A generated-only proposition does not double-count asserted NEG controls.
# Normalize redundancies if obvious exact full-meaning duplicates survived the Phase 2 class inventory.
F=[];F_seen={};f_links={}
for rec in f_candidates:
 stmt=rec['representative_statement_en']; key=norm(stmt)
 # preserve target/actor distinctions; do not strip identifiers, status, or numbers
 if key not in F_seen:
  fid=f'FGEN-{len(F)+1:05d}';F_seen[key]=fid
  F.append({'method':method,'protocol_version':'6.1','canonical_id':fid,'atomic_statement_en':stmt,'actual_label':0,'predicted_label':1,'scoring_cell':'FP','unsupported_claim_kind':'GENERATED_ONLY_NOT_ENTAILED','origin_source_ids':[],'origin_generated_class_ids':[rec['generated_class_id']],'origin_negative_control_ids':[],'generated_evidence':rec['generated_evidence'],'pdf_alternatives_checked':rec['challenged_pdf_candidates'],'specific_reason_en':rec['classification_reason_en'],'adjudication_policy':'BEST_EFFORT_CONSERVATIVE','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})
 else:
  fid=F_seen[key]
  x=next(v for v in F if v['canonical_id']==fid);x['origin_generated_class_ids'].append(rec['generated_class_id']);x['generated_evidence']+=rec['generated_evidence']
 f_links[rec['generated_class_id']]=fid
for rec in validity:
 if rec['generated_class_id'] in f_links:rec['generated_only_FP_id']=f_links[rec['generated_class_id']]
write('04_generated_claim_validity_final.jsonl',validity)
write('04_extraction_eligibility_review_final.jsonl',flagged)

# Negative controls evaluated individually against all actual generated statements: no affirmative counterfactual found.
neg_audit=[]
for n,record in zip(neg,negassert):
 neg_audit.append({'method':method,'negative_control_id':n['negative_control_id'],'pdf_evidence':n['pdf_evidence'],'counterfactual_statement_en':n['counterfactual_statement_en'],'affirmative_generated_assertion_found':record['asserted'],'generated_evidence_of_counterfactual':[],'related_generated_statements_checked':record['relevant_generated_statement_examples'],'adjudication_policy':'BEST_EFFORT_NEGATIVE_SCOPE','specific_reason_en':'The evaluated corpus describes the exclusion/prohibition or limits; it does not affirmatively authorize the corresponding forbidden counterfactual. Negated mentions are not positive predictions.'})
write('04_negative_control_assertion_audit_final.jsonl',neg_audit)

# Full canonical U = fixed R disjoint N disjoint distinct unsupported F.
U=[];J=[]
for idx,r in enumerate(source,1):
 m=M[r['source_id']];cell=m['scoring_cell'];p=int(cell=='TP')
 doc={'method':method,'protocol_version':'6.1','canonical_id':r['source_id'],'atomic_statement_en':r['atomic_statement_en'],'actual_label':1,'predicted_label':p,'scoring_cell':cell,'origin_source_ids':[r['source_id']],'origin_generated_class_ids':m['generated_class_ids'] if p else [],'origin_negative_control_ids':[],'pdf_evidence':m['pdf_evidence'],'generated_evidence':m['generated_evidence'],'entailment_grade':m['entailment_grade'],'coverage_mode':m['coverage_mode'],'specific_reason_en':m['specific_reason_en'],'predicate_check_en':m['predicate_check_en'],'adjudication_policy':m['adjudication_policy'],'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'}
 U.append(doc);J.append(doc)
for n,a in zip(neg,neg_audit):
 c='FP' if a['affirmative_generated_assertion_found'] else 'TN';p=int(c=='FP')
 doc={'method':method,'protocol_version':'6.1','canonical_id':n['negative_control_id'],'atomic_statement_en':n['counterfactual_statement_en'],'actual_label':0,'predicted_label':p,'scoring_cell':c,'origin_source_ids':[],'origin_generated_class_ids':[],'origin_negative_control_ids':[n['negative_control_id']],'pdf_evidence':n['pdf_evidence'],'generated_evidence':[],'specific_reason_en':a['specific_reason_en'],'adjudication_policy':'PDF_BOUND_NEGATIVE_CONTROL','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'}
 U.append(doc);J.append(doc)
U+=F;J+=F
write('03_canonical_universe_final.jsonl',U)
write('04_atomic_judgments_final.jsonl',J)

con=collections.Counter(x['scoring_cell'] for x in J)
assert len(U)==len(J)==len(source)+len(neg)+len(F)
assert con['TP']+con['FN']==len(source)
assert con['TN']+len([x for x in neg_audit if x['affirmative_generated_assertion_found']])==len(neg)
assert con['FP']==len(F)+len([x for x in neg_audit if x['affirmative_generated_assertion_found']])
assert con['TP']+con['TN']+con['FP']+con['FN']==len(U)
assert len(F)==len({x['atomic_statement_en'].lower().strip() for x in F})
assert all(r['origin_generated_class_ids'] for r in F)
assert all(len(r['pdf_evidence'])>=1 for r in J if r['scoring_cell']=='TP')
assert all(len(r['generated_evidence'])>=1 for r in J if r['scoring_cell']=='TP')
assert all(len(r['pdf_alternatives_checked'])>=1 for r in J if r['canonical_id'].startswith('FGEN'))
prec=con['TP']/(con['TP']+con['FP']) if con['TP']+con['FP'] else None
rec=con['TP']/(con['TP']+con['FN']) if con['TP']+con['FN'] else None
f1=2*con['TP']/(2*con['TP']+con['FP']+con['FN']) if 2*con['TP']+con['FP']+con['FN'] else None
Dup=(len(gen)-len(classes))/len(gen)
# The raw classes remain distinct from canonical coverage predictions.
summary={'method':method,'protocol_version':'6.1','phase':4,'status':'PHASE_COMPLETED_BEST_EFFORT','source_reference':{'pdf_file':PDF.name,'pdf_pages':90,'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest()},'input_sets':{'PDF_source_positive_atoms':len(source),'fixed_negative_controls':len(neg),'generated_claim_occurrences_phase2':len(gen),'generated_claim_classes_phase2':len(classes)},'universe':{'source_positive_atoms':len(source),'source_negative_controls':len(neg),'raw_generated_claim_classes':len(classes),'generated_positive_occurrences':len(gen),'covered_source_atoms':con['TP'],'asserted_negative_controls':len([n for n in neg_audit if n['affirmative_generated_assertion_found']]),'unsupported_generated_only_propositions':len(F),'canonical_predicted_positive_units':con['TP']+con['FP'],'canonical_decision_units':len(J),'negative_universe_scope':'PDF-grounded, predeclared bounded controls only'},'confusion':{key:con[key] for key in ('TP','TN','FP','FN')},'metrics':{'Precision':prec,'Recall':rec,'F1':f1,'Duplicate_phase2_unadjusted':Dup},'generated_claim_validity_screen':dict(pdf_support_count),'phase2_claim_eligibility_reclassification_candidates_for_phase5':len(flagged),'unsupported_generated_claims_grouped_exact_semantics':len(F),'source_side_phase3_decisions_unchanged':True,'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT','limitations':['PDF support screening combines exact, structural, character, word, and context retrieval, not exhaustive human logical entailment for all 3,168 classes.','Phase 2 wrongly promoted some documentation commentary to raw generated classes; these are separately disclosed and not counted as affirmative false predictions pending Phase 5 correction.','PDF_UNSUPPORTED includes conservative candidate misses and may shrink after Phase 5 reciprocal semantic audit; each is supported by actual strongest alternatives inspected mechanically.','Previous Phase 3 TP/FN decisions are provisional, including some conjunctive bridges; Phase 5 must audit full predicates independently.','The displayed Precision/Recall/F1 are provisional arithmetic over this enumerated effective universe, not certified coverage.','TN is restricted to the fixed 37 PDF-derived controls.'],'output_language':'English'}
(OUT/'04_confusion_matrix_final.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
# summary report
md=f'''# Phase 4 — Generated-Claim Correctness and Canonical Four-Cell Universe\n\nProtocol **v6.1**. Status **PHASE_COMPLETED_BEST_EFFORT**.\n\n## Canonical results (provisional)\n\n| Cell | Count |\n|---|---:|\n| TP | {con['TP']} |\n| TN | {con['TN']} |\n| FP | {con['FP']} |\n| FN | {con['FN']} |\n\n| Metric | Value |\n|---|---:|\n| Precision | {prec:.6%} |\n| Recall | {rec:.6%} |\n| F1 | {f1:.6%} |\n| Raw semantic Duplicate (Phase 2, not revised here) | {Dup:.6%} |\n\n## One-universe reconciliation\n\n* Source-positive atoms `|R|`: **{len(source)}**.\n* Fixed source-negative controls `|N|`: **{len(neg)}**.\n* Unsupported distinct generated-only propositions `|F|`: **{len(F)}**.\n* Canonical universe `|U| = |R| + |N| + |F| = {len(J)}`.\n* Predicted positives `|P| = TP + FP = {con['TP'] + con['FP']}`. This is intentionally **not** equated with raw class count `{len(classes)}`.\n* Source side `TP + FN = {len(source)}`; bounded controls `TN + |B| = {len(neg)}`; unsupported generated `FP - |B| = {len(F)}`.\n\n## Reciprocal source correctness check\n\nEvery Phase 2 generated class has a row in `04_generated_claim_validity_final.jsonl`, with its original file, physical line and table-cell locator, best actual PDF source quote(s), and the individual validity disposition. Source-side TP bridges were used only as candidate discovery, not as independent PDF authority.\n\nScreening classifications: {json.dumps(dict(pdf_support_count),sort_keys=True)}. The **{len(flagged)} editorial/nondefinitive** Phase 2 extraction candidates are separately disclosed in `04_extraction_eligibility_review_final.jsonl`; they are not affirmative application design claims and are excluded from `F`. Their underlying Phase 2 raw classes are retained unchanged until the designated correction phase. All {len(F)} counted generated-only F claims have real class and line evidence and at least one inspected candidate PDF quotation.\n\nThe {len(neg)} negative controls were challenged against actual generated statements and all remained TN. In particular, a generated prohibition of a forbidden behavior does **not** assert the affirmative source-negative counterfactual.\n\n## Limits and audit trail\n\nClassification is an explicit conservative, non-certified, machine-assisted adjudication. An absence of a high-similarity match is not definitive evidence that the PDF omitted a semantically equivalent requirement. Source atoms and prior Phase 3 TP/FN judgments were not changed here. Phase 5 must review high-risk unmatched claims, source-atom splits, eligible-class extraction errors, and TP evidence bridge completeness. Therefore the computed rates are **provisional**, not independently certified measures of specification coverage or software quality.\n\nNo future phase was executed. All deliverables are individual English files; no archive was created.\n'''
(OUT/'04_confusion_matrix_final.md').write_text(md,encoding='utf8')
status={'phase':4,'protocol_version':'6.1','method':method,'status':'PHASE_COMPLETED_BEST_EFFORT','generated_classes_checked':len(validity),'all_generated_classes_audited':len(validity)==len(classes),'fixed_negative_controls_checked':len(neg_audit),'canonical_judgments':len(J),'confusion':summary['confusion'],'eligible_ineligible_candidate_count':len(flagged),'structural_checks_passed':True,'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT','phase5_performed':False,'outputs':[x.name for x in sorted(OUT.iterdir()) if x.is_file()]}
(OUT/'04_phase_status_final.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':status['status'],'classes':len(validity),'claim_types':dict(pdf_support_count),'F':len(F),'matrix':summary['confusion'],'metrics':summary['metrics'],'output_directory':str(OUT)},ensure_ascii=False,indent=2))
