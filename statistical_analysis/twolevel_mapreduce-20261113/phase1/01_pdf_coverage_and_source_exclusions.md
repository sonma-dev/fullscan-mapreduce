# OrionDesk AI — Phase 1 PDF Coverage and Source Exclusions

**Protocol:** 6.1  
**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Scope:** PDF source positive atoms `R` and bounded PDF-negative controls `N` only. The eight supplied Markdown files were verified present and are reserved for Phase 2; no generated claims were scored in this phase.

## PDF identity and stable comparison baseline

- Authoritative current upload: `OrionDesk_AI_Detailed_Design_Specification(10).pdf`.
- Document: `OD-AI-DDS-001`, `R1.0 / revision 1.3`; **90 physical pages**.
- Current PDF SHA-256: `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`.
- Source-positive ledger: **1,024** atoms, `PDF-00001`–`PDF-01024`; original ledger SHA-256 `8a6c97eaf52e3cbe544de9515e22a9f806b173ceac4c12c800f3888ad9053dbc`.
- Fixed negative-control ledger: **37** controls, `NEG-00001`–`NEG-00037`; original ledger SHA-256 `ba48d66de139609fbf7d5ff3d3783a1e3792d5f5120b81c404e129ef1561a253`.
- The current PDF is byte-identical to the PDF identity recorded for `fullload_cal`. Both materialized historical R/N ledger files are copied unchanged, including source IDs, English quotations, evidence pages, and historical canonical source filename.
- The unchanged historical canonical filename is mapped to the actual current PDF upload in `01_input_manifest_final.json`; it is **not** a claim that the current upload literally bears the old filename.

## Page and evidence verification

- **90/90** physical pages parsed and inspected, including front matter, chapter figures, all tables and appendices.
- **31** pages contain an embedded raster illustration; the contact-sheet visual review covered these pages. Chapter diagrams are examined as logical illustrations and fictional console mockups are not treated as selected production configuration.
- **2,564/2,564** citation locations successfully rechecked against this PDF: **2,561** normalized-exact textual matches on the stated physical page and **3** manually inspected quotations in Figure 1.1 on physical page 8.
- The quote checks verify presence and physical-page fidelity, not automatically normative force or full semantic atomicity. Details are enumerated in `01_pdf_quote_verification_final.jsonl` and per-page inspection in `01_pdf_page_coverage_final.jsonl`.
- **133** non-scored exclusion records are logged in `09_excluded_units.jsonl` for recurring running furniture, navigation-only front matter, UI mockups, purely illustrative fixtures, diagram-layout assumptions, example configuration, and unresolved choices. This exclusion log is an explicit audit sample by occurrence/category rather than a claim of exhaustive word-by-word enumeration of every nonnormative phrase.

## Positive and negative source polarity

- A source prohibition such as a high-risk publication ban remains an `R`-positive duty to enforce that ban. An affirmative counterfactual may independently appear as a fixed bounded `N` control, without treating the two logical propositions as interchangeable.
- All 37 negative controls were rechecked against PDF exclusion, prohibition or deferral language before looking at any generated prediction for this new evaluation. Their controls are bounded, not an exhaustive list of everything absent from the PDF.
- No historical TP, TN, FP, FN, Precision, Recall, F1, duplicate metrics, or prior matcher judgments were carried forward.

## Source atomization challenge and limits

- Exact normalization of the **1,024** `atomic_statement_en` values found no identical duplicates. This syntactic check does **not** rule out paraphrased overlap or parent/child double scoring.
- **21** specific audit challenges are enumerated in `01_source_atomization_challenge_final.jsonl`: tests versus substantive implementation predicates; universal interface boilerplate; component/contract registers; context-dependent Appendix B fields; illustrative A2A fields; and parent architecture overview versus testable child commitments.
- The TST-001–TST-016 verification matrix explicitly asks for tests. Their execution obligations may be independently scoreable, but their expected behavior must not silently duplicate an already scored implementation outcome. Appendix B field atoms inherit their entity and table-column context.
- The user-requested common `fullload_cal` source inventory is preserved **unchanged** for cross-method comparability. No method-specific denominator correction was made in Phase 1. Any confirmed source split/merge must be recorded and applied uniformly to all methods in the designated correction phase, not silently suppressed or altered for this corpus.
- Consequently, this is a **completed best-effort Phase 1**, not an unconditional certification that all 1,024 items are the smallest independently meaningful propositions. PDF identity and quotation fidelity are verified; semantic atomization remains subject to the recorded challenges.

## Explicit stop boundary

Phase 1 is closed. Do not run generated-corpus occurrence extraction, source-to-generated matching, duplicate scoring, or four-cell metrics until subsequent separate user-authorized phases. All deliverables are individual English files; no archive was created.
