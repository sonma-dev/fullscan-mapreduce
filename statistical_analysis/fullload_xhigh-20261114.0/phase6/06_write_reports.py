import json, pathlib, datetime, hashlib, collections
O=pathlib.Path(__file__).resolve().parent
J=json.loads((O/'06_metrics_final.json').read_text())
C=J['confusion']; M=J['metrics']; G=J['duplicate'];U=J['universe'];F=J['final_fn_root_causes'];
fmt=lambda x:f'{x*100:.2f}%' if x is not None else 'undefined'

conf={k:J[k] for k in ['protocol_version','prefix','phase','status','source_baseline','universe','confusion','metrics']}
conf['validity_note_en']='Provisional best-effort effective-universe confusion matrix. Precision is NOT independently certified; FN does not necessarily mean verified absence.'
conf['source_of_counts']='Independently regenerated from Phase 6 item-level canonical universe and corrected evidence ledgers by compute_metrics.py.'
(O/'04_confusion_matrix_final.json').write_text(json.dumps(conf,indent=2,ensure_ascii=False)+'\n')
(O/'04_confusion_matrix_final.md').write_text(f'''# Final Four-Cell Confusion Matrix — fullload (Phase 6)

**Protocol:** v6.1  
**Evaluation status:** `FINAL_BEST_EFFORT` (semantic certification not established)

| Cell | Final count | Actual | Predicted |
|---|---:|---:|---:|
| TP | {C['TP']} | 1 | 1 |
| FN | {C['FN']} | 1 | 0 |
| FP | {C['FP']} | 0 | 1 |
| TN | {C['TN']} | 0 | 0 |

| Metric | Computed value | Interpretation |
|---|---:|---|
| Precision | {fmt(M['Precision'])} | Provisional: the PDF support of thousands of generated classes remains unverified. |
| Recall | {fmt(M['Recall'])} | Fraction of the {U['source_positive_atoms']} current source atoms adjudicated as entailed; not certified overall coverage. |
| F1 | {fmt(M['F1'])} | Derived from the same four-cell universe. |
| Duplicate | {fmt(M['Duplicate'])} | Raw generated occurrence/class duplication, not an alternate precision denominator. |

The canonical universe has **{U['canonical_decision_units']}** units: {U['source_positive_atoms']} PDF-positive requirements, {U['source_negative_controls']} bounded PDF-negative controls, and {U['unsupported_generated_only_propositions']} positively asserted unsupported generated-only propositions. This does not mean that no other unsupported claims exist; the PDF-support audit is not independently complete.

Equations: TP+FN={C['TP']+C['FN']}=|R|; TN+asserted controls={C['TN']}=|N|; FP=unsupported-only ({U['unsupported_generated_only_propositions']}) + asserted controls ({U['asserted_negative_controls']}); all four cells sum to {sum(C.values())}=|U|. Positive canonical predictions={C['TP']+C['FP']}, **not** raw generated classes ({U['raw_generated_claim_classes']}).

**Scores are strictly provisional.** They measure specification propositions relative to the fictional PDF baseline and are not accuracy or safety certifications of a deployed system.
''')

du={
 'protocol_version':'6.1','prefix':'fullload','phase':6,'status':'FINAL_BEST_EFFORT',
 'eligible_generated_occurrences':G['eligible_occurrences'],'unique_generated_claim_classes':G['unique_generated_classes'],
 'duplicate_excess_occurrences':G['duplicate_excess'],'duplicate_rate':M['Duplicate'],
 'within_file_excess':G['within_file_excess'],'across_file_excess':G['across_file_excess'],
 'repeated_claim_class_count':G['repeated_claim_class_count'],'cross_file_repeated_class_count':G['cross_file_repeated_class_count'],
 'counting_rule':'One raw eligible generated occurrence per class membership, excess sorted in source-file/line/cell order.',
 'interpretation':'Full semantic equivalence of all 5,991 classes is not independently certified; this is a best-effort duplicate estimate.'}
