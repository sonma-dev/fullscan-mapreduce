# OrionDesk AI — Phase 1 PDF-Source Inventory Report

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
| Source-positive requirements (`R`) | 1,024 |
| Bounded negative controls (`N`) | 37 |
| Positive PDF evidence quotations | 2,527 |
| Negative PDF evidence quotations | 37 |
| Total source evidence quotations | 2,564 |
| Exact normalized text confirmations | 2,451 |
| Page-token matches requiring layout context | 110 |
| Source figure quotations inspected visually | 3 |
| Unlocated evidence quotations | 0 |
| Pages containing source-positive atom references | 76 |
| Pages without standalone positive atom references | 14 |
| Reused source-ledger byte identity | PASS |
| Reused negative-control byte identity | PASS |

**PDF SHA-256:** `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`  
**Source-positive ledger SHA-256:** `8a6c97eaf52e3cbe544de9515e22a9f806b173ceac4c12c800f3888ad9053dbc`  
**Negative-control ledger SHA-256:** `ba48d66de139609fbf7d5ff3d3783a1e3792d5f5120b81c404e129ef1561a253`

The PDF hash matches the prior recorded original. The 90-page page-by-page extracted-text and rendered-thumbnail inventory is recorded in `01_pdf_page_coverage_final.jsonl`. Source-positive evidence appears on 76 pages; the 14 other pages are pages 1, 2, 3, 4, 5, 6, 14, 33, 43, 47, 60, 67, 77, 81 and include front matter, contents, or reference illustrations rather than separately scored positive atoms in the reused inventory. This is not a claim that those pages contain no text or no information.

## Evidence-verification method

Every listed source quotation was tested against its recorded physical page. A contiguous match was preferred. Where the PDF's columns, floating invariant label, or cells disrupt reading order, complete on-page token coverage is recorded rather than falsely calling it a contiguous exact match. The three raster-only assertions in Figure 1.1 on page 8 were independently inspected in the rendered original page image and matched to the recorded text. `01_pdf_quote_verification_final.jsonl` retains the evidence-level categories and exact source quotations.

The 37 negative controls are derived from **5 explicit exclusions**, **3 release deferrals**, and **29 explicit prohibitions**. They are a bounded diagnostic set, **not all conceivable nonexistent requirements**. The negative controls are not a substitute for source-positive prohibitions.

## Source-atomization integrity and limits

The inventory has no duplicate source IDs and no exact duplicates after normalized source-statement comparison. This does **not** establish the absence of semantic duplicates, boilerplate multiplication, parent-child double counting, or overlapping test-matrix predicates. An explicit audit watchlist of 100 records identifies possible acceptance-test, cross-cutting-interface, and figure overlap areas without altering the inherited shared inventory. These issues are carried to the designated Phase 5 correction/audit, where any real source error must be corrected consistently across all compared methods. The ledger preserves prior normalization notes, including instances of conservative sentence/clause segmentation.

Illustrative source examples, screenshot mock values, placeholder identifiers and unadopted Appendix F settings must not independently become scored normative obligations or adopted production values. `09_excluded_units.jsonl` records 17 selected located exclusions. This exclusions list is diagnostic, not a claim to have enumerated every nonnormative sentence.

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
