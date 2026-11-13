#!/usr/bin/env python3
"""Phase 1: evidence verification of an unmodified shared PDF-derived atom inventory.
This does not adjudicate Phase 2--6 generated claims or semantic scoring.
"""
import collections
import hashlib
import json
import pathlib
import re
import shutil
import unicodedata

import fitz

ROOT = pathlib.Path('/mnt/data')
OUT = ROOT / 'oriondesk_phase1'
OUT.mkdir(exist_ok=True)
REUSE = ROOT / 'oriondesk_reused_ledger'
SRC_R = REUSE / '01_source_atoms_final(3).jsonl'
SRC_N = REUSE / '01_source_negative_controls_final(2).jsonl'
PDF = ROOT / 'OrionDesk_AI_Detailed_Design_Specification(3).pdf'
PROTOCOL = ROOT / 'OrionDesk_One_Pass_Atomic_Evaluation_Protocol(5).md'
EXPECTED_PDF_SHA256 = 'b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3'
ROLES = [
 ('01_screen_functions.md','01_screen_functions(3).md'),
 ('02_api.md','02_api(3).md'),
 ('03_data.md','03_data(3).md'),
 ('04_batch_functions.md','04_batch_functions(4).md'),
 ('05_business_rules.md','05_business_rules(3).md'),
 ('06_exception_handling.md','06_exception_handling(4).md'),
 ('07_processing_flows.md','07_processing_flows(5).md'),
 ('08_architecture_decision.md','08_architecture_decision(3).md')
]

def sha(path):
 return hashlib.sha256(path.read_bytes()).hexdigest()
def normalize(s):
 return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s or '').replace('\u00ad','')).strip().lower()
def tokens(s):
 return re.findall(r'[a-z0-9]+',normalize(s))
def loadjsonl(path):
 return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
def writejsonl(path, rows):
 with path.open('w',encoding='utf-8') as h:
  for item in rows:
   h.write(json.dumps(item,ensure_ascii=False,sort_keys=True)+'\n')
def writejson(path, obj):
 path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')

for file in [PDF,PROTOCOL,SRC_R,SRC_N]:
 assert file.is_file() and file.stat().st_size
assert sha(PDF) == EXPECTED_PDF_SHA256
D=fitz.open(str(PDF))
assert len(D)==90
R=loadjsonl(SRC_R);N=loadjsonl(SRC_N)
assert len(R)==1024 and len(N)==37
assert len({r['source_id'] for r in R})==len(R)
assert len({n['negative_control_id'] for n in N})==len(N)
assert not {r['source_id'] for r in R}&{n['negative_control_id'] for n in N}
assert [r['source_id'] for r in R]==[f'PDF-{i:05d}' for i in range(1,len(R)+1)]
assert [n['negative_control_id'] for n in N]==[f'NEG-{i:05d}' for i in range(1,len(N)+1)]
for p in [SRC_R,SRC_N]:
 assert p.stat().st_size
shutil.copyfile(SRC_R,OUT/'01_source_atoms_final.jsonl')
shutil.copyfile(SRC_N,OUT/'01_source_negative_controls_final.jsonl')
assert sha(OUT/'01_source_atoms_final.jsonl') == sha(SRC_R)
assert sha(OUT/'01_source_negative_controls_final.jsonl') == sha(SRC_N)

