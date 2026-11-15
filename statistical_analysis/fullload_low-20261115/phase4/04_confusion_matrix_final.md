# Phase 4 — Generated-Claim Validity and Four-Cell Universe

**Status:** `PHASE_COMPLETED_BEST_EFFORT`. Protocol version 6.1. One complete supplied eight-Markdown set, method `supplied_set_01`. Neither full-predicate semantic support nor actual software conformance is certified by these provisional counts.

## Canonical universe

| Set | Count |
|---|---:|
| Positive source atoms `R` | 1,024 |
| Fixed original-PDF negative controls `N` | 37 |
| Eligible generated occurrences `GO_m` | 2,339 |
| Raw generated semantic classes `G_m` | 2,259 |
| Source coverage set `A_m` | 545 |
| Asserted prohibited negative controls `B_m` | 0 |
| Unsupported generated-only provisional propositions `F_m` | 599 |
| Canonical decisions `U_m = R ⊎ N ⊎ F_m` | 1,660 |

## Four-cell confusion matrix

| Actual / Prediction | Positive | Negative |
|---|---:|---:|
| PDF-positive | **TP 545** | **FN 479** |
| PDF-negative | **FP 599** | **TN 37** |

**Precision:** 0.476399 (47.64%). **Recall:** 0.532227 (53.22%). **F1:** 0.502768 (50.28%). **Provisional raw semantic Duplicate:** 0.034203 (3.42%).

## Generated validity

- PDF_ENTAILED (source-backed, not fully independently audited): 407.
- SUPPORTED_NONCOVERING (source-backed, no retained R atom covered): 1,253.
- PDF_UNSUPPORTED (conservatively unresolved/unsupported): 599.
- Distinct initial reverse FP candidates later corrected against cited original PDF passages: 304.
- Additional false-positive classification inconsistencies corrected using Phase 3 original-PDF TP citations: 53.
- Nondefinitive bibliographic/metadata extractions removed: 30 classes in total.

## Four-cell equations

`TP + FN = 545 + 479 = R (1024)`. `TN + B = 37 + 0 = N (37)`. `FP = F + B = 599 + 0`. `TP + TN + FP + FN = 1660 = U_m`. `TP + FP = 1144 = P_m`, which is **not** generally equal to the raw generated class count 2259.

## Evidence quality and limitations

The class validity decisions cite **actual original PDF pages** and real Markdown lines. Initial word/character retrieval produced demonstrably false unsupported outcomes; source-page reverse checks and cross-ledger checks corrected known cases in this phase. **Remaining conservative FP classifications may still be false positives caused by split tables, paraphrases or multi-clause bridges**. Conversely, `PDF_ENTAILED`/`SUPPORTED_NONCOVERING` includes contextual/automated judgments without full independent predicate proof. Consequently, Precision and F1 are **provisional and potentially materially unstable**, not verified indicators of source-supported design correctness. The 479 inherited Phase 3 FNs also include 344 conservative unresolved decisions; they are not certified missing requirements. Phase 5 must re-audit every source TP/FN and generated-only F claim and make item-level corrections when warranted.

`TN` counts only the 37 predeclared PDF-negative controls, not all unasserted requirements. This scored set's actual generation method was not identified by its filenames; `supplied_set_01` is an input-set identifier only. Source PDF and all eight supplied Markdown documents were left unchanged, and no bundled archive was created. This response closes Phase 4 and does not execute Phase 5.
