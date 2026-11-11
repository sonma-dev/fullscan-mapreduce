# OrionDesk v6.1 — Final Semantic Duplication Metric

**Status:** FINAL_BEST_EFFORT (structurally reproduced, semantic equivalence provisional)

| Item | Independently recomputed value |
|---|---:|
| Eligible generated occurrences | 3,350 |
| Unique within-method claim classes | 3,218 |
| Excess duplicate occurrences | 132 |
| Within-file excess | 16 |
| Across-file excess | 116 |
| Repeated classes | 86 |
| Repeated classes spanning multiple files | 82 |
| **Duplicate** | **3.94%** |

Formula: `(eligible generated occurrences - distinct raw generated semantic classes) / eligible generated occurrences`.

Checks: `within-file + across-file = excess` and `excess = eligible occurrences - unique classes`.
This metric is independent of the effective source-atom coverage projection. Class equivalence remains best-effort.
