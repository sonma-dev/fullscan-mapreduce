# Phase 2 — Generated Corpus Coverage, Exclusions, and Raw Semantic Classes

**Status:** `PHASE_COMPLETED_BEST_EFFORT`

**Scope:** One unambiguously role-mapped eight-file supplied Markdown corpus. Its generation method was not explicitly identified; the neutral method label `unlabeled_single_supplied_corpus` avoids attributing it to full-load, one-level, or two-level.

## Source files and full physical line/cell coverage

| Scored input (unchanged filename) | Physical lines inspected | Table cells inventoried | Eligible definitive occurrences | Excluded units |
|---|---:|---:|---:|---:|
| `01_screen_functions.md` | 495 | 858 | 471 | 438 |
| `02_api.md` | 696 | 1360 | 692 | 649 |
| `03_data.md` | 474 | 882 | 553 | 340 |
| `04_batch_functions.md` | 588 | 503 | 438 | 305 |
| `05_business_rules.md` | 481 | 838 | 380 | 432 |
| `06_exception_handling(1).md` | 432 | 651 | 388 | 400 |
| `07_processing_flows(1).md` | 565 | 525 | 411 | 559 |
| `08_architecture_decision.md` | 225 | 691 | 16 | 624 |

**Totals:** 3,956 physical lines; 6,308 table cells; 3,349 eligible generated occurrences; 3,260 full-predicate semantic classes.

## Eligibility and exclusion policy

All files were read as UTF-8, line by line; each Markdown table was traversed by row and physical cell, retaining the section hierarchy, header, row key, and unchanged real filename. The line/cell coverage ledger lists the disposition for every physical line and every table cell, including metadata, unresolved decisions and code examples.

A definitive design commitment is included if it imposes a concrete operation, authorization, interface, field, state, status, data constraint, output, limit, testable guard, or required processing outcome. Both prohibitions and positive obligations are eligible. Each occurrence keeps its original quotation and section/row/column context. Compound fragments are split only at safe statement or semicolon boundaries; shared predicates and inherited conditions are preserved rather than flattened.

The architecture decision register is scored, but the 76 unresolved AD items are not treated as human-approved commitments; the 12 narrow RES items are considered individually. Unsupported proposed browser exchange examples, illustrative SSE frames, diagrams repeating prose, reference-only citations, unresolved status values and pure test-trigger fixtures are excluded. Definitive clauses remain eligible even beside an unresolved detail when separable.

## Raw within-method duplication (provisional Phase 2 ledger)

- Eligible occurrences: **3,349**.
- Unique semantic classes: **3,260**.
- Excess occurrences: **89** (within-file **7**; across-file **82**).
- Repeated classes: **68**; classes spanning files: **64**.
- **Important:** This raw class inventory is not the source-positive coverage set or the canonical predicted-positive decision count; a universal generated claim can later justify multiple distinct PDF atoms without adding raw generated occurrences.

## Evidence and structural checks

- Every eligible occurrence belongs to exactly one method-specific raw semantic class; class occurrence memberships reconcile.
- Every occurrence has an unchanged input filename, physical line, source quotation, inherited scope and a table-cell locator where applicable.
- A line/cell disposition is available for all original Markdown lines and table cells, including explicit exclusions and structural-only cells.
- Semantic grouping uses text normalization, high-similarity candidate discovery, and guarded full-predicate target/actor/numeric/endpoint equivalence rather than generic word overlap alone.
- Raw excess = eligible occurrences − semantic classes = within-file excess + across-file excess.
- Phase 1 PDF exclusions remain intact in the shared `09_excluded_units.jsonl`; the Phase 2 generated exclusions were appended.

## Limits and correction boundary

This phase is structurally reconciled but **not semantically certified exhaustively**. Automatic segmentation of long table cells and conservative near-equivalence clustering can both miss nuances. Full manual predicate equivalence for every candidate was not independently verified; any remaining false splits or merges belong to the designated Phase 5 correction step, not a repeated Phase 2.

Only generated-corpus occurrence/class extraction and raw duplication were performed. **No PDF entailment grade, TP/FN source coverage judgment, generated claim validity, canonical FP/TN decision universe, Precision, Recall, or F1 is asserted.**

## Produced artifacts

`02_generated_atoms_final.jsonl`, `02_generated_classes_final.jsonl`, `04_duplicate_classes_final.jsonl`, `02_generated_exclusions_final.jsonl`, `02_generated_line_cell_coverage_final.jsonl`, `09_excluded_units.jsonl`, and `02_phase_status_final.json`.