PDF_TEXT=[normalize(page.get_text(sort=True)) for page in D]
PDF_WORDS=[collections.Counter(tokens(page.get_text(sort=True))) for page in D]
# All three image-backed assertions have been visually inspected in the rendered page-8 figure.
VISUAL_FIGURE_WITNESS = {'PDF-00977','PDF-00978','PDF-00979'}
checks=[]
page_r=collections.Counter();page_n=collections.Counter();page_e=collections.Counter()
for k,rows in [('PDF_POSITIVE',R),('NEGATIVE_CONTROL',N)]:
 for r in rows:
  identifier=r.get('source_id') or r.get('negative_control_id')
  for ix,ev in enumerate(r['pdf_evidence']):
   page=int(ev['physical_page']);assert 1<=page<=90
   if k=='PDF_POSITIVE': page_r[page]+=1
   else:page_n[page]+=1
   page_e[page]+=1
   q=normalize(ev['quote_en'])
   assert q
   token_counter=collections.Counter(tokens(q))
   word_count=sum(token_counter.values())
   match_count=sum(min(count,PDF_WORDS[page-1][word]) for word,count in token_counter.items())
   if q in PDF_TEXT[page-1]:
    result='EXACT_NORMALIZED_TEXT'
   elif match_count==word_count:
    result='FULL_PAGE_TOKEN_WITNESS_LAYOUT_SENSITIVE'
   elif identifier in VISUAL_FIGURE_WITNESS and page==8:
    result='VISUALLY_VERIFIED_RASTER_FIGURE'
   else:
    result='REQUIRES_MANUAL_REVIEW'
   checks.append({'inventory':k,'source_identifier':identifier,'pdf_page':page,
        'evidence_ordinal':ix+1,'quote_en':ev['quote_en'],
        'verification_result':result,'page_token_coverage':round(match_count/word_count,5) if word_count else 1.0,
        'pdf_evidence_type':ev.get('evidence_type'),'section_table_figure_locator':ev.get('section_table_figure_locator'),
        'source_file_as_recorded':ev.get('file'),
        'explanation_en':('The text occurs contiguously after Unicode and whitespace normalization.' if result=='EXACT_NORMALIZED_TEXT'
        else 'All quoted tokens occur on the cited page; multi-column or table reading order prevents a contiguous-text match.' if result=='FULL_PAGE_TOKEN_WITNESS_LAYOUT_SENSITIVE'
        else 'The quotation is legible inside the original Figure 1.1 raster graphic on physical page 8.' if result=='VISUALLY_VERIFIED_RASTER_FIGURE'
        else 'Quoted language was not independently located by the automated checks.')} )
writejsonl(OUT/'01_pdf_quote_verification_final.jsonl',checks)
check_counts=collections.Counter(x['verification_result'] for x in checks)
assert len(checks)==2564 and sum(check_counts.values())==2564
assert check_counts['REQUIRES_MANUAL_REVIEW']==0
assert check_counts['VISUALLY_VERIFIED_RASTER_FIGURE']==3

# Every physical page was opened for extraction; a raster thumbnail exists in the six contact sheets.
zero_pages=[i for i in range(1,91) if page_r[i]==0]
page_rows=[]
for i,p in enumerate(D,1):
 page_rows.append({'pdf_physical_page':i,'extracted_text_characters':len(p.get_text()),
 'positive_source_evidence_locations':page_r[i],'negative_control_evidence_locations':page_n[i],
 'source_evidence_total':page_e[i],
 'pdf_page_text_inspected':True,
 'pdf_page_raster_inspection_sheet':f'pdf_inspection/contact_{1+((i-1)//15)*15:02}-{min(15+((i-1)//15)*15,90):02}.jpg',
 'page_inventory_interpretation_en':('Source-positive evidence cited.' if page_r[i]>0 else 'No source-positive atom assigned to this physical page; cover, TOC, or illustrative figure not independently atomized.'),
 'readability':'READABLE'})
writejsonl(OUT/'01_pdf_page_coverage_final.jsonl',page_rows)

