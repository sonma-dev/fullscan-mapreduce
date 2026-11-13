#!/usr/bin/env python3
"""Independently reconcile a shared OrionDesk PDF-only requirement baseline.

This script verifies the uploaded PDF and current Markdown inputs without
using any generated specification or historical scoring judgment to create
source requirements. Original positive/negative ledgers remain byte-identical.
"""
from __future__ import annotations
import collections
import hashlib
import json
import pathlib
import re
import shutil
import unicodedata
from datetime import datetime, timezone

import fitz

ROOT = pathlib.Path('/mnt/data')
PRIOR = ROOT / '_prior_fullload_source'
OUT = ROOT / 'oriondesk_phase1_current'
SOURCE_INPUT = ROOT / 'OrionDesk_AI_Detailed_Design_Specification(8).pdf'
PROTOCOL_INPUT = ROOT / 'OrionDesk_One_Pass_Atomic_Evaluation_Protocol(10).md'
EXPECTED_PDF_SHA256 = 'b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3'
SCORING_INPUTS = [
    ('01_screen_functions', ROOT / '01_screen_functions(7).md'),
    ('02_api', ROOT / '02_api(7).md'),
    ('03_data', ROOT / '03_data(7).md'),
    ('04_batch_functions', ROOT / '04_batch_functions(7).md'),
    ('05_business_rules', ROOT / '05_business_rules(7).md'),
    ('06_exception_handling', ROOT / '06_exception_handling(8).md'),
    ('07_processing_flows', ROOT / '07_processing_flows(8).md'),
    ('08_architecture_decision', ROOT / '08_architecture_decision(7).md'),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def as_rows(path):
    return [json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]

def dump_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def dump_jsonl(path, obj):
    with path.open('w', encoding='utf-8') as f:
        for row in obj:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')

def normalize(s):
    s = unicodedata.normalize('NFKC', s)
    for a,b in [('\u00ad',''), ('\u200b',''),('–','-'),('—','-'),('−','-'),('“','"'),('”','"'),('’',"'")]:
        s=s.replace(a,b)
    return re.sub(r'\s+', ' ', s).strip().casefold()

assert SOURCE_INPUT.is_file()
assert PROTOCOL_INPUT.is_file()
assert sha(SOURCE_INPUT) == EXPECTED_PDF_SHA256
assert len(SCORING_INPUTS) == 8
assert len({name for name,_ in SCORING_INPUTS}) == 8
for _,p in SCORING_INPUTS:
    assert p.is_file()
    p.read_text(encoding='utf-8')

pdf = fitz.open(SOURCE_INPUT)
assert len(pdf) == 90
assert all(p.get_text('text').strip() for p in pdf)
page_texts = [p.get_text('text', sort=False) for p in pdf]
page_norm = [normalize(s) for s in page_texts]
image_pages = [i+1 for i,p in enumerate(pdf) if p.get_images(full=True)]
assert len(image_pages) == 31

# Preserve the requested common fullload_cal source inventory verbatim.
for filename in ('01_source_atoms_final.jsonl',
                 '01_source_negative_controls_final.jsonl',
                 '01_source_atomization_challenge_final.jsonl'):
    shutil.copyfile(PRIOR / filename, OUT / filename)
    assert sha(PRIOR / filename) == sha(OUT / filename)
shutil.copyfile(SOURCE_INPUT, OUT / 'OrionDesk_AI_Detailed_Design_Specification.pdf')
assert sha(OUT / 'OrionDesk_AI_Detailed_Design_Specification.pdf') == EXPECTED_PDF_SHA256

R=as_rows(OUT / '01_source_atoms_final.jsonl')
N=as_rows(OUT / '01_source_negative_controls_final.jsonl')
challenge=as_rows(OUT / '01_source_atomization_challenge_final.jsonl')
assert len(R)==1024 and len(N)==37 and len(challenge)==19
assert [a['source_id'] for a in R] == [f'PDF-{i:05d}' for i in range(1,1025)]
assert [n['negative_control_id'] for n in N] == [f'NEG-{i:05d}' for i in range(1,38)]
assert len({a['source_id'] for a in R}) == len(R)
assert len({n['negative_control_id'] for n in N}) == len(N)
assert {a['source_id'] for a in R}.isdisjoint({n['negative_control_id'] for n in N})
assert not (set(normalize(a['atomic_statement_en']) for a in R) &
            set(normalize(n['counterfactual_statement_en']) for n in N))

verified = []
match_counts=collections.Counter()
evidence_per_page=collections.Counter()
source_evidence_per_page=collections.Counter()
raster_ids={'PDF-00977','PDF-00978','PDF-00979'}
visual_assertion_page=8
for record_type, rows, key in [('SOURCE_POSITIVE', R, 'source_id'), ('NEGATIVE_CONTROL', N, 'negative_control_id')]:
    for row in rows:
        evidence = row['pdf_evidence']
        assert isinstance(evidence,list) and evidence, (record_type,row[key])
        for i,e in enumerate(evidence,1):
            page=e['physical_page']
            quote=e['quote_en']
            assert 1 <= page <= 90
            assert quote.strip()
            if row[key] in raster_ids and page==visual_assertion_page:
                assert record_type=='SOURCE_POSITIVE'
                method='VISUAL_FIGURE_1_1_PAGE_8'
                status='VISUALLY_INSPECTED'
                assert any(x in normalize(quote) for x in
                           ['tenant_id','immutable evidence','idempotent event processing'])
            else:
                assert normalize(quote) in page_norm[page-1], (row[key],page,quote[:100])
                method='NORMALIZED_EXACT_TEXT_ON_PHYSICAL_PAGE'
                status='MATCHED'
            verified.append({
                'record_type':record_type,
                'record_id':row[key],
                'evidence_sequence':i,
                'physical_page':page,
                'evidence_type':e.get('evidence_type','PDF_TEXT'),
                'original_pdf_quote_en':quote,
                'verified_against_uploaded_pdf':True,
                'verification_method':method,
                'verification_status':status,
            })
            match_counts[method]+=1
            evidence_per_page[page]+=1
            if record_type=='SOURCE_POSITIVE':
                source_evidence_per_page[page]+=1
assert len(verified)==2564
assert match_counts['NORMALIZED_EXACT_TEXT_ON_PHYSICAL_PAGE']==2561
assert match_counts['VISUAL_FIGURE_1_1_PAGE_8']==3

dump_jsonl(OUT/'01_pdf_quote_verification_final.jsonl',verified)

# Independently inspect every physical page and its text blocks. The older
# estimate of excluded text units is preserved as a historical estimate only.
prior_pages=as_rows(PRIOR/'01_pdf_page_coverage_final.jsonl')
assert len(prior_pages)==90
pos_by_page=collections.Counter(r['physical_page'] for r in R)
page_coverage=[]
for idx,p in enumerate(pdf):
    number=idx+1
    old=prior_pages[idx]
    assert old['physical_page']==number
    blocks=p.get_text('blocks')
    info={
        'physical_page':number,
        'readable_text':bool(page_texts[idx].strip()),
        'text_characters_current_extraction':len(page_texts[idx]),
        'text_lines_current_extraction':len(page_texts[idx].splitlines()),
        'physical_text_blocks_current_extraction':len(blocks),
        'embedded_image_count':len(p.get_images(full=True)),
        'visual_review_mode':('RENDERED_AND_INSPECTED_IN_CONTACT_SHEETS' if number in image_pages else 'NONE_PRESENT'),
        'positive_source_atoms':pos_by_page[number],
        'positive_evidence_locations':source_evidence_per_page[number],
        'all_evidence_locations_including_negative_controls':evidence_per_page[number],
        'prior_excluded_text_block_estimate':old['excluded_text_units'],
        'exclusion_estimate_is_individually_revalidated':False,
        'inspection_status':'INSPECTED_PDF_TEXT_AND_VISUALS' if number in image_pages else 'INSPECTED_PDF_TEXT',
    }
    if number == 8:
        info['specific_figure_assertions_visually_checked']=['PDF-00977','PDF-00978','PDF-00979']
    page_coverage.append(info)
assert sum(p['positive_source_atoms'] for p in page_coverage)==1024
assert sum(p['positive_evidence_locations'] for p in page_coverage)==2527
assert sum(p['all_evidence_locations_including_negative_controls'] for p in page_coverage)==2564
assert sum(p['prior_excluded_text_block_estimate'] for p in page_coverage)==274
dump_jsonl(OUT/'01_pdf_page_coverage_final.jsonl',page_coverage)

# Source exclusions are page-grouped, not invented as 274 independently
# classified text fragments. The page-block estimate is disclosed separately.
screenshot_pages={7,14,33,43,47,60,67,77,81}
exclusions=[]
for p in page_coverage:
    number=p['physical_page']
    old_count=p['prior_excluded_text_block_estimate']
    if old_count<=0:
        continue
    if number==1:
        category='COVER_AND_PUBLICATION_METADATA'
        evidence='SOFTWARE ENGINEERING / CONTROLLED SAMPLE'
    elif 2<=number<=6:
        category='TABLE_OF_CONTENTS_NAVIGATION'
        evidence='ORIONDESK AI'
    elif number in screenshot_pages:
        category='ILLUSTRATIVE_UI_OR_PAGE_DECORATION'
        evidence='ORIONDESK AI'
    elif number==90:
        category='EXAMPLE_CONFIGURATION_AND_PAGE_DECORATION'
        evidence='ORIONDESK AI'
    else:
        category='REPEATED_PAGE_DECORATION_OR_NONNORMATIVE_CONTEXT'
        evidence='ORIONDESK AI'
    assert normalize(evidence) in page_norm[number-1]
    exclusions.append({
        'excluded_unit_id':f'EXCL-SRC-PAGE-{number:03d}',
        'direction':'SOURCE',
        'scope':'PAGE_GROUPED_EXCLUSION_CONTEXT',
        'source':{
            'file':'OrionDesk_AI_Detailed_Design_Specification.pdf',
            'physical_page':number,
            'quote_en':evidence,
        },
        'exclusion_category':category,
        'excluded_text_block_estimate':old_count,
        'eligible_for_pdf_positive_inventory':False,
        'eligibility_reason_en':'Navigation, representative visual or publication/section decoration is not itself an independent normative product requirement. Source-positive statements on the same page remain scored in the unchanged source ledger.',
        'itemization_limitation_en':'This record is a grouped exclusion indicator, not proof that each estimated excluded text block was separately classified.',
    })
# The following semantically important illustrative contexts are separately
# retained with actual source-page text, never as source-positive atoms.
for number,quote,cat,reason in [
    (7,'Reference UI A - a fictitious case workspace with a visible decision gate.',
        'REPRESENTATIVE_UI_SCREENSHOT',
        'Illustrative screenshot values are not operational metrics, defaults, approved route aliases, or required extra screens.'),
    (87,'case_demo','EXAMPLE_TASK_PAYLOAD',
        'An illustrative A2A case identifier is not an approved adapter for a UUID-typed MCP field.'),
    (90,'run_timeout_seconds','EXAMPLE_CONFIGURATION',
        'An example timeout setting is not an adopted runtime default or deadline policy.'),
]:
    if normalize(quote) in page_norm[number-1]:
        exclusions.append({
            'excluded_unit_id':f'EXCL-SRC-EXAMPLE-{number:03d}',
            'direction':'SOURCE', 'scope':'SPECIFIC_SOURCE_ILLUSTRATION',
            'source':{'file':'OrionDesk_AI_Detailed_Design_Specification.pdf','physical_page':number,'quote_en':quote},
            'exclusion_category':cat,
            'eligible_for_pdf_positive_inventory':False,
            'eligibility_reason_en':reason,
            'itemization_limitation_en':'Explicit example qualifier; independently normative neighboring source statements are retained.',
        })
dump_jsonl(OUT/'09_excluded_units.jsonl',exclusions)

# Preserve all original challenges, with no hidden split/merge or renumbering.
assert sum(bool(c['correction_applied']) for c in challenge)==0
coverage_review={
    'source_positive_atoms':len(R),
    'fixed_negative_controls':len(N),
    'quote_evidence_locations':len(verified),
    'text_quote_locations_verified':match_counts['NORMALIZED_EXACT_TEXT_ON_PHYSICAL_PAGE'],
    'figure_1_1_visual_quotes_verified':match_counts['VISUAL_FIGURE_1_1_PAGE_8'],
    'verified_all_uploaded_pdf_pages':len(pdf),
    'image_bearing_pages':len(image_pages),
    'source_exclusions_grouped_records':len(exclusions),
    'prior_page_block_exclusion_estimate':274,
    'original_atomization_challenge_records':len(challenge),
    'source_atomization_changes_made':0,
    'source_ledger_sha256':sha(OUT/'01_source_atoms_final.jsonl'),
    'negative_control_ledger_sha256':sha(OUT/'01_source_negative_controls_final.jsonl'),
    'source_ledger_byte_identical_to_retrieved_fullload_cal':True,
    'negative_control_ledger_byte_identical_to_retrieved_fullload_cal':True,
    'source_only_status':'PHASE_COMPLETED_BEST_EFFORT',
    'semantic_certification':'SOURCE_EVIDENCE_LOCATORS_VERIFIED; ATOMIZATION_INDEPENDENCE_NOT_CERTIFIED',
    'method_scoring_performed':False,
}
dump_json(OUT/'01_source_evidence_verification_final.json',coverage_review)

def input_row(name,path):
    raw=path.read_bytes()
    return {'role':name,'actual_filename':path.name,'bytes':len(raw),
            'sha256':hashlib.sha256(raw).hexdigest(),
            'utf8_decodable':True,'physical_lines':len(raw.decode('utf-8').splitlines()),
            'present':True,'scored_or_extracted_in_phase1':False}

manifest={
    'phase':1,'protocol_version':'6.1',
    'method':'UNSPECIFIED_SINGLE_EIGHT_FILE_SET',
    'source_pdf':{'uploaded_actual_filename':SOURCE_INPUT.name,
                  'canonical_evidence_filename':'OrionDesk_AI_Detailed_Design_Specification.pdf',
                  'sha256':EXPECTED_PDF_SHA256,'physical_pages':90,
                  'bytes':SOURCE_INPUT.stat().st_size,
                  'document_id':'OD-AI-DDS-001',
                  'design_baseline':'R1.0 / revision 1.3',
                  'byte_identical_to_fullload_cal_pdf':True},
    'instruction_document':input_row('PROTOCOL',PROTOCOL_INPUT),
    'scored_markdown_inputs':[input_row(n,p) for n,p in SCORING_INPUTS],
    'source_ledger_provenance':{
        'fullload_cal_shared_positive_inventory':'01_source_atoms_final.jsonl',
        'fullload_cal_shared_negative_inventory':'01_source_negative_controls_final.jsonl',
        'source_atom_count':len(R),'negative_control_count':len(N),
        'source_atoms_preserved_byte_for_byte':True,
        'negative_controls_preserved_byte_for_byte':True,
        'source_quotes_independently_reverified_against_uploaded_pdf':True,
        'prior_generated_predictions_and_scores_used':False,
    },
    'no_archive_created':True,
}
dump_json(OUT/'01_input_manifest_final.json',manifest)

status={
    'phase':1,'phase_name':'Independent PDF requirements and fixed controls',
    'protocol_version':'6.1','status':'PHASE_COMPLETED_BEST_EFFORT',
    'source_pdf_verified':True,'all_90_pages_inspected':True,
    'source_positive_atoms':len(R),'fixed_negative_controls':len(N),
    'source_quote_evidence_matched':len(verified),
    'unmatched_source_quotes':0,
    'legacy_source_ledger_byte_preserved':True,
    'source_atomization_challenge_records':len(challenge),
    'source_atomization_changes_applied':0,
    'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT',
    'phase2_started':False,'scored_corpus_touched':False,
    'next_authorized_phase':'PHASE_2_ON_NEXT_USER_REQUEST',
    'limitations':[
        'Exact PDF quotation integrity is not a proof of meaningful atomization.',
        'The historical source inventory is preserved for stable comparison as requested; 19 substantive atomization challenge records remain identified for Phase 5 adjudication.',
        'Excluded text block counts are page-level prior estimates, not independently reviewed line-by-line exclusion decisions.',
        'Only source-side PDF requirements and source-negative controls have been processed; no generated judgments or scores exist for this turn.',
    ],
}
dump_json(OUT/'01_phase_status_final.json',status)

report=f'''# OrionDesk AI — Phase 1: PDF Source Requirements and Controls

**Protocol:** v6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Scope:** Original source PDF only. Generated-corpus scoring has not begun.

## Identity and input coverage

- Uploaded authoritative PDF: `{SOURCE_INPUT.name}`.
- Canonical evidence filename: `OrionDesk_AI_Detailed_Design_Specification.pdf` (byte-identical copy included with the deliverables).
- Document: `OD-AI-DDS-001`, release `R1.0`, design revision `1.3`.
- SHA-256: `{EXPECTED_PDF_SHA256}`.
- Physical source pages inspected: **90/90**; all pages contain readable extractable text.
- Embedded-image pages inspected: **31**, including the Figure 1.1 runtime assertions on physical page **8**.
- Scored Markdown inputs present and UTF-8 readable: **8/8**; eligible generated assertions are reserved for Phase 2.

## Common PDF-only inventories

| Inventory | Count | Provenance |
|---|---:|---|
| Source-positive atomic propositions (`R`) | {len(R):,} | Original `fullload_cal` ledger, copied unchanged and independently checked against this exact PDF |
| Source-negative controls (`N`) | {len(N):,} | Fixed PDF-grounded counterfactuals, copied unchanged and independently verified |
| Original PDF evidence locations | {len(verified):,} | {match_counts['NORMALIZED_EXACT_TEXT_ON_PHYSICAL_PAGE']:,} normalized text matches and 3 independently inspected Figure 1.1 assertions |
| Unmatched PDF evidence quotations | 0 | Evidence verification enumerated in `01_pdf_quote_verification_final.jsonl` |
| Prior excluded text-block estimate | 274 | Page-level historical estimate, **not** item-by-item semantic certification |
| Atomization challenge records | {len(challenge)} | 16 Appendix E test-overlap candidates; 3 grouped chapter boilerplate / verification / field-context challenges |

Source-positive IDs `PDF-00001`–`PDF-01024` and negative IDs `NEG-00001`–`NEG-00037` remain unchanged. All original English propositions, source quotations, page references, evidence types and fields are preserved byte-for-byte. Both inventories are common inputs to any supported method; neither Markdown-generated requirements nor historical scores determine the PDF denominator.

## Source atomization qualification

This phase preserves the user's requested common `fullload_cal` evidence universe while applying the protocol v6.1 source-access checks. **Matching a quotation does not certify that every retained proposition is independently meaningful.** The 19 recorded challenges include Appendix E acceptance-test overlap, repeated universal contract/verification language and inherited entity/table/DDL context. The 19 records are review groups, **not 19 confirmed incorrect source atoms**, and no unsupported denominator modification was silently applied.

The 274 historical excluded-text units are retained only as an aggregate page-estimate. `09_excluded_units.jsonl` contains current-source page-grouped exclusions plus explicitly grounded illustrative examples. It deliberately does not invent 274 item-level quotations. The original PDF excludes purely illustrative fixture values and example-only configuration from independently adopted implementation requirements. Figure 1.1's three actual cross-cutting runtime assertions remain positive source evidence rather than illustration-only exclusions.

## Phase closure and score interpretation

- This phase completed source inspection, PDF-positive / PDF-negative inventories, direct evidence verification, source identity checks and source-atomization risk recording.
- **No** generated occurrence/class extraction, TP/TN/FP/FN judgment, Precision, Recall, F1, Duplicate metric, or archive was produced.
- Phase 2 begins only on a subsequent user instruction. Source-atomization concerns remain explicitly visible for the designated correction phase; baseline stability does not imply semantic certification.

## Deliverable inventory

- `01_source_atoms_final.jsonl` — 1,024 preserved source-positive items with English PDF evidence.
- `01_source_negative_controls_final.jsonl` — 37 preserved bounded PDF-negative controls.
- `01_pdf_page_coverage_final.jsonl` — verified physical-page coverage and current extraction properties.
- `01_pdf_quote_verification_final.jsonl` — 2,564 verified evidence locators.
- `01_source_atomization_challenge_final.jsonl` — 19 real source-denominator review groups.
- `09_excluded_units.jsonl` — current PDF-only exclusion records and audit limitations.
- `01_source_evidence_verification_final.json` — independently recomputed evidence counts.
- `01_input_manifest_final.json` — exact attached file identity, hashes, roles and Phase 1 boundary.
- `01_phase_status_final.json` — explicit best-effort phase closure.
- `OrionDesk_AI_Detailed_Design_Specification.pdf` — identical canonical source evidence file.
- `verify_phase1.py` — English-only reproducibility script.
'''
(OUT/'01_pdf_coverage_and_source_exclusions.md').write_text(report, encoding='utf-8')

assert all((OUT/f).is_file() for f in ['01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl','01_pdf_page_coverage_final.jsonl','01_pdf_quote_verification_final.jsonl','01_source_atomization_challenge_final.jsonl','09_excluded_units.jsonl','01_source_evidence_verification_final.json','01_input_manifest_final.json','01_phase_status_final.json','01_pdf_coverage_and_source_exclusions.md'])
print(json.dumps({'status':status['status'],'R':len(R),'N':len(N),'evidence':len(verified),'exclusion_group_records':len(exclusions),'image_pages':len(image_pages),'input_files':len(SCORING_INPUTS),'output':str(OUT)},indent=2))
