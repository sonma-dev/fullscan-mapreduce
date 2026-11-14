# Phase 6 Coverage, Verification and Limitations

**Final status:** `FINAL_BEST_EFFORT`. **Protocol:** 6.1. **Scope:** one complete set of eight generated Markdown specifications; original PDF is the sole normative authority.

## Input Scope and Inspection

- Original authoritative PDF: 90 physical pages, present and readable. The preceding Phase 1 recorded 90 page-coverage entries; this phase checked the PDF again and performed independent quotation-location checks.
- Scored generated Markdown: eight actual files, 8,330 physical text lines, including source tables and DDL/code contexts. Earlier Phase 2 reported all substantive line/cell inspection; Phase 6 independently confirmed all files and original line locations.
- Original source-positive and negative-control JSONL files supplied by the user were preserved. The phase-corrected source positive inventory has 1,024 meaningful atoms, and the fixed negative inventory has 37 controls.

| Actual scored Markdown filename | Physical lines |
|---|---:|
| `01_screen_functions(1).md` | 864 |
| `02_api(1).md` | 1,201 |
| `03_data(1).md` | 1,034 |
| `04_batch_functions(1).md` | 1,323 |
| `05_business_rules(2).md` | 1,442 |
| `06_exception_handling(3).md` | 737 |
| `07_processing_flows(2).md` | 1,143 |
| `08_architecture_decision(2).md` | 586 |

## Final Canonical Performance (Provisional)

- TP 680, TN 37, FP 426, FN 344; U=1,487.
- Effective-universe Precision **61.48%**, Recall **66.41%**, F1 **63.85%**.
- Raw-class Duplicate **2.40%**; GO=3,746, GC=3,656, excess=90 (8 within-file + 82 across-file).
- A shared or universal generated rule can support multiple independent source atoms when its full applicability bridge holds. Therefore TP + FP = P is **not** generally equal to raw GC. Treating GC as the Precision denominator would mix two different scoring units.
- TN is limited to 37 PDF-grounded, predeclared forbidden/deferred counterfactuals. It is not population-wide true-negative accuracy.

## Independent Source and Evidence Audits

False-negative recovery and best effort semantic checks are tracked with explicit evidence, not inferred from successful arithmetic.

- PDF quote references: 2,527, across the corrected PDF-positive ledger. Normalized PDF-extracted-text substring matches: **2,414**; raster/figure visual confirmation required: **3**; PDF layout or text quotation not directly matched by this extraction technique: **110**. Nonmatching text spans may be benign PDF wrapping, table reconstruction, or inaccurate extraction and are not independently certified by this check.
- Every final TP has one audit entry with original PDF evidence, generated source-file/physical-line evidence and ten predicate-check categories. **680 / 680** records are present, including newly corrected matches. A predicate checklist and correctly located original lines do not mechanically prove the logical implication.
- Final FN root causes: **20** `TRUE_MISSING`; **243** `PARTIAL_ENTAILMENT`; **81** `CONSERVATIVE_UNRESOLVED` (total 344). These three categories are not equivalent to proven absence. All terminal FNs have reverse-search candidate evidence and explicit source IDs.
- Across the historical candidate-FN audit, **416** candidates were corrected to TP; the ledger also records one removed/merged source context item. These are audit candidates, not additional source atoms.
- Phase 5 source atomization changes: one redundant architecture-context parent removed, one compound obligation split into two independent PDF atoms, and one normative/example mixture narrowed. Old/new source atom IDs appear in `07_change_delta.jsonl`. No further denominator manipulation occurred during Phase 6.
- Phase 6 specifically corrected **34** explicit PDF/Markdown false negatives; reclassified **13** FP candidates as PDF-supported noncovering, and excluded **12** nondefinitive explanation/status assertions. See `06_phase6_corrections_summary.json`.
- Source-to-generated diagnostic regression probes for the case title field, workspace retention class, duplicate same-key case creation/identical response, physical DDL, and event payloads are in `06_exact_match_regression_probes_final.jsonl`. Remaining normalized direct quote-in-line FN alerts: **0**. This does not prove all remaining semantic alternatives were found.

## Generated Claim Validity and False Positive Boundaries

Each of the 3,656 retained generated classes has one validity record; the final 426 generated-only unsupported propositions have actual original Markdown evidence and a bounded PDF reverse-candidate review. Claims labeled `SUPPORTED_NONCOVERING` are PDF-supported smaller/restated requirements without a complete independently scored R coverage bridge; they are not automatically FP. Some FP classifications remain conservative due to PDF layout, missing complete conditions, unresolved design status, or insufficient semantic evidence.

The generated `Needs confirmation`, `TBD`, `Proposal`, and unadopted options are not final implementation commitments. The raw class and excluded-unit ledgers distinguish them; the existence of a requirement field or a source PDF discussion does not authorize a guessed API schema, provider, or production setting.

## Independent Recomputability and Final Stop Rule

Run `python compute_metrics.py --directory /mnt/data/phase6` from an environment containing the current original files. The program reads the final item-level ledgers, recomputes R/N/A/B/F, all four confusion cells, duplication, class membership, FN and TP audit coverage, and original input line/file presence. Its structural audit finished with **zero errors**. Optional source evidence and semantic checks do not turn this into an external ground-truth certification.

- The current final labels are **best-effort semantic judgments**, not a verified measure of application correctness or production safety. Recall may be understated by undetected E2/universal matches or overstated by permissive contextual entailment; source atomization could also change the denominator.
- The source PDF's numeric targets are assumptions for a fictional design, not measured operating values. No production results should be inferred from the evaluation.
- The method is identified as `single_supplied_set` because one complete eight-file set was provided. No cross-method comparison is warranted or produced.
- All authored deliverables are English. No archive was created. Phase 6 closes the six-turn protocol under `FINAL_BEST_EFFORT`, rather than repeating a phase to chase subjective disambiguation.
