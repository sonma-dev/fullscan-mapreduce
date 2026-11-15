# OrionDesk Phase 1: PDF Coverage and Source-Inventory Audit

**Protocol:** v6.1. **Phase:** 1 of 6. **Status:** `PHASE_COMPLETED_BEST_EFFORT`.

## Inputs and authority

- Authoritative document: `OrionDesk_AI_Detailed_Design_Specification(10).pdf` (90 physical pages, readable text on all pages).
- User-supplied positive candidate ledger: `01_source_atoms_final(9).jsonl`.
- User-supplied bounded negative-control ledger: `01_source_negative_controls_final(20261115-060104).jsonl`.
- The original PDF alone supplies normative authority. The two provided ledgers were reused as the initial candidate inventories; they were not blindly treated as independently certified gold standards.
- All eight Markdown specifications are available but are deliberately excluded from Phase 1 source extraction, controls construction, and scoring.

## Coverage and identity checks

- 90/90 PDF pages readable; all pages examined through text extraction and source/page structure checks. The figure on page 8 and the eight illustrative operator-view pages were also visually checked.
- 1,024 distinct PDF-positive source IDs retained; 1,021 verbatim quotes found in the corresponding page text, plus 3 page-8 figure assertions confirmed by direct visual inspection.
- 37 unique PDF-negative controls; all 37 PDF evidence quotations match their cited pages. Negative controls are affirmative counterfactuals of explicit exclusions, deferrals, or prohibitions; they are not all possible absent requirements.
- Source positive atoms occur on 76 physical pages. The other 14 pages are cover/contents or reference-UI-only pages; see the per-page ledger.
- No exact duplicate normalized positive-statement pair was found. Distinct field/endpoint/test predicates in shared source paragraphs were retained rather than eliminated by identical PDF-quote text.
- 7 unambiguous table-reconstruction corrections were applied to the candidate statements, retaining the original source IDs and exact PDF quotations. See `01_source_normalization_corrections.jsonl`.

## Meaningful atomicity challenge

- Shared boundary requirements (`tenant_id`, revision, actor, timestamp and correlation) are represented as universally scoped predicates, not copied for every chapter/endpoint.
- Appendix A.2 REST rows were interpreted using the method/path, scope, result, and behavior column together. Separate actor/status/path predicates remain independently testable.
- Appendix B.1 entity fields were interpreted in the entity and selected-field context. The selected-field catalog does not establish missing physical DDL types or nullability.
- Repeated chapter event-verification obligations are associated with named event types. The generic positive/cross-tenant/replay/evidence-retention test duty is not multiplied once per chapter.
- Appendix E named test scenarios are retained as explicit verification obligations rather than treated as extra evidence that the underlying implementation already exists. Potential overlaps with implementation predicates require the independent Phase 5 source-atomization audit.
- 6 parent/child or multi-predicate candidates remain flagged for the required later semantic re-audit. These records are **not** silently promoted to certified independently meaningful source atoms.

## Scope of exclusions

Representative exclusions are listed in `09_excluded_units.jsonl`: title and TOC metadata; example/reference UI values on pages 14, 33, 43, 47, 60, 67, 77, 81; and unadopted configuration examples in Appendix F. Explicit deferrals and prohibitions may contribute to the fixed negative-control inventory, but are not automatically positive implementation features.

## Verification limitations and next-phase boundary

The supplied source-positive ledger is large and was algorithmically atomized before this turn. All individual source **quotes** were validated, while full independent semantic atomicity and parent/child nonoverlap were checked with rules and selected manual challenges, not human-certified for every one of the 1,024 propositions. The exact retained denominator is therefore provisional pending the Phase 5 atomization correction process. This phase has complete source evidence access, so it is closed as `PHASE_COMPLETED_BEST_EFFORT`, not terminated for unavailable inputs.

No confusion matrix, Precision, Recall, F1, duplication score, or generated-document entailment judgment is produced during Phase 1. The eight scored Markdown inputs remain unchanged for Phase 2.

## Positive evidence by PDF page