(O/'05_duplicate_metrics_final.json').write_text(json.dumps(du,indent=2)+'\n')
(O/'05_duplicate_metrics_final.md').write_text(f'''# Semantic Duplicate Metrics — fullload (Phase 6)

**Status:** `FINAL_BEST_EFFORT`

| Item | Final count |
|---|---:|
| Eligible generated occurrences (`GO_m`) | {G['eligible_occurrences']} |
| Raw semantic classes (`G_m`) | {G['unique_generated_classes']} |
| Excess occurrences | {G['duplicate_excess']} |
| Within-file excess | {G['within_file_excess']} |
| Across-file excess | {G['across_file_excess']} |
| Repeated semantic classes | {G['repeated_claim_class_count']} |
| Repeated classes spanning multiple files | {G['cross_file_repeated_class_count']} |
| **Duplicate rate** | **{fmt(M['Duplicate'])}** |

The observed 89 excess occurrences partition into 2 within-file and 87 across-file excess occurrences. This raw-occurrence calculation is separate from source-atom coverage and does not require TP+FP to equal the raw class count. Candidate paraphrases not consolidated in prior phases remain a possible downward bias in the duplicate estimate. The 20 recovered definitive source clauses are retained as separate generated occurrences/classes in the corrected ledger.
''')

(O/'06_metrics_final.md').write_text(f'''# Final Independent Recalculation — OrionDesk AI

**Method:** `fullload`  
**Protocol:** v6.1  
**Final status:** `FINAL_BEST_EFFORT`  
**PDF authority:** *OrionDesk AI Detailed Application Design Specification* (`OD-AI-DDS-001`, R1.0 / revision 1.3)

## Final metrics

| Measure | Final |
|---|---:|
| PDF-positive source atoms | {U['source_positive_atoms']} |
| Fixed PDF-negative controls | {U['source_negative_controls']} |
| Canonical decision units | {U['canonical_decision_units']} |
| TP | {C['TP']} |
| FN | {C['FN']} |
| FP | {C['FP']} |
| TN | {C['TN']} |
| Precision | {fmt(M['Precision'])} (provisional, not certified) |
| Recall | {fmt(M['Recall'])} (best effort) |
| F1 | {fmt(M['F1'])} (best effort) |
| Semantic duplication | {fmt(M['Duplicate'])} (best effort) |

## Independent reconciliation

The recomputation reads individual canonical judgments rather than previous aggregate scores. TP+FN={C['TP']}+{C['FN']}={U['source_positive_atoms']}; TN+asserted negatives={C['TN']}+{U['asserted_negative_controls']}={U['source_negative_controls']}; FP={U['unsupported_generated_only_propositions']}+{U['asserted_negative_controls']}={C['FP']}; and the four cells sum to {U['canonical_decision_units']}.

Raw occurrence/class accounting is {G['eligible_occurrences']} minus {G['unique_generated_classes']} = {G['duplicate_excess']}, partitioned into {G['within_file_excess']} within-file and {G['across_file_excess']} across-file excess. Canonical predicted positives are {U['canonical_predicted_positive_units']}; they are not the raw generated class count.

## Additional Phase 6 corrections

- 55 specific initial false negatives were corrected to TP with source quotes and generated-file/line evidence.
- 20 definitive generated occurrences omitted from the preceding extraction were restored from the original, unchanged Markdown files.
- Six negative-control canonical identities were repaired after collision with the split source atoms `PDF-01025`–`PDF-01030`; no negative controls or source requirements were added or discarded by this identity repair.
- Missing method metadata for 23 directly reviewed generated-class validity rows was filled with the sole selected method, `fullload`.
- The source inventory remains {U['source_positive_atoms']}, incorporating three Phase-5 source-atomization corrections. The original PDF and all eight scored Markdown files remain unmodified.

## Outcome limitations

The independent checker validates record uniqueness, the entire canonical universe, PDF-page references, generated input quotation positions, FN root-cause membership, TP proof-audit presence, negative-control non-overlap and duplicate partitions. It does **not** certify semantic entailment for each claim. **{J['generated_pdf_support_unverified']:,}** generated classes retain uncertified original-PDF support assessments. A `FP=0` count is therefore an absence of *adjudicated* unsupported assertions, not proof that every generated statement is correct.

Final FN: **{C['FN']}** = {F.get('PARTIAL_ENTAILMENT',0)} partial-entailment cases + {F.get('CONSERVATIVE_UNRESOLVED',0)} conservative unresolved cases. Neither category should be presented as a verified absence. The exact-quotation regression checker found {J['remaining_exact_quote_fn_exception_count']} remaining full-line exact-match exceptions, but contextual/semantic misses could remain.

Details, original evidence, and uncertainties: `08_coverage_and_limitations.md`. Reproduction: `python compute_metrics.py` from this output directory.
''')

