# Phase 1 — Source-Atom Ledger Adoption and PDF Evidence Validation

**Protocol:** OrionDesk One-Pass Atomic Evaluation Protocol, version 6.1  
**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Scope:** Phase 1 only; no Phase 2 analysis or scores.

## Source selection and input identity

At the user's explicit request, the two uploaded source evidence ledgers were adopted as the starting positive and fixed-negative inventories. Their individual JSONL rows, normalized statements, source IDs, quotations, and fields were copied byte-for-byte into the canonical deliverable names. This is **not** a new independent derivation of the atom boundaries from the PDF; the provenance marker `independent_source_extraction: true` belongs to the supplied input and does not certify this run's independent extraction.

The original PDF has **90 physical pages** and identifies **OD-AI-DDS-001**, **R1.0 / revision 1.3**. Its actual uploaded basename is `OrionDesk_AI_Detailed_Design_Specification(9).pdf`. The supplied ledgers use the shorter documentary citation basename `OrionDesk_AI_Detailed_Design_Specification.pdf`; the manifest explicitly records this alias. All eight scored Markdown roles and the protocol are present and readable, but no Markdown content was evaluated for semantic coverage in this phase.

## Frozen-input inventory (not yet a verified semantic denominator)

| Inventory | Uploaded rows | Unique IDs | Page validity | Evidence access |
|---|---:|---:|---|---|
| PDF-positive source atoms R | 1,024 | 1,024 | All valid | 1,021 PDF text-page matches, plus 3 visually checked page-8 figure quotes |
| PDF-negative controls N | 37 | 37 | All valid | 37 PDF text-page matches |

All atom/control IDs are unique and sequential; no exact duplicate English normalized atomic statements or negative-control statements were found. This does **not** certify nonduplication by semantic equivalence or prove that every atomic statement is a fully faithful implication of its PDF quote.

## Evidence check methodology and findings

- **1,021** positive quotes are contiguous after normalization in the PDF's page text extraction.
- **0** additional positive quotes have all their words on the cited page but not in one contiguous extraction span; many refer to multi-column tables. Page-level token matching alone does **not** verify row/column inheritance, full applicability, or literal quotation layout.
- **3** figure-sourced positive statements (`PDF-00977`–`PDF-00979`) were verified visually in the rendered page-8 diagram, whose text is not in the extractable PDF text layer.
- **37** negative-control quotes have contiguous PDF-page text evidence; **0** others are token-supported on the specified page.
- **0** quotes were left without a supported PDF page-level textual or verified illustrated location.

The file `01_pdf_evidence_checks.jsonl` contains an individual evidence-access verdict for all **1,061** source/control records. The check does not assert independent full semantic entailment of every normalized statement.

## Physical-page review

All 90 pages were opened and text-extracted, and the relevant figure pages were rendered for visual inspection. The source atoms cite **76** distinct physical pages. Pages without an adopted positive atom: **1, 2, 3, 4, 5, 6, 14, 33, 43, 47, 60, 67, 77, 81**. The figure-dominant pages are: **14, 33, 43, 47, 60, 67, 77, 81**. Lack of an atom on a navigation, figure-only, or appendix page is not by itself proof that all its possible normative content is absent or out of scope.

The Appendix A API table, Appendix B entity/DDL tables, Appendix C event/tool schema, Appendix D/E negative and release tests, and Appendix F examples were explicitly included in the validation; the corresponding original page images were inspected. Figure-derived assertions were assessed separately from text-layer matches. Page-specific counts and scan details are in `01_pdf_page_coverage.json`.

## Atomicity, semantic, and source-denominator limitations

The supplied source ledger splits named endpoint method/path, actor, status, and behavior; individual entity fields; independent DDL constraints; event contract properties; and explicit test scenarios. Such splits can be valid but cannot be accepted or rejected merely because textual statements look similar. The high-repetition evidence groups include: `NORMATIVE_PROSE (341), COMPONENT_CONTRACT (110), DATA_FIELD (80), REGISTER_API (68), EVENT_VERIFICATION (44), REGISTER_EVENT (44), INTERFACE_VALIDATION (43), EVENT_CONTRACT (24)`. In particular, Appendix D/E test scenarios must not automatically duplicate the corresponding substantive application obligation, and repeated chapter-level validation boilerplate must not manufacture source denominators.

No objective statement-level contradiction or exact duplicate ID was discovered in these checks. However, a full **independent semantic atomization** and field/row-context audit of all 1,024 supplied statements was not completed in this response, and some evidence checks establish page-level tokens only. Therefore the source denominator is an **adopted best-effort working inventory**, not independently certified coverage gold. Potential overlap and split/merge checks are documented in `01_source_atomization_challenge.jsonl` for the designated Phase 5 correction process; any proven change must be applied to the common source universe for every method.

The fixed controls are explicitly PDF-grounded prohibitions, exclusions, or deferrals and remain identical for all compared methods. The 37 controls constitute a deliberately bounded diagnostic N set, not a population-wide count of absent software requirements. No TN, TP, FP, FN, Precision, Recall, F1 or Duplicate metric is computed in Phase 1.

## Completion decision

`PHASE_COMPLETED_BEST_EFFORT` — All mandatory inputs for this phase are accessible; the user-supplied positive and negative ledgers are adopted with 1,061 individually checkable PDF evidence-access records, a 90-page inspection register, and documented atomization caveats. The stricter `PHASE_COMPLETED_VERIFIED` claim is not made because copying/quote validation is not independent full-PDF semantic atomization. Phase 2 is the next permitted phase upon a new user instruction; it has not been started.
