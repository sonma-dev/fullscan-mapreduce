# OrionDesk Phase 5 — Corrected Source, Generated, Coverage and Duplication Audits

**Protocol:** 6.1. **Status:** `PHASE_COMPLETED_BEST_EFFORT`. **Method:** `current_scored_8` (the supplied eight Markdown files).

## Changes from Phase 4

| Metric | Phase 4 | Phase 5 |
|---|---:|---:|
| PDF-positive source atoms | 1,016 | 1,009 |
| TP | 1,003 | 997 |
| TN | 37 | 37 |
| FP | 0 | 0 |
| FN | 13 | 12 |
| Canonical decision units | 1,053 | 1,046 |
| Generated eligible occurrences | 3,265 | 3,068 |
| Generated semantic classes | 3,168 | 2,944 |

Seven additional source atoms were retired with original PDF evidence: PDF-00757 through PDF-00762 (illustrative Appendix A.3 schema fields, including a second duplicate of the explicit safe-details allowance) and PDF-00964 (fictional specimen metadata, not an independently testable implementation requirement). Their removal is recorded for every method in `07_change_delta.jsonl`. Source-positive R is now 1009; the same N=37 controls are retained from `fullload_cal`. This correction does **not** change the underlying PDF.

## Canonical scores — provisional

| Statistic | Value |
|---|---:|
| Precision | 100.0000% |
| Recall | 98.8107% |
| F1 | 99.4018% |
| Duplicate (raw classes) | 4.0417% |

These are exact arithmetic results over the **current adjudicated ledgers**, but **not independently semantically certified**. In particular, a zero observed FP is a bounded evidence finding, not a demonstration of perfect accuracy. The prior `SUPPORTED_NONCOVERING` category contains thousands of context-based source associations, and an independent full-predicate validation of every association has not been demonstrated. There remains uncertainty in both directions, including false TP and false FN.

## Reciprocal FN dispositions

The remaining 12 FN judgments are 7 `CONSERVATIVE_UNRESOLVED` and 5 `PARTIAL_ENTAILMENT`, recorded with actual generated-file candidates and specific unmet propositions in `03_fn_root_cause_audit_final.jsonl`. PDF-00964 was removed as nonnormative. A missing or weak automated retrieval hit is never treated by itself as verified absence of the requirement.

## TP audit and source atomization

All 997 retained TP decisions have a corresponding item in `05_tp_evidence_audit_final.jsonl` with original PDF quotes, generated file/line/table evidence, and a predicate-check map. Six prior positive judgments were retired because their source atoms were not independently normative; their audit rows remain as `SOURCE_ATOM_REMOVED`. No third-party or manual verification has independently certified the entire predicate-check collection; automated corroboration must not be confused with complete semantic proof.

The source audit has one row for each of the former 1,016 atoms, documenting retained independent predicates, exact-quote groups, illustrative-example removals and the risk of duplicated parent/child verification. Splitting individual database fields and separate event responsibilities is retained where these are independently testable. Additional atomization ambiguity is explicitly preserved.

## Generated semantic duplication

Eligible generated occurrences: 3068. Corrected unique classes: 2944. Excess occurrences: 124. Within-file excess: 5; across-file excess: 119. Repeated classes: 88, including 84 classes spanning multiple source Markdown files.

The phase excluded 200 nondefinitive or bare-trigger occurrences, merged 27 additional extremely close classes, and **restored three expected-result cells** omitted by the earlier table parser. Each occurrence is assigned to exactly one final raw generated class. These corrections affect Duplicate, not the number of PDF-positive effective predictions.

## Limits and next phase

Both the PDF extraction and generated extracted classes were comprehensively indexed, but a fully independent human review of each of the more than one thousand source-to-generated predicate entailments and several thousand source-support judgments is not attested. Semantic uncertainty cannot be expressed as a statistical error bar from this evidence. The Phase 6 independent recomputation, diagnostic exact-match probes, cross-ledger verification and final limitations report are **not executed in this turn**.
