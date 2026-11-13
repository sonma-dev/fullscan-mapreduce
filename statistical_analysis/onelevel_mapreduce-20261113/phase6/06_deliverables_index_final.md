# OrionDesk AI — Phase 6 Individual Deliverables

Status: `PHASE_COMPLETED_BEST_EFFORT`. Semantic proof remains `NOT_INDEPENDENTLY_CERTIFIED_BEST_EFFORT`.

This directory contains the 90-page source PDF, eight unmodified scored Markdown documents, the corrected source/generated/judgment ledgers, the independent Phase-6 metrics, reproducibility checks, evidence inspections, and the audit script. There are no archives.

## Files

| File | Purpose |
|---|---|
| [01_pdf_page_coverage_final.jsonl](01_pdf_page_coverage_final.jsonl) | Final physical PDF page coverage |
| [01_pdf_quote_verification_final.jsonl](01_pdf_quote_verification_final.jsonl) | Final PDF quotation verification ledger |
| [01_screen_functions(7).md](01_screen_functions(7).md) | Exact unchanged scored Markdown input |
| [01_source_atoms_final.jsonl](01_source_atoms_final.jsonl) | Final PDF-positive source atom ledger |
| [01_source_negative_controls_final.jsonl](01_source_negative_controls_final.jsonl) | Fixed negative-control ledger |
| [02_api(7).md](02_api(7).md) | Exact unchanged scored Markdown input |
| [02_generated_atoms_final.jsonl](02_generated_atoms_final.jsonl) | Eligible generated atomic occurrence ledger |
| [02_generated_classes_final.jsonl](02_generated_classes_final.jsonl) | Unique raw semantic generated classes |
| [02_generated_line_and_cell_coverage_final.jsonl](02_generated_line_and_cell_coverage_final.jsonl) | Original Phase-2 physical line and table-cell scan |
| [03_canonical_universe_final.jsonl](03_canonical_universe_final.jsonl) | Final canonical proposition universe |
| [03_data(7).md](03_data(7).md) | Exact unchanged scored Markdown input |
| [03_evidence_matches_final.jsonl](03_evidence_matches_final.jsonl) | Final PDF-to-generated coverage decisions |
| [03_fn_root_cause_audit_final.jsonl](03_fn_root_cause_audit_final.jsonl) | Initial false-negative disposition ledger |
| [03_semantic_coverage_bridges_final.jsonl](03_semantic_coverage_bridges_final.jsonl) | Full evidence locators and coverage bridge records |
| [04_atomic_judgments_final.jsonl](04_atomic_judgments_final.jsonl) | One TP/TN/FP/FN judgment per canonical unit |
| [04_batch_functions(7).md](04_batch_functions(7).md) | Exact unchanged scored Markdown input |
| [04_confusion_matrix_final.json](04_confusion_matrix_final.json) | Final corrected canonical confusion matrix |
| [04_confusion_matrix_final.md](04_confusion_matrix_final.md) | Final corrected confusion matrix explanatory report |
| [04_duplicate_classes_final.jsonl](04_duplicate_classes_final.jsonl) | Per-class raw generated duplication inventory |
| [04_generated_claim_validity_final.jsonl](04_generated_claim_validity_final.jsonl) | Per-generated-class correctness classifications |
| [04_negative_control_assertion_audit_final.jsonl](04_negative_control_assertion_audit_final.jsonl) | Per-control generated assertion analysis |
| [05_business_rules(7).md](05_business_rules(7).md) | Exact unchanged scored Markdown input |
| [05_duplicate_metrics_final.json](05_duplicate_metrics_final.json) | Corrected raw duplication metrics |
| [05_duplicate_metrics_final.md](05_duplicate_metrics_final.md) | Corrected duplication explanatory summary |
| [05_remaining_fn_recheck_final.jsonl](05_remaining_fn_recheck_final.jsonl) | Final 39 false-negative rechecks |
| [05_source_atomization_audit_final.jsonl](05_source_atomization_audit_final.jsonl) | Source split/merge/duplicate assessment ledger |
| [05_tp_evidence_audit_final.jsonl](05_tp_evidence_audit_final.jsonl) | Final TP evidence and predicate review audit |
| [06_evidence_integrity_audit_final.json](06_evidence_integrity_audit_final.json) | Evidence-locator integrity and weak-bridge counts |
| [06_exception_handling(8).md](06_exception_handling(8).md) | Exact unchanged scored Markdown input |
| [06_generated_locator_validation_final.jsonl](06_generated_locator_validation_final.jsonl) | 4,217 generated source-line location checks |
| [06_input_coverage_final.json](06_input_coverage_final.json) | Original PDF and eight Markdown coverage |
| [06_metrics_final.json](06_metrics_final.json) | Independent Phase-6 canonical metrics (machine-readable) |
| [06_metrics_final.md](06_metrics_final.md) | Independent Phase-6 canonical metrics (readable) |
| [06_pdf_evidence_validation_final.jsonl](06_pdf_evidence_validation_final.jsonl) | 2,560 original PDF evidence location checks |
| [06_phase_status_final.json](06_phase_status_final.json) | Phase-6 completion and limits status |
| [06_regression_probes_final.jsonl](06_regression_probes_final.jsonl) | Bidirectional retrieval regression probes |
| [06_validation_checks_final.json](06_validation_checks_final.json) | 52 independent structural checks |
| [07_change_delta.jsonl](07_change_delta.jsonl) | Phase-5 substantive correction history |
| [07_processing_flows(8).md](07_processing_flows(8).md) | Exact unchanged scored Markdown input |
| [08_architecture_decision(7).md](08_architecture_decision(7).md) | Exact unchanged scored Markdown input |
| [08_coverage_and_limitations.md](08_coverage_and_limitations.md) | Evaluation scope, reliability limits and noncertification |
| [09_excluded_units.jsonl](09_excluded_units.jsonl) | PDF and generated exclusions |
| [OrionDesk_AI_Detailed_Design_Specification(8).pdf](OrionDesk_AI_Detailed_Design_Specification(8).pdf) | Authoritative 90-page PDF input, exact copy |
| [compute_metrics.py](compute_metrics.py) | Executable independent recomputation and audit script |

Run `python compute_metrics.py` from this directory to regenerate the Phase-6 outputs; only standard Python and PyMuPDF (`fitz`) are needed.
