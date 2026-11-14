# Phase 5 Corrected Confusion Matrix (Provisional)

**Status:** `PHASE_COMPLETED_BEST_EFFORT` - OrionDesk protocol 6.1 - Phase 5 only

| Actual / Predicted | Positive | Negative |
|---|---:|---:|
| PDF source-positive | TP 646 | FN 378 |
| Bounded PDF-negative and generated-only | FP 451 | TN 37 |

- R = 1024; N = 37; F = 451; U = 1512; asserted N = 0.
- Precision = 58.887876%; Recall = 63.085938%; F1 = 60.914663%.
- Raw eligible occurrences = 3744; raw semantic classes = 3654.
- TP + FN = R; TN = N; FP = F; all four cells sum to U.
- TP + FP is an **effective canonical proposition count**; it is **not** the raw generated-class count.
- The 37 TN items belong only to predeclared source-grounded negative counterfactuals, not the universe of every absent feature.

These metrics are **provisional**: arithmetic is validated, but conservative FN/FP labels and independent predicate-coverage proofs are not a fully certified semantic evaluation. Source-atomization and excluded-class changes are enumerated in the delta and audit ledgers.
