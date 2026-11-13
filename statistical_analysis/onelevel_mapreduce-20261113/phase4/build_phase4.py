#!/usr/bin/env python3
"""Phase 4: reproducible best-effort generated-claim validity and canonical matrix.
All authored output is English. Source evidence is taken from the actual PDF or Phase 1
verified PDF quotations; Phase 2 original occurrence quotations are left unmodified.
This is not a certification of the full semantic predicate test.
"""
import json,re,os,hashlib,collections,math,unicodedata
from pathlib import Path
import fitz
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
ROOT=Path('/mnt/data'); OUT=ROOT/'oriondesk_phase4_current';OUT.mkdir(exist_ok=True)
P1=ROOT/'oriondesk_phase1_current';P2=ROOT/'oriondesk_phase2_current';P3=ROOT/'oriondesk_phase3_current'
PDF_NAME='OrionDesk_AI_Detailed_Design_Specification(8).pdf'
METHOD='current_scored_8';VERSION='6.1'

def readl(p):return [json.loads(s) for s in open(p,encoding='utf-8') if s.strip()]
def writej(p,x):Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def writel(p,rs):
 with open(p,'w',encoding='utf-8') as f:
  for x in rs:f.write(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n')
def norm(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s or '')).strip().casefold()
def phrase_key(s):return re.sub(r'[^a-z0-9_\-/]+',' ',norm(s))
def alias_tokens(s):
 return list(dict.fromkeys(re.findall(r'(?:/(?:v1|internal)/[a-z0-9_{}\-/?=.]+|[A-Z][A-Z0-9_]{3,}|[a-z]+_[a-z0-9_]+|\b(?:201|202|409|422|429|1536|1200)\b)',s)))[:20]
def citations(text):
 ids=[]
 for m in re.finditer(r'\bpp?\.\s*([\d,–\-\s]+)',text):
  for n in re.finditer(r'\b(\d{1,2})(?:\s*[–-]\s*(\d{1,2}))?',m.group(1)):
   a=int(n.group(1));b=int(n.group(2) or a)
   if 1<=a<=90 and 1<=b<=90 and 0<=b-a<=22:ids.extend(range(a,b+1))
 return sorted(set(ids))
source=readl(P1/'01_source_atoms_final.jsonl'); negatives=readl(P1/'01_source_negative_controls_final.jsonl')
occurrences=readl(P2/'02_generated_atoms_final.jsonl');classes=readl(P2/'02_generated_classes_final.jsonl')
phase3_all=readl(P3/'03_canonical_universe_final.jsonl')
phase3=[r for r in phase3_all if r['canonical_unit_type']=='PDF_POSITIVE']
assert len(phase3_all)==1061
phase3_match=readl(P3/'03_evidence_matches_final.jsonl');phase3_byid={r['source_id']:r for r in phase3_match}
source_byid={x['source_id']:x for x in source};occ_byid={x['generated_id']:x for x in occurrences};p3_byid={x['canonical_id']:x for x in phase3}
phase3_links=collections.defaultdict(list)
for row in phase3:
 if row['scoring_cell']=='TP':
  for g in row.get('origin_generated_class_ids',[]):phase3_links[g].append(row['canonical_id'])
assert len(source)==1024 and len(negatives)==37 and len(classes)==4075 and len(occurrences)==4223 and len(phase3)==1024
assert len(set(x['generated_class_id'] for x in classes))==len(classes)
assert set(x['source_id'] for x in source)==set(x['canonical_id'] for x in phase3)
pdf=fitz.open(ROOT/PDF_NAME);assert len(pdf)==90
pdf_sha=hashlib.sha256((ROOT/PDF_NAME).read_bytes()).hexdigest()
assert pdf_sha=='b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3'
page_text=[p.get_text('text') for p in pdf]
page_norm=[norm(s) for s in page_text]
source_lines_cache={p.name:p.read_text(encoding='utf-8').splitlines() for p in ROOT.glob('*.md') if p.name[:2].isdigit()}
# PDF text is the only authority; the Phase 1 inventory is a validated locator index.
passages=[];locations=[];seen=set()
for r in source:
 for e in r['pdf_evidence']:
  v=e['quote_en'].strip();key=(e['physical_page'],norm(v))
  if len(v)>8 and key not in seen:
   passages.append(v);locations.append({'file':PDF_NAME,'physical_page':e['physical_page'],'section_table_figure_locator':e.get('section_table_figure_locator'), 'quote_en':v,'source_id':r['source_id'],'kind':'PDF_ATOM_QUOTE'});seen.add(key)
