# Phase 2 — Generated Corpus Extraction and Raw Semantic Classes

**Status:** `PHASE_COMPLETED_BEST_EFFORT`

**Protocol:** 6.1

**Method:** supplied unprefixed eight-file set (method label not inferred)

## Counts

| Measure | Value |
|---|---:|
| Scored Markdown inputs | 8 |
| Physical lines inspected | 7,698 |
| Physical table cells inspected | 16,577 |
| Eligible generated assertion occurrences | 5,226 |
| Unique raw semantic classes | 5,195 |
| Excess duplicate occurrences | 31 |
| Repeated semantic classes | 27 |
| Classes repeated across input files | 27 |
| Within-file excess | 0 |
| Across-file excess | 31 |
| Excluded/undecided evidence records | 2,738 |
| Provisional raw duplicate fraction | 0.59319% |

## Input identity and physical coverage

| Exact scored filename | Lines | Eligible occurrence count | Bytes |
|---|---:|---:|---:|
| `01_screen_functions.md` | 709 | 632 | 133,085 |
| `02_api.md` | 1286 | 1079 | 161,787 |
| `03_data.md` | 1051 | 749 | 164,101 |
| `04_batch_functions.md` | 1133 | 749 | 133,823 |
| `05_business_rules.md` | 1107 | 607 | 111,135 |
| `06_exception_handling(2).md` | 767 | 600 | 115,158 |
| `07_processing_flows(1).md` | 1090 | 767 | 141,413 |
| `08_architecture_decision(1).md` | 555 | 43 | 106,482 |

## Eligibility and reconstruction policy

A physical-line audit covers every input line; for Markdown tables, a per-cell disposition records the real column heading and full row context. Eligible cell assertions include the row key, inherited section scope, header and original unchanged quotation. Condition/result tables carry triggering context into the reconstructed assertion. Unadopted proposals, open decisions, bare references and illustrative code were not counted as definitive new commitments. Distinct source identifiers, API paths, scope, numeric restrictions, and statuses were deliberately not discarded in normalization. A few separate testable predicates may remain bundled in broad cells; this is best-effort extraction, not a complete manual semantic certification.

For a class with multiple occurrences, excess occurrences were partitioned in input-file/line order into within-file repeats (a prior occurrence in the same file) and across-file repeats (first occurrence in that file following an earlier occurrence elsewhere). These counts refer to raw generated occurrences/classes, not expanded source coverage.

## Deliverable integrity

- `02_generated_atoms_final.jsonl`
- `02_generated_classes_final.jsonl`
- `04_duplicate_classes_final.jsonl`
- `02_generated_exclusions_final.jsonl`
- `02_markdown_line_cell_coverage_final.jsonl`
- `02_generated_lookup_index_final.jsonl`
- `02_phase2_status_final.json`

## Limitations and next phase

- This is a rule-based, original-text and full-predicate-normalized extraction; ambiguous table cells, embedded clauses, and semantically paraphrased repetition may require human reclassification in Phase 5.
- The class partition is conservative: exact fully normalized claims merge; a very high threshold permits limited near-verbatim merges while protecting distinctive identifiers, scopes and numeric constraints.
- A table cell may bundle more than one testable predicate when it contains multiple conditions or outcomes. Such cases may be split after detailed semantic audit.
- No source coverage TP/FN judgments, generated correctness FP/TN judgments, or final Precision/Recall/F1 values are made during Phase 2.
- Unapproved architectural alternatives and unresolved open-question text are excluded as definitive predictions.

Phase 3 will evaluate PDF-positive proposition coverage (TP/FN), challenge provisional FN matches bidirectionally, and record supported bridges. This Phase 2 does not score coverage and does not modify the source-positive or negative inventories supplied in Phase 1.

## Structural audit and semantic limitations

- Structural audit: **PASS**. Exact Markdown evidence cell and physical-line ranges, class membership, individual file hashes, and duplicate arithmetic were checked.
- The overall generated source ledger and negative controls remain unchanged from Phase 1 (R=1024, N=37).
- The provisional duplicate rate **0.5932%** is sensitive to conservative under-merging of meaning-preserving paraphrases and must not be treated as certified semantic duplication.
- Main remaining audit risks: inherited table-cell context, overly broad or bundled statements, and paraphrases not captured by near-verbatim grouping. These uncertainties affect raw-class counts and will be reviewed during the Phase 5 correction stage.
- The architecture decision register was scored only for explicitly resolved, definitive statements. Unapproved alternatives, TBD items, and Needs confirmation entries were excluded.

**Additional evidence:** `02_qa_validation_final.json` and cumulative `09_excluded_units.jsonl`.
