# OrionDesk AI — Phase 5 Reaudit, Corrections, and Limitations

**Protocol:** 6.1  
**Evaluation scope:** One unlabeled, complete eight-document Markdown set  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Semantic certification:** `NOT_CERTIFIED`

## Fixed source and input scope

The original English PDF has 90 physical pages; all eight supplied scored Markdown documents are present and their original filenames/line coordinates are preserved. The independent PDF source-positive inventory remains 979 atoms, and the fixed predeclared PDF-negative-control inventory remains 37 controls. The source PDF is the only normative authority; generated claims and earlier goldsets are not used to create PDF requirements.

Two source-atom normalization issues were corrected without altering the common denominator: `PDF-00193` now correctly says `/members` (the source's p.23 table splits the word across lines), and `PDF-00591` retains the independent storage-cost accounting requirement without treating the typical 1 MB / 40–120 chunks sizing illustration as a binding output requirement. See `07_change_delta.jsonl` and the 979-row `05_source_atomization_audit_final.jsonl`.

## Corrected coverage decisions

| Item | Result |
|---|---:|
| Source-positive inventory R | 979 |
| Fixed negative controls N | 37 |
| TP | 647 |
| FN | 332 |
| TN (bounded controls) | 37 |
| FP established | 0 |
| Newly corrected FN-to-TP | 60 |
| TP audit records | 647 |
| Initial candidate-FN root-cause records retained | 782 |
| Canonical universe rows | 1016 |

### Provisional rates

- Precision: **100.000000%** (NOT verified).
- Recall: **66.087845%** (best-effort source coverage).
- F1: **79.581796%**.

The preliminary 60 Phase-5 FN recoveries are accompanied by verbatim Markdown evidence and actual line/table-cell locators; representative examples include policy override by an LLM (`PDF-00388`), delayed-indexing runbook recovery and verification (`PDF-00973/00974`), meaningful accessibility announcements (`PDF-00512`), review data capture (`PDF-00392`), and approved file input constraints (`PDF-00271`). Some recovered composite requirements rely on several explicitly cited generated statements. Their status is best effort and is not independent formal proof of logical implication.

### Remaining FN dispositions

| Disposition | Final FN count | Interpretation |
|---|---:|---|
| `PARTIAL_ENTAILMENT` | 185 | A retrieved generated assertion addresses some but not all source predicates. |
| `CONSERVATIVE_UNRESOLVED` | 142 | The actual candidates are inconclusive; these are not verified omissions. |
| `TRUE_MISSING` | 5 | No complete relevant affirmative generated claim identified in the bounded corpus challenge. |
| **Total** | **332** | One final FN disposition per uncovered source atom. |

Phase 3's earlier 390 source-to-generated retrieval misses and Phase 5's additional 60 recoveries remain traceable in the initial-FN audit and correction delta. The review compared direct equivalent text, table row/column context, common/universal rules, conjunctive cross-file claims, source-specific limits, and the best retrieved contrary examples. Exact identifier coincidence alone did not establish a TP.

## Generated claim correctness and uncertainty

| Claim-level provisional category | Count |
|---|---:|
| `PDF_ENTAILED` | 1483 |
| `SUPPORTED_NONCOVERING` | 5368 |
| Evidence-established `PDF_UNSUPPORTED` | 0 |
| Weak PDF-corroboration claim records | 3904 |

The claim-validity categories above **are provisional, not a verified independent support audit**. In particular, many `SUPPORTED_NONCOVERING` labels rely on lexical/contextual retrieval instead of affirmative complete-PDF-predicate proof. No distinct definitively unsupported affirmative implementation proposition was established with adequate evidence in this bounded phase. Consequently, the reported **FP=0 and Precision=100% must not be interpreted as correct absence of unsupported implementation commitments**. A future independent review may alter FP, TP/FN, or the source denominator; this result is neither a proven lower bound nor a certified coverage estimate.

The negative-control set is a PDF-derived diagnostic sample, not all possible non-requirements. Mentions of an excluded or deferred behavior are not affirmative adoption. Its 37 TN rows contribute no improvement to Precision, Recall, or F1.

## Duplicate and eligibility audit

| Metric | Value |
|---|---:|
| Eligible generated occurrences `GO` | 6929 |
| Raw unique generated classes `G` | 6851 |
| Excess occurrences | 78 |
| Within-file excess | 5 |
| Across-file excess | 73 |
| Repeated claim classes | 66 |
| Repeated classes spanning files | 63 |
| Duplicate rate | 1.125704% |

Nine unadopted Proposal classes were excluded from the final eligible generated universe. Five exact full-assertion merges were applied where the underlying target/scope matched. Potential paraphrased duplicates that cannot be established safely with the original row and actor scope remain unmerged; the measured rate should not be treated as an exhaustive semantic-duplication census.

## Structural evidence verification

`05_independent_structural_validation_final.json` reports 20 structural checks: unique source and control IDs, one-to-one class membership for eligible occurrences, original Markdown quote provenance, canonical ledger uniqueness, all 647 TP proof-audit entries, all 332 FN dispositions with candidate quotations, 979 source atomization records, and the within/across-file duplication partition. All 20 checks passed. The checks do not substitute for independent expert review of actual entailment.

The canonical equations were reconciled on one universe: `TP + FN = R`, `TN + asserted negative controls = N`, `FP = unsupported generated propositions + asserted negative controls`, and `TP + TN + FP + FN = U`. The raw generated class count is not the denominator of the canonical prediction set, and it must not be forced equal to `TP+FP`.

## Phase boundary

Phase 5 is complete. No independent Phase 6 metric recomputation, release certification, archive generation, or multi-method comparison was performed. The next authorized phase is Phase 6.
