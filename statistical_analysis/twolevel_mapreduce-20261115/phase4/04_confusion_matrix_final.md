# OrionDesk AI — Phase 4 Canonical Confusion Matrix (Best Effort)

**Status:** `PHASE_COMPLETED_BEST_EFFORT` (Phase 4 only). **Protocol:** v6.1. **Method:** supplied_eight_file_set.

## Canonical four-cell results

| Cell | Actual | Predicted | Count |
|---|---:|---:|---:|
| TP | 1 | 1 | 943 |
| FN | 1 | 0 | 81 |
| TN | 0 | 0 | 37 |
| FP | 0 | 1 | 0 |
| **Universe** | | | **1,061** |

- **Precision:** 1.000000 (100.00%) **provisional**.
- **Recall:** 0.920898 (92.09%) **provisional**.
- **F1:** 0.958821 (95.88%) **provisional**.
- **Raw duplicate ratio (not the canonical scoring denominator):** 0.030809; preliminary Phase 2 value, final Phase 5 audit pending.

## One shared unit and the equations

`R=1024`, `N=37`, `A=943`, `B=0`, `F=0`. Hence `U=R+N+F=1061`, `P=A+B+F=943`.

`TP=|A|=943`; `FN=|R|-|A|=81`; `TN=|N|-|B|=37`; `FP=|B|+|F|=0`.

`TP+FN=1024=|R|`; `TN+B=37=|N|`; `FP-B=0=|F|`; `TP+TN+FP+FN=1061=|U|`; `TP+FP=943=|P|`. **Do not assert** `TP+FP=|G_m|`; here `|G_m|=3020`.

## Evidence and reliability limitations

All eight original scored Markdown files and the original 90-page PDF were available. The Phase 3 PDF-positive decisions were retained without correcting their possible atomization defects. The negative controls were challenged against the generated corpus, and no definitive affirmative assertion of the 37 prohibited counterfactuals was established. Class-level reverse PDF retrieval covered all 3,020 generated classes; `2,361` classes are flagged for further full-predicate or eligibility review. **Low lexical similarity is not proof of a false positive**, and a source-cited generated passage is not automatically semantically complete.

Zero scored FP means **no distinct affirmative, definitive source-unsupported claim was established under the bounded Phase 4 best-effort review**, **not** that the generated design is flawless. The resulting 100% provisional precision is especially sensitive to the unfinished independent generated-class/FP validity audit. TP proofs, original-source atomicity, 589 previously unresolved synonym-pair candidates and correction deltas remain Phase 5 work. No achieved production result or release sign-off is implied.

The TN universe is exactly the 37 predeclared PDF-grounded prohibited/explicitly excluded counterfactuals. It is *not* the set of all nonexistent possible requirements, and adding negative controls changes TN but not Precision, Recall or F1.
