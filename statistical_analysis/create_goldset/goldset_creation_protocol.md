# OrionDesk AI — Global-and-Shard Gold Set Creation Protocol

**Version:** 3.0  
**Purpose:** Construct one PDF-grounded positive Gold Set (`R`) and one bounded negative-control set (`N`).  
**Source:** Original *OrionDesk AI Detailed Application Design Specification* PDF.  
**Method:** One global extraction, 29 isolated shard extractions (up to two per phase), immediate incremental reconciliation, one targeted audit, and one final freeze.  
**Artifact language:** English.

## 1. Core rules

1. **PDF authority.** Use only the original PDF to establish requirements. Exclude generated specifications, historical Gold Sets, prior scores, and preferred atom totals.
2. **Two extraction views.** The global pass sees the entire PDF. Each shard pass extracts only its assigned pages without access to global or other-shard candidates **until its extraction is saved**. Within a two-shard phase, lock both independent extractions before reconciling either; then integrate the two shards in order. Use a clean task/context for each shard where possible; otherwise disclose the isolation limitation. Do not claim independent model judgments merely because results were written to separate files.
3. **Meaningful atomicity.** Score one independently meaningful normative obligation, not every sentence, field, endpoint mention, or repeated test. Preserve all mandatory constituent fields, constraints, conditions, exceptions, and outcomes within the appropriate atom. Split only where a distinct obligation would otherwise be lost.
4. **Cross-document scope.** A proven universal rule is one atom; its applications are locators, not extra atoms. Keep distinct endpoint-specific, security, timing, error, or lifecycle obligations separate. Repeated acceptance tests are evidence, unless a separate verification duty is explicitly required.
5. **Negative controls.** Derive `N` only from explicit prohibitions, exclusions, or deferrals; preserve polarity and scope. Do not invent controls from silence or `TBD`.
6. **Evidence first.** Every accepted atom/control must have an actual PDF physical page and a short exact quote or precisely located visual evidence. Restore section, table-row/column, and figure context when needed.
7. **Best effort, bounded work.** Use indexes and focused semantic checks. Do not perform all-pairs semantic comparisons or repeatedly reread the entire PDF. Record material uncertainty instead of fabricating certainty.
8. **Immutable phase outputs.** Once a phase is complete, do not rewrite it. Carry later corrections as deltas. Do not calculate TP, TN, FP, FN, Precision, Recall, or F1 during Gold Set creation.

## 2. Fixed PDF partition

Verify PDF identity, SHA-256, physical page count, and boundaries in Phase 01. Expected source: 90 physical pages.

| Shard | Content | Physical pages |
|---|---|---|
| S01 | Front matter | 1–7 |
| S02 | Chapter 1 | 8–10 |
| S03 | Chapter 2 | 11–14 |
| S04 | Chapter 3 | 15–17 |
| S05 | Chapter 4 | 18–20 |
| S06 | Chapter 5 | 21–23 |
| S07 | Chapter 6 | 24–26 |
| S08 | Chapter 7 | 27–29 |
| S09 | Chapter 8 | 30–33 |
| S10 | Chapter 9 | 34–36 |
| S11 | Chapter 10 | 37–39 |
| S12 | Chapter 11 | 40–43 |
| S13 | Chapter 12 | 44–47 |
| S14 | Chapter 13 | 48–50 |
| S15 | Chapter 14 | 51–53 |
| S16 | Chapter 15 | 54–56 |
| S17 | Chapter 16 | 57–60 |
| S18 | Chapter 17 | 61–63 |
| S19 | Chapter 18 | 64–67 |
| S20 | Chapter 19 | 68–70 |
| S21 | Chapter 20 | 71–73 |
| S22 | Chapter 21 | 74–77 |
| S23 | Chapter 22 | 78–81 |
| S24 | Appendix A | 82–84 |
| S25 | Appendix B | 85–86 |
| S26 | Appendix C | 87 |
| S27 | Appendix D | 88 |
| S28 | Appendix E | 89 |
| S29 | Appendix F | 90 |

Each physical page belongs to exactly one shard. Inspect applicable tables, figures, captions, and appendices. If boundaries differ materially, stop and record the mismatch; do not silently repartition.

## 3. Eighteen phases

