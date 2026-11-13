# Final Independent Metric Recalculation

**Protocol:** v6.1. **Method:** the eight supplied Markdown specifications (one method).  
**Final status:** FINAL_BEST_EFFORT.

## Recomputed four-cell ledger

| Cell | Count |
|---|---:|
| TP | 654 |
| TN | 37 |
| FP | 812 |
| FN | 370 |

Precision **44.61%**; Recall **63.87%**; F1 **52.53%**.

## Independent identities

- R = 1024; N = 37; F = 812; asserted N = 0.
- TP + FN = R = 654 + 370 = 1024.
- TN + asserted N = 37 + 0 = 37.
- FP = F + asserted N = 812 + 0 = 812.
- U = R + N + F = 1024 + 37 + 812 = 1873.
- TP + TN + FP + FN = 1873.
- P = TP + FP = 1466, **not** the raw-class count of 2550.

## Semantic duplication

Eligible raw occurrences = 2618; raw semantic classes = 2550; excess = 68; within-file = 6; across-file = 62; duplication = **2.60%**.

## Source and reliability statement

All 90 physical PDF pages contain extractable text, and the three diagram-only quotations on physical page 8 have been visually verified. All eight scored Markdown roles were available and their 3956 physical lines were covered by earlier exhaustive inspection and phase-6 source-locator checks. At this stage, 1021 / 1024 source-positive quotations are directly located in extracted page text, and the other three are native figure text. All 872 recorded source-to-generated evidence quotation locators match the original Markdown lines.

The script `compute_metrics.py` recomputes the scores entirely from the final item ledgers and verifies one canonical binary universe. **It does not establish expert-grade logical entailment or a certified population-wide coverage estimate.**
