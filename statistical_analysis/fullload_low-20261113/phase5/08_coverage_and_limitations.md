# Phase-5 Coverage, Corrections and Limitations

**Method:** The eight original attached Markdown specifications (unchanged).  
**Protocol:** v6.1, Phase 5 of 6.  
**Status:** PHASE_COMPLETED_BEST_EFFORT; not certified semantic coverage.

## Source baseline

The same 1,024 source-positive IDs and 37 fixed negative controls from the earlier `fullload_cal` inventory were reused. One normalized source statement, `PDF-00193`, was corrected from an OCR/text-wrap-truncated `/me` to `/members` against the same original PDF page-23 quotation. All source quotes and IDs remain unchanged; no source denominator correction was necessary after checking the 16 mandated minimum release tests, repeated component-target verification, universal interface rules, and Appendix B field scope.

## Corrections

- FN to TP after original-input reciprocal review: **55**.
- TP to FN because only the API path, not the PDF-required schema and bounded errors, was proved: **22**.
- Nondefinitive generated classes excluded as reference-only: **55**.
- Predicate-preserving raw class merges: **18** groups; **20** excess raw classes unified.
- PDF-grounded generated-only FP candidates reclassified as supported: **19**.

## Corrected score and scope

TP=654; FN=370; FP=839; TN=37. Precision=43.804421%; Recall=63.867188%; F1=51.966627%. The canonical U contains **1900** rows, all on the same binary universe. The bounded N contributes exactly **37** TN, with no positive assertions of an explicitly prohibited capability found.

## FN diagnostic and evidence limitations

{"TRUE_MISSING": 111, "CONSERVATIVE_UNRESOLVED": 191, "PARTIAL_ENTAILMENT": 68}

Each remaining FN was challenged against actual generated candidates in the retained Stage-3 review plus Stage-5 candidate retrieval. Source-to-generated ranking is not a proof; each match must satisfy target, action, actor, condition, scope, timing, exception and outcome. The remaining `CONSERVATIVE_UNRESOLVED` decisions are not certified absence and may move in either direction. 654 final TP records have a locator-and-predicate audit entry; the proof records remain bounded expert-rule adjudications, not independently certified end-to-end semantics. Some earlier TP proof templates are boilerplate and cannot be treated as evidence solely because every check was marked `MET`.

## Source atomization audit

Every retained source-positive atom has an audit entry. Sixteen appendix-E test scenarios are retained as separately mandatory release test obligations, not re-scored feature duplicates. Repeated chapter component rows keep their distinct named target; global boilerplate cannot create an extra nameless requirement. Appendix B field entries inherit their entity/table row. PDF p.23 word wrap was normalized without altering its underlying quote. No uncertain atomization group was merged without proof of duplicate full predicates.

## Generated validity audit

Every retained generated semantic class has a validity row. `SUPPORTED_NONCOVERING` requires affirmative PDF evidence and does not create a new source-positive atom. Some PDF_UNSUPPORTED rows remain best-effort; an exact error label, field name, or topical overlap is not accepted without full context. No raw class is counted twice as a generated-only FP and a negative-control assertion.

## Duplication and completion boundary

Eligible occurrences=2618; classes=2550; repeated excess=68 (within=6; across=62); duplicate rate=2.597403%. Every occurrence belongs to one raw class. This is Phase 5 only. Phase 6 independent recomputation and final delivery validation have not been performed.
