# Phase 6 Final Four-Cell Evaluation

**Status:** `FINAL_BEST_EFFORT`  
**Protocol:** 6.1  
**Method:** single supplied eight-file set  
**Authority:** original 90-physical-page English design PDF, not generated specification claims.

## One Enumerated Binary Universe

| | Predicted positive | Predicted negative |
|---|---:|---:|
| Actual source-positive R | **TP 680** | **FN 344** |
| Actual PDF-negative controls and generated-only unsupported claims | **FP 426** | **TN 37** |

- R = 1,024 unique source-positive requirements.
- N = 37 fixed PDF-derived negative controls; asserted controls B = 0.
- F = 426 distinct generated-only claims judged unsupported after the bounded reciprocal review.
- U = R + N + F = **1,487** scored propositions; P = TP + FP = **1,106**.
- GO = 3,746 raw eligible generated occurrences; GC = 3,656 within-method semantic classes. P is not required to equal GC.

## Independently Recomputed Metrics

- Precision = TP / (TP + FP) = **61.48%**.
- Recall = TP / (TP + FN) = **66.41%**.
- F1 = 2TP / (2TP + FP + FN) = **63.85%**.
- Raw duplication = (GO - GC) / GO = **2.40%**.

## Meaning and Reliability

TN counts only 37 predeclared explicitly forbidden/deferred counterfactuals; it cannot measure all absent features. All rates are conventional binary measures over the *effective canonical proposition universe*, not raw-class precision. A universal generated rule may entail several independently warranted PDF atoms without creating new GO/GC occurrences.

**Structural checks passed. Semantic certification was not established.** The final FN inventory includes 20 judged missing, 243 partially covered, and 81 conservatively unresolved source requirements. The 426 remaining FP entries are conservative unsupported-generation judgments, not independently proven source contradictions. Direct evidence and class-eligibility corrections from Phase 6 are recorded in `07_change_delta.jsonl` and `06_phase6_corrections_summary.json`.
