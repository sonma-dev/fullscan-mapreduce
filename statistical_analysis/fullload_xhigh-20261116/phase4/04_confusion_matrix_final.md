# Phase 4 — Generated-Claim Validity and One Canonical Binary Universe

**Protocol:** v6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method:** `supplied_eight_file_set`  
**Reliability:** Provisional / semantic certification NOT achieved.

## Common universe

- Frozen PDF-positive atoms `R`: 1,024.
- Frozen PDF-negative controls `N`: 37.
- Raw generated occurrences `GO`: 5,955; raw semantic classes `G`: 5,888.
- Asserted negative controls `B`: 0.
- Generated-only unsupported propositions **established in this bounded pass** `F`: 0.
- Canonical effective universe `U = R ⊎ N ⊎ F`: 1,061.
- Canonical predicted positives `P = A ∪ B ∪ F`: 384; not the raw class count.

## Four-cell confusion matrix (provisional)

| Actual / Predicted | Positive | Negative |
|---|---:|---:|
| PDF-positive actual (R) | TP = 384 | FN = 640 |
| PDF-negative actual (N ∪ F) | FP = 0 | TN = 37 |

| Metric | Formula | Provisional value |
|---|---|---:|
| Precision | TP/(TP+FP) | 1.000000 |
| Recall | TP/(TP+FN) | 0.375000 |
| F1 | 2TP/(2TP+FP+FN) | 0.545455 |
| Duplicate | (GO-G)/GO | 0.011251 |

## Arithmetic reconciliation

- TP + FN = 384+640 = 1024.
- TN + B = 37+0 = 37.
- FP = F + B = 0+0 = 0.
- TP + TN + FP + FN = 1061 = |U|.
- TP + FP = 384 = |P|; **not** required to equal the raw class total 5888.

## Evidence-quality warning

**The zero established generated-only unsupported claims is NOT a verified claim that all 5,888 generated classes are PDF-supported.** Source-to-generated coverage uses the uncorrected Phase-3 best-effort determinations. Reverse-source retrieval examined every generated class but left **3,973 low-confidence support-classifications** requiring independent semantic adjudication. As a result, the provisional Precision of 1.0 is an unverified and potentially inflated point estimate; it is not a correctness guarantee or an evidence-based lower bound. In Phase 5, unsupported definitive commitments must be promoted to distinct `F_m` entries when supported by a real contradiction/non-entailment proof and duplicate semantic classes must be merged without artificial FP multiplication. The absence of a source atom for a narrow correct generated claim does not establish FP.

The bounded negative controls are not the universal population of all absent requirements; 37 PDF-grounded counterfactuals were challenged. Counterfactual mentions in failure tests, explicit prohibitions or unresolved design discussions were not affirmative implementation claims. All 37 remained TN at this evidence level.

**Structural validity and semantic evidence certification are separate.** This phase closes as best effort; Phase 5 is the designated correction and independent audit phase.
