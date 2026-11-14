# OrionDesk AI — Phase 6 Independent Recalculation

**Protocol:** 6.1
**Status:** `PHASE_COMPLETED_BEST_EFFORT`
**Semantic certification:** `NOT_CERTIFIED`
**Method:** One unlabeled complete eight-document set

## Canonical four-cell results

| | Predicted positive | Predicted negative |
|---|---:|---:|
| Actual positive | TP 647 | FN 332 |
| Actual negative | FP 0 | TN 37 |

- Source-positive atoms (R): **979**.
- Fixed PDF-negative controls (N): **37** (bounded diagnostic inventory).
- Generated-only unsupported canonical propositions (F): **0 identified** (not proof of absence).
- Asserted negative controls (B): **0 identified**.
- Universe size: **1016** canonical propositions.
- Precision: **100.000000%** (provisional).
- Recall: **66.087845%** (provisional).
- F1: **79.581796%** (provisional).

## Raw generated duplication (separate counting unit)

- Eligible occurrences (GO): **6929**.
- Unique raw classes (G): **6851**.
- Excess occurrences: **78**.
- Within-file excess: **5**.
- Across-file excess: **73**.
- Repeated classes: **66**; across-file spanning classes: **63**.
- Duplicate rate: **1.125704%** (conservative best effort).

## Independent structural checks

Passed: **46/46**.
The checks recompute the confusion matrix and duplicate partition from individual rows, validate exact source and negative-control coverage, and reload every generated/TP/FN evidence quote from the original Markdown files.
The original PDF inspection found **2484** directly matching PDF-text evidence locators and **3** separately tagged embedded-visual locators.

## Why this is not semantically certified

- **3904** generated-class validity records lack established full PDF semantic support; therefore zero identified FP and 100% calculated precision do **not** verify all predictions.
- **142** final FN outcomes remain genuinely ambiguous, not verified omissions.
- All TP records have checked locators and structured predicate-field entries, but the evidence audit is best effort rather than independent expert semantic adjudication.
- Do not force the effective predicted-positive count to equal the raw generated semantic-class count.

## Scope boundary

The Phase-6 operation only recomputes and verifies final Phase-5 ledgers. It does not add another evaluation method, modify scored Markdown, produce an archive, or assert a new gold standard.

See `08_coverage_and_limitations.md` for full provenance and limitations.
