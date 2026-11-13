# Phase 3 — Semantic PDF-to-Generated Coverage (Best Effort)

**Protocol:** v6.1. **Stage:** Phase 3 only. **Status:** PHASE_COMPLETED_BEST_EFFORT.

## Scope

- Original PDF source-positive atoms: 1024 (unchanged).
- Fixed source-negative controls: 37 (unchanged; unscored until Phase 4).
- Definitive generated occurrences: 2516.
- Raw generated semantic classes: 2437.
- Eight scored Markdown documents; all physical lines and tabular cells were available in Phase 2.
- Phase 3 PDF-positive coverage: **TP=895**, **FN=129** (provisional; not a full four-cell confusion matrix).
- Non-direct coverage bridges with explicit evidence: 882.
- Initial FN proposals receiving reciprocal generated-corpus challenge: 565.

## FN root-cause dispositions

| Final disposition | Count |
|---|---:|
| CONSERVATIVE_UNRESOLVED | 28 |
| PARTIAL_ENTAILMENT | 64 |
| TRUE_MISSING | 37 |

## Method and evidence

Each source-positive unit has a genuine physical-page quotation, a candidate search, and a final TP/FN record. Direct tests inspect exact methods, paths, actors, API statuses, table row/column inheritance, relational fields, event schemas, model/tool constraints, and acceptance scenarios. Cross-document and universal/shared rules use separate evidence locators and identify the membership bridge. Corpus-wide candidate retrieval combines word-level and character-level TF-IDF, exact structural identifiers, row context and reverse class/line checks. Each final FN has a separately retained root-cause record and the strongest actual generated quotations/locators. The record distinguishes lack of matching text from overlap missing a required predicate.

## Reliability boundaries

**These counts are BEST_EFFORT, not a verified semantic recall measurement.** The matching procedure is deterministic and extensive, but is not a human or model-expert proof of every predicate. Rule-level bridges and prose paraphrases require further adversarial review; linked evidentiary records preserve the exact words and locations for that review. In particular, the independently frozen source atomicity and the generated Phase 2 segmentation remain potential sources of false FN and false TP. The pending negative controls and generated-only unsupported assertions are not guessed as TN/FP.

A high score is not a certificate of implementation quality, and a low score does not demonstrate that the generated specifications genuinely lack those requirements. Phase 4 evaluates raw-generated-class validity and completes the four-cell universe; Phase 5 rechecks FN root causes, all TP proofs, atomization, and duplicate metrics. No Phase 4 work was performed here.

## Mandatory reciprocal FN challenge results

All 565 initially FN-nominated source atoms received additional full-physical-line retrieval across the eight inputs. At the first reciprocal-search checkpoint, **130 were corrected to TP** (80 specific source-line adjudications and 50 high-content-overlap corrections), leaving 435 provisional FN at that intermediate checkpoint. Subsequent context and exact-table challenges corrected additional candidates; the final Phase 3 results are stated above. The initial and corrected decisions, actual candidate line quotations, method/path/code and source-predicate exclusions are retained in `03_fn_root_cause_audit_final.jsonl`, `03_reciprocal_search_audit_final.jsonl` and `03_reciprocal_change_delta.jsonl`.

These corrections are supported by actual source lines; however, a high lexical overlap or a curated same-domain quote does not itself certify full semantic entailment. The remaining **12 curated proposals were not promoted** because the necessary exact constraints, conditions or definitive status were not established. Verification remains Phase 5's independent obligation.

## Subsequent explicit-line audit and source normalization repair

A targeted source-table and document-specific reciprocal review reclassified **160 additional initial FN** records as TP, using real original-file line quotations. **45 candidate corrections were not promoted**, because an exact named state, scope, code, property, or eligible occurrence was not established. Source-to-generated evidence remains subject to independent complete-predicate review.

Two source atoms (`PDF-00192`, `PDF-00193`) originally recorded a truncated `/v1/workspaces/{workspaceId}/me` path. The original PDF p.23 register line wraps the last four letters of *members*; independent text in p.23 §5.3.1 gives `PUT /v1/workspaces/{workspaceId}/members`. The **same IDs and underlying PDF quoted evidence** were retained while the normalized statements were corrected to `/members` for every method. This changes the R ledger bytes compared with the original fullload source copy but does not change cardinality. The transparent two-row delta is `03_source_atom_corrections_final.jsonl`; this correction is not a method-specific denominator change.

## Reciprocal register / original short-cell challenge

A final source-to-generated/category-to-source retrieval challenge established **113 further positive coverage mappings**, including **110** PDF source register obligations. In each register case, the same 03_data.md category-wide invariant at L63 was instantiated for a specifically identified subject in the 22-row source register. One generated category rule legitimately supports several source atoms without replicating occurrences. This is not an assertion that every listed logical register subject has a physical table.

**Generated atomization limitation:** 112 evidence uses bare table subjects/short cells that were missing from the earlier Phase-2 occurrence ledger; exact rows and source IDs are retained in `03_generated_segmentation_gap_audit.jsonl`. The explicit Markdown text supports the *source-coverage projection*, but those missing raw semantic occurrences/classes are not silently inserted into Phase 2. They require the independent Phase-5 atomization and duplicate-class audit. The 0 other examined rows not promoted remain conservative.

## Final exact semantic-reciprocal challenge (no new phase)

An additional **30** source-positive FN candidates were corrected using original generated-scored Markdown lines, exact table scope, and, for registered events, a literal global rule with explicit event-class membership. Examples include the `GET /v1/me` API inventory, DAT-006 case metadata, API-053 event envelope and log/audit requirements, the `CaseCreated` event consumer, `knowledge.search@v1` typed cells, explicit TST acceptance rows, and incident-runbook steps. The underlying Phase 2 extracted GO/GCLASS ledgers were not modified; 126 original short-cell references are retained as a generated atomization exception list for Phase 5.

These coverage bridges are **BEST_EFFORT**, not individually certified semantic proofs. The A2A illustrative fields, error example schema and incomplete cross-cutting verification universals remain conservatively assessed unless exact definitive commitments prove their full predicate. TP/FN here are coverage diagnostics only; no TP/FP/TN/FN four-cell metrics have been computed in Phase 3.

Further three exact-source-line/eligible-class matches were corrected, including the formal GET /v1/me reference, TST-010 review-expiry acceptance, and complete incident-documentation runbook step.

## Final structural consistency check

The independently executable `verify_phase3.py` passes: 1,024 unique PDF-positive IDs, 37 frozen and unscored controls, 2,516 unchanged generated occurrences, 2,437 unchanged raw generated classes, 1,061 draft canonical rows (895 TP, 129 FN, 37 Phase-4-pending negative controls), 565 initial FN challenge records, 436 corrected initial FN cases, 882 non-direct TP bridges, and 1,322 matching generated-evidence line locators. There were two documented normalizations of PDF API path wrapping and 126 source-to-generated short-cell extraction-gap records. The raw class catalog is unchanged; some raw original table cells are used in source-coverage conjunctions and remain flagged for Phase-5 generated atomization audit.

**Structural PASS is not semantic certification.** The labels remain `PHASE_COMPLETED_BEST_EFFORT`; Phase 4 alone will decide the FP and TN cells. Neither Precision, Recall, F1 nor duplicate metrics are finalized here.
