# Phase 5 — Evidence Audits, Corrections and Recalculation

**Protocol:** v6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method:** supplied eight-file set  
**Original source:** 90-page English PDF  

## Source atomicity and denominator

The initial 1024 source-positive rows were reviewed against the Phase-1 source-atomization preflight, parent/child overlap, repeated boilerplate, selected-field inheritance and the explicit release-test catalog. 10 clearly redundant or nonnormative summary/metadata/figure rows were removed from the **common** R for all evaluated methods (this run has one method), retaining all original PDF quotes and related source IDs in `05_source_atomization_audit_final.jsonl`. The revised R has **1014** atoms. The 16 minimum release test-pack rows remain independently retained because the source requires their execution as a distinct release acceptance activity; T-01..T-12 negative exercises remain separately testable from the implementation controls. Unproven duplication in other source categories is recorded as a source-denominator uncertainty rather than arbitrarily discarded.

## FN challenge and TP audit

Phase 3 previously corrected 148 candidate false negatives. This phase additionally corrected **65** with actual original Markdown evidence, including state catalogs, ACL/cache timing, idempotent retry behavior, source normalization and deployment/release controls. In all, **449** final TP candidates now have an evidence-bearing, predicate-keyed audit row with a quote and original physical line. These are **documented best-effort reviews**, not independent certified semantic proofs. Existing candidate FN root-cause histories have been updated in place, with removed source IDs explicitly marked.

Final FN audit dispositions: `CONSERVATIVE_UNRESOLVED` = 140, `PARTIAL_ENTAILMENT` = 360, `TRUE_MISSING` = 65. Their sum is 565. The remaining FN are conservative, source-to-generated coverage judgments; lexical misses are not proof of actual omissions.

## Generated correctness and negative controls

All 5889 previously enumerated raw classes and 37 bounded negative controls remain itemized. The audit did not establish a complete positive assertion of the prohibited negative controls, and it did not establish a distinct fully disproven generated-only commitment at the available certainty level. **FP = 0 must not be read as verified absence of false positives**. There are **3973** generated classes whose PDF support remains unverified at complete-predicate level; previously optimistic validity labels have not been certified. Misclassifying all of these as FP without contradictory or absent-PDF full-predicate evidence would recreate artificial FP inflation. A later independent metric check may identify unsupported propositions but cannot treat the provisional zero as proven.

## Updated four-cell measurement

- R=1014; N=37; A=449; B=0; F=0; U=1051.
- TP=449; TN=37; FP=0; FN=565.
- Precision=100.000000% (unverified); Recall=44.280079%; F1=61.380725%.
- Raw duplication: GO=5956, G=5889, excess=67, within=7, across=60, rate=1.124916%.

**Caveat:** The arithmetic is structurally consistent, not a semantic-coverage certification. Neither the computed Recall nor Precision should be interpreted as an independently verified measure of real missing or correct requirements. The denominator and E2 contextual bridges still carry material best-effort uncertainty.
