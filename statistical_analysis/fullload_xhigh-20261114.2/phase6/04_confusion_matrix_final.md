# Phase 5 — Corrected Canonical Confusion Matrix

**Status:** `PHASE_COMPLETED_BEST_EFFORT` — not semantically certified.

| Actual / Predicted | Positive | Negative |
|---|---:|---:|
| PDF-positive | TP 647 | FN 332 |
| PDF-negative controls and unsupported claims | FP 0 | TN 37 |

Precision: 100.000000%; Recall: 66.087845%; F1: 79.581796%.

R=979; N=37; F=0; U=1016; P=647. One enumerated canonical universe: TP+FN=R, TN+asserted controls=N, FP=F+asserted controls, TP+TN+FP+FN=U.

**Caution:** The computed Precision of 100.00% is not evidence of zero unsupported generated requirements. Approximately 3904 generated classes have insufficient independent PDF predicate support from automated retrieval; the current FP register contains only evidence-established violations. Conservative FN are not verified omissions. A negative-control TN is one bounded PDF-grounded counterfactual, never a population-wide negative.
