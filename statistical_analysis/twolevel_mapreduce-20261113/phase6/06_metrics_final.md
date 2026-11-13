# Phase 6 Final Metrics — OrionDesk AI

**Protocol:** v6.1  
**Method:** `supplied_set_1` (one complete supplied eight-document set; no distinct generation method is asserted)  
**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Scoring status:** `FINAL_BEST_EFFORT`, **NOT** `FINAL_VERIFIED`.

## One canonical proposition universe

| Source-positive `R` | Bounded source-negative `N` | Generated-only unsupported `F` | Canonical universe `U` |
|---:|---:|---:|---:|
| 1,008 | 37 | 0 | 1,045 |

| Cell | Count |
|---|---:|
| TP | 963 |
| TN | 37 |
| FP | 0 |
| FN | 45 |

| Metric | Result | Definition |
|---|---:|---|
| Precision | 100.00% | `TP / (TP + FP)` |
| Recall | 95.54% | `TP / (TP + FN)` |
| F1 | 97.72% | `2 TP / (2 TP + FP + FN)` |
| Semantic duplication | 7.99% | `(GO - GC) / GO` |

`TP + FN = 1008`; `TN + B = 37`; `FP = F + B = 0 + 0`.  
`U = R + N + F = 1008 + 37 + 0 = 1045`.  
`P = TP + FP = 963`; this **need not equal** raw generated class count `2349`.

## Raw generation and duplication

| Measure | Value |
|---|---:|
| Eligible generated occurrences `GO` | 2,553 |
| Unique raw semantic classes `GC` | 2,349 |
| Duplicate excess occurrences | 204 |
| Within-file excess | 1 |
| Across-file excess | 203 |
| Repeated classes | 144 |
| Repeated classes spanning files | 143 |

## Independent reconciliation

- Recomputed all four cells directly from 1045 canonical item-level judgments; **not** from a stored score table.
- Recomputed 204 duplicate occurrences from the 2553 occurrence membership records and class partitions.
- Verified source IDs, negative-control IDs, occurrence/class membership and evidence-ledger referential integrity.
- Reconciled the historical Phase 4 `03_canonical_universe_final.jsonl` (1125 rows per the Phase 4 status) against the 1045 Phase 5 judgment rows. Its final representation now contains 1045 rows. This did **not** modify the cell labels or scores.
- Checked all 90 PDF page coverage records, 2,926 Markdown physical-line coverage records and 3,769 table-cell records.
- Source quote text recheck: 1005/1008 normalized contiguous matches and 3 independently inspected figure-rendered text matches, leaving 0 unverified source quotes. Original Phase 1 records confirm 2,564/2,564 PDF evidence quotes using its own verification method.

## Interpretation

The precision of 100.00% is an **adjudicated provisional arithmetic result**, not proof of zero unsupported generated commitments. The class validity ledger still has 1,269 E1 (partial-evidence) classes, including 36 that were labeled `PDF_ENTAILED`. An E1 grade is not a complete proof. Retained FNs include 13 `TRUE_MISSING`, 20 `PARTIAL_ENTAILMENT`, and 12 `CONSERVATIVE_UNRESOLVED`. Human-level semantic certification was not completed. The 37 TNs represent only explicitly predefined PDF-negative counterfactuals.

No archive was produced; individual files are the required deliverables.