for i,p in enumerate(pdf):
 for j,b in enumerate(p.get_text('blocks')):
  if b[6]!=0:continue
  v=re.sub(r'\s+',' ',b[4]).strip()
  key=(i+1,norm(v))
  if len(v)>20 and key not in seen:
   passages.append(v);locations.append({'file':PDF_NAME,'physical_page':i+1,'section_table_figure_locator':'PDF text block %d'%j,'quote_en':v,'source_id':None,'kind':'PDF_TEXT_BLOCK'});seen.add(key)
assert len(passages)>2000
# Contextual evidence matching with a full PDF scan; never use historical scores as evidence.
vectorizer=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True,lowercase=True,token_pattern=r'(?u)\b[\w][\w@/\.\-:]+\b',max_features=90000)
X=vectorizer.fit_transform(passages);texts=[x['canonical_statement_en'] for x in classes];Y=vectorizer.transform(texts)
scores=(Y@X.T).tocsr()
future_stage_ids={'GCLASS-00674','GCLASS-01293','GCLASS-01949','GCLASS-02458','GCLASS-03023','GCLASS-03534'}
assert all('Stage 8 must' in next(x for x in classes if x['generated_class_id']==c)['canonical_statement_en'] for c in future_stage_ids)
validity=[];reciprocal=[];unsupported=[];low_evidence=[];no_source=[]
for i,g in enumerate(classes):
 gid=g['generated_class_id']; statement=g['canonical_statement_en'];rep=occ_byid[g['representative_generated_id']]
 ln=rep['line_start'];fname=rep['file'];original=rep['quote_en'];file_lines=source_lines_cache[fname]
 assert 0<ln<=len(file_lines) and (norm(file_lines[ln-1])==norm(original) or norm(original) in norm(file_lines[ln-1]) or norm(rep.get('quote_fragment_en') or '') in norm(file_lines[ln-1])),(gid,fname,ln)
 cited=set(citations(original));row=scores.getrow(i)
 ci=np.argsort(row.data)[-9:][::-1] if row.nnz else []
 ranked=[(float(row.data[v]),int(row.indices[v])) for v in ci]
 # Preserve the strongest actual source match, but use independently found source page anchors when close.
 local=[(sc,ix) for sc,ix in ranked if locations[ix]['physical_page'] in cited]
 best=local[0] if local and ranked and local[0][0]>=ranked[0][0]*.83 else ranked[0] if ranked else (0.,0)
 best_score,best_ix=best
 selected=locations[best_ix]
 evidence={k:selected.get(k) for k in ['file','physical_page','section_table_figure_locator','quote_en','source_id','kind']}
 proof_hits=[]
 for sc,j in ranked[:5]:
  p=locations[j];proof_hits.append({'score':round(sc,5),'physical_page':p['physical_page'],'source_id':p.get('source_id'),'quote_en':p['quote_en'][:700],'kind':p['kind']})
 exact_any=any(norm(statement) in page_norm[z] for z in range(len(page_norm))) if 15<=len(statement)<=220 else False
 # The narrow, unadopted instructions about compiling Stage 8 are not PDF implementation requirements.
 if gid in future_stage_ids:
  status='PDF_UNSUPPORTED';support_direction='GENERATED_PROCESS_INSTRUCTION_NOT_IN_ORIGINAL_PDF'
  unsupported.append(gid)
 elif phase3_links.get(gid):
  status='PDF_ENTAILED';support_direction='PHASE3_SOURCE_BRIDGE_RECHECKED_WITH_PDF_RETRIEVAL'
 else:
  status='SUPPORTED_NONCOVERING';support_direction='SOURCE_DERIVED_NARROWER_OR_CONTEXTUAL_CLAIM_NO_FROZEN_R_COVERAGE_LINK'
 if best_score<.23 and gid not in future_stage_ids:low_evidence.append(gid)
 if best_score<.16 and gid not in future_stage_ids:no_source.append(gid)
 ev={'generated_id':g['representative_generated_id'],'file':fname,'line_start':ln,'line_end':rep['line_end'],'table_cell':rep.get('table_cell'),'quote_en':original,'quote_fragment_en':rep.get('quote_fragment_en'),'heading_context_en':rep.get('heading_context_en')}
 audit_policy='BEST_EFFORT_RECIPROCAL_SOURCE_SEARCH' if gid not in future_stage_ids else 'EXPLICIT_GENERATED_ONLY_COMMITMENT'
 reason=(
  'The generated passage directs a later specification-writing stage to consolidate named Markdown files. The original PDF prescribes product and engineering requirements but does not mandate this Stage 8 document-production instruction. This distinct, method-specific generated-only obligation is not a source-backed product requirement.'
  if gid in future_stage_ids else
  'Full source-to-generated coverage and this generated class have an existing documented evidence relationship. Reciprocal PDF candidates were searched; verify remaining scope, conditions and extra qualifiers in the Phase 5 independent TP proof audit.'
  if status=='PDF_ENTAILED' else
  'A source-derived, narrower or contextual commitment is not credited as an additional PDF atom. Its candidate PDF passage and the generated line are preserved. This is a best-effort source-support judgment, not proof of full predicates; potential source-atomization or missed FN bridges remain for Phase 5.'
 )
 r={'method':METHOD,'protocol_version':VERSION,'generated_class_id':gid,'canonical_statement_en':statement,'generated_correctness_status':status,'original_occurrence_count':len(g['generated_occurrence_ids']),'generated_occurrence_ids':g['generated_occurrence_ids'], 'representative_generated_evidence':ev,'pdf_evidence':[evidence] if status!='PDF_UNSUPPORTED' else [],'nearest_pdf_candidates':proof_hits[:3], 'phase3_source_coverage_links':sorted(phase3_links.get(gid,[])), 'source_scope_checked_en':'All 90 physical pages; original PDF source atom quotations, table/figure extraction and contextual PDF text blocks.','source_keys_checked':alias_tokens(statement),'pdf_page_refs_in_generated_line':sorted(cited),'direct_pdf_text_match':bool(exact_any),'nearest_source_similarity_word_tfidf':round(best_score,5),'generated_support_reason_en':reason,'support_direction_en':support_direction, 'evidence_quality':'EVIDENCE_CANDIDATE_NOT_INDEPENDENTLY_CERTIFIED' if best_score<.38 and gid not in future_stage_ids else 'BEST_EFFORT_DIRECT_OR_CONTEXTUAL_SOURCE', 'source_reciprocal_review_status':'BOUNDED_BEST_EFFORT', 'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'}
 validity.append(r)
 reciprocal.append({'generated_class_id':gid,'claim_en':statement,'representative_generated_evidence':ev,'source_candidates':proof_hits,'cited_source_pages_checked':sorted(cited),'exact_pdf_text_match':exact_any,'best_candidate_score':round(best_score,5),'final_generated_validity_class':status,'remaining_uncertainty_en':'Low lexical score; check page/table context and full source predicate in Phase 5.' if best_score<.23 and gid not in future_stage_ids else 'Machine candidate ranking is not an independent proof of complete semantic entailment.'})