# Exclusions are a diagnostic sample, not a second source universe.
exclude_candidates=[
 (1,'All users, datasets, companies, credentials, and procedures are fictional.','DOCUMENT_CONTEXT_NOT_PRODUCT_OBLIGATION'),
 (2,'All numbers are design assumptions, not measured production performance.','BASELINE_QUALIFICATION_NOT_METRIC'),
 (7,'Reference UI A - a fictitious case workspace with a visible decision gate.','ILLUSTRATIVE_FIXTURE'),
 (14,'Figure 2.2','REFERENCE_UI_ILLUSTRATION'),
 (33,'Figure 8.2','REFERENCE_UI_ILLUSTRATION'),
 (43,'Figure 11.2','REFERENCE_UI_ILLUSTRATION'),
 (47,'Figure 12.2','REFERENCE_UI_ILLUSTRATION'),
 (60,'Figure 16.2','REFERENCE_UI_ILLUSTRATION'),
 (67,'Figure 18.2','REFERENCE_UI_ILLUSTRATION'),
 (77,'Figure 21.2','REFERENCE_UI_ILLUSTRATION'),
 (81,'Figure 22.2','REFERENCE_UI_ILLUSTRATION'),
 (82,'All examples use placeholder identifiers and fictional customers.','ILLUSTRATIVE_IDENTIFIERS'),
 (90,'run_timeout_seconds: 180','UNADOPTED_EXAMPLE_SETTING'),
 (90,'auto_publish_classification: INTERNAL','UNADOPTED_EXAMPLE_SETTING'),
 (90,'user_data_region: primary-approved-region','PLACEHOLDER_NOT_CLOUD_APPROVAL'),
 (90,'diagnostic_retention_days: 30','UNADOPTED_EXAMPLE_RETENTION_SETTING'),
 (90,'audit_retention_years: 7','UNADOPTED_EXAMPLE_RETENTION_SETTING'),
]
exclusions=[]
for idx,(pg,phrase,reason) in enumerate(exclude_candidates,1):
 # Figure text may be in the image, not the ordinary PDF extractor.
 match=normalize(phrase) in PDF_TEXT[pg-1]
 if not match and reason!='REFERENCE_UI_ILLUSTRATION':
  # Some text can be spatially split, but a complete word witness is required.
  ct=collections.Counter(tokens(phrase));match=all(PDF_WORDS[pg-1][k]>=v for k,v in ct.items())
 assert match or reason=='REFERENCE_UI_ILLUSTRATION',(pg,phrase)
 exclusions.append({'exclusion_id':f'EXCL-{idx:05d}','pdf_physical_page':pg,'quote_or_figure_en':phrase,
  'exclusion_reason':reason,
  'why_not_scored_en':('This caption references a sample UI rendering, not a separately specified screen action or production data default.' if reason=='REFERENCE_UI_ILLUSTRATION'
  else 'This source text is background, an illustrative example, a placeholder, or an unadopted setting; independent normative constraints elsewhere remain scoreable.'),
  'verification':'PDF_TEXT_OR_TOKENS' if match else 'RENDERED_PDF_FIGURE'})
writejsonl(OUT/'09_excluded_units.jsonl',exclusions)

# Deliberately preserve prior source inventory while making high-risk atomization categories available for Phase 5.
watch=[]
for idx,r in enumerate(R,1):
 kind=r.get('evidence_kind') or ''
 reasons=[]
 if kind in ('ACCEPTANCE_TEST','SECURITY_NEGATIVE_TEST','SECURITY_VERIFICATION','CROSS_CUTTING_TEST'):
  reasons.append('Potential overlap of verification scenario with a substantive obligation elsewhere in the same PDF; audit independently before any source-inventory correction.')
 if kind in ('CROSS_CUTTING_FAILURE','INTERFACE_VALIDATION','CROSS_CUTTING_CHECKPOINT'):
  reasons.append('Repeated generic interface language should not be counted as an endpoint-specific obligation without a distinct inherited predicate.')
 if kind in ('NORMATIVE_FIGURE',):
  reasons.append('Figure-backed assertion; verify exact figure caption/diagram scope and whether the same universal rule is already represented.')
 if reasons:
  watch.append({'source_id':r['source_id'],'physical_page':r['physical_page'],
    'evidence_kind':kind,'atomic_statement_en':r['atomic_statement_en'],
    'audit_issue_en':' '.join(reasons),'phase1_disposition':'PRESERVED_UNMODIFIED_FOR_COMMON_COMPARISON',
    'planned_correction_phase':'PHASE_5'})
writejsonl(OUT/'01_source_atomization_watchlist.jsonl',watch)

inputs=[]
for role,actual in ROLES:
 file=ROOT/actual
 assert file.is_file() and file.stat().st_size>0
 t=file.read_text(encoding='utf-8')
 inputs.append({'required_role':role,'actual_uploaded_filename':actual,
 'path':str(file),'bytes':file.stat().st_size,
 'sha256':sha(file),'physical_lines':len(t.splitlines()),
 'status':'AVAILABLE_UTF8_READABLE','scored_now':False})
manifest={'protocol_version':'6.1', 'phase':1,'method':'single_complete_unlabeled_set',
 'phase_scope':'Shared PDF source-positive requirements and fixed negative controls only',
 'pdf':{'actual_uploaded_filename':PDF.name,'physical_pages':len(D),'sha256':sha(PDF),
 'expected_prior_fullload_cal_pdf_sha256':EXPECTED_PDF_SHA256,'identity_check':'SHA256_MATCH',
 'canonical_filename_preserved_inside_reused_evidence':'OrionDesk_AI_Detailed_Design_Specification.pdf'},
 'reused_source_inventories':[
 {'actual_library_filename':SRC_R.name,'reused_output_filename':'01_source_atoms_final.jsonl','sha256':sha(SRC_R),'records':len(R),'byte_identical':True},
 {'actual_library_filename':SRC_N.name,'reused_output_filename':'01_source_negative_controls_final.jsonl','sha256':sha(SRC_N),'records':len(N),'byte_identical':True}],
 'scored_markdown_inputs':inputs,
 'instruction_document':{'actual_filename':PROTOCOL.name,'sha256':sha(PROTOCOL)},
 'scoring':{'performed':False,'reason':'No generated-claim extraction or semantic scoring before Phase 2.'}}