v=J['generated_pdf_support_unverified'];
(O/'08_coverage_and_limitations.md').write_text(f'''# Coverage, Evidence Quality, and Limitations

## Scope and authority

This is the final Phase-6 report for **one `fullload` method**, using the eight originally uploaded English Markdown specifications, the original English PDF of 90 physical pages, and the `OrionDesk_One_Pass_Atomic_Evaluation_Protocol` v6.1. All input filenames and record locators use their actual mounted names. The eight Markdown specifications are scored; the protocol document, prior goldsets, and historical scores are not scored source inputs. The PDF alone is authoritative for source-positive obligations and bounded negative counterfactuals.

The original PDF was re-opened, and all {J['source_pdf']['physical_pages']} pages had extractable text. The Phase-1 quote audit accounted for {U['source_positive_atoms']} current scored source atoms; {J['source_pdf']['source_quote_exact_line_normalized_count']} quotations matched independently extracted PDF page text verbatim after whitespace normalization. Three remaining PDF citations refer to visual/laid-out content reviewed in the earlier Phase-1 raster inspection; there are no missing PDF pages. This three-item distinction must not be mistaken for a complete visual semantic recertification in Phase 6.

All eight scored Markdown inputs were readable and hash-matched the Phase-1 manifest. The line-coverage ledger represents **{J['generated_input_coverage']['physical_lines']} physical lines**, and the cell-coverage ledger contains **{J['generated_input_coverage']['table_cell_coverage_rows']} table-cell records**. The checker verifies that generated TP quotations actually occur at their cited original file/line, including table-context locators; a matching string alone does not prove full semantic support.

## Final source and negative-control universes

- The corrected source-positive inventory contains **{U['source_positive_atoms']}** individually scored PDF propositions. Phase 5 retired one non-independent overview atom and split two compound atoms into six more independently testable obligations (a net increase from 1,024 to 1,027). Old/new IDs are preserved in `05_source_atomization_audit_final.jsonl` and `07_change_delta.jsonl`.
- **{U['source_negative_controls']}** controls were predeclared from explicit source exclusions, prohibitions and release deferrals. Their {C['TN']} TNs are only a bounded diagnostic collection: they are *not* all possible absent requirements and do not increase Precision/Recall/F1.
- **{U['unsupported_generated_only_propositions']}** generated-only unsupported predictions and **{U['asserted_negative_controls']}** asserted negative controls were confirmed in the current best-effort ledger. This produces FP={C['FP']} but is **not** independently complete generated-claim verification.
- Exactly **{U['canonical_decision_units']}** distinct units have one actual label, one prediction, and one four-cell assignment. Six canonical-ID collisions between newly split source atoms and negative-control rows were fixed in Phase 6; the correction does not change source or negative-control content.

## TP evidence and FN reciprocal audit

- **{C['TP']}** final TP entries are represented one-to-one in `05_tp_evidence_audit_final.jsonl`, with source/page, generated/line/table, mode (E2/E3), and separate predicate fields. **{J['tp_proof_audit']['generated_direct_quote_locators_verified']}** generated evidence locations were directly validated against unchanged Markdown files. This is locator and bounded predicate validation, **not** exhaustive expert certification of logical entailment.
- The initial FN root ledger has {sum(J['fn_root_causes'].values())} rows, comprising {J['corrected_initial_fn_candidates']} previously corrected matcher false negatives, {J['source_atomization_corrected_parents']} corrected/retired source atomization items, and {C['FN']} final FN decisions. Its final FN dispositions reconcile to **{F.get('PARTIAL_ENTAILMENT',0)} `PARTIAL_ENTAILMENT`**, **{F.get('CONSERVATIVE_UNRESOLVED',0)} `CONSERVATIVE_UNRESOLVED`**, and **{F.get('TRUE_MISSING',0)} `TRUE_MISSING`**.
- **55 additional explicit source-to-generated false negatives** were corrected in Phase 6. The original Phase-2 extractor had missed 20 definitive Markdown clauses; their actual input lines were restored without altering any scored Markdown input. Correction-by-correction proof is in `06_regression_corrections_final.jsonl` and the consolidated `07_change_delta.jsonl`.
- Diagnostic probes were executed for case title, workspace retention-class settings, replaying the same case-creation key, foreign-tenant non-disclosure, ACL, citations, and named event payloads. `06_regression_probes_final.jsonl` records their current TP/FN distributions. The exact normalized quote scanner reports **{J['remaining_exact_quote_fn_exception_count']} remaining full-quote-line FN exceptions**. This does not exclude other contextual false negatives.

## Generated claim validity, duplication and support risk

- There are **{G['eligible_occurrences']}** eligible generated occurrences and **{G['unique_generated_classes']}** provisional semantic classes. The raw excess is **{G['duplicate_excess']}** (within-file {G['within_file_excess']}; across-file {G['across_file_excess']}), yielding **{fmt(M['Duplicate'])}**. Structural partitions reconcile, but meaning-equivalence merging remains best effort.
- Of {G['unique_generated_classes']} classes, **{v}** still have `semantic_certification=NOT_VERIFIED` in their PDF-support audit. Historical labels such as `PDF_ENTAILED` for those classes signify a best-effort classification and **must not be represented as fully verified support**.
- There remain **22** source atoms in the corrected inventory using the pattern `... immutable derivative tracks SHA-256 source/revision provenance`. The original PDF's repeated boilerplate may have been over-atomized into component-specific instances. The source-denominator sensitivity is unresolved; the script does not silently merge or discard source requirements merely to improve scores.
- Sixteen source atoms explicitly mention `Test TST-*` scenarios, some of which may overlap substantive product obligations. Earlier source-atomization adjustments were applied, but exhaustive independent semantic deduplication of test scenarios is not claimed.
- The FP=0 / Precision=100% result is not proof that generated specifications contain no unsupported commitments. Some claims may be over-broad, unapproved, or wrongly treated as adopted; the residual source-support risk is material. The computed Recall={fmt(M['Recall'])} is likewise not certified completeness, and there is no justified statistical confidence interval or guaranteed upper/lower bound.

## Structural validity versus semantic certification

**Structural result: PASS, after Phase-6 repairs.** Input hashes, 90-page extent, line/cell coverage, ID noncollision, generated occurrence/class membership, one canonical four-cell universe, TP/FN evidence-ledger one-to-one relationships, duplicate partitions, and equations reconcile independently. In particular: TP+FN={U['source_positive_atoms']}; TN+asserted negative controls={U['source_negative_controls']}; FP=unsupported-only+asserted negatives={C['FP']}; all four cells={U['canonical_decision_units']}; TP+FP={U['canonical_predicted_positive_units']}, **not** {G['unique_generated_classes']} raw classes.

**Semantic certification: NOT VERIFIED.** Thousands of generated claims and many TP E2 bridges still need deeper expert-level full-predicate corroboration; 55 final FNs remain conservative unresolved cases. Consequently, the run closes at `FINAL_BEST_EFFORT`, not `FINAL_VERIFIED`. This is an honest final deliverable, not a request to repeat an already completed phase.

## Exclusions, paths and delivery

`09_excluded_units.jsonl` retains nonnormative PDF illustrations and nondefinitive Markdown clauses from the extraction stages. `02_generated_line_coverage_final.jsonl` and `02_generated_table_cell_coverage_final.jsonl` provide line/cell-level coverage; `01_pdf_page_coverage_final.jsonl` and `01_pdf_quote_verification_final.jsonl` provide PDF inspection references. The scored inputs were not modified. All final outputs are individual files in `oriondesk_phase6`; **no ZIP/TAR archive** is created under the binding protocol. There is only one evaluated method, so cross-method comparison files are not applicable.
''')