| Page | Positive atoms | Extractable text characters | Embedded image count |
|---:|---:|---:|---:|
| 1 | 0 | 692 | 0 |
| 2 | 0 | 4890 | 0 |
| 3 | 0 | 6042 | 0 |
| 4 | 0 | 6087 | 0 |
| 5 | 0 | 5943 | 0 |
| 6 | 0 | 5146 | 0 |
| 7 | 12 | 1140 | 1 |
| 8 | 22 | 2252 | 1 |
| 9 | 7 | 4008 | 0 |
| 10 | 19 | 3351 | 0 |
| 11 | 12 | 2008 | 1 |
| 12 | 9 | 4082 | 0 |
| 13 | 12 | 3040 | 0 |
| 14 | 0 | 314 | 1 |
| 15 | 12 | 2010 | 1 |
| 16 | 14 | 3900 | 0 |
| 17 | 13 | 3234 | 0 |
| 18 | 12 | 2118 | 1 |
| 19 | 11 | 3976 | 0 |
| 20 | 12 | 2971 | 0 |
| 21 | 11 | 2071 | 1 |
| 22 | 8 | 3878 | 0 |
| 23 | 12 | 3050 | 0 |
| 24 | 21 | 2104 | 1 |
| 25 | 11 | 3905 | 0 |
| 26 | 12 | 2936 | 0 |
| 27 | 9 | 1920 | 1 |
| 28 | 8 | 4151 | 0 |
| 29 | 12 | 3079 | 0 |
| 30 | 8 | 2087 | 1 |
| 31 | 9 | 3905 | 0 |
| 32 | 12 | 3060 | 0 |
| 33 | 0 | 314 | 1 |
| 34 | 16 | 2050 | 1 |
| 35 | 6 | 3794 | 0 |
| 36 | 12 | 2965 | 0 |
| 37 | 7 | 2099 | 1 |
| 38 | 7 | 3918 | 0 |
| 39 | 12 | 2964 | 0 |
| 40 | 7 | 2124 | 1 |
| 41 | 9 | 3909 | 0 |
| 42 | 13 | 2952 | 0 |
| 43 | 0 | 316 | 1 |
| 44 | 10 | 1813 | 1 |
| 45 | 5 | 4044 | 0 |
| 46 | 12 | 3093 | 0 |
| 47 | 0 | 316 | 1 |
| 48 | 18 | 2036 | 1 |
| 49 | 8 | 3898 | 0 |
| 50 | 12 | 2972 | 0 |
| 51 | 10 | 2116 | 1 |
| 52 | 8 | 3882 | 0 |
| 53 | 12 | 2944 | 0 |
| 54 | 10 | 2104 | 1 |
| 55 | 9 | 3881 | 0 |
| 56 | 12 | 2969 | 0 |
| 57 | 17 | 2124 | 1 |
| 58 | 8 | 3883 | 0 |
| 59 | 13 | 2936 | 0 |
| 60 | 0 | 316 | 1 |
| 61 | 9 | 2131 | 1 |
| 62 | 7 | 3877 | 0 |
| 63 | 12 | 2941 | 0 |
| 64 | 10 | 2120 | 1 |
| 65 | 9 | 3847 | 0 |
| 66 | 12 | 2950 | 0 |
| 67 | 0 | 316 | 1 |
| 68 | 7 | 2120 | 1 |
| 69 | 7 | 3860 | 0 |
| 70 | 12 | 2962 | 0 |
| 71 | 10 | 1866 | 1 |
| 72 | 7 | 4107 | 0 |
| 73 | 11 | 2966 | 0 |
| 74 | 9 | 2168 | 1 |
| 75 | 6 | 3868 | 0 |
| 76 | 12 | 2955 | 0 |
| 77 | 0 | 316 | 1 |
| 78 | 10 | 2201 | 1 |
| 79 | 5 | 3760 | 0 |
| 80 | 12 | 3184 | 0 |
| 81 | 0 | 316 | 1 |
| 82 | 10 | 1512 | 0 |
| 83 | 62 | 4586 | 0 |
| 84 | 8 | 721 | 0 |
| 85 | 98 | 2672 | 0 |
| 86 | 28 | 1077 | 0 |
| 87 | 43 | 2356 | 0 |
| 88 | 26 | 2697 | 0 |
| 89 | 22 | 2747 | 0 |
| 90 | 7 | 1994 | 0 |