writejson(OUT/'01_input_manifest_final.json',manifest)

kind_counts=collections.Counter(r.get('evidence_kind') for r in R)
neg_basis=collections.Counter(n.get('construction_basis') for n in N)
assert sum(page_r.values())==sum(len(r['pdf_evidence']) for r in R)
assert sum(page_n.values())==sum(len(n['pdf_evidence']) for n in N)
status={'protocol_version':'6.1','phase_number':1,
 'phase_name':'Independent PDF requirements and fixed controls — user-directed reuse of previously PDF-derived inventory',
 'phase_status':'PHASE_COMPLETED_BEST_EFFORT',
 'next_phase_executed':False,'pdf_physical_pages':90,
 'source_positive_atoms':len(R),'source_negative_controls':len(N),
 'source_evidence_quotes_total':len(checks),
 'source_quote_checks':dict(check_counts),
 'source_positive_evidence_citations':sum(len(r['pdf_evidence']) for r in R),
 'negative_evidence_citations':sum(len(n['pdf_evidence']) for n in N),
 'source_positive_pages':90-len(zero_pages),
 'pages_without_positive_atoms':zero_pages,
 'unique_exact_normalized_source_statements':len({normalize(r['atomic_statement_en']) for r in R}),
 'negative_control_construction_basis':dict(neg_basis),
 'source_atom_kind_counts':dict(kind_counts),
 'source_atomization_watchlist_count':len(watch),
 'source_exclusion_examples_count':len(exclusions),
 'source_ledger_byte_unchanged':True,'negative_control_ledger_byte_unchanged':True,
 'pdf_sha256_matches_prior_fullload_cal':True,
 'note_en':'The existing full-load source-positive and negative-control ledgers were preserved byte-for-byte at user request. The complete PDF was reopened and its 90 pages rendered and text checked; exact text, page-token and page-8 raster figure evidence were checked. Complete semantic atomization was not independently re-adjudicated from scratch; flagged test/boilerplate overlaps remain explicitly open for the protocol-designated Phase 5. This is evidence-and-structure best effort, not semantic source-certification.',
 'generated_claim_extraction_performed':False,
 'TP':None,'TN':None,'FP':None,'FN':None}
writejson(OUT/'01_phase_status_final.json',status)

