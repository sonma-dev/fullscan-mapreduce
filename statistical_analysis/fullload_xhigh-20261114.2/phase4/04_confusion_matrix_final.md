# Phase 4 — Generated Claim Validity and Canonical Confusion Matrix

**Protocol:** 6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Semantic certification:** Not certified

## Effective canonical proposition universe

| Measure | Count |
|---|---:|
| Frozen source-positive requirements `R` | 979 |
| Predeclared PDF-negative controls `N` | 37 |
| Evidence-established unsupported generated-only propositions `F` | 0 |
| Enumerated canonical units `U = R + N + F` | 1,016 |
| Raw generated classes examined (Phase 3 inheritance) | 6,865 |
| Generated occurrences examined (Phase 3 inheritance) | 6,938 |

## Provisional confusion matrix

| Actual / Predicted | Predicted positive | Predicted negative |
|---|---:|---:|
| Actual positive | TP = 587 | FN = 392 |
| Actual negative | FP = 0 | TN = 37 |

**Precision:** 100.000000% (provisional, not verified)  
**Recall:** 59.959142% (provisional)  
**F1:** 74.968072% (provisional)

`TP + FN = 587 + 392 = 979`; `TN + asserted negative controls = 37 + 0 = 37`; `FP = |F| + |B| = 0 + 0 = 0`; `|U| = 587 + 37 + 0 + 392 = 1016`; `|P| = TP + FP = 587`. Do not substitute the raw generated class count for `|P|`.

## Generated claim validity, preliminary

| Adjudication | Count |
|---|---:|
| PDF_ENTAILED | 1,488 |
| SUPPORTED_NONCOVERING | 5,368 |
| EXCLUDED_NONDEFINITIVE (explicitly unapproved proposal) | 9 |
| PDF_UNSUPPORTED established | 0 |

Every raw class has a record in `04_generated_claim_validity_final.jsonl` with an original generated Markdown line/table-cell locator, an original PDF text quotation, and a review tier. `SUPPORTED_NONCOVERING` is provisional for weak matches, not independent proof of entailment. The nine proposal records are retained as extraction corrections and never scored as adopted permissions.

## Mandatory evidence caveat

**The computed 100% Precision must not be interpreted as verified perfect generated correctness.** The present FP count denotes only affirmative unsupported propositions established by the bounded Phase 4 adjudication. The PDF-evidence search alone does not establish complete semantic entailment for every raw generated class. In particular, 3,904 weak-corroboration classes require an independent substantive review, and 1,464 additional classes are supported only by moderate lexical evidence. Therefore `FP=0` remains vulnerable to later corrections, and the displayed Precision is an optimistic provisional point estimate, not a statistically established lower bound or completeness finding.

The 37 TN cases are a fixed bounded PDF-derived set only. Mentions of prohibited capabilities, explicit exclusions, and deferred options are not treated as affirmative implementation commitments. Details of the top retrieved generated mentions for each negative control are in `04_negative_control_assertion_audit_final.jsonl`.

Phase 3 source-side judgments were carried forward unchanged; independent TP bridge, FN and source-atomization reaudits are reserved for Phase 5. The Phase 4 validity and canonical ledgers are complete structurally, while semantic certification is not claimed. No Phase 5 or Phase 6 results are included.
