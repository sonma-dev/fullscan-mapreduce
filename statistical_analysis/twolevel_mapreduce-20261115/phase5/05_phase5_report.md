# OrionDesk AI — Phase 5 corrected coverage and duplication audit

**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`. Protocol v6.1; only Phase 5 is performed in this response; Phase 6 has **not** been run.

## Grounded corrections

- Identified the physical PDF p.23 register-path wrap that split `/v1/workspaces/{workspaceId}/members` into `/me` and `mbers`; corrected **two** source atoms and matched the existing generated API-020 row and S+B contract. No `/me` API is inferred.
- Excluded 19 improperly independent PDF scoring units: eight Appendix C.2 illustrative A2A example fields, six Appendix A.3 error-example fields lacking universal requiredness, and five overlapping/background summary statements. Kept explicit source requirements for safe errors, A2A authorization and typed MCP contracts.
- Corrected 35 Phase 3 conservative FN labels to TP after inspecting named Markdown locations and the original PDF scopes. One earlier TP, PDF-00613 (complete IaC resource inventory), was downgraded because the generated text did not entail the complete PDF requirement.
- Recovered 12 definitive generated subclaims skipped by the first paragraph extraction. Merged 14 proven equivalent raw classes in 13 groups; independently recomputed the within-file and across-file excess.
- Individually recorded all 978 previously/finally TP-relevant source audit entries, all 115 flagged or changed source atomization records, all 589 duplicate candidates, and the complete 924 FN-origin/correction audit rows. Audit counts are structural, not external semantic certification.

## Provisional corrected canonical universe

| Item | Value |
|---|---:|
| Source-positive R | 1005 |
| Fixed negative controls N | 37 |
| Raw definitive generated occurrences | 3128 |
| Raw semantic classes | 3018 |
| TP | 977 |
| FN | 28 |
| TN | 37 |
| FP established | 0 |
| Precision | 100.0000% |
| Recall | 97.2139% |
| F1 | 98.5873% |
| Duplicate | 3.5166% |

FN root causes: {"CONSERVATIVE_UNRESOLVED": 20, "PARTIAL_ENTAILMENT": 8}.

## Evidence limitations and unresolved semantics

1. Earlier Phase 4 had thousands of class-level support judgments with E1 or automatically retrieved PDF quotations. They are **not** all complete semantic proofs. Their original uncertainty is preserved in `04_generated_claim_validity_final.jsonl`; no unsupported-class FP has been certified. Therefore Precision and F1 are still provisional and may change upward or downward after a true exhaustive generated-claim validation.
2. The `05_tp_evidence_audit_final.jsonl` maps every retained positive to original PDF and real Markdown locations and records predicate categories. Its `CONFIRMED_TP` is a bounded best-effort adjudication, not certified human expert verification. A complete precondition/scope distinction in the original paragraph remains mandatory; automatic scores are not proof.
3. Source rows previously marked E1/E0 retain a concrete closest candidate and uncertainty. `CONSERVATIVE_UNRESOLVED` means no demonstrated complete entailment, **not** a verified absence in the generated corpus. Earlier initial retrieval false negatives are preserved but do not remain scored FN when decisively corrected.
4. Most nominally similar candidate pairs carry different methods/fields/states or insufficient proof of scope equivalence. Unresolved pairs were retained separately, not silently counted as duplicates. Raw duplication may therefore still be underestimated.
5. Original PDF 90 physical pages and all eight unchanged authored Markdown inputs remain the only authoritative source and scored corpus respectively. The source-atom and generated-atom corrections are evaluation ledgers; the scored input Markdown and PDF were not edited.
6. Fixed negative controls are a **bounded PDF-derived diagnostic set of 37**, not a comprehensive TN population. Their absence does not certify production safety.

## Phase boundary

Phase 5 completed once, with reproducible item-level ledgers, source correction history and corrected four-cell arithmetic. Phase 6 independent recomputation and final individual delivery are still pending.
