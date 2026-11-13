# Semantic Duplicate Metrics — fullload (Phase 6)

**Status:** `FINAL_BEST_EFFORT`

| Item | Final count |
|---|---:|
| Eligible generated occurrences (`GO_m`) | 6080 |
| Raw semantic classes (`G_m`) | 5991 |
| Excess occurrences | 89 |
| Within-file excess | 2 |
| Across-file excess | 87 |
| Repeated semantic classes | 69 |
| Repeated classes spanning multiple files | 68 |
| **Duplicate rate** | **1.46%** |

The observed 89 excess occurrences partition into 2 within-file and 87 across-file excess occurrences. This raw-occurrence calculation is separate from source-atom coverage and does not require TP+FP to equal the raw class count. Candidate paraphrases not consolidated in prior phases remain a possible downward bias in the duplicate estimate. The 20 recovered definitive source clauses are retained as separate generated occurrences/classes in the corrected ledger.
