# OrionDesk AI: Phase 6 Independent Ledger Recalculation

**Protocol:** 6.1  
**Status:** `FINAL_BEST_EFFORT`  
**Scope:** Supplied eight Markdown specifications versus one original 90-page fictional PDF.

## Effective canonical confusion universe

| Canonical category | Count |
|---|---:|
| PDF-positive `R` | 1,009 |
| Fixed PDF-negative controls `N` | 37 |
| Unsupported generated-only propositions `F` | 0 |
| Asserted negative controls `B` | 0 |
| Canonical decision universe `U = R + N + F` | 1,046 |
| Canonical predicted-positive units `P = TP + FP` | 997 |

| Cell | Count |
|---|---:|
| TP | 997 |
| TN | 37 |
| FP | 0 |
| FN | 12 |

**Exact equations:** TP + FN = 997 + 12 = 1,009; TN + B = 37 + 0 = 37; FP = F + B = 0 + 0 = 0; four-cell total = 1,046.

## Independently recomputed metrics

| Metric | Rate |
|---|---:|
| Precision, TP / (TP + FP) | 100.000000% |
| Recall, TP / (TP + FN) | 98.810704% |
| F1, 2TP / (2TP + FP + FN) | 99.401795% |
| Duplicate, (GO - G) / GO | 4.041721% |

Raw eligible generated occurrences `GO` = 3,068; raw semantic classes `G` = 2,944; excess duplicates = 124; within-file excess = 5, across-file excess = 119, repeated classes = 88.

**Important:** TP + FP = 997 is the effective source/proposition predicted-positive count, **not** the raw class count 2,944. TN covers only the predeclared PDF-derived negative-control inventory, not the universe of all conceivable absent features.

## Verification quality

Structural equations and file/item references: **PASS**. Semantics: **NOT INDEPENDENTLY CERTIFIED**. The 0 observed FP cells do not certify perfect precision. At least 1,636 generated classes labeled `SUPPORTED_NONCOVERING` occur in TP evidence for 926 source atoms; these require separate generated-claim validity reconciliation. Every one of the 997 retained TP proof rows is marked not independently certified. Exact regression probe records and unresolved FN evidence are linked in the accompanying JSONL.
