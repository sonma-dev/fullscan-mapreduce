# Phase 4 — Canonical Atomic Evaluation

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** v6.1; one supplied eight-file method, one fixed PDF baseline.

## One-universe four-cell results

| Actual / predicted | Predicted positive | Predicted negative |
|---|---:|---:|
| PDF-positive source atoms | TP **582** | FN **442** |
| PDF-negative controls and generated-only claims | FP **481** | TN **37** |

| Metric | Provisional result |
|---|---:|
| Precision | 54.75% |
| Recall | 56.84% |
| F1 | 55.77% |

`|R|=1,024`, `|N|=37`, `|B|=0`, `|F|=481`, `|U|=1,542`, `|P|=1,063`. The effective predicted positives are not required to equal the 3,818 raw generated classes.

**Structural checks:** `TP+FN=1024`, `TN+|B|=37`, `FP−|B|=481`, `TP+TN+FP+FN=|U|=1542`, `TP+FP=|P|=1063`. Every equation was recomputed from individual canonical rows.

## Per-class PDF validity

| Label | Raw classes |
|---|---:|
| `PDF_ENTAILED` | 159 |
| `PDF_UNSUPPORTED` | 785 |
| `SUPPORTED_NONCOVERING` | 2,874 |

| Scoring disposition | Raw classes |
|---|---:|
| `MATCHED_SOURCE_POSITIVE_COVERAGE` | 159 |
| `NOT_ELIGIBLE_FOR_CANONICAL_FP_PHASE2_LEAKAGE` | 304 |
| `SHORT_CONTEXTUAL_SUBCLAIM_PDF_SUPPORT_UNCERTAIN` | 811 |
| `SOURCE_SUPPORTED_NO_LINKED_PHASE3_TP` | 2,063 |
| `SUBSTANTIVE_GENERATED_ONLY_CANDIDATE` | 481 |


## Source evidence challenge and limitations

Every raw class has an original Markdown quote and at least one reciprocal original-PDF candidate or a genuine noncommitment-exclusion reason. Fixed negative controls were tested for affirmative assertions, not mere lexical occurrence. The reciprocal challenges retained original paragraph, source-page, and table context; 84 additional targeted source checks updated the earliest provisional results within **this phase**.

**This is not a semantically verified evaluation.** The 481 generated-only FPs are best-effort source-non-entailment candidates, not proven PDF contradictions. The provisional 582 TPs and 442 FNs are carried from Phase 3 and still require independent proof inspection, including class-ID gaps. Phase 2 contains substantive and nonsubstantive extraction mixtures; open decisions, missing-contract prose, and shorthand are excluded from affirmative FP scoring where identified. Corrective class/atomization review and full recomputation are reserved for Phase 5. The fixed 37 TN controls are a bounded sample, not an exhaustive negative universe.

**No Phase 5 work was performed.**
