# OrionDesk Phase 6 — Individual Deliverables

Status: `FINAL_BEST_EFFORT`. Protocol version 6.1. The original PDF and eight original Markdown inputs were not modified.

All files below are individual English-language outputs. No ZIP, TAR or other archive is provided.

| File | Contents |
|---|---|
| [01_source_atoms_final.jsonl](01_source_atoms_final.jsonl) | Original-PDF positive atomic requirements |
| [01_source_negative_controls_final.jsonl](01_source_negative_controls_final.jsonl) | Fixed PDF-negative controls |
| [02_generated_atoms_final.jsonl](02_generated_atoms_final.jsonl) | Generated definitive occurrence inventory |
| [02_generated_classes_final.jsonl](02_generated_classes_final.jsonl) | Raw semantic-class inventory with updated final status metadata |
| [03_canonical_universe_final.jsonl](03_canonical_universe_final.jsonl) | Final canonical scoring universe |
| [03_evidence_matches_final.jsonl](03_evidence_matches_final.jsonl) | Source-to-generated evidence matches |
| [03_semantic_coverage_bridges_final.jsonl](03_semantic_coverage_bridges_final.jsonl) | Direct/contextual/conjunctive coverage bridges |
| [03_fn_root_cause_audit_final.jsonl](03_fn_root_cause_audit_final.jsonl) | Initial FN candidates and final dispositions |
| [04_generated_claim_validity_final.jsonl](04_generated_claim_validity_final.jsonl) | Generated-class correctness assessment |
| [04_atomic_judgments_final.jsonl](04_atomic_judgments_final.jsonl) | One score per canonical unit |
| [04_confusion_matrix_final.json](04_confusion_matrix_final.json) | Four-cell metrics in JSON |
| [04_confusion_matrix_final.md](04_confusion_matrix_final.md) | Four-cell metrics explained |
| [04_duplicate_classes_final.jsonl](04_duplicate_classes_final.jsonl) | Semantic duplication membership and partition |
| [05_duplicate_metrics_final.json](05_duplicate_metrics_final.json) | Raw duplication counts in JSON |
| [05_duplicate_metrics_final.md](05_duplicate_metrics_final.md) | Raw duplication counts explained |
| [05_tp_evidence_audit_final.jsonl](05_tp_evidence_audit_final.jsonl) | TP predicate-check audit |
| [05_source_atomization_audit_final.jsonl](05_source_atomization_audit_final.jsonl) | Source splitting/merging review |
| [06_metrics_final.json](06_metrics_final.json) | Independently recomputed final metrics |
| [06_metrics_final.md](06_metrics_final.md) | Final evaluation summary |
| [07_change_delta.jsonl](07_change_delta.jsonl) | Corrections and source-atomization delta |
| [08_coverage_and_limitations.md](08_coverage_and_limitations.md) | Evidence reliability, scope and unresolved issues |
| [09_excluded_units.jsonl](09_excluded_units.jsonl) | Non-normative and non-definitive exclusions |
| [compute_metrics.py](compute_metrics.py) | Standalone ledger recomputation script |

## Additional audit aids

- `06_phase6_corrected_retrieval_matches.jsonl` documents the ten Phase-6 FN-to-TP corrections.
- `06_metadata_reconciliation.json` documents generated-class status metadata normalization.
- `06_delivery_validation.json` documents final file/format/language/equation validation.
- `01_pdf_page_coverage_final.jsonl` and `02_generated_line_and_cell_coverage.jsonl` contain original physical-input coverage.

## Reproduction

```bash
python compute_metrics.py --base /path/to/final/output --inputs /path/to/original/inputs --write
```

The `--inputs` directory must contain the original uploaded PDF and all eight original scored Markdown files with their unchanged supplied filenames.
