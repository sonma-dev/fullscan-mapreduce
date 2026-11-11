# Phase 3 — Source Requirement Coverage and Reciprocal FN Challenge

**Status:** `PHASE_COMPLETED_BEST_EFFORT`. **Phase 3 closed; Phase 4 not started.**

## Fixed source and generated inventories

- Source-positive PDF atoms: **1,024** (`R`), unchanged from the byte-identical fullload_cal source ledger.
- Source-negative bounded controls: **37** (`N`), unchanged and reserved for Phase 4 assertion classification.
- Definitive generated occurrences: **3,810**; semantic classes: **3,675**, including 18 corrected definitive exclusions identified during reciprocal review. The original Phase 2 files were not overwritten.
- All **1,024** source atoms have an actual evidence row and a provisional TP/FN coverage judgment.
- Provisional full-entailment decisions: **809 TP** (not independently certified).
- Provisional source atoms lacking a demonstrated complete entailment: **215 FN** (not certified absence).
- Non-direct/contextual bridge rows: **794**.
- Reciprocal FN-challenge rows: **630**, including **415** initially missed by lexical-only retrieval and corrected to source-complete provisional TP.

**Caution:** These Phase 3 intermediate TP/FN counts are *not* final Recall, and no four-cell scores, Precision, Recall, F1 or Duplicate were computed. This result is a machine-assisted evidence-backed approximation, not independently verified semantic coverage.

## Evidence and applicability method

1. Restore source predicates from the original PDF-positive atoms and their physical-page quotations.
2. Retrieve generated occurrences via independent word/character n-grams and uncapped exact API/path/event/field/code indexes.
3. Reconstruct inherited Markdown table rows, headings, and full cell statements from each original actual input file.
4. Check direct meaning matches and explicit universal rules, with named route/event/field/category membership where applicable.
5. Where candidates jointly describe a source rule, test an explicitly traceable limited conjunction; never synthesize an unselected role, timing, production status, or business predicate.
6. Check each provisional non-entailment in both directions, capture strongest actual candidates with line/table-cell locators, and document unmet logical conditions.
7. Retain the original generated occurrence/class counts even when one universal generated claim proves several independent source requirements.

The evidence ledgers record direct (`E3`) and bridge-based (`E2`) decisions along with source/target/action/actor/scope/timing/condition/exception/outcome/version checks. This class-level checklist is not proof of an independent full human semantic review; treat borderline matches as correction candidates.

## FN challenge outcomes

| Disposition | Count | Interpretation |
|---|---:|---|
| `TRUE_MISSING` | 0 | No sufficiently close definitive generated assertion found by exact + semantic retrieval; not certified exhaustive absence |
| `PARTIAL_ENTAILMENT` | 117 | Closely related definite content but complete source predicates not demonstrably entailed |
| `CONSERVATIVE_UNRESOLVED` | 98 | Partial or ambiguous accessible evidence; conservatively left uncovered |
| `MATCHER_FALSE_NEGATIVE_CORRECTED` | 415 | Initial lexical-only misses were corrected by genuine source-scoped candidate evidence and explicit universal/table bridges |
| `SOURCE_ATOMIZATION_ERROR_CORRECTED` | 0 | Phase 1 source inventory intentionally kept fixed; separate possible atomization issues are reserved for source-wide review |

Every FN row has at least one real generated candidate, actual file name and line, original phrase, reconstructed table row when applicable, source-specific exact keys, and an explanation of why complete entailment was not established. FN labels with `E1`/`E0` are provisional coverage decisions, not allegations of absent product behavior.

## Core source-specific probes

The matching procedure checks case metadata title/context, workspace retention class, same-key case idempotency, explicit API method/path and scope/status, physical data fields/types/nullability, event producers/consumers, shared interface preallocation validation, generated registered-event guarantees, and specified lifecycle state catalogs. These probes are ordinary source-derived retrieval diagnostics; they do not force any TP score.

## Structural reconciliation

| Invariant | Result |
|---|---|
| One coverage decision per `PDF-*` source atom | **PASS** (1,024 unique) |
| `TP + FN = |R|` | **PASS** (809 + 215 = 1,024) |
| Non-direct TP has original generated and PDF quotations | **PASS** (794 bridge records) |
| Every final FN has a reciprocal search audit | **PASS** (215 records, plus 415 corrected lexical misses) |
| All eight Markdown source files used without modification | **PASS** |
| Existing original source/negative IDs reused without rewriting | **PASS** |
| Generated-only unsupported propositions `F_m` adjudicated | **NOT IN PHASE 3** |
| Negative control assertion `B_m` adjudicated | **NOT IN PHASE 3** |
| Four-cell universe finalized | **NOT IN PHASE 3** |
| Independent human evidence certification | **NOT CLAIMED** |

## Deliverables

- `03_evidence_matches_final.jsonl`: source-by-source current coverage decisions with original PDF/generated evidence and grades.
- `03_semantic_coverage_bridges_final.jsonl`: all non-direct provisional TP proof records.
- `03_fn_root_cause_audit_final.jsonl`: every provisional FN, opposite-direction candidates, and final bounded disposition for this phase.
- `03_recovered_definitive_occurrences_final.jsonl` and `03_phase2_eligibility_corrections.jsonl`: narrowly reclassified definitive generated content from Phase 2 exclusions, with original location and source support.
- `03_tp_predicate_checks_draft.jsonl`: the complete provisional TP evidence/predicate audit, for mandatory Phase 5 re-review.
- `03_canonical_universe_final.jsonl`: Phase-3 source-positive decisions and negative-control placeholders (generated-only FP units added in Phase 4).
- `03_phase_status_final.json`: phase gate and validation summary.

**Phase gate:** Complete as best effort. Do not advance to Phase 4 in this turn. In the designated Phase 5 correction pass, verify TP predicates, challenge E1/E0 FN, correct demonstrated matcher misses, and apply any source atomization corrections consistently across methods.
