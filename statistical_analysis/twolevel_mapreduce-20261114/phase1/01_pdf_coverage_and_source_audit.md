# Phase 1 — PDF Source Inventory and Fixed Negative Controls

**Protocol:** OrionDesk six-turn atomic requirement evaluation, version 6.1  
**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**PDF baseline:** `OrionDesk_AI_Detailed_Design_Specification(8).pdf` (`OD-AI-DDS-001`, R1.0 / design revision 1.3)  
**Physical pages inspected by automated full-page extraction:** 90/90  
**Source-positive requirement atoms (R):** 1024  
**Fixed explicit source-negative controls (N):** 37  

## Source selection and evidence integrity

The user supplied `01_source_atoms_final(20261114-023550).jsonl` and `01_source_negative_controls_final(20261114-023550).jsonl` as already PDF-derived evidence inventories. Both inventories were reused as the common, method-neutral candidate denominator and verified against the actual uploaded original PDF. Source IDs, negative-control IDs, source propositions, original English quotations and logical modalities were preserved. Source evidence file locators were updated to the actual uploaded filename rather than the ledger's unsuffixed historical display name; no source assertion was edited.

- Positive records whose complete English quote occurs in normal extracted PDF text: **1021**.
- Additional positive records verified by alternate PDF reading order: **0**.
- Positive records present only in the rendered normative Figure 1.1 on page 8: **3** (`PDF-00977`, `PDF-00978`, `PDF-00979`), confirmed by visual inspection.
- Unlocated positive quotations: **0**.
- Negative controls with a source-page textual quotation verified against the PDF: **37/37**.
- Unique, consecutive IDs and disjoint positive-versus-negative identifiers: **pass**.

The canonical source-negative inventory is bounded: 5 explicit exclusions, 3 release deferrals, and 29 explicit prohibited counterfactuals. These are not a population of all nonexistent features.

## All-page coverage

Every physical PDF page returned extractable text and was included in automated page and layout inspection. Requirement locations appear on **76** different physical pages. The pages with no independent positively scored source atom are: **1, 2, 3, 4, 5, 6, 14, 33, 43, 47, 60, 67, 77, 81**. Pages 1–6 are cover/map pages, and pages 14, 33, 43, 47, 60, 67, 77 and 81 contain representative fictional user-console figures, not independent confirmed field defaults or production KPIs. Figure-only pages were reviewed at a contact-sheet level; selected main-page and register figures were additionally rendered at higher resolution.

The PDF includes source-wide normative diagram text (page 7 and Figure 1.1 on page 8), chapter narrative, per-chapter component and interface registers, the endpoint table on page 83, DDL on page 86, event/tool tables on page 87, security tests on page 88, and release test fixtures on page 89. Their evidence is carried by the positive ledger; Appendix F illustrative settings on page 90 are not automatically adopted operational defaults. See `01_pdf_page_coverage.jsonl` and `09_excluded_units.jsonl`.

## Atomicity, cross-references and remaining risks

The supplied atomization intentionally distinguishes API method/path, caller, status and behavioral outcome; Appendix B entity and DDL field contexts; source-negative counterfactuals; substantive security controls; and independently required negative tests. Exact normalized duplicate atomic statements were not found. Repeated shared interface boilerplate is represented through a common scope rather than repeating all five fields for each endpoint.

There are **8** explicit checks or review flags in `01_source_atomization_review.jsonl`. The most material unresolved issues are possible parent/child overlap in the architecture summary; multi-duty figure-summary atoms; and possible duplication between Appendix D security-negative tests and Appendix E verification cases. They were not silently removed or rephrased, because the user explicitly requested use of these two supplied inventories and the protocol reserves source-atomization corrections for Phase 5. If proven, an item-level old/new ID change must be recorded and the same revised denominator applied to every compared generation method.

## Completion boundary

The phase is closed as **best effort**, not source-semantic certification. This phase establishes a PDF-grounded candidate `R` and `N`, explicit exclusions, all-page coverage and reproducible quote checks. It does **not** inspect definitive claims for scoring, calculate a confusion matrix, certify semantic equivalences, or advance to Phase 2. The eight supplied Markdown specifications remain unchanged for the next turn.
