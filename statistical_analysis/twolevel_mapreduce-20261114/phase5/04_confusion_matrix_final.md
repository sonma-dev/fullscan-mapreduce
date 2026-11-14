# Phase 5 — Revised Four-Cell Confusion Matrix

**Protocol:** v6.1  
**Status:** PHASE_COMPLETED_BEST_EFFORT; semantic coverage not independently certified.

| Actual / Predicted | Predicted 1 | Predicted 0 |
|---|---:|---:|
| PDF source-positive requirements (R) | TP **990** | FN **23** |
| PDF negatives plus unsupported generated residuals | FP **0** | TN **37** |

| Metric | Recomputed value |
|---|---:|
| Precision (effective canonical universe) | 100.0000% |
| Recall (effective canonical universe) | 97.7295% |
| F1 | 98.8517% |
| Raw semantic duplication rate | 4.6250% |
| R / fixed bounded N / unsupported-only F | 1,013 / 37 / 0 |
| Canonical U | 1,050 |
| Raw G / occurrences GO | 2,289 / 2,400 |

## Equations

- TP + FN = 990 + 23 = 1013 = |R|.
- TN + asserted N = 37 + 0 = 37 = |N|.
- FP = unsupported F + asserted N = 0 + 0 = 0.
- U = R + N + F = 1013 + 37 + 0 = 1050.
- TP + TN + FP + FN = 1050 = |U|.
- Predicted positives = TP + FP = 990; **not required** to equal raw class count 2289.

## Material corrections

- Removed 11 source-side rows identified as overview/parent description, nonnormative fixture provenance or mandatory error-envelope fields improperly atomized from a p.84 illustrative JSON.
- Corrected PDF-00762 FN to TP using p.84 operative safe-details prose and actual generated `02_api(8).md` line 402.
- Excluded 19 nondefinitive generated classes and reviewed 223 prior duplicate candidates with a conservative full-predicate equivalence rule.

## Reliability

**The numerical Precision of 100% is not verified precision.** Generated-only residuals were not conclusively classified from every class in a complete independent manual semantic audit; 1,412 retained raw classes have unresolved full-predicate PDF support. Individual TP lines are mechanically rechecked but their semantic bridge proof is not independently certified. FN dispositions and PDF evidence remain documented. This is a provisional best-effort score, not a claim of complete implementation requirements or absence of errors.
