# OrionDesk AI — Phase 3 Completion Report

**Protocol:** v6.1  
**Phase:** 3 — Complete source-side semantic coverage and reciprocal FN challenge  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`

## Preserved source scope

The user-supplied PDF-positive inventory contains **1,024** items, and the PDF-grounded negative controls contain **37** items. The inventories are unchanged. The Phase 2 ledger contains **3,909** occurrences and **3,818** classes across eight supplied Markdown inputs. The method is recorded as a single supplied set rather than inferring a production method from copy suffixes.

## Source-side provisional coverage

| Result | Count |
|---|---:|
| TP | 582 |
| FN | 442 |
| Source-positive denominator | 1,024 |
| Provisional source-only Recall | 56.84% |
| E3 | 286 |
| E2 (bridged TP) | 296 |
| E1 (partial/noncovering) | 422 |
| E0 (no complete match) | 20 |

No final TN, FP, Precision or F1 are reported here: the negative-control assertion test and generated-only validity review belong to Phase 4. A provisional source-only Recall is not certified semantic coverage.

## Reciprocal FN challenge

Every initially uncovered source claim was searched against the eligible generated occurrences and the entire original eight-file corpus through lexical and character ngram retrieval, exact method/path and named-identifier reverse lookup, table-row/header reconstruction and multi-file conjunction checks. Each resulting FN has its strongest actual candidate quotations and the specific unproven content predicates in `03_fn_root_cause_audit_final.jsonl`.

| Disposition | Count |
|---|---:|
| `TRUE_MISSING` | 20 |
| `PARTIAL_ENTAILMENT` | 303 |
| `CONSERVATIVE_UNRESOLVED` | 119 |
| `MATCHER_FALSE_NEGATIVE_CORRECTED` | 320 |


## Provenance and limitations

- **296** source positives use an E2 contextual/universal/conjunctive bridge, with original generated file/line citations and a stated membership proof.
- **538** TP decisions cite an original Markdown line beyond a Phase 2 occurrence quote; **233** are not yet linked to an eligible Phase 2 `GCLASS`. These are independently identifiable extraction/traceability issues for subsequent phase review, **not** invented witnesses.
- **726** raw generated classes were shortlisted for possible generated-only claim scrutiny; none is automatically an FP because a source match was not identified.
- The original PDF source evidence references are reused from the verified attached ledger. Known atomization watchlist items remain open for the designated Phase 5 audit. No source denominator was changed.
- These judgments include heuristic, bounded semantic approximations. Structural evidence locators were checked, but the proofs were not individually certified by a human semantic reviewer. Source polarity, conditions, actor, and complete outcome may still be imperfectly aligned; even E3/E2 entries remain subject to the independent Phase 5 audit. Do not treat this as `FINAL_VERIFIED`.

## Individual deliverables

- `03_canonical_universe_final.jsonl` — draft `R ∪ N` skeleton, with N explicitly unscored.
- `03_evidence_matches_final.jsonl` — all 1,024 source judgments, source and generated quotations, grades, and predicate-check rationale.
- `03_semantic_coverage_bridges_final.jsonl` — itemized E2 bridges.
- `03_fn_root_cause_audit_final.jsonl` — all provisional FN root-cause challenge records, with true/partial/conservative distinctions and any corrected misses.
- `03_potential_unsupported_generated_claims.jsonl` — unscored shortlist for Phase 4.
- `03_phase3_validation_summary.json` — reconciliation and limitations.

**Phase boundary:** This phase is closed; Phase 4 has not started.

## Phase 3 reciprocal correction pass

A second pass inspected direct semantic paraphrases, source-named API/table fields, named events with shared event rules, and universal scope membership. Previously missed complete matches were changed from FN to TP and recorded in `03_fn_root_cause_audit_final.jsonl` as `MATCHER_FALSE_NEGATIVE_CORRECTED`. The result remains best effort, not semantically verified.

## Final direct-match regression audit

The final same-phase audit corrected 20 additional explicit source matches, including case title, workspace RLS, append-only schema versioning, event payload, and the idempotent case-creation test. Individual corrections and original line citations are recorded in `03_direct_match_regression_corrections.jsonl`. No Phase 4 negative-control or generated-only assertion evaluation was performed.