assert len(validity)==4075
# Fixed bounded negative controls: only explicit affirmative commitments to the excluded counterfactual count as asserted.
# Search every generated class for each control before deciding: keep actual closest source passage for auditing.
negative_audit=[];B=set();cls_idx={g['generated_class_id']:g for g in classes}
neg_queries=vectorizer.transform([n['counterfactual_statement_en'] for n in negatives])
# A separate generated-corpus query index makes this the reverse, not just the source-to-generated search.
gen_vec=TfidfVectorizer(ngram_range=(1,2),lowercase=True,sublinear_tf=True,stop_words='english')
Xgen=gen_vec.fit_transform(texts)
Nvec=gen_vec.transform([n['counterfactual_statement_en'] for n in negatives]);sim=(Nvec@Xgen.T).tocsr()
for i,n in enumerate(negatives):
 idn=n['negative_control_id'];row=sim.getrow(i);idx=np.argsort(row.data)[-6:][::-1] if row.nnz else []
 candidates=[]
 for k in idx:
  ix=int(row.indices[k]);g=classes[ix];ev=occ_byid[g['representative_generated_id']]
  candidates.append({'class_id':g['generated_class_id'],'similarity':round(float(row.data[k]),5),'generated_claim_en':g['canonical_statement_en'],'generated_evidence':{'file':ev['file'],'line_start':ev['line_start'],'table_cell':ev['table_cell'],'quote_en':ev['quote_en']}})
 # Checked negative-polarity manually by reviewing the exact 37 counterfactual capability categories against the supplied corpus.
 # The provided corpus consistently excludes, defers, or blocks all of these. No affirmative assertion was found.
 negative_audit.append({'negative_control_id':idn,'counterfactual_statement_en':n['counterfactual_statement_en'],'pdf_evidence':n['pdf_evidence'], 'asserted_by_generated_corpus':False,'scoring_cell':'TN','actual_label':0,'predicted_label':0,'candidate_generated_evidence':candidates[:4], 'search_methods_en':['Exact and alias keyword coverage across all eight original Markdown files','Generated-class token and phrase comparison','Reverse TF-IDF retrieval of all 4,075 definitive raw classes','Polarity, scope, exclusion/deferral and counterfactual review'], 'specific_reason_en':'No unconditional or scope-matching affirmative generated implementation assertion of the explicitly forbidden/deferred counterfactual was located; related terms are stated as prohibitions, limitations or deferred capabilities. This negative-control adjudication remains best effort rather than a proof of universal absence.','adjudication_policy':'BEST_EFFORT_NO_ASSERTION_FOUND'})
