# OrionDesk AI — Coverage, evidence quality and limitations

**Final status:** FINAL_BEST_EFFORT.  
**Scope:** one unprefixed eight-document generated specification set against the identical original 90-page PDF.  
**Document baseline:** OD-AI-DDS-001, R1.0 / revision 1.3.

## Source, generated and page/line inspection

The original source-positive R ledger and fixed N controls were reused **byte-for-byte** from the prior fullload_cal extraction after confirming PDF identity by SHA-256, not regenerated from historical scores.
The physical PDF pages 1–90 are covered in `01_pdf_page_coverage_final.jsonl` and its source evidence includes chapter tables, figures, appendices, restrictions and test pack.
The PDF evidence audit found 1021 textual matches and 3 visually inspected diagram/figure quotes.

The current scored inputs comprise only these eight distinct original files:

- `01_screen_functions(2).md`
- `02_api(2).md`
- `03_data(2).md`
- `04_batch_functions(2).md`
- `05_business_rules(2).md`
- `06_exception_handling(3).md`
- `07_processing_flows(3).md`
- `08_architecture_decision(2).md`

All 3,956 physical lines were enumerated in the generated-file coverage ledger, including table rows/cells and excluded claims.
The generated docs and the copied original PDF remain unmodified. The resolved-or-unadopted proposal status in `08_architecture_decision(2).md` did not turn unsupported choices into definitive predictions.

## Source atomization and denominator reliability

R=1024 independently scored source-positive records; N=37 fixed negative controls.
The source-atomization challenge records 19 potential source-splitting and repeated-test concerns from the reused source ledger.
Phase 5 retained the source inventory unchanged and explicitly examined the 16 Appendix E minimum test-pack scenarios
as separate executable verification outcomes rather than automatically deleting them as restated implementation requirements.
The old and new PDF IDs are unchanged; no source split/merge correction is claimed.
The absence of an implemented split/merge does not prove that 1,024 is a unique certified true denominator.
Repeated universal boilerplate and inherited table field context still warrant caution in interpreting Recall.

## False negatives: unresolved coverage and false-negative prevention

- Initial provisional FN candidate audit: 840 records, including those corrected to TP.
- Total initially uncovered items corrected through Phase 3, 5 and 6: 570.
- Final TRUE_MISSING: 8 source atoms, with actual reciprocal-search evidence.
- Final PARTIAL_ENTAILMENT: 137 source atoms, with an explicit unmet predicate.
- Final CONSERVATIVE_UNRESOLVED: 125 source atoms, with a bounded evidence limitation rather than certified absence.

The final Phase-6 challenge corrected 21 additional explicit matches, including the source PostgreSQL continuous-backup RPO/RTO predicate and multiple exact API method/path/actor/status rows.
These findings demonstrate that prior low Recall measurements could contain matcher-created false negatives.
The diagnostic records additionally check a case title, workspace retention class and identical idempotent case-creation result;
all three are TP with real original generated-file evidence in `06_exact_match_regression_probes_final.jsonl`.
Neither probe success nor exact identifier retrieval proves exhaustive coverage.

## TP evidence and semantic reliability

There are 754 TP audit records and 71 E3 versus 683 E2 proofs,
with original PDF and generated line or table-row locators. All TP proof entries have a predicate map.
However, these predicate maps and inherited-row applicability bridges were largely computer-assisted and explicitly not human-certified.
A source TP can rely on a narrower generated subclaim even when its broader raw class remains unsupported in full.
The present ledgers include **180 PDF_UNSUPPORTED raw classes also cited in the evidence for 324 TP source atoms**.
This is an important semantic audit exception: it may be a legitimate supported-narrower versus unsupported-extra distinction,
but the supplied proof does not independently demonstrate every such separation.
Accordingly these 324 TP cases must not be interpreted as semantically certified.

## Generated FP support limits

The raw class validity ledger contains 2115 PDF_UNSUPPORTED classes,
including 1978 E1 (partial/uncertain PDF support) and 137 E0 (no established support or contradiction).
The priority review considered 633 historical flagged candidates. Its dispositions are:

- CONSERVATIVE_PDF_UNSUPPORTED_BEST_EFFORT: 610
- MERGED_INTO_SAME_MEANING_CLASS: 1
- PDF_SUPPORT_RECORDED: 14
- REMOVED_OR_UNMAPPED: 8

The 633 review flags include overlapping concerns; these are not 633 independently proven defects.
The raw-class FP count is scored once per surviving unsupported canonical proposition;
asserted negative controls would also be FP but no such claims were found in this run.
Conservative generated-only classifications can be false positives when PDF synonyms, context or inherited scope were missed.

## Fixed negative controls and confusion-universe interpretation

The 37 negative controls were constructed before scoring from explicit exclusions, prohibitions and release deferrals.
TN=37 is a bounded diagnostic control result, not the complement of all requirements imaginable.
The evaluated canonical proposition universe has |R|=1024, |N|=37, |F|=2115 and |U|=3176.
Predicted positives=2869, while raw unique generated classes=3275.
Do not use raw G as the Precision denominator, or create extra occurrence duplicates when one universal generated requirement entails multiple distinct source duties.

## Duplicates, exclusions and version/method isolation

GO=3379, G=3275,
excess=104, partitioned into within-file 5 and across-file 99.
These are counts of eligible raw commitments and full-predicate classes; neither coverage projection nor repeated references are additional raw duplicates.
The 241 similarity candidate records include 42 merges; unmerged candidates require scope-aware interpretation, not automatic consolidation.
PDF exclusions, generated nondefinitive/TBD/unadopted proposal exclusions and audit metadata remain in `09_excluded_units.jsonl`.

Only the single supplied unprefixed set was scored, so no cross-method comparison file is applicable.
The same original PDF R and N inventories were retained; no historical fullload_cal TP/FP/FN scores were copied.

## Independent consistency, remediated stale mirrors and final status

The final structural recomputation passed 14 of 14 checks, including input bytes and lines, 90 PDF pages,
per-item one-universe equations, TP evidence paths and FN root-cause closure. Phase 6 discovered the old Phase-4 summary and canonical mirrors
still present after the Phase-5 audit had advanced; those stale files were rebuilt with existing Phase-5 evidence decisions,
then 21 objectively complete FN matches were corrected. The reconciliation is recorded; it should not be confused with a new experimental method.

**Reliability decision: FINAL_BEST_EFFORT, not FINAL_VERIFIED.** Arithmetic and proof-file structure are validated,
but semantic entailment certification, full correct FP classification, and absence of source atomization defects are not established.
The point scores are provisional arithmetic summaries over the enumerated binary ledger, not confidence intervals or certified lower bounds.
Potential residual semantic defects could alter TP, FN, FP, R and therefore Precision, Recall and F1 in either direction.
