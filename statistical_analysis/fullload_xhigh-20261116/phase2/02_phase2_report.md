# Phase 2 — Generated Corpus Inspection and Raw Semantic Duplication

**Protocol:** 6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method identifier:** `supplied_eight_file_set` (one complete supplied eight-document set; no prefix inferred)

## Inputs inspected

| Role | Unchanged uploaded filename | Physical lines | SHA-256 |
|---|---|---:|---|
| 01 | `01_screen_functions(1).md` | 864 | `78b4097061beaaa7306ce5d4a89bf2d4187986966a11b888bd2dea5b27a47b97` |
| 02 | `02_api(1).md` | 1,201 | `7cdd0d5338b42e8a4a367c5fa822bc7e31631bcada3fd2f458386ede8c44219c` |
| 03 | `03_data(1).md` | 1,034 | `a58ca76f98ca4a7dc361c0fbde65f5bd2ccaadfbdff269d24491937db4974646` |
| 04 | `04_batch_functions(1).md` | 1,323 | `0903402cd4cef1e9e0e4a0e6d0631ab51fdb56a36535480eaa74bc0027fe22cb` |
| 05 | `05_business_rules(1).md` | 1,442 | `e82f7083ea3933672804ce15cc7f03c4a277e0868bace21044bc28b7c4d3f370` |
| 06 | `06_exception_handling(3).md` | 737 | `b54a943d2e27589444feb99d6753704e9f466e9561e61162527650dbbdfd323e` |
| 07 | `07_processing_flows(2).md` | 1,143 | `dea1dc48d15b9f5fceb621de22e82a99e7e6533ad61c82e17e04e80b4adb81a6` |
| 08 | `08_architecture_decision(2).md` | 586 | `93067f5ac1bebf29ce4117682b2dff86a7d380a4cdc054c4eaf37bd7abc3a2cb` |

## Extracted inventories

- Eligible generated occurrences (`GO`): **5,922**.
- Raw unique semantic classes (`G`): **5,855**.
- Excess occurrences: **67**.
- Preliminary duplicate rate: **1.131375%**.
- Repeated classes: **57**; across-file repeated classes: **50**.
- Within-file excess occurrences: **7**; across-file excess occurrences: **60**.
- Physical lines inspected: **8,330**; line/cell units classified: **19,636**.
- Excluded nondefinitive, metadata, and supporting units: **8,530** (including table-cell exclusions; overlap with source/metadata context is explicit).

## Extraction rules

All eight unchanged source Markdown files were decoded as UTF-8 and inspected from the first to last physical line. Markdown tables were split into cells with escaped-pipe and inline-code awareness. Each retained cell receives its physical line, column index, column header and original row anchor. Prose and semicolon-separated assertions were extracted into source-quoted atomic candidates. Nested section and conditional table context is preserved, not inferred from stand-alone literals alone. Code blocks are classified separately; verifiable reference DDL terms are eligible while illustrative, unresolved or decorative code is excluded.

Unapproved proposals, TBD/Needs confirmation statements, open questions, conflict registers, unsupported inferences and bare citations do not become definitive generated claims. Where a line contains both resolved and unresolved subclaims, only the resolvable independent portion is eligible. Examples and baseline screenshots are not adopted as production configuration.

Raw classes are grouped by normalized target/operation/scope where structurally explicit. Exact normalized predicates merge. Very close textual variants merge only with preserved critical paths, fields, statuses and numeric constraints. Nonidentical actor, resource, operation, precondition or outcome remains separate. Duplicate excess is assigned deterministically to the earliest occurrence, and split into within-file vs across-file as required by the protocol.

## Structural checks

All eight scored roles were present. Every extracted occurrence has one valid original file line and belongs to exactly one semantic class. No occurrence belongs to two classes, no class has zero members, all references point to the uploaded filenames, and the duplicate partition reconciles to the occurrence/class count. Each inspected line/table cell has a recorded classification and all extracted units have at least one occurrence ID.

## Limitations and next phase

This is a fully enumerated **best-effort** extraction, not certified manual semantic atomization. Some subtle paraphrases are intentionally left as separate classes unless the full semantic predicates are defensibly equivalent; the reported duplicate rate is provisional. Class correctness against the PDF and source-atom coverage are not decided here. They require item-level PDF evidence and reciprocal source/generated retrieval in phases 3–5. No TP, TN, FP, FN or coverage percentage is reported in this phase.

## Deliverables

- `02_generated_atoms_final.jsonl` — eligible definitive occurrences, original quotations, physical locations and class assignments.
- `02_generated_classes_final.jsonl` — canonical within-method raw semantic classes and all member occurrence IDs.
- `04_duplicate_classes_final.jsonl` — class-level repetition and within/across-file partition.
- `02_generated_exclusions_final.jsonl` — explicitly excluded nondefinitive source units.
- `02_line_cell_coverage_final.jsonl` — physical-line and table-cell inspection register, including structural units.
- `02_reciprocal_lookup_keys_final.jsonl` and `02_reciprocal_key_to_classes_final.json` — bidirectional retrieval aids for phase 3.
- `09_excluded_units.jsonl` — phase-1 PDF exclusions and phase-2 excluded generated units.
- `02_phase2_status.json` — machine-readable completeness, counts, assumptions and limitations.

## Reproducible validation

- `extract_generated_phase2.py` — deterministic, best-effort extraction and clustering procedure.
- `validate_phase2.py` — independent line/cell locator, complete-input, class membership and duplicate-arithmetic validation. The validator passed for this delivery.
