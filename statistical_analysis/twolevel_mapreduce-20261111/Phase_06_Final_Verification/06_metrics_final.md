# Phase 6 — Final Independent Metric Recalculation

**Protocol:** `OrionDesk_One_Pass_Atomic_Evaluation_Protocol(6).md` (version 6.1)  
**Method:** `current_user_supplied_eight_document_set`  
**Phase:** 6 of 6 (closed)  
**Final evaluation status:** `FINAL_BEST_EFFORT`  
**Structural recalculation:** PASS  
**Independent semantic certification:** NOT ESTABLISHED

## Independently recomputed results

| Quantity | Value |
|---|---:|
| PDF-positive normative source atoms (`R`) | 1,024 |
| Fixed PDF-negative controls (`N`) | 37 |
| Eligible generated occurrences (`GO`) | 3,810 |
| Raw generated semantic classes (`G`) | 3,652 |
| Covered source atoms (`A`) | 979 |
| Asserted negative controls (`B`) | 0 |
| Distinct unsupported generated-only propositions (`F`) | 0 |
| Canonical predicted positives (`P`) | 979 |
| Total enumerated canonical decisions (`U`) | 1,061 |

| Cell | Actual label | Predicted label | Recomputed |
|---|---:|---:|---:|
| TP | 1 | 1 | **979** |
| TN | 0 | 0 | **37** |
| FP | 0 | 1 | **0** |
| FN | 1 | 0 | **45** |

| Metric | Current best-effort result | Exact numerator/denominator |
|---|---:|---|
| Precision | **100.00%** | 979 / (979 + 0) |
| Recall | **95.61%** | 979 / (979 + 45) |
| F1 | **97.75%** | 2 × 979 / (2 × 979 + 0 + 45) |
| Duplicate | **4.15%** | (3810 − 3652) / 3810 |

These are conventional Precision, Recall, and F1 on the **effective canonical proposition universe**, not raw occurrence or raw semantic-class precision. A source-wide generated rule can independently satisfy multiple distinct PDF atoms without multiplying generated occurrences. Duplicate is separately defined using only raw generated occurrences and classes.

## One-universe reconciliation

- `TP + FN = 979 + 45 = 1024 = |R|`.
- `TN + |B| = 37 + 0 = 37 = |N|`.
- `FP = |B| + |F| = 0 + 0 = 0`.
- `TP + TN + FP + FN = 1061 = |R| + |N| + |F| = 1061`.
- `TP + FP = 979 = |P|` (not necessarily `|G| = 3652`).
- `GO − G = 158` and `within-file 0 + across-file 158 = 158`.

The negative-control inventory comprises only **37 predeclared PDF-grounded counterfactuals**. Its 37 TNs are not an estimate of all nonexistent requirements. Adding more unasserted negative controls could increase TN but not these Precision/Recall/F1 values.

## Duplicate metrics

| Raw occurrence/class measure | Independently counted |
|---|---:|
| Eligible generated occurrences | 3,810 |
| Distinct raw semantic classes | 3,652 |
| Excess occurrences | 158 |
| Within-file excess | 0 |
| Across-file excess | 158 |
| Repeated classes | 123 |
| Repeated classes spanning multiple files | 123 |

Classification follows actual file, line and table-cell location order. The 18 definitive occurrences recovered in Phase 3 are included in GO and G membership: `3792 + 18 = 3810`.

## Independent provenance and proof checks

- All **90** physical PDF pages are present; PDF SHA-256 `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3` agrees with Phase 1.
- All **8** actual Markdown inputs match their Phase 1 hashes; Phase 2 coverage ledgers enumerate every nonblank line, including table context.
- **2,561** PDF-text evidence quotes match the original physical pages; **3** additional figure-only locators are from the embedded illustration on physical page 8.
- **979** final TP records have corresponding proof-audit entries, including **15 E3 direct** and **964 E2 logical-bridge** decisions.
- **1,525** TP generated quotation locators agree with the actual original Markdown lines.
- **630** initial candidate FN records are accounted for: **585** corrected to TP and **45** remaining FN records, each with a documented disposition and a Phase 6 corpus-wide reciprocal search.
- **3652** generated classes, **3810** occurrences, and their one-class-per-occurrence mapping reconcile exactly.

## Evidence-quality boundary

The arithmetic is independently reproduced and the cited passages physically exist, but the **semantic outcomes remain best-effort**. Specifically:

- 964 TP records use E2 bridges which are not independent human-reviewed entailment certifications.
- 11 final FN are partially entailed, and 34 remain conservatively unresolved. They are not all proven missing requirements.
- The generated-class validity ledger contains 3,218 E1-grade entries with incomplete independent semantic proof. **FP=0 and Precision=100% must not be interpreted as proof that no generated claim is unsupported.**
- The source-atomization inventory retains context-dependent review decisions, including high-level summary/normativity-boundary cases, without adjusting the shared denominator to favor this method.
- Duplication depends on conservative semantic-class equivalence decisions and can change after independent semantic adjudication.

**Reproduction:** From this output directory run `python compute_metrics.py`. The checker reads the final item-level JSONL ledgers, original uploaded inputs and PDF; recomputes every equation; verifies PDF/Markdown evidence locations; writes `06_metrics_final.json` and `06_independent_validation_final.json`; and fails on detectable structural contradictions. The checker does not claim to prove human-level semantic correctness.

**Final stop rule:** All six phases are complete. No Phase 7 exists and no archive was created.
