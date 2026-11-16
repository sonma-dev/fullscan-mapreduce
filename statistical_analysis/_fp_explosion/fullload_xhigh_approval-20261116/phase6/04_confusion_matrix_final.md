# Phase 5 Corrected Four-Cell Confusion Matrix

**Status:** `PHASE_COMPLETED_BEST_EFFORT` (semantic scores provisional, not certified).

| Cell | Count |
|---|---:|
| TP | 715 |
| TN | 37 |
| FP | 1642 |
| FN | 308 |

| Metric | Value |
|---|---:|
| Precision | 30.3352% |
| Recall | 69.8925% |
| F1 | 42.3077% |
| Raw semantic Duplicate | 0.5861% |

Source-positive R: 1023; fixed bounded controls N: 37; unsupported residual F: 1642.
Canonical U: 2702; predicted positives P: 2357; raw semantic classes: 5258; eligible occurrences: 5289.

Equations: TP+FN=1023=|R|; TN=37=|N| because no fixed control is asserted; FP=1642=|F|; |U|=|R|+|N|+|F|=2702; TP+FP=2357=|P| (not necessarily |G|).

These numbers are reproducible over the present item-level judgments, **not independent certification of semantic entailment**. The large conservative FP residual, possible unsplit composite generated statements, and remaining uncertain FN entailments can change the result in either direction.
