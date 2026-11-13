# Phase 3 — Semantic Coverage and Reciprocal False-Negative Challenge

## Status and inputs

- **Protocol**: 6.1; **status**: `PHASE_COMPLETED_BEST_EFFORT`.
- Authoritative source: `OrionDesk_AI_Detailed_Design_Specification(8).pdf` (90 physical pages, SHA-256 `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`).
- Preserved PDF-side universe: **1024** positive atoms and **37** bounded negative controls from Phase 1.
- Generated evidence: all **4223** Phase 2 definitive occurrences and **4075** raw semantic classes across eight supplied Markdown files, using actual unchanged filenames and physical lines.
- The source denominator has not been changed in this phase. No previous scoring decisions were imported.

## Draft positive-source decisions (not a final four-cell confusion matrix)

| Source coverage | Count |
|---|---:|
| Full entailment, provisional TP (E2/E3) | 801 |
| Not fully proved, provisional FN (E0/E1) | 223 |
| Positive source atoms | 1024 |
| PDF-negative controls, held for Phase 4 | 37 |

These are **best-effort semantic adjudications**, not independently certified semantic coverage or verified absence. TP evidence and generated-class correctness require Phase 5 review. Do not interpret these as final Precision/Recall/F1 or as proof of absence.

## Mandatory FN challenge

Every source atom initially missed by the strict single-statement matcher has a source-side and candidate-side evidence record, an exact-identifier/alias key list, the best actual Markdown quotations, and a challenge disposition. The recorded dispositions are:

- `MATCHER_FALSE_NEGATIVE_CORRECTED`: **737**
- `SOURCE_ATOMIZATION_ERROR_CORRECTED`: **0**
- `TRUE_MISSING`: **8**
- `PARTIAL_ENTAILMENT`: **97**
- `CONSERVATIVE_UNRESOLVED`: **118**


The two-way search uses sparse word and character indexes for **all** eligible generated assertions, exact field/route/event/status/test identifiers, original row text, literal table-header/row context, explicit shared rules, and cross-file conjunction candidates. Similarity hits alone do not become TP. For every provisional E1/E0 FN, the evidence file identifies a concrete strongest candidate (if any) and records why a complete bridge was not established. Reciprocal search is mechanical and best effort, not a substitute for independent manual adjudication.

## Bridge review

The TP bridge ledger contains **424** source-specific semantic equivalence, inherited-context, universal-instantiation, or conjunctive proofs with genuine file/line/row evidence and predicate checks. Direct unbridged matches remain in the evidence matches file. Register-category membership is identified in **95** review exception records for independent semantic scrutiny.

The source's explicitly prohibited actions, release deferrals, and example-only settings are not promoted from unapproved generated text. Cases with unresolved definitive claims remain conservative. Some Phase 2 occurrence/class eligibility decisions may also change in the Phase 5 full audit; this phase does not silently relabel the eight scored Markdown inputs.

## Phase boundary

`03_canonical_universe_final.jsonl` currently contains 1024 positive source rows with `TP` or `FN` and 37 negative-control rows marked `PENDING_PHASE4_NEGATIVE_CONTROL_CHECK`. Unsupported generated-only canonical units and full TP/TN/FP/FN are **not** invented in Phase 3; they must be added and recomputed in Phase 4. No final metrics are published in this phase.

## Reciprocal correction pass

Corrected **158** initial false negatives by checking actual generated table cells, DDL, chapter-event families, acceptance/security fixtures and meaning-preserving prose. The correction ledger retains each original FN and its real generated line evidence. The source and negative-control inventories are unchanged.

Corrections by source evidence kind:

- `ACCEPTANCE_TEST`: 14
- `API_BEHAVIOR`: 7
- `CROSS_CUTTING_FAILURE`: 3
- `DDL_CHECK_OR_DEFAULT`: 5
- `DDL_FK`: 2
- `DDL_KEY`: 2
- `DDL_NULL`: 7
- `DDL_RLS`: 1
- `DDL_TYPE`: 8
- `DESIGN_GOVERNANCE`: 1
- `EVENT_VERIFICATION`: 22
- `NORMATIVE_INVARIANT`: 7
- `NORMATIVE_PROSE`: 40
- `REGISTER_EVENT`: 28
- `RUNBOOK`: 4
- `SECURITY_NEGATIVE_TEST`: 7

## Final bounded source-context challenge

An additional **81** clear source-context or semantic-equivalence errors were corrected using current generated corpus evidence, bringing total documented corrections to **239**. No score-certified Recall is claimed; 271 E0/E1 source-coverage cases remain conservatively adjudicated for Phase 5 review.

## Direct-match regression closure

48 additional explicit matches were checked and corrected. 7 proposed direct-match candidates were withheld for insufficient complete-predicate proof. This phase does not certify a final Recall or any FP/TN score.

## Final structural checks

- Physical Markdown evidence locators: 1065 direct and 0 markup-normalized quote matches; 0 quotations flagged for additional verification.
- All 960 initial FN challenges have one final disposition and full candidate-search provenance.
- Source-positive decisions: 801 provisional TP, 223 conservative FN (the latter is **not certified absent**).
- Fixed controls held for Phase 4: 37. All 4075 raw generated classes are available in the Phase 4 review queue; unmatched classes are not scored FP by default.
- Source and generated class evidence IDs, line locations, one-universe source counts, and root cause ledgers were mechanically reconciled. No arithmetic or lexical check independently certifies semantic completeness.
