# Final Canonical Confusion Matrix — Phase 6

**Protocol:** 6.1  
**Method scope:** One complete, unlabelled eight-file Markdown generation set  
**Status:** `FINAL_BEST_EFFORT` — independently arithmetically recomputed, not semantically certified.

| Canonical cell | Count | Meaning |
|---|---:|---|
| TP | 990 | Source-positive atomic propositions provisionally fully covered |
| FN | 23 | Source-positive propositions not fully demonstrated after recorded reciprocal review |
| TN | 37 | Unasserted PDF-grounded bounded negative controls |
| FP | 0 | Asserted forbidden controls or uniquely demonstrated unsupported generated residuals *in this bounded review* |

Source inventory `|R| = 1013`; fixed controls `|N| = 37`; independently enumerated generated-only unsupported residues `|F| = 0`.  
Canonical universe `|U| = |R| + |N| + |F| = 1050`; canonical predicted-positive count `|P| = TP + FP = 990`.

| Metric | Recomputed value |
|---|---:|
| Precision | 100.00% |
| Recall | 97.73% |
| F1 | 98.85% |
| Raw semantic duplicate rate | 4.625% |

Definitions: `Precision=TP/(TP+FP)`, `Recall=TP/(TP+FN)`, `F1=2TP/(2TP+FP+FN)`. Each unit has exactly one `actual_label`, `predicted_label`, and cell. **Do not apply** `TP+FP=|G|`: the raw generated semantic classes (2289) are different units from the canonical source-proposition projection.

The calculated **100% Precision is not certified precision**. 1412 generated classes remain without an independently complete PDF entailment proof. The zero FP is the current detected count, not an affirmative proof that all generated definitive claims are PDF-supported. The 37 TN apply solely to a fixed, selected negative-control set and do not estimate all absent requirements.

See `06_metrics_final.json`, `06_independent_checks.json`, and `08_coverage_and_limitations.md` for full reproducibility, corrections, and residual uncertainty.
