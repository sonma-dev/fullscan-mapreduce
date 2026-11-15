# Phase 6 — Final Best-Effort Canonical Four-Cell Matrix

**Status:** `FINAL_BEST_EFFORT`  
**Protocol:** 6.1  
**Evaluated method:** `supplied_set_01` (one complete attached eight-file set)  
**Source of counts:** Final canonical judgment rows, recomputed by `compute_metrics.py`. No historical total is used as input.

| Cell | Actual | Predicted | Count |
|---|---|---|---|
| TP | 1 | 1 | 584 |
| FN | 1 | 0 | 435 |
| FP | 0 | 1 | 571 |
| TN | 0 | 0 | 37 |
| Total | — | — | 1627 |

| Metric | Exact decimal | Display |
|---|---|---|
| Precision | 0.505627705628 | 50.56% |
| Recall | 0.573110893032 | 57.31% |
| F1 | 0.537258509660 | 53.73% |
| Semantic duplicate rate | 0.034051724138 | 3.41% |

**Universe:** `R=1019`, `N=37`, `F=571`, `B=0`, and `|U|=1627`. `|P|=TP+FP=1155`.

```text
TP + FN = 584 + 435 = 1019 = |R|
TN + |B| = 37 + 0 = 37 = |N|
FP - |B| = 571 - 0 = 571 = |F|
|U| = |R| + |N| + |F| = 1019 + 37 + 571 = 1627
|P| = TP + FP = 584 + 571 = 1155
```

This is **one effective proposition universe**, not a union of source-side coverage counts with an unrelated raw generated-class denominator. The raw generated class count `2241` does **not** equal canonical predicted-positive count `1155` and is not forced to do so. The 37 negative controls are a bounded original-PDF-grounded diagnostic set; their TN count does not describe all absent features.

**Certification limitation:** Structural arithmetic is reproducible. Full semantic correctness of all E2/E3 bridges, source atomization decisions, and PDF-unsupported classifications has not been independently certified. The scores are `FINAL_BEST_EFFORT`, not verified implementation quality or production performance.
