# Phase 4 — Coverage and Evidence Limitations

**Protocol:** 6.1. **Stage:** Phase 4 only. **Status:** PHASE_COMPLETED_BEST_EFFORT.

## Grounded input and fixed inventories

- Original 90-page OrionDesk PDF checked under Phase 1; the original PDF is the sole normative source.
- Eight original supplied Markdown files, with unchanged source paths and line/table-cell locators.
- Source-positive inventory R: 1,024 items. Fixed source-negative inventory N: 37 items. Neither inventory was modified.
- Generated raw inventory inherited from the Phase-3 correction: 2,672 eligible occurrences and 2,624 semantic classes.

## Current provisional outcome

| Category | Count |
|---|---:|
| TP, provisionally fully covered PDF atoms | 621 |
| FN, not proven covered in Phase-3 best effort | 403 |
| FP, generated-only PDF-unentailed classes under Phase-4 conservative screening | 915 |
| TN, unasserted bounded PDF-negative controls | 37 |

## Distinguish arithmetic from semantic certification

The four-cell total is internally reconciled over one explicit effective universe. The denominator is neither a count of all possible absent requirements nor the raw generated class count. Class-to-source mapping may be many-to-many. The 37 true negatives are bounded diagnostic controls only.

**Semantic certification is not supported at this stage.** The retrieved-PDF passages and source-positive witnesses underpin a bounded, partly algorithmic class-level screening. This is not independent human review of all generated predicates. A low or high precision/recall cannot be interpreted as independently certified correctness or completeness.

In particular, the `PDF_UNSUPPORTED` group is a *provisional PDF-entailment failure finding*, not proof that the generated feature is technically wrong, unsafe, or absent from the original PDF. Phase 4 deliberately retains unproved candidate matches as conservative FP judgments pending Phase-5 reciprocal auditing. The incoming Phase-2/Phase-3 generated class inventory may still contain non-commitment documentation metadata, over-split clauses or spurious cross-reference mappings. Such eligibility defects must be corrected instead of being treated as real design defects.

## Explicit proof corrections

- 22 previously provisionally unsupported generated classes were rechecked with an explicit source-side semantic bridge and reclassified as supported within Phase 4. Exact generated and PDF locators are retained in `04_explicit_source_proof_corrections_final.jsonl`.
- These 22 class corrections do not change the 621/403 source-side TP/FN partition inherited from Phase 3.
- The remaining provisional generated-only FP rows carry their actual nearest PDF candidate and a support-gap disposition; unreviewed close matches may still be corrected in Phase 5.

## Required Phase-5 challenges, not completed here

- Verify every remaining Phase-3 FN candidate with bidirectional exact/semantic and table-context retrieval.
- Independently challenge all source-side TP bridges for every relevant predicate.
- Challenge each generated-only FP against the full PDF, including universal rules, test fixtures, diagrams and appendices; correct generated metadata eligibility and source atomization when needed.
- Challenge `SUPPORTED_NONCOVERING` against the source-positive atom inventory and original PDF quotations.
- Recompute the canonical matrix after all corrections. Phase 6 performs an independent final review.

## Machine verification

`04_structural_verification_final.json` confirms the item-level one-universe arithmetic and unique class/occurrence mapping. It does not establish full semantic entailment.
