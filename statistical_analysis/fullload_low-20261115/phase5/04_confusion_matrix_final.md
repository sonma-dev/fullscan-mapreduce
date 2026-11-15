# Phase 5 corrected four-cell confusion matrix — best effort

Protocol 6.1; one eight-Markdown corpus, `supplied_set_01`. No unsupported semantic verification claims.

| Cell | Count |
|---|---:|
| TP | 574 |
| TN (fixed source-negative controls only) | 37 |
| FP (generated claims without demonstrated complete PDF support) | 571 |
| FN (not fully entailed) | 445 |

**Precision:** 0.501310 (50.13%). **Recall:** 0.563297 (56.33%). **F1:** 0.530499 (53.05%). **Raw Duplicate:** 0.034052 (3.41%).

`R=1019`, `N=37`, `F=571`, `B=0`, `|U|=1627=R+N+F`, `TP+FN=1019=R`, `TN+B=37=N`, `TP+FP=1145=|P|` (not necessarily `|G|=2241`).

Source-positive source inventory corrected by 5 nonindependent parent/figure restatements. Generated classes split by one endpoint-context mismatch and 19 nonpredictive editorial items excluded. 29 additional FN to TP, 0 TP to FN, and 9 unsupported-class classification corrections.

Uncertainty: 324 remaining conservative FN and 571 conservative generated-only unsupported claims are **not** necessarily genuine omissions or hallucinated requirements. Provisional statistics can move in either direction. The source-positive and generated validity decisions are semantically best effort; structural equations alone cannot certify them.