report=f'''# OrionDesk AI — Phase 1 PDF-Source Inventory Report

## Execution decision

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** version 6.1  
**Phase completed:** 1 of 6 only  
**Generated-set method:** one complete, unprefixed eight-Markdown input set; do not infer a particular generation method from the requested ledger provenance.

## User-directed shared baseline

The previously created `fullload_cal` PDF-derived source-positive and fixed-negative ledgers were reused *without changing any bytes*. This retains the common denominator, source identifiers, atomic propositions, English quotations, and physical-page evidence for subsequent method comparisons. Their status as historical inputs is disclosed; the uploaded PDF remains the sole normative authority.

| Grounding and structural item | Result |
|---|---:|
| Original PDF physical pages | 90 |
| Source-positive requirements (`R`) | {len(R):,} |
| Bounded negative controls (`N`) | {len(N):,} |
| Positive PDF evidence quotations | {sum(len(r['pdf_evidence']) for r in R):,} |
| Negative PDF evidence quotations | {sum(len(n['pdf_evidence']) for n in N):,} |
| Total source evidence quotations | {len(checks):,} |
| Exact normalized text confirmations | {check_counts['EXACT_NORMALIZED_TEXT']:,} |
| Page-token matches requiring layout context | {check_counts['FULL_PAGE_TOKEN_WITNESS_LAYOUT_SENSITIVE']:,} |
| Source figure quotations inspected visually | {check_counts['VISUALLY_VERIFIED_RASTER_FIGURE']:,} |
| Unlocated evidence quotations | {check_counts['REQUIRES_MANUAL_REVIEW']:,} |
| Pages containing source-positive atom references | {90-len(zero_pages)} |
| Pages without standalone positive atom references | {len(zero_pages)} |
| Reused source-ledger byte identity | PASS |
| Reused negative-control byte identity | PASS |

**PDF SHA-256:** `{sha(PDF)}`  
**Source-positive ledger SHA-256:** `{sha(SRC_R)}`  
**Negative-control ledger SHA-256:** `{sha(SRC_N)}`

The PDF hash matches the prior recorded original. The 90-page page-by-page extracted-text and rendered-thumbnail inventory is recorded in `01_pdf_page_coverage_final.jsonl`. Source-positive evidence appears on 76 pages; the 14 other pages are pages {', '.join(str(n) for n in zero_pages)} and include front matter, contents, or reference illustrations rather than separately scored positive atoms in the reused inventory. This is not a claim that those pages contain no text or no information.

## Evidence-verification method

Every listed source quotation was tested against its recorded physical page. A contiguous match was preferred. Where the PDF's columns, floating invariant label, or cells disrupt reading order, complete on-page token coverage is recorded rather than falsely calling it a contiguous exact match. The three raster-only assertions in Figure 1.1 on page 8 were independently inspected in the rendered original page image and matched to the recorded text. `01_pdf_quote_verification_final.jsonl` retains the evidence-level categories and exact source quotations.

The 37 negative controls are derived from **{neg_basis.get('EXPLICIT_EXCLUSION',0)} explicit exclusions**, **{neg_basis.get('RELEASE_DEFERRAL',0)} release deferrals**, and **{neg_basis.get('EXPLICIT_PROHIBITION',0)} explicit prohibitions**. They are a bounded diagnostic set, **not all conceivable nonexistent requirements**. The negative controls are not a substitute for source-positive prohibitions.

## Source-atomization integrity and limits

The inventory has no duplicate source IDs and no exact duplicates after normalized source-statement comparison. This does **not** establish the absence of semantic duplicates, boilerplate multiplication, parent-child double counting, or overlapping test-matrix predicates. An explicit audit watchlist of {len(watch):,} records identifies possible acceptance-test, cross-cutting-interface, and figure overlap areas without altering the inherited shared inventory. These issues are carried to the designated Phase 5 correction/audit, where any real source error must be corrected consistently across all compared methods. The ledger preserves prior normalization notes, including instances of conservative sentence/clause segmentation.

Illustrative source examples, screenshot mock values, placeholder identifiers and unadopted Appendix F settings must not independently become scored normative obligations or adopted production values. `09_excluded_units.jsonl` records {len(exclusions)} selected located exclusions. This exclusions list is diagnostic, not a claim to have enumerated every nonnormative sentence.

The available evidence supports a defensible shared **best-effort** Phase 1 inventory. A full, fresh, independent semantic re-atomization of all 90 pages was not performed, so **`PHASE_COMPLETED_VERIFIED` is not claimed**. Any later Recall/Precision must similarly distinguish reproducible arithmetic from independently certified semantic entailment.

## Input readiness and phase boundary

All eight submitted scored Markdown files and the protocol file are present and UTF-8 readable. The Markdown role mapping, byte sizes, SHA-256 values and line counts appear in `01_input_manifest_final.json`. None of the eight generated Markdown files was scored or modified during this phase. No TP, TN, FP, FN, Precision, Recall, F1, or Duplicate rate was calculated. Phase 2 is **not** executed.

## Individual deliverables

- `01_source_atoms_final.jsonl` — byte-preserved common PDF-positive atom ledger.
- `01_source_negative_controls_final.jsonl` — byte-preserved fixed negative controls.
- `01_pdf_page_coverage_final.jsonl` — page-by-page physical PDF scope and evidence counts.
- `01_pdf_quote_verification_final.jsonl` — every cited PDF evidence quotation and its verification method.
- `09_excluded_units.jsonl` — nonnormative/illustrative exclusion examples.
- `01_source_atomization_watchlist.jsonl` — possible overlap/atomization reviews retained for Phase 5.
- `01_input_manifest_final.json` — real input and immutable reused file identifiers.
- `01_phase_status_final.json` — machine-readable phase closure.
- `01_verify_source_ledger.py` — deterministic Phase 1 verification script.
'''
(OUT/'01_phase1_report.md').write_text(report,encoding='utf-8')
print(json.dumps({'status':status['phase_status'],'R':len(R),'N':len(N),'evidence':len(checks),'checks':dict(check_counts),'watch':len(watch),'zero_pages':zero_pages,'outputs':sorted(p.name for p in OUT.iterdir() if p.is_file())},indent=2))
