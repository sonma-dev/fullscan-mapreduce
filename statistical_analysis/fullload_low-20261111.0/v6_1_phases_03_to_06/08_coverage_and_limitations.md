# OrionDesk v6.1 — PDF / Markdown Coverage and Evidence Limitations

**Final status: FINAL_BEST_EFFORT — structurally consistent, not semantically certified.**

## Input and inspected scope

- Authoritative document: `OrionDesk_AI_Detailed_Design_Specification.pdf` (90 physical pages, R1.0/revision 1.3). The source-positive inventory was independently extracted from the original English PDF; generated documents cannot define source requirements.
- Eight scored original Markdown input files: `01_screen_functions.md`, `02_api.md`, `03_data.md`, `04_batch_functions.md`, `05_business_rules.md`, `06_exception_handling(1).md`, `07_processing_flows(1).md`, and `08_architecture_decision.md`.
- All 3,956 physical input lines and 6,308 recorded table cells were covered in the existing line/cell ledger. Unadopted architecture questions and proposals are excluded from definitive commitments.
- All 90 pages appear in the PDF coverage ledger. Three figure-derived assertions (PDF-00977, PDF-00978, PDF-00979) lack a PDF *text-extraction* match but are legible in the page 8 source figure, which was visually inspected. No missing input blocker was identified.
- The excluded-unit ledger and the generated exclusions ledger are retained. They are not additional scored source documents.

## Reciprocal FN audit and corrected false negatives

- Final Recall on the enumerated canonical source propositions: **65.72%** = 673/1024.
- Corrected candidate FNs in the root-cause ledger: 177 (cumulative from the v6.1 adjudication ledger, not an exclusively Phase 6 count).
- Phase 6 directly corrected two provable extraction/matcher misses: PDF-01013 (`language`) and PDF-01014 (`classification`) using the exact SearchChunk row of `03_data.md`, line 182. Their old/new classifications and evidence are in `07_change_delta.jsonl`.
- Final FN root-cause counts: TRUE_MISSING = 0; PARTIAL_ENTAILMENT = 134; CONSERVATIVE_UNRESOLVED = 217. These sum to 351.
- Remaining 351 FNs are **not** a verified list of missing features. Partial/unresolved classifications require substantive case-by-case review; a topical search flag does not prove absence.
- Universal/common requirements may entail multiple independently testable PDF atoms without generating extra raw occurrences or artificial duplicates. Their applicability proof must carry scope, actor, conditions, exceptions, version, timing and outcome when material.

## TP evidence and source atomization

- All 673 final TPs have one confirmed TP evidence-audit record with PDF/generated locations and a predicate map. 3 figure-only source quotes require visual rather than plain-text verification.
- Several proof maps and bridge explanations were normalized from existing Phase 5 records in this final phase; structural presence is **not** independent confirmation of whole-statement logical entailment.
- The source-atomization audit contains 1 recorded decision row(s), reporting no Phase 5 changes. Potential parent/child overlap, repetitive interface boilerplate, source narrative mistaken for a requirement, and the Appendix E acceptance-test double-counting question are ongoing semantic risks. Repeated general rules should not be multiplied by the number of endpoints; distinct endpoint contracts must be preserved. A single `NO_ATOMIZATION_CHANGES` audit marker does not conclusively prove the 1,024-atom denominator is optimal.

## Generated correctness and unsupported-claim review

- Total raw generated semantic classes: 3,218; definitive generated occurrences: 3,350.
- 722 classes currently categorized as `SUPPORTED_NONCOVERING` have only E1 support. They cannot be treated as independently certified PDF-entailed claims without full-predicate review.
- 210 canonical generated-only unsupported predictions carry E1 PDF-support ambiguity. The 210 counted FPs are therefore provisional binary judgments rather than established implementation errors.
- A supported-but-noncovering claim is not a false positive merely because it does not cover an entire frozen source atom; an unsupported residual predicate becomes an FP only once per distinct canonical class.
- The 37 fixed source-negative controls are a **bounded diagnostic test set** predeclared from explicit PDF prohibitions or deferrals. Their TN does not estimate the universe of all absent features and cannot inflate Precision, Recall, or F1.

## Structural repair and separate denominators

- Phase 5 judgments contained 1,271 rows but the canonical-universe file still contained 1,296. The 25 stale unsupported-only rows were removed from the canonical-universe ledger; the individual judgments and validity ledger already excluded them. Both files now contain exactly 1,271 identically serialized canonical decisions.
- One effective universe: R=1,024, N=37, F=210. Its predicted positives = TP+FP=883, not raw G_C=3,218.
- Raw Duplicate = (GO - G_C)/GO = 132/3350 = 3.94%; within-file 16 + across-file 116 = 132.
- Arithmetic and locator verification succeeded. The `compute_metrics.py` verifier is reproducible and explicitly does **not** certify semantic evidence from string similarity, structural counts or quoted locators.

## Final disposition

**FINAL_BEST_EFFORT**, not `FINAL_VERIFIED`. Residual uncertainty is quantified: 217 unresolved FN source atoms, 134 partial FN source atoms, 722 only-E1 supported/noncovering generated classes and 210 unsupported E1 generated classes. Neither the final Recall nor Precision may be treated as verified ground truth for method comparison or real-world implementation safety.