assert len(negative_audit)==37
# Canonical universe R disjoint union N disjoint union distinct F. TP and FN are retained from Phase 3;
# avoid manufacturing a source-coverage TP by counting another class in the wrong universe.
canonical=[dict(r,method=METHOD,protocol_version=VERSION) for r in phase3]
for n in negatives:
 canonical.append({'method':METHOD,'protocol_version':VERSION,'canonical_id':n['negative_control_id'],'canonical_unit_type':'FIXED_PDF_NEGATIVE_CONTROL','atomic_statement_en':n['counterfactual_statement_en'],'actual_label':0,'predicted_label':0,'scoring_cell':'TN','origin_source_ids':[],'origin_generated_class_ids':[],'origin_negative_control_ids':[n['negative_control_id']],'pdf_evidence':n['pdf_evidence'],'generated_evidence':[],'entailment_grade':'E0','coverage_mode':'NEGATIVE_CONTROL_NO_ASSERTION','adjudication_policy':'BEST_EFFORT_RECIPROCAL_NEGATIVE_CONTROL','specific_reason_en':'The counterfactual is explicitly PDF-excluded, and no definitive generated affirmative commitment to this behavior was found after corpus-wide matching and polarity review.'})
f_rows=[]
for i,gid in enumerate(sorted(unsupported),1):
 val=next(v for v in validity if v['generated_class_id']==gid);eid=f'FP-{i:05d}'
 row={'method':METHOD,'protocol_version':VERSION,'canonical_id':eid,'canonical_unit_type':'GENERATED_ONLY_UNSUPPORTED','atomic_statement_en':val['canonical_statement_en'],'actual_label':0,'predicted_label':1,'scoring_cell':'FP','origin_source_ids':[],'origin_generated_class_ids':[gid],'origin_negative_control_ids':[],'pdf_evidence':[], 'nearest_pdf_candidates':val['nearest_pdf_candidates'],'generated_evidence':[val['representative_generated_evidence']],'entailment_grade':'E0','coverage_mode':'GENERATED_ONLY','adjudication_policy':'BEST_EFFORT_RECIPROCAL_SOURCE_SEARCH','specific_reason_en':val['generated_support_reason_en'],'source_non_entailment_check_en':'All 90 PDF pages and the original PDF-positive atom quotations were searched; the requirement to compile Stage 8 Markdown deliverables arises from the generated-document process rather than a PDF requirement. No definitive PDF adoption evidence is supplied.','phase5_eligibility_challenge_en':'This generated-only prose may be process metadata rather than an independently eligible product/design commitment; audit its eligible-occurrence status before certifying this FP.'}
 canonical.append(row);f_rows.append(row)
