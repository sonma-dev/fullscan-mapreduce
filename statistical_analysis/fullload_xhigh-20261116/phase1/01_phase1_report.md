# Phase 1 — PDF Requirements and Fixed Negative Controls

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** 6.1  
**Actual PDF:** `OrionDesk_AI_Detailed_Design_Specification(1).pdf`  
**Baseline:** OD-AI-DDS-001, release R1.0, design revision 1.3  
**Scope:** Source-side requirements and bounded source-negative controls only; no generated-document scoring.

## Results

- Physical PDF pages reviewed: **90 of 90**.
- Supplied positive candidate atoms retained: **1024**, with unique `PDF-*` identifiers.
- Fixed negative controls retained: **37**, with unique `NEG-*` identifiers.
- Exact normalized English quote verified on the stated physical PDF page: **1021 source atoms, 37 negative controls**.
- Figure assertions visually verified on PDF page 8: **3** (`PDF-00977`–`PDF-00979`).
- Malformed status/behavior segmentation corrected without changing IDs: **2** (`PDF-00706`, `PDF-00727`).
- Grounded excluded-source records: **17**.

## Input and evidence handling

The two supplied JSONL files are the requested reusable source inventory. Their records were not treated as independent authority: all claimed source quotes were checked against the actual 90-page PDF. Their historical source-filename references were updated to the actually mounted PDF basename; original ID numbering and quoted text were preserved. Three Figure 1.1 assertions are supported by visually inspected embedded graphics rather than machine-selectable PDF text.

## Source atomization and denominator policy

The supplied source inventory contains independently testable API result codes, actors, methods, field presence, DDL constraints, event envelope properties, tests, and runtime controls. Distinct method/path, type/nullability/keys, and scoped protocol duties are not collapsed merely for vocabulary similarity. Conversely, repeated generic interface boilerplate must not be multiplied across printed chapters. The supplied inventory uses globally scoped requirements for such recurring boilerplate and records cross-reference scopes.

Quote verification is **not** a proof of the independent normative status of every row. Review the item-level atomization preflight ledger, particularly narrative parent/child overlap, normatively adopted figure scope, example-versus-contract scope, and acceptance/security test overlap. These are disclosed residual semantic risks, not silently certified as independent obligations. The count 1,024 is a retained **provisional shared denominator** pending the designated semantic correction audit; it is not a certified goldset cardinality.

## Specific corrections

- `PDF-00706`: Appendix A.2 `PATCH /v1/cases/{caseId}` lists `200 / 409` in **Result**, not `/ 409` as a behavior. Rephrased to capture HTTP 409 as a possible conflict result.
- `PDF-00727`: Appendix A.2 `POST /v1/approvals/{approvalId}/decision` lists `200 / 409` in **Result**; the malformed `/ 409` behavior fragment is normalized to the conflict-result obligation.
- `PDF-00977`–`PDF-00979`: Figure 1.1 text is visually readable and corroborated, but absent from extracted PDF text. Evidence type changed to `PDF_FIGURE_RASTER`.

## Atomization preflight category counts

| Category | Count |
|---|---:|
| `EXAMPLE_VS_NORMATIVE_CONTRACT_REVIEW_REQUIRED` | 14 |
| `FIGURE_SCOPE_AND_DUPLICATION_REVIEW_REQUIRED` | 3 |
| `GENERAL_RULE_ATOMICITY_REVIEW_REQUIRED` | 349 |
| `MALFORMED_ATOM_CORRECTED_IN_PHASE1` | 2 |
| `PARENT_CHILD_OVERLAP_REVIEW_REQUIRED` | 4 |
| `REQUIREMENT_VS_VERIFICATION_OVERLAP_REVIEW_REQUIRED` | 28 |
| `RETAINED_SOURCE_CANDIDATE` | 624 |

## Exclusions, fixtures and status boundaries

The excluded-unit ledger separately records the preliminary nonnormative document-control material, illustrative screenshots, selected synthetic example values and unadopted Appendix F deployment settings. A field in a normative table is not excluded merely because its physical type was not defined; unapproved proposals cannot add new PDF requirements.

## Next phase gate

Phase 1 is closed at `PHASE_COMPLETED_BEST_EFFORT`. The eight scored Markdown files are present but have not been atomized or scored. The next authorized turn is Phase 2: exhaustive generated occurrence extraction and within-method class deduplication. This response creates no Phase 2 deliverables and no confusion matrix.

## Produced individual files

- `01_source_atoms_final.jsonl`
- `01_source_negative_controls_final.jsonl`
- `01_pdf_page_coverage.json`
- `01_source_atomization_preflight.jsonl`
- `09_excluded_units.jsonl`
- `01_phase1_status.json`
- `01_phase1_report.md`
