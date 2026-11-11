# OrionDesk AI — Phase 6 final independent recomputation

**Status:** FINAL_BEST_EFFORT  
**Protocol:** 6.1  
**Evaluated method:** unprefixed_eight_markdown_set (the supplied eight Markdown files)  
**Source baseline:** original 90-page PDF; frozen fullload_cal-derived source-positive and negative-control ledgers.

## Recomputed four-cell results

| Cell | Number of canonical propositions |
|---|---:|
| TP | 754 |
| TN | 37 |
| FP | 2,115 |
| FN | 270 |
| **Total U** | **3,176** |

| Metric | Value | Definition |
|---|---:|---|
| Precision | 26.2809% | TP / (TP + FP) |
| Recall | 73.6328% | TP / (TP + FN) |
| F1 | 38.7362% | 2TP / (2TP + FP + FN) |
| Duplicate | 3.0778% | (Eligible generated occurrences - raw generated classes) / eligible generated occurrences |

The common universe is U = R disjoint-union N disjoint-union F, with
R=1,024, N=37,
F=2,115 and U=3,176.
The effective canonical predicted-positive count is 2,869.
This count is **not** the raw unique-generated-class count (3,275).
An explicitly applicable shared or universal generated rule may entail more than one independently sourced PDF atom without multiplying raw generated occurrences.

TN=37 covers only the 37 explicitly predeclared PDF-grounded negative controls.
It is not a count of all possible requirements absent from the original design.

## Independent recomputation and evidence gates

The independently authored `compute_metrics.py` reads the final JSONL items, not previous scores.
It checks unique IDs, one-to-one raw occurrence ownership, method isolation, source/negative/unsupported partition,
TP proof records, FN reciprocal dispositions, negative-control nonoverlap, all four equations,
duplicate within/across-file partition, all 90 physical PDF page records, and every physical line of all eight inputs.

- Structural checks passed: 14 of 14.
- Final TP source atoms and proof-audit entries: 754 each.
- TP E3 direct evidence: 71; E2 contextual/universal/conjunctive proof: 683.
- Final FN root-cause records: 270.
- Distinct original generated-file/line references from the TP proof audit: 609.
- Unresolvable TP generated evidence locations: 0.
- Recorded input inspection: 90 physical PDF pages, 8 complete scored Markdown files, 3,956 original Markdown lines.
- Source quote-audit provenance: 1021 text-grounded source quotes and 3 visual-source quotes.

These checks confirm structural consistency and evidence-location integrity, **not** independent human-grade semantic validity.

## Final FN and generated-validity dispositions

| Final source FN root cause | Count |
|---|---:|
| TRUE_MISSING | 8 |
| PARTIAL_ENTAILMENT | 137 |
| CONSERVATIVE_UNRESOLVED | 125 |
| **Total** | **270** |

| Generated raw class validity | Count |
|---|---:|
| PDF_ENTAILED | 397 |
| SUPPORTED_NONCOVERING | 763 |
| PDF_UNSUPPORTED | 2,115 |
| **Total G** | **3,275** |

A conservative E1 unsupported-generated classification may reflect incomplete contextual proof; it is not a certified design mistake.
Raw classes are evaluated for PDF correctness independently of whether their narrower contents cover a frozen R atom.

## Raw semantic duplication

GO=3,379, G=3,275,
excess=104 (within file=5, across files=99).
Repeated classes=87; classes spanning multiple original files=86.
The Phase-5 similarity review examined 241 candidate pairs and merged 42 compatible full-predicate classes,
keeping export-only, deletion-only and jointly scoped controls distinct.

## Phase 6 corrections and comparability

The final checker found that some Phase-5 canonical/validity files had reverted to Phase-4 versions,
although the Phase-5 source evidence and audit records were updated. The original false negative dispositions
were therefore reconstructed from the Phase-5 evidence ledgers and existing documented correction deltas.
An additional 21 demonstrable full-row or contextual matches were corrected from FN to TP in the final Phase-6 challenge.
All corrections are itemized in `06_exact_match_corrections_final.jsonl`,
`06_ledger_reconciliation_audit.json` and `07_change_delta.jsonl`.
The source PDF inventory and fixed negative controls are unchanged.

The final FN counts are derived from all current item-level judgments, not from the previous Phase-5 narrative.

## Final interpretation

**FINAL_BEST_EFFORT.** The source atom inventory, matching and generated correctness judgments
are reproducible, with unresolved conservative cases explicitly documented. Do not interpret
Precision, Recall or F1 as independently certified implementation correctness, production quality,
or exact real-world completeness of a generated specification. Both numerator and denominator
may move upon closer semantic and source-atomization review.
