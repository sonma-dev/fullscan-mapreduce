# Phase 5 — Correction, Evidence Re-Audit and Limitations

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** OrionDesk One-Pass Atomic Evaluation v6.1  
**Source:** `OrionDesk_AI_Detailed_Design_Specification(3).pdf` (SHA-256 `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`; 90 physical pages).  
**Input:** Exactly eight user-supplied English Markdown files; neither instructions nor this report is scored.  
**Next phase:** Not started.

## Results

The corrected canonical universe has **979 TP, 37 TN, 0 FP, 45 FN**. Its rates are **Precision 100.0000%, Recall 95.6055%, F1 97.7534%, Duplicate 4.1470%**. These are auditable *best-effort numerical classifications*, not externally certified semantic truth.

## Audits performed and corrections

1. All 1024 PDF source atoms were checked against their retained evidence kind, source quote, same-passage children and potential summary-versus-child overlap. Two `PDF-00192`/`PDF-00193` malformed source-path normalizations were corrected using original physical page 23's unbroken prose. No source item was invented, dropped or renumbered and the common denominator remains 1024.
2. All 979 final TP items are present in `05_tp_evidence_audit_final.jsonl`; 170 newly corrected FN candidates have actual file and line/table-cell evidence bridges. Direct citation consistency was checked independently of arithmetic; 0 items remain evidence-certification exceptions, not verified complete proofs.
3. All 630 prior FN-candidate records were re-adjudicated; final FN dispositions: {'CONSERVATIVE_UNRESOLVED': 34, 'PARTIAL_ENTAILMENT': 11}. Residual partial and conservative decisions should not be interpreted as proven source feature absence.
4. All 37 fixed negative controls were crosschecked for affirmative adoption versus prohibition/deferral. No definite counterfactual assertion was established, so they remain TN.
5. 231 potential generated class-duplicate pairs were inspected for target, actor, timing, exception, scope and outcome. 23 equal-predicate class pairs were consolidated; changed-scope paraphrases remain separate. Every occurrence remains in its original input file/line.
6. Class validity classifications were reconciled against corrected source coverage, but PDF validity is not certified for all 3652 classes. Do not infer that FP=0 means 100% genuine correctness.

## Source and generated evidence limitations

- PDF source inventory: 1024 requirements, 37 bounded negative controls. The same original source ID and exact original English quote are retained, except for verified normalization of two wrapped endpoint propositions. There are **no** revised requirements added from generated Markdown.
- Original PDF requirements are independently anchored; repeated contract boilerplate was not copied once per endpoint without source-specific behavior.
- The generated Markdown extraction was inherited from Phase 2, including 18 definitively recovered Phase 3 occurrences. It remains a machine-assisted best-effort atomization, especially on very long compound paragraphs and narrow table cells.
- The TP proof audit is **structurally complete at item level**, but automatic source-target checks and contextual matching cannot certify every actor, exception and temporal predicate. 
- All score arithmetic and duplicate partitions reconcile in one universe, which is **not** a semantic-evidence quality guarantee. No statistical confidence interval or claim that Recall is necessarily a lower bound is made.

## Important independent files

`05_tp_evidence_audit_final.jsonl`, `05_source_atomization_audit_final.jsonl`, `03_fn_root_cause_audit_final.jsonl`, `05_semantic_duplicate_candidate_review_final.jsonl`, `05_negative_control_reaudit_final.jsonl`, `07_change_delta.jsonl`, `05_duplicate_metrics_final.json`, `05_duplicate_metrics_final.md`, `04_confusion_matrix_final.json`, `04_confusion_matrix_final.md`, `04_atomic_judgments_final.jsonl`, and the corrected common source/bridge/class/canonical ledgers.
