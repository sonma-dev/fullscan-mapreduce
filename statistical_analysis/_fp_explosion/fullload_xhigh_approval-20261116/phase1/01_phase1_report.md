# Phase 1 — PDF Source-Inventory Verification and Fixed Negative Controls

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** version 6.1  
**Authoritative source:** `OrionDesk_AI_Detailed_Design_Specification.pdf`; document ID `OD-AI-DDS-001`, R1.0 / design revision 1.3  
**Input policy:** The two user-designated source ledgers are reused byte-for-byte, not silently re-extracted or modified. The original PDF remains the authoritative normative evidence for every scored item.

## Completion and input checks

| Check | Result |
|---|---:|
| Physical PDF pages opened and rendered | 90 / 90 |
| Source-positive inventory entries `R` | 1024 |
| Negative controls `N` | 37 |
| Positive quotes matched to actual PDF page text | 1021 |
| Positive quotes confirmed from a rendered diagram/figure | 3 |
| Negative-control evidence quotes matched to PDF page text | 37 / 37 |
| Duplicate source or negative-control IDs | 0 |
| Source-positive pages represented in the ledger | 76 |
| Illustration-only pages checked | 14, 33, 43, 47, 60, 67, 77, 81 |
| Required scored Markdown roles found, unmodified | 8 / 8 |

Pages 1–6 are non-scored cover and document-map pages. Pages 14, 33, 43, 47, 60, 67, 77, 81 are primarily representative UI mockups whose numeric values, navigation illustrations and sample case labels do not by themselves create independent functional requirements. Text-bearing specification pages, data/contract tables, appendix definitions, and normative figures were included in the PDF-side examination. The three diagram-derived quotations are `PDF-00977`, `PDF-00978`, and `PDF-00979` on page 8.

## Source ledger scope

The nominated positive inventory contains 1024 recorded normative propositions (IDs `PDF-00001`–`PDF-01024`). The fixed negative control inventory contains 37 counterfactuals (IDs `NEG-00001`–`NEG-00037`), constructed from explicitly excluded features, release deferrals and prohibitions.

The PDF-positive/negative distinction is one of **logical polarity**, not lexical negation: a PDF duty to prohibit an unsafe behavior is a PDF-positive requirement, while the affirmative unsafe behavior is a source-negative control. This inventory will remain common to the evaluated specification set; negative controls will not be expanded based on generated-document content.

## Atomization challenges and evidence limitations

- **API duplication candidate review:** 14 method/path groups occur both in chapter API registers and in Appendix A's public API table. These groups contain 15 apparent repeated API-existence rows beyond one canonical occurrence. Distinct actor, status-code, parameter and conditional commitments must remain separate. Each candidate with original PDF locators is enumerated in `01_source_atomization_review_candidates.jsonl`.
- **Additional candidate issues:** A summary-level workflow assertion (`PDF-00001`), a compound hash-and-provenance assertion (`PDF-00003`), and baseline metadata phrased as an atom (`PDF-00029`) require an independent-testability challenge. These are **identified review exceptions**, not secretly discarded requirements.
- **Acceptance and test-matrix overlap:** 16 `ACCEPTANCE_TEST` atoms need independent execution-obligation versus implementation-restatement adjudication, while preserving the original test triggers and expected outcomes. Existing `SECURITY_NEGATIVE_TEST` scenarios are separately traceable as explicit verification exercises.
- **Inherited predicate metadata gaps:** Null/empty fields in the supplied source records: `actor`=1009, `target`=399, `scope_en`=1016, `precondition_en`=975, `exception_en`=1024, `timing_en`=981, `expected_outcome_en`=1024. The underlying exact PDF quotation and context must be consulted during entailment, especially for table fields and shared universal requirements. Empty metadata does not imply that a corresponding predicate is absent from the PDF.
- **Evidence certification boundary:** Exact PDF quote verification and machine-readable ledger reconciliation do not prove that all substantive PDF duties have been independently and correctly atomized. No unreviewed semantic match is granted verified status from these source-side checks.

Given the user's explicit reuse request, the two scored source input ledgers are **byte-identical copies** of their attachments. This Phase 1 result therefore closes as `PHASE_COMPLETED_BEST_EFFORT` rather than claiming a fully corrected and certified independent source denominator. The identified possible corrections are retained for the source-atomization correction audit in Phase 5; any actual change must carry old/new IDs, PDF evidence and apply uniformly to every method being evaluated. No prior historical source count or score was treated as truth.

## Files and next phase boundary

- `01_source_atoms_final.jsonl`: the supplied positive source inventory `R` preserved exactly.
- `01_source_negative_controls_final.jsonl`: the supplied predeclared source-negative controls `N` preserved exactly.
- `01_pdf_page_coverage_final.jsonl`: 90 per-page text/render/image/atom coverage observations.
- `01_source_evidence_audit_final.jsonl`: one original-PDF evidence verification per source-positive atom.
- `01_negative_control_evidence_audit_final.jsonl`: one original-PDF verification per fixed negative control.
- `01_source_atomization_review_candidates.jsonl`: source-side possible overcount/atomicity exceptions and proposed dispositions, without altering the user's input.
- `09_excluded_units.jsonl`: explicit non-scored front matter, representative UI fixtures and illustrative example material.
- `01_phase1_status_final.json`: machine-readable phase status, source counts and input hashes.

**Phase 2 has not been executed.** It will inspect all eight scored Markdown inputs, assign eligible generated occurrence and semantic-class IDs and calculate raw semantic duplication. TP/TN/FP/FN and corresponding metrics are intentionally **not reported in Phase 1**.
