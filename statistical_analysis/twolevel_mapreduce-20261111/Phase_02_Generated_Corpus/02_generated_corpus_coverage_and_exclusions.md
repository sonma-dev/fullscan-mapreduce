# Phase 2 — Full Generated Corpus and Raw Semantic-Class Inventory

**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method label:** `current_user_supplied_eight_document_set`  
**Protocol:** Version 6.1  
**Boundary:** Exactly Phase 2 is closed. Phase 3 has not begun.

## Input universe and unchanged source inventory

The source evidence universe reused from `fullload_cal` consists of **1,024 PDF-positive atoms** and **37 PDF-negative controls**. Both Phase 1 files remain **unchanged**. All eight required current Markdown files were read as UTF-8 and checked against the prior input manifest. No Markdown scored input was modified.

## Extracted generated occurrences and deduplicated raw claims

| Counting field | Preliminary Phase 2 count |
|---|---:|
| Eligible generated occurrence records, `|GO_m|` | **3,792** |
| Unique raw semantic classes, `|G_m|` | **3,657** |
| Excess repetitions, `|GO_m|-|G_m|` | **135** |
| Repeated classes | **108** |
| Repeated classes spanning files | **108** |
| Within-file excess repetitions | **0** |
| Across-file excess repetitions | **135** |
| Recorded potential near-duplicate pairs not automatically merged | **231** |
| Nondefinitive/generated-excluded fragments | **2,734** |

**Important:** The class/excess counts are a provisional Phase 2 inventory, **not** a final Duplicate score and not a TP/TN/FP/FN confusion matrix. Raw class and effective canonical source coverage are distinct levels. Phase 5 will audit the merges and calculate the final Duplicate rate.

## File- and cell-level inspection coverage

| Scored input (actual file) | Physical lines | Nonblank lines inspected | Table data rows | Eligible occurrences | Excluded fragments |
|---|---:|---:|---:|---:|---:|
| `01_screen_functions(3).md` | 437 | 325 | 172 | 524 | 308 |
| `02_api(3).md` | 482 | 366 | 168 | 676 | 421 |
| `03_data(3).md` | 411 | 308 | 149 | 645 | 234 |
| `04_batch_functions(3).md` | 274 | 204 | 86 | 462 | 312 |
| `05_business_rules(3).md` | 391 | 301 | 154 | 443 | 290 |
| `06_exception_handling(4).md` | 346 | 260 | 105 | 432 | 243 |
| `07_processing_flows(4).md` | 369 | 280 | 106 | 486 | 317 |
| `08_architecture_decision(3).md` | 216 | 175 | 100 | 124 | 609 |

Each eligible record carries an exact original filename, physical line, original English excerpt, heading/section context, and the Markdown table's row/column/heading when applicable. Each distinct occurrence belongs to **exactly one** raw class. Table row keys are inherited as context rather than counted as standalone assertions. Registered API method/path, declared fields, actor/permission scopes, exact statuses, and independent behavior clauses are considered separately whenever the cell text makes them independently testable.

Table headings, separator rows, citations, reference-to-earlier-file columns, open-question fields, explicitly unselected architecture options, illustrative JSON/YAML/HTTP values, and mermaid-only diagram text are excluded or treated as context. Explicit confirmed restrictions embedded in otherwise unresolved paragraphs can remain eligible. The complete generated-exclusion ledger gives actual line/cell locators.

## Conservative semantic-class resolution

Two eligible claims merge automatically only if their **target, action, actor, scope, condition, exception, version and outcome** are not distinguishable by the available canonical text. Exact canonical matches are merged, while only exceptionally strong near-verbatim paraphrases with matching hard API/literal/field anchors, numeric values and polarity are additionally merged. Similar-looking obligations tied to distinct endpoints or resources remain separate. Potentially equivalent, nonmerged pairs are listed in `02_semantic_duplicate_review_candidates.jsonl` as **review candidates**, not accepted duplicates.

A single class may later support more than one independently extracted PDF source proposition through the semantic bridge process. That does **not** add `GEN-*` occurrences, change `GCLASS-*` counts, or create duplication by itself.

## Structural checks

- All eight scored input files are present and each physical nonblank line has a recorded parsed disposition.
- Every eligible occurrence has exactly one `GEN-*` ID and exactly one `GCLASS-*` assignment.
- Summed class member counts equal the eligible occurrence count.
- Within-file excess plus across-file excess equals all excess class occurrences.
- The source atom ledger and negative-control ledger remain byte-identical to Phase 1.
- No phase 3 entailment judgments, source-to-generated matches, Precision, Recall, F1 or final Duplicate metrics were produced.

## Accuracy limitations

This is a **best-effort generated-claim extraction and conservative class clustering**, not a semantic certification. A short table cell may require the neighboring row or global guards for a fully entailed behavior; this context is recorded for later use, not silently assumed. A high lexical resemblance cannot establish semantic identity; uncertainty is preserved in the candidate audit, which the protocol's correction phase will address. Excluded rows with tentative wording are *not* implementation commitments.

## Individual Phase 2 deliverables

- `02_generated_atoms_final.jsonl` — eligible definitive generated-claim occurrences.
- `02_generated_classes_final.jsonl` — one raw semantic class per normalized unique proposition.
- `04_duplicate_classes_final.jsonl` — class memberships, representative locators, and within/across-file excess partition.
- `02_generated_exclusions_final.jsonl` — nondefinitive generated fragments with exact source locations.
- `02_line_cell_coverage_final.jsonl` — exhaustive eight-file physical-line inspection accounting.
- `02_reciprocal_lookup_keys_final.jsonl` — target, endpoint, identifier, state and token indexes for later reciprocal retrieval.
- `02_semantic_duplicate_review_candidates.jsonl` — conservative semantic-equivalence challenge cases.
- `09_excluded_units.jsonl` — Phase 1 PDF-only exclusion rows plus Phase 2 generated exclusions.
- `02_phase_status_final.json` — machine-readable status, count reconciliation and limitations.

**Completion:** Phase 2 finished with best-effort semantic clustering and auditable file/cell coverage. The source denominator and the next-phase boundary are unchanged.
