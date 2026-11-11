# Coverage, Source Provenance, and Reliability Limitations

## Scope and provenance

- The authoritative PDF is the supplied 90-page English OrionDesk AI detailed design, release R1.0/revision 1.3; SHA-256: `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`. The current upload and the `fullload_cal` PDF have equal digests. No historical scores or generated Markdown were used to invent authoritative requirements.
- Exactly 8 scored Markdown documents were included: `01_screen_functions(1).md`, `02_api(1).md`, `03_data(1).md`, `04_batch_functions(1).md`, `05_business_rules(1).md`, `06_exception_handling(2).md`, `07_processing_flows(2).md`, `08_architecture_decision(1).md`. They contain 3,123 physically inspected lines and 4,744 table cells in the retained inspection coverage ledger. Generated textual claims preserve their source file and line/table locator.
- PDF page coverage includes all 90 pages. 1,006 source-positive quotes match normalized PDF text; the 3 remaining quotes are figure assertions visually inspected on physical PDF page 8. The records for this figure are included in `06_pdf_visual_figure_evidence.jsonl`. 0 PDF-positive quotes remain without the corresponding PDF locator; 0 negative-control quotation mismatches.
- The common source `R` contains 1,009 independently normalized positive items, after the existing correction history. The fixed negative-control `N` contains 37 controls. This report does not treat the 90-page document's example-only values as adopted implementation defaults.

## Bidirectional FN retrieval and source atomization

- The final ledger contains 12 provisional FN: 0 `TRUE_MISSING`, 5 `PARTIAL_ENTAILMENT`, 7 `CONSERVATIVE_UNRESOLVED`. These are **not all verified omissions**.
- The full historical candidate-FN review has 319 records, with outcomes: `CONSERVATIVE_UNRESOLVED` 7, `MATCHER_FALSE_NEGATIVE_CORRECTED` 299, `PARTIAL_ENTAILMENT` 5, `SOURCE_ATOMIZATION_ERROR_CORRECTED` 8. The corrected and removed source-atom IDs are preserved in `07_change_delta.jsonl`.
- Source atomization was reviewed in 1016 retained audit rows. The correction history excludes nonnormative examples and redundant source atoms across methods, but the remainder has not been independently re-atomized in this phase.
- The reciprocal probe file `06_reciprocal_regression_probes.jsonl` documents exact/meaning-preserving searches including the `title` case field, workspace `retention class`, and same-key duplicate case creation with identical response, plus 12 current FN cases with their source and nearest generated evidence. The probes are diagnostic retrieval checks, **not automatic TP labels**. No identified exact/full-predicate direct match was silently converted to TP in this recomputation phase.

## TP predicates and generated claim validity

- All 997 final TPs have a source-to-generated proof audit row and actual PDF and generated-file evidence. The E2 bridge count is 587; E3 source coverage count is 410. Physical citation existence, identifier validity and generated quote/line consistency were checked independently.
- **Semantic proof has not been independently certified:** 997 of 997 final TP audit rows and 2944 of 2944 generated class validity rows contain best-effort evidence and commentary rather than independent, complete entailment adjudication.
- 1636 `SUPPORTED_NONCOVERING` generated classes were nonetheless referenced by 926 TP evidence records. A `SUPPORTED_NONCOVERING` class may legitimately supply one part of a conjunctive bridge even when it does not independently cover a complete R atom. Nevertheless, these links do not certify the full conjunction, so independent scope and predicate review is still required; the counts are disclosed rather than automatically relabeled.
- The generated-validity ledger records 775 `PDF_ENTAILED`, 2169 `SUPPORTED_NONCOVERING`, and 0 `PDF_UNSUPPORTED` classes. The latter count is an *observed ledger classification*, not an independently verified absence of unsupported generated commitments. Positive PDF quotation and complete generated predicates have not been checked by an independent semantic adjudicator for each contextual class.
- The reported FP = 0 is the result of the existing itemized ledger, not certified precision. Its provisional value can change after stronger claim-validity review. Likewise, TP and FN can move in either direction; this is not a statistical confidence interval and no lower-bound claim is made.

## Bounded TN, duplicates, and metric universe

- TN counts only PDF-based, predeclared prohibited capabilities/deferrals; it is not a population-wide true-negative total. `R`, `N`, and unsupported `F` must remain disjoint. All four cells are itemized in `04_atomic_judgments_final.jsonl`.
- Duplicate uses raw generated occurrences (3,068) and within-method classes (2,944), not the effective source-atom coverage projection (997 TPs). Its excess count is 124, split into 5 within-file and 119 across-file.
- Raw semantic-class merging is intentionally conservative. Further semantic duplicate merges or splits may change Duplicate but should not be used to manufacture new source-positive requirement IDs.

## Certification and completion

- Item-level completeness, arithmetic, input hashing, physical PDF/Markdown citation existence, and duplicate partitions were recomputed independently by `compute_metrics.py`. The structural verdict is **PASS**; 0 structural failures, 4 semantic/reporting warnings.
- Status is `FINAL_BEST_EFFORT`. The result is a **reproducible final best-effort ledger calculation**, not a semantically certified effectiveness assessment. A stronger claim would require independent full-predicate review of all TP evidence bridges and all generated class validity judgments. This limitation is intrinsic to the existing artifacts, not a reason to silently substitute historical scores.
