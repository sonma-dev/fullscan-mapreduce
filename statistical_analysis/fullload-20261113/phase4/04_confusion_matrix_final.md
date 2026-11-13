# OrionDesk AI — Phase 4 Canonical Four-Cell Evaluation

**Protocol:** 6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method:** `provided_eight_documents`  
**Stage limitation:** Phase 4 only; Phase 5 corrections and Phase 6 independent certification have not run.

## Shared universes

| Inventory | Enumerated count |
|---|---:|
| PDF-positive `R` | 1,024 |
| Fixed PDF-negative `N` | 37 |
| Eligible generated occurrences `GO` (inherited) | 2,672 |
| Raw generated classes `G` (inherited) | 2,624 |
| Canonical distinct unsupported generated propositions `F` (provisional) | 915 |
| Asserted PDF-negative controls `B` | 0 |
| Effective canonical decision universe `U = R ⊔ N ⊔ F` | 1,976 |

## Four-cell matrix

| | Predicted positive | Predicted negative |
|---|---:|---:|
| PDF-positive (actual 1) | **TP 621** | **FN 403** |
| PDF-nonpositive (actual 0) | **FP 915** | **TN 37** |

| Metric | Calculation | Value |
|---|---|---:|
| Precision | `621 / (621 + 915)` | **40.43%** |
| Recall | `621 / (621 + 403)` | **60.64%** |
| F1 | `2 × 621 / (2 × 621 + 915 + 403)` | **48.52%** |
| Raw duplicate rate (not four-cell score) | `(2672 - 2624) / 2672` | 1.80% |

## Generated class validity

| Reciprocal PDF support finding | Classes |
|---|---:|
| `PDF_ENTAILED` (provisional, includes preexisting source-TP witnesses) | 895 |
| `SUPPORTED_NONCOVERING` (source-grounded subclaims requiring Phase-5 challenge) | 814 |
| `PDF_UNSUPPORTED` (canonicalized as provisional F) | 915 |

## Structural equations

- `TP + FN = 621 + 403 = 1024 = |R|`.
- `TN + |B| = 37 + 0 = 37 = |N|`.
- `FP - |B| = 915 - 0 = 915 = |F|`.
- `TP + TN + FP + FN = 1976 = |U|`.
- `TP + FP = 1536 = |P|`, **not** `|G|=2624`.
- `|GO|=2672 ≥ |G|=2624`; raw excess duplicates = 48.

## Interpretation and unresolved semantic risk

The matrix is reproducible from each item of the effective canonical universe. A shared universal generated commitment can support several independent source atoms without being duplicated in the raw class inventory. `TN` consists only of the 37 independently fixed explicit PDF prohibition/deferral counterfactual controls; it is not the total number of unmentioned features.

**Semantic certification is not claimed.** The PDF support classification uses original PDF text fragments, inherited tabular context, exact identifiers, semantic equivalence checks, and bounded candidate retrieval. A number of classifications remain machine-assisted conservative best-effort judgments, including the generated-only unsupported residuals. Source-side TP bridges and all provisional generated class validity outcomes require independent full-predicate review in Phase 5. `SUPPORTED_NONCOVERING` records include evidence and a stated rationale but remain subject to that audit. No changes to the scored Markdown, source-positive R, or predeclared N were made.

Phase 3 preserved 111 `TRUE_MISSING`, 79 `PARTIAL_ENTAILMENT`, and 213 `CONSERVATIVE_UNRESOLVED` source-positive FN judgments. These do not represent 403 certified missing requirements. Phase 3 also corrected 196 provisional matcher false negatives. Phase 4 inherits those decisions rather than silently certifying them.

## Deliverable index

- `04_generated_claim_validity_final.jsonl`: all generated classes with actual PDF and Markdown evidence, support/unsupported category, candidate-check result and follow-up status.
- `04_unsupported_generated_propositions_final.jsonl`: canonical unsupported F proposals and their generation sources.
- `04_negative_control_assertion_audit_final.jsonl`: all 37 fixed counterfactuals with their PDF prohibitions and real generated mentions.
- `03_canonical_universe_final.jsonl`: complete R ⊔ N ⊔ F.
- `04_atomic_judgments_final.jsonl`: exactly one actual/predicted/TP-TN-FP-FN judgment for each canonical unit.
- `04_confusion_matrix_final.json`: machine-readable arithmetic and limitations.
- `04_phase_status_final.json`: Phase-4 completion state.