| Phase | Work package | Required artifact |
|---|---|---|
| **01 — Global extraction** | Verify source/partition. Extract provisional positives and controls from the **whole PDF**; record coverage and limits, then lock. | `01_global.jsonl` |
| **02 — S01–S02** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `02_shards_01_02.jsonl` |
| **03 — S03–S04** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `03_shards_03_04.jsonl` |
| **04 — S05–S06** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `04_shards_05_06.jsonl` |
| **05 — S07–S08** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `05_shards_07_08.jsonl` |
| **06 — S09–S10** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `06_shards_09_10.jsonl` |
| **07 — S11–S12** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `07_shards_11_12.jsonl` |
| **08 — S13–S14** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `08_shards_13_14.jsonl` |
| **09 — S15–S16** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `09_shards_15_16.jsonl` |
| **10 — S17–S18** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `10_shards_17_18.jsonl` |
| **11 — S19–S20** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `11_shards_19_20.jsonl` |
| **12 — S21–S22** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `12_shards_21_22.jsonl` |
| **13 — S23–S24** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `13_shards_23_24.jsonl` |
| **14 — S25–S26** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `14_shards_25_26.jsonl` |
| **15 — S27–S28** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `15_shards_27_28.jsonl` |
| **16 — S29** | Extract and lock each assigned shard independently; reconcile in ascending shard order. | `16_shard_29.jsonl` |
| **17 — Targeted audit** | Check cross-shard duplicates, over-merges, universal scope, test repetition, controls, and priority uncertainties; record deltas without full re-integration. | `17_audit.jsonl` |
| **18 — Freeze** | Reconstruct from ordered deltas; validate source evidence, IDs, lineage, coverage, and hashes; freeze the paired reference and disclose limitations. | `common_atomic_reqs.jsonl`, `common_negative_controls.jsonl`, `reference_freeze.json` |

For Phases 02–15, finish **both shards and their reconciliations within the same phase**; Phase 16 contains S29 alone. Execute phases in order. Do not advance while required pages, candidates, or reconciliations remain unprocessed. A genuine processing limit requires a resumable incomplete status, not fabricated completion. Artifacts produced under the former six-shard partition are incompatible and must not be reused; restart at Phase 01.

## 4. Extraction and incremental reconciliation

### 4.1 Extract first, integrate second

For each Phase 02–16:

1. Extract candidates using **only each assigned shard's pages**. Save and lock all assigned shards' `SHARD_ATOM` and `SHARD_CONTROL` records **separately before any integration**. Use clean contexts where feasible; otherwise disclose isolation limits.
2. Reconcile the locked shards one by one in shard order. For each, load the current inventory from `01_global.jsonl`, prior phase deltas, and earlier deltas from this phase. Build or reuse indexes of identifiers, API methods/paths, data fields, events, actors, actions, rule families, conditions, and exact numbers.
3. Retrieve a small set of plausible existing candidates for **each new shard candidate**; always include exact identifier collisions and relevant universal/exception rules even if they fall outside a similarity ranking. Never compare every atom against every other atom.
4. Judge equivalence and applicability against real PDF evidence. Use one focused candidate expansion when a material ambiguity remains. Record one disposition for every shard candidate:
   - `MERGE_EQUIVALENT`: same complete obligation; preserve additional evidence.
   - `ATTACH_APPLICATION`: already covered by a proven broader rule; preserve scope/application evidence.
   - `ATTACH_MEMBER_OR_TEST`: constituent contract detail or nonindependent test evidence; preserve all required predicates.
   - `ADD_DISTINCT`: independently normative obligation absent from the working inventory.
   - `EXCLUDE`: nonnormative, unsupported, or repeated non-scoring statement.
   - `REVIEW_FLAG`: unresolved substantive distinction; retain the candidate and source location for Phase 17 rather than silently dropping it.
5. Append `DELTA` rows for additions, merges, source-locator additions, corrections, and control changes. Update temporary indexes. Do not rewrite earlier phase files.

**Do not merge merely related claims.** Different actors, actions, conditions, versions, exceptions, statuses, or outcomes usually imply different obligations. A specific rule does not become identical to a universal rule merely because the universal rule applies to it. A shard-only claim is not automatically accepted, and a global-only claim is not automatically rejected.

### 4.2 Prevent quadratic comparison

