# Phase 2 — Generated Corpus and Raw Claim Deduplication

**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method label:** `unlabeled_eight_document_set` (the supplied filenames are not explicitly labeled as fullload, onelevel, or twolevel; no generation-method identity is inferred).  
**Protocol:** OrionDesk Six-Turn Atomic Requirement Evaluation Protocol, version 6.1.  
**Scope:** Eight actual supplied scored Markdown specifications; this document is an audit aid and is not itself a scored input.

## Summary

- All **8,330 physical Markdown lines**, including **15,945 parsed table cells**, were visited and classified by a reproducible rule-based scanner. This is *structural coverage*, not proof that every semantic requirement was perfectly atomized.
- Extracted eligible affirmative generated occurrences `|GO_m|`: **6,742**.
- Formed conservative, raw within-method semantic classes `|G_m|`: **6,669**.
- Repeated excess occurrence count: **73**; within-file excess **5**, across-file excess **68**.
- Repeated semantic class count: **63**; repeated classes spanning two or more input files: **60**.
- The **provisional, conservative** excess fraction is **1.0828%**. It is **not** a final semantic Duplicate score; fuller paraphrase and source-scope adjudication occurs in Phase 5.
- Generated exclusion records: **12,529**, comprising source/status metadata, headings, nondefinitive open questions, proposals, unsupported claims of missing implementation contracts, reference-only cells, and similar units. One source line can contribute multiple exclusions.
- Phase 1 source baselines were retained without alteration: **979 source-positive atoms** and **37 fixed negative controls**. No Phase 3 or Phase 4 judgments were issued.

## Complete Input Inventory

| Actual unchanged filename | Scored role | Physical lines | Parsed table cells | Eligible occurrences | Exclusion records |
|---|---|---:|---:|---:|---:|
| `01_screen_functions(2).md` | `01_screen_functions.md` | 864 | 2,585 | 1,068 | 1,712 |
| `02_api(2).md` | `02_api.md` | 1,201 | 2,892 | 1,096 | 2,199 |
| `03_data(2).md` | `03_data.md` | 1,034 | 2,757 | 900 | 2,160 |
| `04_batch_functions(3).md` | `04_batch_functions.md` | 1,323 | 1,617 | 926 | 1,373 |
| `05_business_rules(8).md` | `05_business_rules.md` | 1,442 | 1,661 | 1,052 | 1,210 |
| `06_exception_handling(20261114-124408).md` | `06_exception_handling.md` | 737 | 1,551 | 806 | 1,091 |
| `07_processing_flows(4).md` | `07_processing_flows.md` | 1,143 | 1,283 | 874 | 1,197 |
| `08_architecture_decision(3).md` | `08_architecture_decision.md` | 586 | 1,599 | 20 | 1,587 |

## Interpretation of Extraction

A source cell is interpreted with its enclosing Markdown heading, table column, and table row key, including source-defined API IDs, DDL fields, workflow step IDs, error codes, and acceptance assertions. A bare `201`, `Owner`, `NOT NULL`, or resource ID is never treated as a free-standing global rule; the occurrence ledger stores the actual context needed to reconstruct the scoped assertion.

Confirmed constraints within otherwise incomplete sections may remain eligible if they are separable. Explicit `Needs confirmation`, `TBD`, `Proposal`, `Unadopted proposal`, unanswered architecture choices, missing API contracts, unapproved JSON mappings, and file-to-file cross-reference cells are excluded as definitive predictions. The Architecture Decision Register was scanned, but its unresolved questions were **not** converted into approved decisions.

Canonical class consolidation uses normalized matching with inherited row/column and target identity, augmented by very high-similarity paraphrases only where numeric limits and polarity agree. Distinct API methods, resources, fields, and role constraints are not equated by topic alone. This deliberately favors avoiding false merges, at the expense of missing some semantically equivalent paraphrases.

## Evidence and Lookup

