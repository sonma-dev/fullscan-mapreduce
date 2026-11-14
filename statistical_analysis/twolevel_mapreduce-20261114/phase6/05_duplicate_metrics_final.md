# Raw Semantic Duplication — Phase 6

**Status:** `FINAL_BEST_EFFORT` (raw-class equivalence is a reviewed approximation).

| Measure | Recomputed count |
|---|---:|
| Eligible occurrences (`GO`) | 2400 |
| Unique within-method semantic classes (`G`) | 2289 |
| Excess occurrences | 111 |
| Repeated classes | 75 |
| Repeated classes spanning multiple files | 74 |
| Excess within an earlier-represented file | 1 |
| Excess appearing in other files first | 110 |
| Duplicate rate `(GO-G)/GO` | 4.625% |

For each class, sort occurrences by scored file order, physical line, and table-cell position. The earliest is representative; classify subsequent occurrences against prior members. The within/across partition sums to the complete excess count.

Unmerged similarity is not automatically duplication; different subjects, actor scope, numerical limits, retry policy, and exceptions remain separate. This duplicate metric does not use the TP coverage projection.
