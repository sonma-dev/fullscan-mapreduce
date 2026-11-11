# OrionDesk AI — Atomic Requirement Evaluation Artifacts

This archive groups the principal outputs of the six-phase evaluation by phase. All archived artifact bodies are the files as produced, without rewriting the requirement evidence or scoring ledgers. Original scored inputs and PDF are not bundled because they are evaluation inputs rather than generated outputs.

## Navigation

- `Phase_01_Source_Evidence/`: PDF-positive atomic source requirements, fixed negative controls, page/quotation checks, input manifest and phase report.
- `Phase_02_Generated_Corpus/`: generated claim occurrences/classes, exclusions, line/cell coverage and retrieval indexes.
- `Phase_03_Semantic_Coverage/`: canonical decision universe, generated evidence matches, bridges, FN audit and source-to-output mapping.
- `Phase_04_Claim_Validity_and_Confusion/`: generated claim validity, item judgments, bounded negative controls, and confusion matrix.
- `Phase_05_Duplication_and_Corrections/`: final deduplicated class ledger, duplicate metrics, TP/source atomization audits, change history and correction reports.
- `Phase_06_Final_Verification/`: final metrics, independent checks, retrieval audits, recomputation scripts and final limitations report.

## Reproducibility and interpretation

- Protocol version: 6.1; evaluation completion: `FINAL_BEST_EFFORT`.
- Reference count: 1,024 PDF-positive atoms and 37 bounded negative controls.
- Final tabulated counts: TP=979, TN=37, FP=0, FN=45; generated occurrences=3,810, classes=3,652.
- Reported rates: Precision 100.00%, Recall 95.61%, F1 97.75%, Duplicate 4.15%.
- These numbers measure the adjudicated canonical inventory. They are not independent certification of semantic completeness; FP=0 should not be interpreted as exhaustive proof that no unsupported commitments exist.
- Current final ledgers are organized by the phase that owns their *function*. Several phase 3 and phase 4 ledgers were corrected during phase 5; the archive carries their final versions only.
- `compute_metrics.py` is placed in Phase 6. The original implementation expects the final ledgers in a common working directory and the original inputs mounted. For reruns, place the extracted ledger files in one working directory as needed. This archive does not change paths inside that script.
- `06_final_artifact_inventory.json` is a pre-packaging snapshot and therefore says no archive existed at the time. This ZIP and its current contents are described instead by `MANIFEST.json`.