Each occurrence contains the **actual supplied filename**, 1-based physical line, section heading, row key, column header and index (for table cells), extracted proposition, original cell/line quotation, normalized statement, `GEN-*` occurrence ID, and `GCLASS-*` class ID. Every class provides its complete membership, representative quote, locators, and its merge rationale. The additional lookup JSON maps observed identifier and method/path literals to eligible occurrences for the reciprocal semantic retrieval in Phase 3.

The comprehensive line/cell coverage ledger includes blanks, Markdown headings, table headers, separators, fenced code, ordinary prose, bullet lists, and table rows. All original source-cell quotations in eligible occurrences were checked against the corresponding immutable input line.

## Exclusions by Reason (Largest Categories)

| Exclusion reason | Number of records |
|---|---:|
| METADATA_SOURCE_STATUS_OR_TRACE_COLUMN | 2,598 |
| OPEN_QUESTION_CONFLICT_TRACE_OR_PROPOSAL_SECTION | 2,269 |
| ROW_KEY_CONTEXT_ONLY | 2,173 |
| TABLE_HEADER_CONTEXT_ONLY | 1,063 |
| UNRESOLVED_QUALIFIED_ASSERTION | 938 |
| UNAPPROVED_AD_DECISION_ROW | 798 |
| HEADING_CONTEXT_ONLY | 437 |
| IDENTIFIER_ONLY | 377 |
| NONDEFINITIVE_QUESTION_OR_PROPOSAL | 327 |
| METADATA_OR_NONDEFINITIVE_NOTE | 317 |
| ILLUSTRATIVE_JSON_HTTP_OR_FLOW_DIAGRAM_NOT_AN_INDEPENDENT_PREDICTION | 247 |
| NONASSERTIVE_FRAGMENT | 214 |
| SHORT_NONCLAIM | 211 |
| ROW_DESCRIPTOR_CONTEXT_ONLY | 176 |
| DOCUMENT_BASIS_METADATA_ONLY | 112 |
| NONDEFINITIVE_OPEN_CONTRACT | 88 |
| CONTEXT_OR_UNRESOLVED_ABSENCE | 46 |
| UNRESOLVED_FACT | 24 |

## Representative Repeated Raw Classes

- `GCLASS-00056` (2 occurrences): The browser must not store long-lived refresh tokens in local storage
- `GCLASS-00162` (2 occurrences): Invalid model output — Confirmed contract: MODEL_OUTPUT_INVALID.
- `GCLASS-01009` (2 occurrences): AC-SCR-025 — Expected result: Exactly one accepted business transition; different artifact cannot publish under old approval
- `GCLASS-01079` (2 occurrences): E — Signed asynchronous boundary — Confirmed authentication and boundary: Background jobs carry immutable tenant identity in signed envelopes
- `GCLASS-01241` (2 occurrences): The orchestrator has no direct database credentials and uses narrow scoped APIs.
- `GCLASS-01269` (2 occurrences): Public responses must not expose secrets or raw provider credentials.

## Known Limitations and Next Phase

1. This pass is substantially rule-assisted; it may miss confirmed clauses that coexist with unresolved qualifiers or over-extract summary/metadata phrases. All exclusions have recorded locations and can be reconsidered when supported by the original source in later adjudication.
2. Some generated cells contain multiple independent conditions or actions. These are preserved with original full-cell evidence but are not uniformly split to the theoretical smallest testable unit. Refine only when the predicate distinctions actually change class identity or scoring.
3. Synonymous but lexically distant statements are not automatically merged. The Phase 5 duplicate audit will challenge possible missed merges while protecting separate endpoint/field/role semantics.
4. No PDF-source entailment, generated correctness, TP, TN, FP, FN, Precision, Recall, or F1 has been computed. Using raw class counts as a confusion-matrix prediction count would violate protocol version 6.1.
5. The phase label is `PHASE_COMPLETED_BEST_EFFORT`; the mechanical coverage and reconciliation checks passed, but semantic certification is not claimed.

**Phase boundary:** Phase 2 is closed. The next user request to continue authorizes **Phase 3 — Semantic Source Coverage**, not a repeat of this phase and not a combined Phase 3–6 execution.
