# Phase 2 — Generated Corpus Inventory and Semantic Classes

**Status:** `PHASE_COMPLETED_BEST_EFFORT`
**Protocol:** 6.1
**Evaluated corpus:** One attached eight-file set (`supplied_set_01`).

## Coverage and raw occurrence extraction

| Role | Actual input filename | Lines | Table cells | Eligible occurrences | Excluded spans |
|---|---|---:|---:|---:|---:|
| screen_functions | `01_screen_functions(9).md` | 495 | 858 | 277 | 737 |
| api | `02_api(2).md` | 696 | 1,360 | 561 | 1,024 |
| data | `03_data(10).md` | 474 | 882 | 342 | 694 |
| batch_functions | `04_batch_functions(20261115-060045).md` | 588 | 503 | 356 | 474 |
| business_rules | `05_business_rules(10).md` | 481 | 838 | 225 | 766 |
| exception_handling | `06_exception_handling(20261115-060054).md` | 432 | 651 | 289 | 571 |
| processing_flows | `07_processing_flows(20261115-060053).md` | 565 | 525 | 286 | 632 |
| architecture_decision | `08_architecture_decision(20261115-060055).md` | 225 | 691 | 20 | 680 |

**Totals:** 3,956 physical lines, 6,308 table-cell positions, 2,356 definitive eligible occurrences, and 5,578 excluded spans.

## Deduplication (conservative, provisional)

- Raw generated classes: **2,262**.
- Excess occurrence count: **94**.
- Repeated classes: **63**; classes spanning multiple files: **59**.
- Within-file excess: **13**; across-file excess: **81**.
- Provisional duplicate ratio: **3.99%**; this uses eligible occurrences and contextual raw classes, never canonical source-coverage projections.
- Non-merged near-equivalence pairs awaiting future review: **47**.

## Eligibility policy and limitations

Complete, definitive generated commitments are retained even when neighboring fields need confirmation. Bare references, status labels, source citations, unapproved proposals, TBD/open questions, code examples, headings, and repeated diagram pointers are excluded. Tables are scoped by headers, row keys, physical lines, and original file names. Separately meaningful obligations are split when the sentence or table cell warrants it; bare field fragments are not treated as self-sufficient without their row context.

Automatic class merging requires full contextual normalized-proposition equality. A separate full-predicate review of the high-similarity class pairs accepted a conservative subset of equivalent paraphrases, with all accepted/rejected pairs and original evidence documented in `02_semantic_merge_review.jsonl`. Other apparently similar phrases remain separate. Candidate retrieval is not exhaustive of semantic paraphrases. This avoids counting a merely similar authorization rule, status, or endpoint as a verified duplicate. This conservative choice can understate the true semantic duplicate fraction.

All eight files were inspected in their supplied order. The line-and-cell coverage ledger records each physical line; table cells are enumerated even when their content is excluded. Every nonblank line has a disposition.

Extraction is heuristic rather than a manual, predicate-by-predicate validation of every candidate. The count and duplication fraction are provisional; they must not be described as fully semantically verified. Class-to-PDF correctness, source-atom entailment, and TP/TN/FP/FN are intentionally deferred to the designated phases.

The input set is unambiguously mapped to eight roles but its generation method was not named. The neutral method key `supplied_set_01` is used, without inventing `fullload`, `onelevel`, or `twolevel` provenance.

## Phase 2 deliverables

- `02_generated_atoms_final.jsonl`: every retained generated occurrence with exact input file, physical line, and table-cell context.
- `02_generated_classes_final.jsonl`: one raw contextual class for each conservatively equivalent group and its full occurrence membership.
- `04_duplicate_classes_final.jsonl`: repeated classes and within-file / across-file assignment.
- `02_generated_exclusions_final.jsonl`: every excluded generated text span and rationale.
- `02_generated_line_and_cell_coverage.jsonl`: disposition of every actual input line.
- `02_potential_semantic_merges_for_review.jsonl`: initial high-similarity pairs, with accepted and rejected current-class mappings.
- `02_semantic_merge_review.jsonl`: adjudicated pair decisions with side-by-side file/line/cell evidence.
- `02_generated_reciprocal_lookup_index.jsonl`: exact IDs, API paths, enum/field names and their complete occurrence/class lists for the required reverse FN challenge.
- `09_excluded_units.jsonl`: cumulative PDF/Markdown exclusions.
- `02_phase2_status.json`: method, inputs, structural reconciliations, and limitations.

## Next authorized step

Phase 3 alone: PDF-positive source entailment against eligible generated classes, reciprocal FN challenge, and TP predicate proofs. No Phase 3 judgments are made here.