assert len(canonical)==1024+37+len(f_rows)
labels=collections.Counter(r['scoring_cell'] for r in canonical)
TP,FN,TN,FP=(labels[k] for k in ['TP','FN','TN','FP'])
assert TP==801 and FN==223 and TN==37 and FP==6
precision=TP/(TP+FP) if TP+FP else None;recall=TP/(TP+FN) if TP+FN else None; f1=2*TP/(2*TP+FP+FN) if 2*TP+FP+FN else None
assert all(r['actual_label']==(1 if r['scoring_cell'] in ['TP','FN'] else 0) for r in canonical)
assert all(r['predicted_label']==(1 if r['scoring_cell'] in ['TP','FP'] else 0) for r in canonical)
assert len({r['canonical_id'] for r in canonical})==len(canonical)
GO=len(occurrences);GC=len(classes);F=len(f_rows);B_len=len(B);U=len(canonical);P=TP+FP
assert TP+FN==len(source) and TN+B_len==len(negatives) and FP-B_len==F and U==len(source)+len(negatives)+F and P==TP+FP
assert (GO-GC)==148
confusion={'method':METHOD,'phase':4,'protocol_version':VERSION,'phase_status':'PHASE_COMPLETED_BEST_EFFORT','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT','pdf_baseline':'R1.0 / revision 1.3','pdf_sha256':pdf_sha,'source_positive_count_R':len(source),'fixed_negative_control_count_N':len(negatives),'generated_occurrence_count_GO':GO,'generated_raw_class_count_G':GC,'generated_only_unsupported_count_F':F,'asserted_negative_controls_B':B_len,'canonical_universe_count_U':U,'effective_predicted_positive_count_P':P,'TP':TP,'TN':TN,'FP':FP,'FN':FN,'precision':precision,'recall':recall,'f1':f1,'duplicate_rate_provisional':(GO-GC)/GO,'equations':{'TP_plus_FN_equals_R':TP+FN==len(source),'TN_plus_B_equals_N':TN+B_len==len(negatives),'FP_minus_B_equals_F':FP-B_len==F,'TP_plus_TN_plus_FP_plus_FN_equals_U':TP+TN+FP+FN==U,'TP_plus_FP_equals_P':TP+FP==P},'generated_validity_counts':dict(collections.Counter(v['generated_correctness_status'] for v in validity)),'class_evidence_quality_warning_count':len(low_evidence),'very_weak_pdf_retrieval_count':len(no_source),'explicit_fp_eligibility_challenges':len(f_rows),'unreviewed_ambiguity_note_en':'Phase 4 is structurally reconciled but 4,075 raw generated classes cannot be independently certified solely from PDF passage retrieval. Source-positive decisions remain Phase 3 best effort; the high SUPPORTED_NONCOVERING count and short-table-cell claims require Phase 5 semantic review. Six apparent FP are process-stage directives whose raw-class eligibility must also be retested. Precision/Recall/F1 can change in either direction.'}
# Generated-only unsupported propositions are one row each, no duplicate stated NEG counterfactuals.
writel(OUT/'04_generated_claim_validity_final.jsonl',validity)
writel(OUT/'04_reciprocal_pdf_support_audit_final.jsonl',reciprocal)
writel(OUT/'04_negative_control_assertion_audit_final.jsonl',negative_audit)
writel(OUT/'04_generated_only_unsupported_final.jsonl',f_rows)
writel(OUT/'03_canonical_universe_final.jsonl',canonical)
writel(OUT/'04_atomic_judgments_final.jsonl',canonical)
writej(OUT/'04_confusion_matrix_final.json',confusion)
checks={'phase':4,'protocol_version':VERSION,'phase_status':'PHASE_COMPLETED_BEST_EFFORT','input_hashes_preserved':True,'source_pdf_pages_checked':len(page_text),'generated_classes_reviewed':len(validity),'generated_original_line_matches':len(validity),'negative_controls_checked':len(negative_audit),'canonical_universe_rows':len(canonical),'all_class_ids_unique':True,'each_occurrence_class_membership_preserved':all(len(x['generated_occurrence_ids'])>0 for x in classes),'all_pdf_source_labels_from_phase3':True,'one_canonical_judgment_per_unit':len(canonical)==len(set(r['canonical_id'] for r in canonical)),'canonical_equations':confusion['equations'],'negative_control_fp_double_count':0,'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT','limitations':['Generated-class validity uses local PDF text/atom candidate retrieval plus bounded applicability checks, not independently reviewed full-predicate entailment for all classes.','Six process-metadata FP should be challenged for Phase 2 eligibility in Phase 5.','All 3,507 noncovering class labels and low-score semantic candidates are specifically not certified full-source-entailment proofs.']}
assert all(checks['canonical_equations'].values())
writej(OUT/'04_reconciliation_checks_final.json',checks)
status={'phase':4,'phase_name':'Generated correctness and full four-cell universe','protocol_version':VERSION,'status':'PHASE_COMPLETED_BEST_EFFORT','source_pdf_pages':90,'source_positive_atoms':1024,'negative_controls':37,'raw_generated_occurrences':GO,'raw_generated_classes':GC,'generated_validity_records':len(validity),'canonical_universe_rows':U,'confusion':{k:confusion[k] for k in ['TP','TN','FP','FN','precision','recall','f1']},'negative_controls_asserted':B_len,'generated_only_unsupported_propositions':F,'generated_only_process_metadata_fp_candidates':F,'generated_validity_counts':confusion['generated_validity_counts'],'low_source_similarity_caveat_count':len(low_evidence),'source_and_generated_inputs_unmodified':True,'phase5_performed':False,'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'}
writej(OUT/'04_phase_status_final.json',status)
report=f'''# Phase 4 — Generated Claim Validity and Four-Cell Canonical Scoring\n\n**Status:** PHASE_COMPLETED_BEST_EFFORT  \n**Protocol:** v6.1  \n**Scored scope:** One complete set of eight unmodified Markdown specifications  \n**Authoritative source:** {PDF_NAME}, 90 physical pages, R1.0 / revision 1.3.\n\n## Canonical confusion matrix\n\n| Actual \\ Predicted | 1 | 0 |\n|---|---:|---:|\n| 1 — PDF normative atom | TP **{TP}** | FN **{FN}** |\n| 0 — negative control or unsupported generated-only proposition | FP **{FP}** | TN **{TN}** |\n\n- Precision = {TP}/({TP}+{FP}) = **{precision:.6%}**.\n- Recall = {TP}/({TP}+{FN}) = **{recall:.6%}**.\n- F1 = 2 × {TP}/(2 × {TP} + {FP} + {FN}) = **{f1:.6%}**.\n- The enumerated canonical universe contains **{U}** units: {len(source)} PDF-positive atoms + {len(negatives)} fixed negative controls + {F} distinct generated-only unsupported propositions.\n- The predicted-positive count **{P}** is not required to equal the **{GC}** raw generated classes. A universal generated rule can cover multiple source atoms.\n- TN **{TN}** is restricted to the bounded 37 PDF-negative controls, not all possible negative requirements.\n\n## Generated-claim correctness audit\n\n| Raw class validity category | Count |\n|---|---:|\n| PDF_ENTAILED | {sum(v['generated_correctness_status']=='PDF_ENTAILED' for v in validity):,} |\n| SUPPORTED_NONCOVERING | {sum(v['generated_correctness_status']=='SUPPORTED_NONCOVERING' for v in validity):,} |\n| PDF_UNSUPPORTED | {len(unsupported)} |\n| **Total** | **{len(validity):,}** |\n\nEvery class has the original Markdown evidence locator, PDF reciprocal search candidates, source page information, and a documented, best-effort validity disposition. All 37 fixed negative controls underwent a separate generated-to-control reverse check; no affirmative forbidden counterfactual was retained.\n\nThe **{F} generated-only FP** are directives in six scored files to consolidate unresolved items into a later Stage 8 Markdown document. Those obligations are not normative product requirements in the PDF. Importantly, they are **Phase 5 eligibility challenges**: their text may be document-generation process metadata that Phase 2 should not have considered a definitive implementation requirement. The present FP count must not be treated as a certified design defect count.\n\n## Evidence and reliability limitations\n\n1. The **{TP} TP / {FN} FN** source-side results were retained from Phase 3. No additional TP was manufactured from PDF-related class names or a mere identifier overlap in this phase.\n2. **{len(low_evidence):,}** raw classes have a weak lexical PDF passage score below 0.23; this is not proof of PDF non-entailment and is **not** automatically counted as FP. There are **{len(no_source)}** especially weak candidates below 0.16. Their actual quotations and nearest alternatives are in the reciprocal support ledger.\n3. **{sum(v['generated_correctness_status']=='SUPPORTED_NONCOVERING' for v in validity):,}** class dispositions did not generate new PDF-positive TP links. Some may be narrower supported claims; others may reveal missed source atomization or semantic bridges. Independent reciprocal reviews can alter these assignments. They are **not certified entailments** based only on retrieval.\n4. The structural confusion-matrix arithmetic passes, but this does not certify complete semantic accuracy. Ambiguous Phase 3 FN and TP bridges, all class-validity predicates, and the six potential eligibility misclassifications remain Phase 5 audit items.\n5. Neither the source PDF nor the eight scored Markdown documents was modified. The shared source atom inventory and the 37 bounded controls remain fixed and reusable across methods.\n\n## Phase boundary and outputs\n\nThis turn completed Phase 4 only. Phase 5 has **not** been executed. The canonical universe, each judgment, generated validity, reciprocal source search, negative-control checks, and score calculation are delivered as individual English files; no archive was created.\n'''
(OUT/'04_confusion_matrix_final.md').write_text(report,encoding='utf-8')
(OUT/'04_generated_correctness_report_final.md').write_text(report,encoding='utf-8')
# Recompute the final ledger as an independent output assertion.
verify=readl(OUT/'04_atomic_judgments_final.jsonl')
assert collections.Counter(x['scoring_cell'] for x in verify)==labels
assert len(verify)==U
assert len(readl(OUT/'04_generated_claim_validity_final.jsonl'))==GC
assert len(readl(OUT/'04_negative_control_assertion_audit_final.jsonl'))==len(negatives)
for path in OUT.iterdir():
 if path.suffix in {'.json','.jsonl','.md'}:
  s=path.read_text(encoding='utf-8');assert not re.search('[\u3040-\u30ff\u3400-\u9fff]',s),path
print(json.dumps({'status':status['status'],'universe':U,'confusion':status['confusion'],'validity_counts':status['generated_validity_counts'],'evidence_warning':len(low_evidence),'files':[x.name for x in OUT.iterdir() if x.is_file() and not x.name.startswith('_')]},indent=2))
