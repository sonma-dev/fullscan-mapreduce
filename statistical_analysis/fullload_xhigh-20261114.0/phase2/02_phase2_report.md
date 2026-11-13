# Phase 2 — Generated Definitive Claims and Raw Deduplication

**Protocol:** 6.1  
**Phase status:** PHASE_COMPLETED_BEST_EFFORT  
**Evaluated method identifier:** `fullload` (single supplied eight-document corpus; generation provenance is not independently verified).

## Input coverage

| Scored input (unchanged filename) | Physical lines | Table cells | Eligible table cells | Eligible occurrences |
|---|---:|---:|---:|---:|
| `01_screen_functions(3).md` | 864 | 2,372 | 678 | 938 |
| `02_api(3).md` | 1,201 | 2,702 | 755 | 1,028 |
| `03_data(3).md` | 1,034 | 2,586 | 726 | 1,036 |
| `04_batch_functions(4).md` | 1,323 | 1,509 | 460 | 888 |
| `05_business_rules(3).md` | 1,442 | 1,549 | 539 | 941 |
| `06_exception_handling(4).md` | 737 | 1,451 | 569 | 823 |
| `07_processing_flows(5).md` | 1,143 | 1,202 | 390 | 900 |
| `08_architecture_decision(3).md` | 586 | 1,511 | 15 | 27 |

## Extracted generated commitments

- Eligible generated occurrences: **6,581**.
- Raw distinct generated classes (conservative exact-full-predicate model): **6,527**.
- Provisional duplicate-excess occurrences: **54**.
- Provisional duplicate rate: **0.82%**.
- Provisional within-file / across-file excess: **2 / 52**.
- Classes appearing in multiple source files: **48**.
- Flagged near-semantic duplicate pairs (not silently merged): **80**.
- Recorded excluded elements: **11,457**.

## Evidence reconstruction and eligibility

Every physical line is represented in the line coverage ledger and every table cell in the cell coverage ledger. Original filenames, exact physical lines, row identifiers, column headers, heading context, and source quotations are retained on eligible occurrence records. This makes the original row/table meaning available for Phase 3 reciprocal entailment review.

Explicitly unresolved questions, unapproved proposals, bare reference/citation cells, standalone identifiers, and illustrative examples are excluded unless a separable definitive obligation is present. The same source-derived constraint can appear in several files; no separate scored occurrence is invented for a citation-only repetition.

## Quality limitations

This is a complete *mechanical evidence-inventory pass* over the supplied physical lines and table cells, followed by a deliberately conservative approximate semantic extraction. It is **not** an independently certified semantic audit. Compound table rows may contain residual under-split propositions; definitive commitments in short field/status cells may require context-specific manual review. These limitations are documented, not converted into missing-file blockers.

The provisional raw duplication count is especially conservative: only normalized exact full-predicate matches with compatible target context are merged. High-similarity candidate paraphrases are recorded separately and must not be treated as verified duplicate classes until their actor, target, modality, conditions, exception and outcome are checked. Provisional duplicate-rate values must not be represented as final Phase 5 metrics.

## Files

- `02_generated_atoms_final.jsonl` — every eligible generated occurrence, with English proposition, evidence and retrieval keys.
- `02_generated_classes_final.jsonl` — raw class representatives and occurrence membership.
- `04_duplicate_classes_final.jsonl` — raw duplication partitions and merge rationale.
- `02_generated_exclusions_final.jsonl` — nondefinitive, proposal, citation and contextual exclusions.
- `02_generated_line_coverage_final.jsonl` — one record per source physical line.
- `02_generated_table_cell_coverage_final.jsonl` — one record per encountered Markdown table cell.
- `02_generated_lookup_keys_final.jsonl` — exact identifier, event, endpoint, literal and word retrieval index.
- `02_possible_semantic_merge_review.jsonl` — high-similarity class pairs retained as unmerged audit candidates.
- `02_phase_status_final.json` — counts and limitations.
- `02_extract_generated.py` — reproducible local extraction code.

No source coverage (Phase 3), generated-vs-PDF validity (Phase 4), final deduplication (Phase 5), or four-cell metrics (Phases 4–6) were executed.
