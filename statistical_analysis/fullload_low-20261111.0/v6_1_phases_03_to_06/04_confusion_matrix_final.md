# OrionDesk v6.1 — Final Canonical Confusion Matrix

**Phase 6 status:** FINAL_BEST_EFFORT; structural recomputation passed, semantic certification not attained.

| Actual / predicted | Predicted positive | Predicted negative |
|---|---:|---:|
| Actual positive (PDF source atoms) | **TP 673** | **FN 351** |
| Actual negative (fixed controls plus generated-only unsupported propositions) | **FP 210** | **TN 37** |

- Source-positive atoms: 1,024; predeclared bounded PDF-negative controls: 37.
- Generated-only unsupported canonical propositions: 210; asserted negative controls: 0.
- Canonical decision universe: 1,271; effective predicted-positive units: 883.
- Precision: **76.22%**; Recall: **65.72%**; F1: **70.58%**.
- Raw generated classes: 3,218; **not** the precision denominator.

Formulas: `TP=|A|`, `FN=|R|-|A|`, `TN=|N|-|B|`, `FP=|F|+|B|`, `|U|=|R|+|N|+|F|`.
Fixed negative controls are a bounded diagnostic selection, **not** all nonexistent requirements. Their count does not improve precision, recall or F1.
The two Phase 6 exact-match corrections are recorded under `PDF-01013` and `PDF-01014` in `07_change_delta.jsonl`.
