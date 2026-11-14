# Phase 4 — Reciprocal Generated-Claim Validity: Uncertainty Register

This is a **best-effort** validity audit, not a semantic certificate. The one-universe arithmetic is checked separately from the meaning of each generated claim.

## Evidence classes

- **879** reverse-linked generated classes have a PDF source-positive record cited in an earlier TP bridge. This establishes a starting witness, but **does not independently prove all qualifiers** in the generated class.
- **1461** classes have a candidate PDF context/partial source witness. They must not be treated as fully entailed source atoms or as automatically unsupported generated claims.
- **841** of these have low-confidence PDF context rather than an independently demonstrated full entailment. They are individually enumerated in `04_pending_reverse_support_review.jsonl` with actual original file/line and physical PDF quotations. The candidate evidence is **not sufficient to label the proposition `PDF_ENTAILED` with verified confidence**.
- **38** formerly scored reference-only or document-metadata classes were excluded from the definitive generated universe. Every removed class is recorded in `04_generated_eligibility_corrections.jsonl`.

## Scoring consequences

This bounded pass did **not establish** a distinct affirmative generated-only unsupported claim with a complete PDF non-entailment proof and adopted scope. The provisional canonical F count is therefore zero. This is **not proof** that no generated false positives exist. The 841 unresolved support challenges can change F and its contribution to precision, and some previously classified source TPs can change after rechecking source-predicate completeness.

The provisional 100% precision is a **numerical output of the current adjudicated ledger only**. It must never be reported as a certified precision measurement. A later auditor must not silently promote the 841 low-confidence rows into proven `SUPPORTED_NONCOVERING` merely because a topical PDF passage was cited. The Phase-5 procedure is to read each original context and either affirmatively verify the narrower source-supported claim, exclude a non-definitive row, or turn a distinct unentailed affirmative residue into an F proposition with reproducible evidence.

## Tests run

- Original generated class/occurrence foreign keys, distinct IDs, PDF-positive references and complete canonical universe assertions.
- Original Markdown line existence for all 2340 retained class representatives.
- PDF physical-page range and original extracted quotation existence for all retained evidence records.
- Every fixed source-negative row has the original cited prohibition/deferral and no asserted affirmative output in the current polarity adjudication.
- Verified all 1,061 canonical units have a single actual/predicted pair and matching cell; TP+FN=1,024 and TN+B=37.

**Unperformed:** independent full semantic verification of every generated class and all prior TP bridges. Structural validation is not semantic verification.
