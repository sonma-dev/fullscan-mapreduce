# Phase 3 — Semantic Source Coverage and Reciprocal False-Negative Challenge

**Protocol:** 6.1  
**Phase:** 3, completed once.  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method:** One supplied unlabelled eight-file Markdown set.  
**Fixed PDF-positive inventory:** 1024  
**Fixed PDF-negative controls:** 37 (decision deferred to Phase 4).

## Adjudicated source-side decision totals (provisional)

| Measure | Count |
|---|---:|
| Complete-source-predicate TP judged, direct or bridged | 990 |
| Conservative FN judged after reciprocal challenge | 34 |
| Initial strict direct TPs | 96 |
| Initial FN candidates challenged over all eight files | 928 |
| Initial matcher FN corrected to TP with actual proof | 894 |
| Final TRUE_MISSING dispositions | 9 |
| Final PARTIAL_ENTAILMENT dispositions | 9 |
| Final CONSERVATIVE_UNRESOLVED dispositions | 16 |
| Complete source evidence-match rows | 1024 |
| Explicit E2 bridge records | 895 |

**These are source-coverage draft counts, not a four-cell confusion matrix, Recall certification, or final scores.** Negative controls are present in the draft universe but have null predicted labels pending Phase 4. Unsupported generated-only propositions are not yet enumerated.

## Semantic scope and reciprocal retrieval

- Reused the exact Phase 1 PDF source IDs, quotes, pages and negative-control inventory; no method-specific PDF atoms were added.
- The full Phase 2 eligible inventory of 2440 occurrences / 2360 raw classes was searched. A Phase-3 correction ledger adds 18 independently eligible omitted generated claims, resulting in 2458 occurrences / 2378 raw classes for subsequent phases. The original eight unchanged Markdown files were also searched for complete Markdown table rows and their headings, including cells not independently isolated as eligible occurrences.
- Candidate discovery combined word and character n-gram retrieval, preserved API method/path and source-specific statuses, and inspected literal fields, entity/field keys, error/test/event identifiers and generated row contexts. Every final FN retains the strongest accessible actual generated candidate quotes, multiple row alternatives, query keys, a generated-to-source reciprocal-hit indicator, and an explicit disposition.
- Universal sources and inherited context were separately checked: 22 component/contract registers and DAT-004 category invariants, O+I and S+B API tables, registered-event envelope/outbox/log-audit rules, boundary identity fields, canonical event schemas, selected entity catalog fields, physical DDL, source API method/caller/status rows, primary-screen lists and required test outcomes.
- A universal statement is not itself proof for arbitrary target names; each bridge describes explicit class membership and checks the relevant original Markdown row, source-proposition identity and applicable scope. Unsupported choices, unapproved proposals, conflicting alternatives and status-only citations were not treated as authorizing implementation.

## Evidence-quality and remaining uncertainty

| Final TP-evidence category | Count |
|---|---:|
| `EXACT_STRUCTURAL` | 279 |
| `STRUCTURAL_CHECKED` | 257 |
| `BEST_EFFORT_MANUAL_TARGETED` | 181 |
| `BEST_EFFORT_SEMANTIC` | 161 |
| `DIRECT` | 91 |
| `BEST_EFFORT_TABLE_CONTEXT` | 14 |
| `HIGH_STRICT` | 5 |
| `BEST_EFFORT_CONJUNCTION` | 2 |

The extracted source inventory contains compound statements and likely parent/child or verification-overlap issues flagged in Phase 1. No source denominator changes were silently introduced in Phase 3. Corrective source atomization is to be rechecked with evidence in Phase 5.

Some entailments use bounded structural/contextual inference or scored textual similarity with exact target/polarity/numeric guards; these are **best-effort semantic judgments**, not individually human- or model-certified full logical proofs. Similarity by itself cannot certify entitlement. The TP predicate maps and source/Markdown quotations are provided so the Phase 5 independent challenge can downgrade any materially incomplete proof. A source classified `CONSERVATIVE_UNRESOLVED` is not a verified absence. `TRUE_MISSING` is corpus-scoped, not a claim about an implementation.

The original Markdown 8 files and Phase 1/2 canonical inventories are unchanged. Phase 4 will validate all raw generated semantic classes for PDF support, classify B_m and F_m, and finalize a single canonical four-cell universe.

## Outputs

- `03_canonical_universe_final.jsonl`: one positive source decision per PDF atom, plus predeclared negative-control units with explicitly pending prediction labels.
- `03_evidence_matches_final.jsonl`: source-to-generated coverage, actual source and generated evidence, candidate retrieval and predicate checks.
- `03_semantic_coverage_bridges_final.jsonl`: explicit non-direct entailment proofs and target membership.
- `03_fn_root_cause_audit_final.jsonl`: every initial FN candidate, corrected or still FN, with actual reciprocal retrieval evidence and final disposition.
- `07_change_delta.jsonl`: initial matcher false-negative corrections (not a change in PDF requirements).
- `03_phase_status.json`: counts, structural tests and current phase boundary.

## Phase-3 extraction and full-predicate corrections

The original Phase-2 ledgers remain unchanged. This Phase-3 directory contains reconciled copies of `02_generated_atoms_final.jsonl` and `02_generated_classes_final.jsonl`, with 18 recovered definitive clauses at actual original Markdown file/line locations. Each now has a valid `GEN-*` and `GCLASS-*` link and an audit row in `03_generated_extraction_corrections.jsonl`. The corrected raw corpus is 2,458 occurrences / 2,378 classes. These additions were made to repair actionable missed generated commitments, not to alter the scored Markdown.

Two apparent TPs (`PDF-00964`, `PDF-01016`) were downgraded because the cited wording omitted a material part of the source predicate. The illustrative error-envelope rows were already conservatively classified FN rather than treating an example as an adopted universal schema. The full-predicate review remains BEST_EFFORT; automatic text similarity and generic predicate-check flags are not certification.

**Downstream Phase 4 must use the Phase-3 revised generated ledgers and the corrected Phase-3 PDF atom copy, not overwrite them with the older Phase-1/2 snapshots.**
