# Phase 2 — Generated Corpus Extraction, Eligibility, and Semantic-Class Deduplication

**Status:** `PHASE_COMPLETED_BEST_EFFORT`

This phase evaluates only the eight currently supplied Markdown documents. It preserves the PDF source-positive and negative-control inventories established in Phase 1. None of the historical `fullload_cal` generated judgments or scores are inputs.

## Input line and table-cell coverage

| Actual filename | Physical lines inspected | Table cells scanned | Eligible generated occurrences | Excluded fragments |
|---|---:|---:|---:|---:|
| `01_screen_functions(1).md` | 504 | 729 | 513 | 579 |
| `02_api(1).md` | 486 | 884 | 462 | 823 |
| `03_data(1).md` | 503 | 805 | 577 | 648 |
| `04_batch_functions(1).md` | 291 | 290 | 474 | 300 |
| `05_business_rules(1).md` | 419 | 588 | 400 | 472 |
| `06_exception_handling(2).md` | 339 | 530 | 331 | 500 |
| `07_processing_flows(2).md` | 377 | 301 | 455 | 374 |
| `08_architecture_decision(1).md` | 204 | 617 | 53 | 501 |

## Counted raw classes and semantic duplication

- Definitive generated occurrence count (GO): **3,265**.
- Unique within-method semantic classes (G): **3,168**.
- Excess duplicate occurrences (GO − G): **97**.
- Provisional raw duplicate ratio: **0.029709** (2.97%).
- Within-file excess: **2**; across-file excess: **95**.
- Repeated semantic classes: **64**.
- Repeated classes spanning more than one source file: **63**.

## Extraction decisions

1. Each line and each Markdown table cell was read and classified; row keys and headings were retained for scoped interpretation.
2. Unresolved, tentative, proposed, example-only, navigation-only, citation-only, and open-question content was excluded. Separately definitive statements in mixed sections were retained where the available segments allowed safe separation.
3. Exact methods, endpoints, selected database fields and independently stated constraints were retained with location and row/column context.
4. Raw classes were merged only on normalized exact propositions or conservatively high-threshold near-equivalence with critical identifiers and numbers protected. More distant paraphrases remain separate pending Phase 5 semantic correction.
5. Figures and Mermaid diagrams were inspected as processing-context summaries but did not independently add executable edges beyond clear prose claims.

## Limitations and next phase

The English authored ledgers preserve actual unchanged input filenames, physical lines, and table-cell locators. Their assertion segmentation is best effort rather than a certified full manual semantic audit. Long cells may contain multiple conditions or implied exception scopes; close paraphrases can remain separate raw classes. These risks are carried forward for source coverage evaluation and the designated correction phase.
The provisional duplicate values above are raw-class diagnostics, not Precision, Recall, F1, TP, TN, FP or FN. No confusion-matrix values have been created in Phase 2.

## Output paths

- `02_generated_atoms_final.jsonl` — eligible occurrences and evidence coordinates.
- `02_generated_classes_final.jsonl` — all raw classes with membership.
- `04_duplicate_classes_final.jsonl` — repeated class details and within/across-file partition.
- `02_generated_exclusions_final.jsonl` — excluded line/cell fragments and reasons.
- `02_line_cell_coverage_final.jsonl` — physical-line and table-cell accounting.
- `02_phase_status_final.json` — structure and caveats.

Phase 2 is closed. Phase 3 has not started.