(O/'06_phase6_report.md').write_text(f'''# OrionDesk AI — Phase 6 Closure Report

**Status: `FINAL_BEST_EFFORT`**  
**Protocol: v6.1**  
**Method: fullload**

The sixth and final phase is complete. Independent ledger recomputation produced TP={C['TP']}, TN={C['TN']}, FP={C['FP']}, FN={C['FN']} over {U['canonical_decision_units']} canonical propositions. Precision {fmt(M['Precision'])} is provisional, Recall {fmt(M['Recall'])}, F1 {fmt(M['F1'])}, and duplicate rate {fmt(M['Duplicate'])}.

Phase 6 corrected 55 demonstrably misclassified FN cases, restored 20 explicitly definitive generated claims missed in the Phase-2 extractor, and eliminated six negative-control/source-atom canonical-ID collisions. The corrected positive inventory remains {U['source_positive_atoms']} and the negative-control inventory remains {U['source_negative_controls']}. All individual ledgers and the original inputs are retained.

Independent structural checks passed. The full semantic quality of {J['generated_pdf_support_unverified']:,} generated claims is not certified, so a Precision value of 100% must not be interpreted as perfect generated-specification correctness. The final uncertainty is described in `08_coverage_and_limitations.md`. No later phase is scheduled or implied.
''')
status={'protocol_version':'6.1','method':'fullload','phase':6,'status':'FINAL_BEST_EFFORT','phase_closed':True,'final_phase':6,'structural_verification':'PASSED','semantic_verification':'NOT_VERIFIED','metrics_file':'06_metrics_final.json','uncertified_generated_support_classes':v,'final_fn':C['FN'],'final_tp':C['TP'],'revision_notes':['55 newly corrected matcher false negatives','20 recovered generated definitive occurrences','six duplicate canonical IDs repaired','23 missing method metadata fields populated']}
(O/'06_phase6_status_final.json').write_text(json.dumps(status,indent=2)+'\n')
validation={'status':'PASS_STRUCTURAL_WITH_SEMANTIC_LIMITATIONS','source_of_checks':'Independent compute_metrics.py run over final JSONL ledgers','equations':J['equations'],'coverage':J['generated_input_coverage'],'pdf':J['source_pdf'],'TP_audit':J['tp_proof_audit'],'FN_root':J['final_fn_root_causes'],'duplicate':G,'uncertified_generated_claims':v,'remaining_exact_quote_FN_exceptions':J['remaining_exact_quote_fn_exception_count'],'limitations':'Semantic full-predicate accuracy is not independently certified; the reported confusion matrix is provisional.'}
(O/'06_phase6_validation_final.json').write_text(json.dumps(validation,indent=2)+'\n')
# File manifest for direct individual delivery. No archive.
entries=[]
for f in sorted(O.iterdir()):
 if f.is_file() and f.name!='06_final_output_manifest.json':
  entries.append({'filename':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'English_artifact':True})
(O/'06_final_output_manifest.json').write_text(json.dumps({'protocol_version':'6.1','status':'FINAL_BEST_EFFORT','individual_files':entries,'archive_created':False},indent=2)+'\n')
print(json.dumps({'outputs':len(entries)+1,'report':str(O/'06_metrics_final.md'),'status':'FINAL_BEST_EFFORT'}))

def len_source():return U['source_positive_atoms']