Search is **new shard candidates → indexed existing inventory**, not every pair of global and shard items. Use deterministic blocking and a few semantically plausible neighbors. Cache resolved family rules and source evidence. Compare other families only when a real shared identifier, scope dependency, contradiction, or collision signal exists.

Phase 17 may perform **up to 60 prioritized groups and 20 reproducibly sampled groups** of additional semantic review. The count is a fixed audit ceiling, not an adaptive algorithm. Correct all clearly identified dependent records in the affected group; disclose unreviewed residual risk instead of starting an unrestricted global search. An ordinary ambiguity is closed as best effort with a flag and rationale.

## 5. Compact record contract

Every JSONL row has `record_type` and an identifier. Use concise English text, short source excerpts, and resolvable references instead of repeated narratives.

- `GLOBAL_ATOM` / `SHARD_ATOM`: `candidate_id`, `statement_en`, `scope`, `required_predicates` (including required members and exceptions), `pdf_evidence` (physical page and quote/visual locator), `review_flags`.
- `GLOBAL_CONTROL` / `SHARD_CONTROL`: `candidate_id`, `counterfactual_en`, `construction_basis`, `scope`, `pdf_evidence`, `review_flags`.
- `PAGE_COVERAGE`: `pages`, inspected sections/tables/figures, unresolved regions, source issues. Record coverage separately for each shard (or one logical range for the global pass).
- `DISPOSITION`: `candidate_id`, `decision`, `target_working_id` or `null`, short `reason_en`, supporting PDF or indexed-candidate locator. Exactly one final disposition per shard candidate.
- `DELTA`: `delta_id`, `operation`, affected candidate/working IDs, source evidence, and changed predicates or links. Keep stable working IDs; record aliases rather than renumbering earlier records.
- `AUDIT_CHANGE`: prior/new status, affected IDs, evidence and reason; preserve earlier decisions.
- `PHASE_SUMMARY`: input counts, extracted/reconciled counts, inspected pages, open flags, and `status`.

`01_global.jsonl` contains global candidates, page coverage, the verified shard partition and a summary. Each Phase 02–16 artifact contains **all assigned shards' locked local candidates first**, then shard-ordered dispositions and deltas, coverage by shard, and a phase summary with per-shard counts. `17_audit.jsonl` contains reviewed groups, changes and a summary. The combined artifacts replace separate manifests, family registries, individual search logs and lengthy reports. Temporary retrieval indexes are not deliverables.

## 6. Final reference and validation

At Phase 18, apply Phases 02–16 deltas in shard order, followed by Phase 17 corrections. Produce unique, stable final `PDF-*` and `NEG-*` IDs, ordered by original source location; retain all originating candidate IDs and any aliases. Keep complete contractual predicates when consolidating atoms.

Required mechanical checks:

```text
original_pdf_sha256_consistent = true
all_physical_pages_accounted_for = true
twenty_nine_shards_cover_each_page_once = true
all_global_and_shard_candidate_ids_unique = true
each_shard_candidate_has_one_disposition = true
all_deltas_resolve_to_known_ids = true
all_final_positive_and_negative_ids_unique = true
all_final_items_have_actual_pdf_evidence = true
all_final_items_have_candidate_lineage = true
all_unresolved_items_and_isolation_limits_disclosed = true
```

Publish `common_atomic_reqs.jsonl` (positive atoms, `actual_label: 1`) and `common_negative_controls.jsonl` (explicit PDF-derived counterfactual controls, `actual_label: 0`). In `reference_freeze.json`, record protocol version `3.0`, PDF and reference SHA-256 digests, physical pages, shard boundaries, candidate/final counts, audit counts, remaining limitations and one honest status:

- `REFERENCE_FROZEN_VERIFIED`: all material source, semantic and evidence issues genuinely resolved.
- `REFERENCE_FROZEN_PROVISIONAL`: usable reference with disclosed unresolved issues or limited review/isolation.
- `REFERENCE_BLOCKED`: mandatory source material or required phase data unavailable or structurally incomplete.

Passing mechanical checks alone does not prove semantic completeness. Do not claim an independent reviewer was used unless one actually was.

**Final rule:** Extract globally once; independently extract and lock up to two shards per phase, then reconcile each in order against an indexed working inventory; perform only a bounded final collision audit; freeze one auditable positive/negative reference pair. Favor finished, evidence-backed best-effort work over repeated exhaustive comparison, without concealing missing inputs or unresolved source obligations.
