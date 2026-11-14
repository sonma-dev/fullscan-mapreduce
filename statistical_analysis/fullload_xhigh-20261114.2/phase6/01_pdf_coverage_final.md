# Phase 1 — PDF Source Inventory and Coverage

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** 6.1  
**Baseline:** OD-AI-DDS-001 / R1.0 / revision 1.3

## Inputs and Evidence Policy

The two uploaded JSONL ledgers are the source-inventory inputs, not independent authority. The original 90-page PDF is the only normative authority. The source-positive inventory and negative controls remain shared across generated methods. No generated Markdown was scored in this phase.

## Coverage Results

- Physical PDF pages opened and inspected: **90/90**; readable text on **90/90** pages.
- PDF pages with retained source-positive atoms: **76**; other pages: document map/cover or illustrative UI-only pages.
- Uploaded PDF quote-bearing positive atoms: **1024**, normalized source-positive atoms: **979**.
- Fixed explicit PDF-negative controls: **37**, all quote-matched to their indicated pages.
- Retained source evidence locators: **2450**, of which **2447** text-matched and **3** verified from the page-8 figure image.
- Repeated input-validation statements consolidated: **43 to 1**; **42** surplus instances retired, all source locators retained.
- Context-only summary atoms excluded from scored R: **3**.

## Exclusions and Atomicity Decisions

`PDF-00020` represents the universalized rule for 43 individually cited request paths and carries an explicit `applicable_endpoints` array. The 42 original members now map to it in `01_source_atomization_audit_final.jsonl`. `PDF-00001`, `PDF-00029`, and `PDF-00058` were excluded as redundant overview or baseline-label context; their original PDF quotation and the reason remain in `09_excluded_units.jsonl`. Independent field, endpoint, event, status, DDL, and test obligations are preserved where distinct.

The eight standalone UI screenshot pages (14, 33, 43, 47, 60, 67, 77, 81) were visually inspected. Their repeated fixture-like illustration data was not elevated to new requirements. Source-backed constraints from surrounding prose remain represented. Example configuration from Appendix F is not assumed as approved production policy.

## Input Role Manifest (not scored in this phase)

1. `01_screen_functions(2).md` — 864 physical lines, SHA-256 `78b4097061beaaa7306ce5d4a89bf2d4187986966a11b888bd2dea5b27a47b97`.
2. `02_api(2).md` — 1201 physical lines, SHA-256 `7cdd0d5338b42e8a4a367c5fa822bc7e31631bcada3fd2f458386ede8c44219c`.
3. `03_data(2).md` — 1034 physical lines, SHA-256 `a58ca76f98ca4a7dc361c0fbde65f5bd2ccaadfbdff269d24491937db4974646`.
4. `04_batch_functions(3).md` — 1323 physical lines, SHA-256 `0903402cd4cef1e9e0e4a0e6d0631ab51fdb56a36535480eaa74bc0027fe22cb`.
5. `05_business_rules(8).md` — 1442 physical lines, SHA-256 `e82f7083ea3933672804ce15cc7f03c4a277e0868bace21044bc28b7c4d3f370`.
6. `06_exception_handling(20261114-124408).md` — 737 physical lines, SHA-256 `b54a943d2e27589444feb99d6753704e9f466e9561e61162527650dbbdfd323e`.
7. `07_processing_flows(4).md` — 1143 physical lines, SHA-256 `dea1dc48d15b9f5fceb621de22e82a99e7e6533ad61c82e17e04e80b4adb81a6`.
8. `08_architecture_decision(3).md` — 586 physical lines, SHA-256 `93067f5ac1bebf29ce4117682b2dff86a7d380a4cdc054c4eaf37bd7abc3a2cb`.

## Limits and Certification

- This phase normalized and verified a provided PDF-derived ledger; it did not independently reconstruct all source propositions from scratch.
- Full-page visual contact sheets and text extraction covered all 90 pages; the figure-only evidences on physical page 8 were checked against a separate full-page image.
- Textual quote matching and a targeted source-atomization review do not prove exhaustiveness or all predicate-level semantic independence for all retained atoms.
- The 43 duplicated request-validation instances were consolidated into a single source-side rule with all original applicability members and PDF quotes retained.
- Some remaining multi-clause source statements may require split/merge changes during the designated Phase 5 atomization audit; such changes must propagate to every method.
- The source universe is method-independent. The eight Markdown files are registered but not scored or compared in Phase 1.
- The negative controls are a bounded explicit-prohibition/deferral/exclusion sample, not all logically absent requirements.
- No TP, TN, FP, FN, Precision, Recall, F1, or Duplicate metric is computed in Phase 1.

**Completion gate:** All mandatory inputs were readable; source-positive and fixed-negative rows have audited PDF locators and a documented, stable, method-independent provisional denominator. Ordinary semantic ambiguity is closed at best effort. The evaluation must not advance beyond Phase 1 in this response.
