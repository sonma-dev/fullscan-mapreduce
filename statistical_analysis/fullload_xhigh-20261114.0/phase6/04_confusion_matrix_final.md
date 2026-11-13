# Final Four-Cell Confusion Matrix — fullload (Phase 6)

**Protocol:** v6.1  
**Evaluation status:** `FINAL_BEST_EFFORT` (semantic certification not established)

| Cell | Final count | Actual | Predicted |
|---|---:|---:|---:|
| TP | 576 | 1 | 1 |
| FN | 451 | 1 | 0 |
| FP | 0 | 0 | 1 |
| TN | 37 | 0 | 0 |

| Metric | Computed value | Interpretation |
|---|---:|---|
| Precision | 100.00% | Provisional: the PDF support of thousands of generated classes remains unverified. |
| Recall | 56.09% | Fraction of the 1027 current source atoms adjudicated as entailed; not certified overall coverage. |
| F1 | 71.87% | Derived from the same four-cell universe. |
| Duplicate | 1.46% | Raw generated occurrence/class duplication, not an alternate precision denominator. |

The canonical universe has **1064** units: 1027 PDF-positive requirements, 37 bounded PDF-negative controls, and 0 positively asserted unsupported generated-only propositions. This does not mean that no other unsupported claims exist; the PDF-support audit is not independently complete.

Equations: TP+FN=1027=|R|; TN+asserted controls=37=|N|; FP=unsupported-only (0) + asserted controls (0); all four cells sum to 1064=|U|. Positive canonical predictions=576, **not** raw generated classes (5991).

**Scores are strictly provisional.** They measure specification propositions relative to the fictional PDF baseline and are not accuracy or safety certifications of a deployed system.
