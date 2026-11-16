# Final Canonical Confusion Matrix — OrionDesk v6.1

**Status:** `FINAL_BEST_EFFORT` (semantic evidence not independently certified).

| Actual / Predicted | Predicted 1 | Predicted 0 |
|---|---:|---:|
| Actual 1 | TP = 456 | FN = 558 |
| Actual 0 | FP = 0 | TN = 37 |

| Metric | Computed value | Evidence limitation |
|---|---:|---|
| Precision | 100.0000% | Numerically 100%; NOT a verified claim of zero unsupported generated commitments. |
| Recall | 44.9704% | Provisional source-atom coverage, sensitive to unreviewed universal/field/test equivalences. |
| F1 | 62.0408% | Inherits Precision and Recall limitations. |
| Raw duplication | 1.1249% | Conservative raw semantic-class grouping, not source coverage. |

Definitions: `R=1014`, `N=37`, `A=456`, `B=0`, `F=0`. The canonical universe has `1051` propositions; the effective predicted-positive set has `456` propositions. The raw generated universe independently contains `5889` classes and `5956` occurrences.

Structural identities: `TP+FN=|R|`, `TN+|B|=|N|`, `FP=|B|+|F|`, `|U|=|R|+|N|+|F|`, and `TP+FP=|P|` all reconcile. **Do not** equate `TP+FP` to the number of raw generated classes. TN is limited to the fixed `37` PDF-negative controls; it is not population-wide true-negative accuracy.
