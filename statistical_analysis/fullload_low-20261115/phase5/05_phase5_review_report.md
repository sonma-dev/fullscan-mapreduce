# Phase 5 — Reciprocal Semantic Correction and Source Atomization Review

**Protocol:** 6.1. **Status:** `PHASE_COMPLETED_BEST_EFFORT`. **Input method:** `supplied_set_01` (actual named generation method unknown). This report covers Phase 5 only; Phase 6 independent final recomputation has not been performed.

## Input and scope

- Reference source: original 90-page `OrionDesk_AI_Detailed_Design_Specification(10).pdf`; 90 readable physical pages checked in Phase 1, page and quote references revisited here.
- Eight scored Markdown documents: all available, including the architecture-decision register, where unapproved alternatives remain nondefinitive. Original input files were not changed.
- The provided PDF-derived atom and negative-control records were treated as auditable candidate inventories, not as independent authorities replacing the PDF.
- Source-inventory and class changes in this turn were applied to the common scoring denominator, not conditioned on which Markdown file was most favorable.

## Source atomization and corrections

- Original source atoms: 1024. Removed/merged nonindependent narrative or figure restatements: **5** (see `05_source_atomization_audit_final.jsonl` and `07_change_delta.jsonl`). Retained source-positive atoms: **1019**. Each retained atom has a source quote, page and testability rationale in the audit.
- Source-negative controls: **37**, unchanged and scoped only to explicit prohibitions/deferrals.
- Generated raw class target correction: **one class split**, separating API-025 export and API-026 delete because they are distinct operations despite identical table-cell wording.
- Eliminated **19** generated editorial/unresolved/nonadopted classes from the prediction inventory.
- Additional initial-FN-to-TP corrections: **29**, each linked to original Markdown text and PDF source. Source-specific literal/endpoint checks led to **0** TP downgrades.
- Previously unsupported generated class judgments corrected with original PDF DDL/endpoint/full-predicate proof: **9**. These do not require inventing new source atoms.

## Evidence audits

- Initial Phase-4 TP records reviewed: **545**; final TP evidence audit rows with `CONFIRMED_TP`: **574**, including Phase-5 FN corrections. Full original file, line, table context, source page, named conditions and resulting predicate-check map are recorded.
- Final FN: **445**. Root-cause dispositions: `TRUE_MISSING` **12**, `PARTIAL_ENTAILMENT` **109**, `CONSERVATIVE_UNRESOLVED` **324**. The last category is not a verified omission; every such row retains actual retrieved candidates and an explicit missing-full-proof statement.
- Final generated-only FP: **571**. These include contextual source support that has *not* been demonstrated to entail the **complete** generated proposition. They are conservatively scored as unsupported **rather than certified false design requirements**. The other generated classes are labeled `PDF_ENTAILED` or `SUPPORTED_NONCOVERING` only on their recorded source evidence; semantic uncertainty remains in contextual matches.

## Corrected four-cell accounting

| Cell | Count |
|---|---:|
| TP | 574 |
| FN | 445 |
| FP | 571 |
| TN | 37 |

Precision **50.13%**, Recall **56.33%**, F1 **53.05%**; the actual universe is 1019 positive + 37 bounded negatives + 571 unsupported distinct generated propositions = **1627**. A single universal generated rule can cover multiple genuine source obligations; therefore source-positive coverage is not measured by raw class equality.

## Semantic duplication

Raw occurrences **2320**, distinct classes **2241**, duplicate excess **79**, within-file excess **3**, across-file excess **76**, duplicate rate **3.41%**. Class membership and file/line anchors are detailed in the duplicate ledger.

## Reliability and limits

This phase completed the accessible review and applies reproducible item-level corrections; however, exact text lookup, retrieval ranking, original-line checks and cross-document entailment are not equivalent to a separate human semantic review of every multimodal PDF predicate. The original source ledger itself contained five nonindependent higher-level assertions. The remaining **324 conservative FNs** and **571 conservative generated-only FPs** can change when material qualifiers are evaluated more deeply. In addition, status `SUPPORTED_NONCOVERING` is a source-supported validity conclusion, not a license to add source coverage after the denominator is frozen.

**Do not interpret these percentages as measured implementation correctness or certified missing specifications.** Phase 6 should independently recalculate from the final item-level ledgers, run the benchmark regression probes and disclose all unresolved semantic evidence issues.

## Output policy

All authored files are English, delivered individually. No ZIP or other archive. No next-phase activity was undertaken.
