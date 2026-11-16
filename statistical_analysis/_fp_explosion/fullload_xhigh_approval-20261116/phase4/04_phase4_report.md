# Phase 4 Completion Report

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol version:** 6.1  
**Scope:** Reverse generated-class PDF correctness, fixed negative-control polarity, and one canonical confusion universe.

## Work performed

1. Read the immutable previous Phase 1, 2 and 3 ledgers and the original PDF.
2. Examined all 5265 generated working semantic classes, each with the original Markdown occurrence and actual PDF textual retrieval candidates. The Phase 3 recovery addendum of 70 original Markdown occurrences is explicitly included without changing the Phase 2 ledger.
3. Evaluated all 37 fixed PDF-grounded negative controls by scanning the generated corpus for source-excluded counterfactual claims; recorded nearest actual generated quotations and candidate-polarity checks.
4. Kept original Phase 3 positive judgments (714 TP and 310 FN) intact; added the negative controls and generated-only residual propositions to one explicitly enumerated `U`.
5. Computed structural formulas in `04_confusion_matrix_final.json` and the matching Markdown report.

## Results

- **TP:** 714; **FN:** 310; **FP:** 1795; **TN:** 37.
- **Canonical decision units:** 2856.
- **Raw generated class decisions:** {'PDF_UNSUPPORTED': 1795, 'SUPPORTED_NONCOVERING': 1402, 'PDF_ENTAILED': 2068}.
- **Precise four-cell interpretation:** source-atom coverage projection, not raw-class classification accuracy.
- **Bounded negative controls asserted:** 0.

## Evidence quality and unresolved issues

Each generated-class validity row references an actual original Markdown line and a real original PDF candidate quote or an existing PDF-positive link. Rule-assisted matching and proximity to a source quotation **do not independently prove all predicates**. The supported-noncovering and unsupported claims require semantic adjudication; no unsupported residual was silently removed. Some generated descriptions of pending contracts and negative requirements were included as raw classes by Phase 2 and are flagged as potential eligibility defects. These uncertainties are not represented as verified false positives or as verified design omissions.

The source-atomization concerns identified in Phase 1 and the fuller Phase 3 TP/FN evidence challenges remain designated for Phase 5. Phase 4 makes no claim of final semantic certification. All individual files are English. No archives were created. **Phase 5 was not performed.**

## Independent structural and evidence-location validation

The separate Phase 4 checker reconciled all raw-class decisions, canonical items, labels, and confusion equations. Original generated quotations were checked as substrings of the actual source Markdown lines. The PDF evidence check found 21 figure-derived PDF-atom excerpts on physical page 8 that are unavailable in the plain-text extraction; those need image verification rather than treating the plain-text omission as a contradiction. Five generated classes have no defensible quoted PDF candidate in the current retrieval index and are explicitly flagged in the QA ledger. A further 146 generated classes marked provisionally unsupported also occur as evidence for a Phase 3 positive-coverage judgment; these are high-priority reciprocal semantic review exceptions, **not** independently proven errors or verified FP claims.

The present Phase 4 numbers must not be represented as certified Precision, Recall or F1. This phase only closes the provisional universe and the auditable generated validity inventory.
