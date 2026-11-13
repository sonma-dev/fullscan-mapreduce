# Phase 2 — Generated Corpus Atomization and Raw Semantic Deduplication

**Protocol:** 6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method label:** `current_scored_8` (exactly one complete uploaded eight-document set; generation method not inferred)  
**Input basis:** The eight actual Markdown files listed below, unmodified.  

## Extracted occurrence and class universe

| Measure | Count |
|---|---:|
| Eligible definitive generated occurrences (G_O) | 4,223 |
| Conservative raw semantic classes (G_C) | 4,075 |
| Duplicate excess occurrences | 148 |
| Provisional raw duplicate fraction | 3.5046% |
| Duplicate excess within file | 12 |
| Duplicate excess across files | 136 |
| Repeated classes | 91 |
| Repeated classes spanning files | 87 |
| Excluded generated fragments/cells | 5,251 |
| Covered physical input lines | 3,123 |
| Reviewed substantive table cells | 4,070 |

The class count is a raw within-method semantic-claim count, not the projected canonical positive prediction count from the later evaluation phases. No source/target entailment judgments or confusion matrix are created here.

## Input line and table-cell coverage

| Actual unmodified input filename | Physical lines | Reviewed table cells | Eligible occurrences | Excluded fragments |
|---|---:|---:|---:|---:|
| `01_screen_functions(7).md` | 504 | 621 | 675 | 589 |
| `02_api(7).md` | 486 | 750 | 625 | 923 |
| `03_data(7).md` | 503 | 699 | 686 | 740 |
| `04_batch_functions(7).md` | 291 | 250 | 522 | 410 |
| `05_business_rules(7).md` | 419 | 496 | 597 | 548 |
| `06_exception_handling(8).md` | 339 | 472 | 520 | 646 |
| `07_processing_flows(8).md` | 377 | 255 | 526 | 509 |
| `08_architecture_decision(7).md` | 204 | 527 | 72 | 886 |

Every physical line is classified in `02_generated_line_and_cell_coverage_final.jsonl`. For each Markdown table data row, each nonblank cell has an explicit eligible/excluded outcome, column position and inherited row/heading context. Physical line references and exact source quotations are retained in the occurrence ledger. Open-question columns, unadopted proposals, bare headings, source citations, example code and illustration-only diagrams are excluded with locator-level reasons.

## Raw class construction and bounded uncertainty

Initial duplicate merges require exactly the same guarded normalized English predicate and the same protected path, code literal, numeric and prohibition signatures. A separate very-high-similarity pass only merges near-identical full predicates whose literal/signature and identifier scopes agree. This is intentionally conservative: it favors separate classes rather than claiming unsupported equivalence. `02_high_similarity_merges_final.jsonl` lists those decisions. Every class refers to actual `GEN-*` occurrences, and each eligible occurrence belongs to one and only one class.

A `Resolved` claim in the architectural decision register may express a definitive constraint, but `TBD`, `Needs confirmation`, `Proposal` and `Unadopted proposal` do not become implementation authority. Where a sentence mixes confirmed requirements and unresolved implementation detail, only independently separable confirmed material is eligible. The exact original line and cells remain available for challenge.

## Invariants and future semantic evaluation

- `sum(class occurrence counts) = |G_O|`.
- `|G_O| - |G_C| = within-file excess + across-file excess`.
- All eight files, every physical line and every nonblank table-data cell have logged classifications.
- The Phase 1 PDF-positive `R` and fixed PDF-negative `N` inventories are not modified.
- Phase 3 is not performed. No generated item is declared PDF-entailed or unsupported in this phase.

**Accuracy limit:** The parser applies explicit classification and high-specificity normalized deduplication, not an independently human-certified semantic equivalence audit. A compound rule may retain multiple predicates for later comparison, and strongly paraphrased duplicates may be undermerged. These are visible `BEST_EFFORT` limitations rather than verified complete semantic duplication estimates. Phase 5 is the designated correction phase.

## Deliverable files

- `02_generated_atoms_final.jsonl`: source-located definitive generated occurrences.
- `02_generated_classes_final.jsonl`: every raw generated semantic class and its membership.
- `04_duplicate_classes_final.jsonl`: occurrence-by-class duplication and exact within/across partition.
- `02_generated_exclusions_final.jsonl`: generated nondefinitive/excluded cells with reasons.
- `09_excluded_units.jsonl`: retained Phase 1 PDF exclusion records plus generated exclusions.
- `02_generated_line_and_cell_coverage_final.jsonl`: full physical line/table-cell inspection ledger.
- `02_canonical_lookup_index_final.json`: literal, endpoint, code, field, identifier and normalized-token lookup index for later bidirectional retrieval.
- `02_high_similarity_merges_final.jsonl`: guarded approximate-merge decisions.
- `02_generated_corpus_coverage_final.json`: input hashes and coverage checks.
- `02_phase_status_final.json`: execution limits, counts, and audit limitations.
- `build_phase2.py`: reproducible extraction and partition script.
