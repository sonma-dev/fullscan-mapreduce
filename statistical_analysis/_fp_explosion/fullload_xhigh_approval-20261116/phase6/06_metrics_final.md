# Phase 6 - Independent Ledger Recalculation

**Protocol:** v6.1. **Method:** `supplied_unprefixed_set`. **Phase status:** `PHASE_COMPLETED_BEST_EFFORT`.
**Structural reconciliation:** `PASS`. **Semantic certification:** `NOT_VERIFIED`.

## Recomputed canonical decision universe

| Ledger unit or cell | Count |
|---|---:|
| PDF positive propositions R | 1023 |
| Fixed PDF negative controls N | 37 |
| Unsupported generated-only canonical propositions F | 1642 |
| Canonical universe U | 2702 |
| Canonical predicted positives P | 2357 |
| TP | 715 |
| TN | 37 |
| FP | 1642 |
| FN | 308 |

## Recomputed rates

| Metric | Exact proportion | Percent |
|---|---|---:|
| Precision | 715/(715+1642) | 30.3352% |
| Recall | 715/(715+308) | 69.8925% |
| F1 | 2*715/(2*715+1642+308) | 42.3077% |
| Duplicate | (5289-5258)/5289 | 0.5861% |

These counts are derived independently from the individual JSONL records. The source-positive/negative partitions and all four arithmetic equations are checked, not inferred from a previously saved metrics JSON.

## Raw generated duplication

- Eligible occurrences GO: **5289**.
- Raw distinct semantic classes G: **5258**.
- Excess occurrences: **31**; within-file **0**, across-file **31**.
- Repeated classes: **27**; repeated classes spanning multiple files: **27**.

Effective predicted positives P = **2357**, which is *not* required to equal the raw semantic-class count G = **5258**.

## Interpretation

The numerical output is a **provisional effective-proposition assessment, not verified design completeness**. FP includes conservative unsupported residuals, not merely documented PDF contradictions. FN includes incomplete/uncertain semantic matches. TN applies to only the **37 predeclared PDF-negative controls**. Structural reconciliation cannot certify natural-language entailment. See `08_coverage_and_limitations.md`, `06_validation_final.json` and `06_regression_probes_final.jsonl`.
