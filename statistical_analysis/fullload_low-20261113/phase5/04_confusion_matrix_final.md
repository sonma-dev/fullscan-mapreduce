# Corrected Phase-5 Confusion Matrix

**Status:** PHASE_COMPLETED_BEST_EFFORT. Source proposition recall and raw generated class precision must not be conflated.

| Actual / predicted | Predicted positive | Predicted negative |
|---|---:|---:|
| PDF-positive | TP 654 | FN 370 |
| PDF-nonpositive | FP 839 | TN 37 |

- Precision: 43.804421%
- Recall: 63.867188%
- F1: 51.966627%
- Canonical universe: 1900 proposition rows (R=1024, N=37, F=839).
- TNs count only predeclared PDF exclusions; they do not represent the population of all absent requirements.
- FP is conservatively adjudicated PDF non-entailment, not a certified count of erroneous design behaviors.
- Structural reconciliation is independent of semantic evidence certification.
