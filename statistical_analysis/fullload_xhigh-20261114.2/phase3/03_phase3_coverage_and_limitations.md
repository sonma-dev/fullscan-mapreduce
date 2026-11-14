# Phase 3: Semantic Source Coverage and Reciprocal False-Negative Audit

**Protocol:** OrionDesk Six-Turn Atomic Requirement Evaluation v6.1  
**Completion status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method:** Unlabeled, single eight-document supplied corpus  
**Current phase:** Phase 3 only. Four-cell generated correctness is reserved for Phase 4.

## Source and generated inputs

- PDF: `OrionDesk_AI_Detailed_Design_Specification(2).pdf`; the full 90-page physical original was verified in Phase 1. The source-positive ledger contains **979** unchanged `PDF-*` atoms and the fixed negative-control ledger contains **37** unchanged `NEG-*` records.
- All eight supplied Markdown roles were inspected by the prior Phase 2; this turn used the unchanged files and their exact physical line and table-cell evidence.
- Prior raw generated extraction: **6,742 occurrences / 6,669 classes**.
- Definite short table-cell omissions recovered from original Markdown in this turn: **196 occurrences / 196 provisional singleton classes**. Effective carryforward: **6938 occurrences / 6865 classes**; Phase 2 original files were not overwritten.

## Source coverage decisions (provisional, not a four-cell score)

| Item | Count |
|---|---:|
| Source positive requirements | 979 |
| Provisional complete-entailment TP | 587 |
| Conservative source FN | 392 |
| Initially identified direct TP | 197 |
| Initial FN candidates re-challenged | 782 |
| Corrected initial false negatives | 390 |
| Full non-direct bridge records | 436 |
| Source negative controls still awaiting Phase 4 generated-assertion check | 37 |

*These are item-level working classifications, not Precision, Recall or F1. The complete canonical four-cell universe cannot be scored until generated-only unsupported propositions and asserted negative controls are audited in Phase 4.*

### Current unentailed-source classifications

| Reciprocal FN disposition | Count |
|---|---:|
| `TRUE_MISSING` | 5 |
| `PARTIAL_ENTAILMENT` | 245 |
| `CONSERVATIVE_UNRESOLVED` | 142 |

The `TRUE_MISSING` disposition is based on bounded reciprocal candidate search, not exhaustive human proof of absence. `PARTIAL_ENTAILMENT` means at least one material source predicate is not demonstrated by the closest eligible generated assertion. `CONSERVATIVE_UNRESOLVED` explicitly preserves uncertain matches rather than asserting absence.

## Semantic method and correction policy

1. Read PDF-positive source propositions and their exact physical-page citations. Keep the Phase 1 source denominator fixed.
2. Reopen every source Markdown role and consume all Phase 2 classes and original line/cell locators. Use word/character indexes, exact method/path, event/field identifiers, shared-rule queries, and multi-cell row reconstruction.
3. Attempt direct equivalent entailment. Require applicable scope, polarity and materially explicit numeric/time/status predicates; named API and field rows are interpreted within their table heading and row key.
4. For provisional FN, challenge source-to-generated retrieval using reverse class/target lookup and source table-cell reconstruction, inherited context, universal instantiation, and limited conjunctive bridges. Record strongest actual evidence and the missing predicates for remaining FN.
5. Correct known false negatives in the current phase. This turn rescued dropped table-cell commitments rather than treating their extraction omission as genuine source requirements missing from the generated corpus. All recoveries have exact original file and physical line evidence in `03_generated_recovered_class_and_occurrence_addendum.jsonl`.
6. Record one `03_evidence_matches_final.jsonl` source-atom judgment per `PDF-*` atom; one FN root-cause row for each initially missed atom including those corrected to TP; and one non-direct TP bridge record per non-direct TP.
7. Carry `NEG-*` rows into the draft canonical universe with `PENDING_PHASE_4`; do not label them TN or FP before a generated-assertion audit.

## Audit caveats

- **Structural consistency:** The final source positives reconcile exactly: {current_tp} TP + {len(S)-current_tp} FN = 979; each of 37 negative controls is preserved but not scored. Each non-direct TP has a bridge row, and the Phase 3 additions have unique class/occurrence IDs and genuine Markdown line locators.
- **Semantic evidence:** The source/target comparisons and numeric/polarity tests are reproducible but substantially programmatic. **Zero of the {current_tp} provisional TP records were independently manually audited predicate by predicate.** The non-direct records contain actual supporting citations and working explanations, not a certification.
- **Remaining risk:** Generated assertions can be more specific/narrower than PDF duties; table-cell eligibility and conjunction boundaries may need correction. The 408 conservative FN decisions must not be represented as verified omissions. The original Phase 1 denominator also remains subject to the planned Phase 5 source-atomization challenge.
- **Phase boundaries:** Unsupported generated claims, exact negative-control assertion matching, `FP`, `TN`, and four-cell metrics are not Phase 3 outputs. Do not infer final Precision/Recall/F1 from these provisional counts.

## Individual output files

- `03_canonical_universe_final.jsonl` — draft source-positive and fixed-negative canonical rows.
- `03_evidence_matches_final.jsonl` — one predicate/evidence judgment per source-positive atom.
- `03_semantic_coverage_bridges_final.jsonl` — non-direct source coverage bridges.
- `03_fn_root_cause_audit_final.jsonl` — initial-FN reciprocal challenges and final dispositions.
- `03_generated_recovered_class_and_occurrence_addendum.jsonl` — recovered eligible table-cell evidence with exact file locators.
- `03_generated_recovered_classes_final.jsonl` and `03_generated_recovered_occurrences_final.jsonl` — schema-compatible recovered class/occurrence records.
- `03_effective_generated_classes_final.jsonl` and `03_effective_generated_atoms_final.jsonl` — merged original and recovered generated inventories for Phase 4.
- `03_phase3_corrections_final.jsonl` — recovered missed matches with evidence and reasons.
- `03_potential_unsupported_generated_claims.jsonl` — *unadjudicated candidate leads*, not FP findings.
- `03_phase3_validation_final.json` — structural reconciliation and quality limitations.

**Next phase on a new user request:** Phase 4, generated correctness and a single complete four-cell universe.
