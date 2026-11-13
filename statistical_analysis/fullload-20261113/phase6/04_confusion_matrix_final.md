# Final Effective-Proposition Confusion Matrix — OrionDesk AI

**Method:** Eight supplied Markdown specifications.  **Protocol:** 6.1.  **Status:** FINAL_BEST_EFFORT.

| Actual / predicted | Positive | Negative |
|---|---:|---:|
| PDF-positive | TP 654 | FN 370 |
| PDF-nonpositive | FP 812 | TN 37 |

- Precision: 44.61% (654 / 1466).
- Recall: 63.87% (654 / 1024).
- F1: 52.53% (1308 / 2490).
- Positive PDF source universe R: 1024; bounded negative controls N: 37.
- Distinct unsupported generated-only propositions F: 812; asserted negative controls B: 0.
- Canonical U = R + N + F: 1873. Predicted-positive canonical units: 1466.

An asserted excluded feature would count once as an FP in the bounded negative-control row. TN does **not** represent all possible absent requirements. Raw generated class count is separate from canonical predicted-positive units and is **not** the Precision denominator. Full semantic entailment is not independently certified.
