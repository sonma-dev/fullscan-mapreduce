# Phase 5 — Corrected Four-Cell Confusion Matrix

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Scope:** Eight actual supplied English Markdown specifications compared with the byte-identical original OrionDesk AI 90-page PDF.  
**Phase boundary:** Phase 5 complete. Phase 6 not started.

| Canonical cell | Count | Meaning |
|---|---:|---|
| TP | **979** | Original PDF requirement entailed under Phase 5 bounded review |
| FN | **45** | Complete entailment not proved; includes partial and conservatively unresolved cases |
| TN | **37** | One of 37 predeclared negative controls is not affirmatively asserted |
| FP | **0** | Independently established PDF-unsupported positive generated-only or asserted negative-control proposition |

| Metric | Value |
|---|---:|
| Precision | **100.0000%** |
| Recall | **95.6055%** |
| F1 | **97.7534%** |
| Duplicate | **4.1470%** |

## Corrected source and duplicate inventories

- Fixed PDF-positive source atoms `|R| = 1024`; fixed PDF-negative controls `|N| = 37`.
- Previous Phase 4 coverage `809 TP / 215 FN`; the Phase 5 reciprocal challenge corrected **170** further false-negative retrieval/adjudication results.
- Two path occurrences in the PDF's physically wrapped Appendix-style register were normalized to `/v1/workspaces/{workspaceId}/members`; historical IDs, original English quotes and PDF physical page 23 evidence were retained.
- **23** previously separate raw generated semantic class pairs were merged after verifying equal target, conditions, actor and outcome. All **231** supplied semantic-duplicate candidate pairs were recorded with accept/retain decisions.
- Raw generated occurrences `|GO| = 3810`; unique generated classes `|G| = 3652`; excess duplicates `158` split into **0 within-file** and **158 across-file** excesses.
- Canonical effective predicted positives `|P| = 979` do **not** have to equal raw generated classes `|G| = 3652`.

## Canonical-universe reconciliation

- `TP + FN = 979 + 45 = 1024 = |R|`.
- `TN + |B| = 37 + 0 = 37 = |N|`.
- `FP = |F| + |B| = 0 + 0 = 0`.
- `|U| = |R| + |N| + |F| = 1024 + 37 + 0 = 1061`.
- `TP + TN + FP + FN = 1061 = |U|`.
- `Duplicate = (GO - G) / GO = (3810 - 3652) / 3810 = 0.04146982`.

## Evidence qualifications

The Phase 5 audit contains 979 TP records, 630 original provisional-FN root-cause records, 1024 source-atomization audits, 37 negative-control audits, and 231 generated-duplicate candidate decisions. The audit records preserve PDF original English evidence and actual unchanged input-file line/table-cell quotes. 0 final TP records lack an independently revalidated exact generated quotation and are explicitly marked uncertified.

The original baseline source totals were kept identical to the requested `fullload_cal` universe, except for the two **verified no-denominator-change line-wrap repairs**. High-level summary atoms and illustrative/sample boundary cases are retained with explicit semantic uncertainty. A strict re-atomization could change the denominator; do not interpret the stable denominator as proof of its optimality.

**FP = 0 is a provisional classification, not proof of complete generated correctness.** 1967 generated classes remain provisionally supported-noncovering, many without independently certified original-PDF predicate evidence. Likewise, each remaining FN is a best-effort lack of proven full entailment, not necessarily a verified missing feature. Both directions are subject to semantic certification limits. The arithmetic passes do not upgrade the status to `FINAL_VERIFIED`.
