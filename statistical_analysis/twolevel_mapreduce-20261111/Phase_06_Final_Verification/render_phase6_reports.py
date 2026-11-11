#!/usr/bin/env python3
"""Render English Phase 6 human-readable reports directly from independent JSON metrics."""
from pathlib import Path
import json,hashlib,collections,re
p=Path(__file__).resolve().parent
m=json.loads((p/'06_metrics_final.json').read_text(encoding='utf-8'))
c=m['confusion'];u=m['universe'];dm=m['duplication'];mtr=m['metrics']
pct=lambda k:('undefined' if mtr[k] is None else f'{100*mtr[k]:.2f}%')
allchecks=all(v is True for v in m['verification_checks'].values())
assert allchecks
if not m['status']=='FINAL_BEST_EFFORT':raise AssertionError('Wrong final semantic status')

page=f"""# Phase 6 — Final Independent Metric Recalculation

**Protocol:** `OrionDesk_One_Pass_Atomic_Evaluation_Protocol(6).md` (version 6.1)  
**Method:** `{m['prefix']}`  
**Phase:** 6 of 6 (closed)  
**Final evaluation status:** `FINAL_BEST_EFFORT`  
**Structural recalculation:** PASS  
**Independent semantic certification:** NOT ESTABLISHED

## Independently recomputed results

| Quantity | Value |
|---|---:|
| PDF-positive normative source atoms (`R`) | {u['source_positive_atoms']:,} |
| Fixed PDF-negative controls (`N`) | {u['source_negative_controls']:,} |
| Eligible generated occurrences (`GO`) | {u['generated_positive_occurrences']:,} |
| Raw generated semantic classes (`G`) | {u['raw_generated_claim_classes']:,} |
| Covered source atoms (`A`) | {u['covered_source_atoms']:,} |
| Asserted negative controls (`B`) | {u['asserted_negative_controls']:,} |
| Distinct unsupported generated-only propositions (`F`) | {u['unsupported_generated_only_propositions']:,} |
| Canonical predicted positives (`P`) | {u['canonical_predicted_positive_units']:,} |
| Total enumerated canonical decisions (`U`) | {u['canonical_decision_units']:,} |

| Cell | Actual label | Predicted label | Recomputed |
|---|---:|---:|---:|
| TP | 1 | 1 | **{c['TP']:,}** |
| TN | 0 | 0 | **{c['TN']:,}** |
| FP | 0 | 1 | **{c['FP']:,}** |
| FN | 1 | 0 | **{c['FN']:,}** |

| Metric | Current best-effort result | Exact numerator/denominator |
|---|---:|---|
| Precision | **{pct('Precision')}** | {c['TP']} / ({c['TP']} + {c['FP']}) |
| Recall | **{pct('Recall')}** | {c['TP']} / ({c['TP']} + {c['FN']}) |
| F1 | **{pct('F1')}** | 2 × {c['TP']} / (2 × {c['TP']} + {c['FP']} + {c['FN']}) |
| Duplicate | **{pct('Duplicate')}** | ({u['generated_positive_occurrences']} − {u['raw_generated_claim_classes']}) / {u['generated_positive_occurrences']} |

These are conventional Precision, Recall, and F1 on the **effective canonical proposition universe**, not raw occurrence or raw semantic-class precision. A source-wide generated rule can independently satisfy multiple distinct PDF atoms without multiplying generated occurrences. Duplicate is separately defined using only raw generated occurrences and classes.

## One-universe reconciliation

- `TP + FN = {c['TP']} + {c['FN']} = {u['source_positive_atoms']} = |R|`.
- `TN + |B| = {c['TN']} + {u['asserted_negative_controls']} = {u['source_negative_controls']} = |N|`.
- `FP = |B| + |F| = {u['asserted_negative_controls']} + {u['unsupported_generated_only_propositions']} = {c['FP']}`.
- `TP + TN + FP + FN = {sum(c.values())} = |R| + |N| + |F| = {u['canonical_decision_units']}`.
- `TP + FP = {u['canonical_predicted_positive_units']} = |P|` (not necessarily `|G| = {u['raw_generated_claim_classes']}`).
- `GO − G = {dm['duplicate_excess_occurrences']}` and `within-file {dm['within_file_excess']} + across-file {dm['across_file_excess']} = {dm['duplicate_excess_occurrences']}`.

The negative-control inventory comprises only **{u['source_negative_controls']} predeclared PDF-grounded counterfactuals**. Its {c['TN']} TNs are not an estimate of all nonexistent requirements. Adding more unasserted negative controls could increase TN but not these Precision/Recall/F1 values.

## Duplicate metrics

| Raw occurrence/class measure | Independently counted |
|---|---:|
| Eligible generated occurrences | {u['generated_positive_occurrences']:,} |
| Distinct raw semantic classes | {u['raw_generated_claim_classes']:,} |
| Excess occurrences | {dm['duplicate_excess_occurrences']:,} |
| Within-file excess | {dm['within_file_excess']:,} |
| Across-file excess | {dm['across_file_excess']:,} |
| Repeated classes | {dm['repeated_claim_class_count']:,} |
| Repeated classes spanning multiple files | {dm['repeated_classes_spanning_files']:,} |

Classification follows actual file, line and table-cell location order. The 18 definitive occurrences recovered in Phase 3 are included in GO and G membership: `3792 + 18 = 3810`.

## Independent provenance and proof checks

- All **90** physical PDF pages are present; PDF SHA-256 `{m['pdf_verification']['sha256']}` agrees with Phase 1.
- All **8** actual Markdown inputs match their Phase 1 hashes; Phase 2 coverage ledgers enumerate every nonblank line, including table context.
- **{m['pdf_verification']['pdf_quote_text_matches']:,}** PDF-text evidence quotes match the original physical pages; **{m['pdf_verification']['embedded_figure_text_locators']}** additional figure-only locators are from the embedded illustration on physical page 8.
- **{m['tp_proof_audit']['tp_records']}** final TP records have corresponding proof-audit entries, including **{m['tp_proof_audit']['e3_direct']} E3 direct** and **{m['tp_proof_audit']['e2_logical_bridge']} E2 logical-bridge** decisions.
- **{m['tp_proof_audit']['generated_evidence_quotes_checked_on_original_lines']:,}** TP generated quotation locators agree with the actual original Markdown lines.
- **{m['fn_candidate_review']['initial_fn_candidates']}** initial candidate FN records are accounted for: **{m['fn_candidate_review']['candidate_false_negatives_corrected_to_tp']}** corrected to TP and **{c['FN']}** remaining FN records, each with a documented disposition and a Phase 6 corpus-wide reciprocal search.
- **{u['raw_generated_claim_classes']}** generated classes, **{u['generated_positive_occurrences']}** occurrences, and their one-class-per-occurrence mapping reconcile exactly.

## Evidence-quality boundary

The arithmetic is independently reproduced and the cited passages physically exist, but the **semantic outcomes remain best-effort**. Specifically:

- {m['tp_proof_audit']['e2_logical_bridge']} TP records use E2 bridges which are not independent human-reviewed entailment certifications.
- {m['fn_root_causes'].get('PARTIAL_ENTAILMENT',0)} final FN are partially entailed, and {m['fn_root_causes'].get('CONSERVATIVE_UNRESOLVED',0)} remain conservatively unresolved. They are not all proven missing requirements.
- The generated-class validity ledger contains {m['generated_validity']['support_grades'].get('E1_BEST_EFFORT',0):,} E1-grade entries with incomplete independent semantic proof. **FP=0 and Precision=100% must not be interpreted as proof that no generated claim is unsupported.**
- The source-atomization inventory retains context-dependent review decisions, including high-level summary/normativity-boundary cases, without adjusting the shared denominator to favor this method.
- Duplication depends on conservative semantic-class equivalence decisions and can change after independent semantic adjudication.

**Reproduction:** From this output directory run `python compute_metrics.py`. The checker reads the final item-level JSONL ledgers, original uploaded inputs and PDF; recomputes every equation; verifies PDF/Markdown evidence locations; writes `06_metrics_final.json` and `06_independent_validation_final.json`; and fails on detectable structural contradictions. The checker does not claim to prove human-level semantic correctness.

**Final stop rule:** All six phases are complete. No Phase 7 exists and no archive was created.
"""
(p/'06_metrics_final.md').write_text(page,encoding='utf-8')

input_rows=[]
for row in json.loads((p/'01_input_manifest_final.json').read_text(encoding='utf-8'))['scored_inputs']:
 input_rows.append(f"| `{row['input_role']}` | `{row['actual_filename']}` | {row['physical_lines']} | `{row['sha256']}` |")
fn_examples=[]
for x in (json.loads(l) for l in (p/'03_fn_root_cause_audit_final.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()):
 if x['final_scoring_cell']=='FN':
  fn_examples.append(x)
fn_sample_rows=[f"| `{x['source_id']}` | `{x['fn_review_disposition']}` | {len(x['best_generated_candidates'])} |" for x in fn_examples[:10]]

coverage=f"""# Phase 6 — Coverage, Semantic Reliability and Limitations

**Final status:** `FINAL_BEST_EFFORT` — completed six-phase evaluation, not independently certified semantic correctness.  
**Source of truth:** 90-page original English OrionDesk AI Detailed Application Design Specification, `OD-AI-DDS-001`, baseline `R1.0 / revision 1.3`.  
**Method scope:** One current eight-file Markdown set; no other method was scored in this run.  
**Evaluation protocol:** Version 6.1.

## 1. Verified input scope and coverage

The authoritative PDF `{json.loads((p/'01_input_manifest_final.json').read_text())['authoritative_pdf']['actual_filename']}` has **90 physical pages**, all represented in `01_pdf_page_coverage_final.jsonl`. SHA-256 equals `{m['pdf_verification']['sha256']}` and is byte-identical to the previously used `fullload_cal` PDF source. The original `fullload_cal` source-positive and fixed-negative inventories were reused. The original source denominator is not derived from any previous score or aggregate JSON.

| Scored document role | Actual unmodified input filename | Physical lines | SHA-256 |
|---|---|---:|---|
"""+'\n'.join(input_rows)+f"""

The instruction document is not a ninth scored Markdown file. Original file names and physical-line locators are retained in evidence records. All eight input hashes and the recorded per-line inspection coverage were verified independently. The PDF contains **{m['pdf_verification']['pdf_quote_text_matches']}** verified text evidence quotations plus **{m['pdf_verification']['embedded_figure_text_locators']}** figure-only assertions from page 8. Seven selected source pages (8, 23, 83, 85, 86, 87, 89) were additionally rendered for figure/table inspection; this visual spot check is distinct from the all-page text coverage ledger.

The generated corpus has **{u['generated_positive_occurrences']}** definitive occurrences: **{m['input_coverage']['original_generated_occurrences']}** from the Phase 2 occurrence ledger plus **{m['input_coverage']['recovered_generated_occurrences']}** recovered after an exclusion-eligibility challenge. They map to **{u['raw_generated_claim_classes']}** semantic classes, with an actual-file/line/table-cell locator per occurrence. **{m['input_coverage']['source_exclusion_records']}** source exclusions and **{m['input_coverage']['generated_exclusion_records']}** generated nondefinitive units are preserved in `09_excluded_units.jsonl`.

## 2. Final measured four-cell universe and its limits

| Canonical unit | Actual label | Predicted label | Count |
|---|---|---|---:|
| PDF-positive fully entailed (`TP`) | 1 | 1 | {c['TP']} |
| PDF-positive not fully demonstrated (`FN`) | 1 | 0 | {c['FN']} |
| PDF-negative counterfactual asserted (`FP` subset) | 0 | 1 | {u['asserted_negative_controls']} |
| Unsupported generated-only definite propositions (`FP` subset) | 0 | 1 | {u['unsupported_generated_only_propositions']} |
| Fixed PDF-negative counterfactual not asserted (`TN`) | 0 | 0 | {c['TN']} |

The canonical decision ledger has **{u['canonical_decision_units']}** units, and all four cells reconcile to that single enumerated universe. `TP + FN = {u['source_positive_atoms']}`; `TN + asserted controls = {u['source_negative_controls']}`; `FP = asserted controls + generated-only unsupported classes`. The tested negative controls are a small, explicit and predetermined PDF-grounded set; TN is **bounded diagnostic evidence**, not a universal true-negative population.

Conventional effective-universe Precision is **{pct('Precision')}**, Recall **{pct('Recall')}**, F1 **{pct('F1')}**. These are **provisional evidence-grounded adjudication rates**. The raw-class positive count and the effective canonical positive count differ because generated universal statements can entail several independently meaningful PDF atoms; it would be mathematically wrong to force `TP + FP = G`. An unmatched generated class is not automatically an FP.

## 3. FN root causes, corrections and reciprocal retrieval

All **{m['fn_candidate_review']['initial_fn_candidates']}** source atoms initially nominated as FN during the earlier matching stage have preserved root-cause records. **{m['fn_candidate_review']['candidate_false_negatives_corrected_to_tp']}** were subsequently corrected to TP (415 during the source coverage stage and {m['change_deltas']['FN_TO_TP_ENTAILMENT_CORRECTION']} during the correction stage). The final FN set is **{c['FN']}**, precisely:

| Final FN disposition | Count | Interpretation |
|---|---:|---|
| `TRUE_MISSING` | {m['fn_root_causes'].get('TRUE_MISSING',0)} | Verified missing within scored corpus after checks |
| `PARTIAL_ENTAILMENT` | {m['fn_root_causes'].get('PARTIAL_ENTAILMENT',0)} | Related specification text exists, but one or more complete predicates are unproven |
| `CONSERVATIVE_UNRESOLVED` | {m['fn_root_causes'].get('CONSERVATIVE_UNRESOLVED',0)} | Accessible evidence is ambiguous after bounded candidate inspection; no verified absence claim |

The entire set of **{c['FN']} final FN** has undergone another Phase 6 source-key/alias scan of every scored Markdown file. Actual generated line candidates are saved to `06_fn_reciprocal_recheck_final.jsonl`, and `03_fn_root_cause_audit_final.jsonl` was supplemented with the real lookup terms and audit references. This resolves an evidence-recording gap found during the Phase 6 independent check; the scoring cells themselves did not change. No final FN was identified by a contiguous exact full-statement match in the corpus. That check is diagnostic: equivalent paraphrases or multi-file bridges can still be missed.

Representative final FN records (not the full ledger):

| Source atom | Disposition | Original reviewed candidates |
|---|---|---:|
"""+'\n'.join(fn_sample_rows)+f"""

The full **{c['FN']}** record-level dispositions are in `03_fn_root_cause_audit_final.jsonl`; these examples do not replace the complete audit.

## 4. TP full-predicate proof limitations

Each of the **{c['TP']}** final TP atoms has a source/target link in `05_tp_evidence_audit_final.jsonl`. They split into **{m['tp_proof_audit']['e3_direct']} E3 direct** and **{m['tp_proof_audit']['e2_logical_bridge']} E2** claims. E2 bridge types are:

| Entailment bridge | TP atoms |
|---|---:|
| `UNIVERSAL_INSTANTIATION` | {m['tp_proof_audit']['bridge_modes'].get('UNIVERSAL_INSTANTIATION',0)} |
| `INHERITED_CONTEXT` | {m['tp_proof_audit']['bridge_modes'].get('INHERITED_CONTEXT',0)} |
| `CONJUNCTIVE_BRIDGE` | {m['tp_proof_audit']['bridge_modes'].get('CONJUNCTIVE_BRIDGE',0)} |
| `SEMANTIC_EQUIVALENCE` | {m['tp_proof_audit']['bridge_modes'].get('SEMANTIC_EQUIVALENCE',0)} |

All **{m['tp_proof_audit']['generated_evidence_quotes_checked_on_original_lines']}** cited generated quotation locations were checked against unchanged original Markdown line text. Nonetheless, many predicate-check maps contain an explicit `not-applicable`/`null` field justified by broad contextual assumptions, and many E2 proofs are machine-assisted, not independent expert semantic review. **No TP has been certified as a human-verified full-predicate proof across all applicability conditions.** The report therefore does not promote Phase 5's `BEST_EFFORT` cells to `VERIFIED` merely because original citations exist.

High-risk areas for further independent human review include inherited role and resource authorization, approval-versus-publication, request acceptance-versus-completion, retry/timeout semantics, aggregate revision concurrency, and exact API method/status/table contexts. This is a risk categorization, not a claim that those individual TPs have failed.

## 5. Generated-only correctness and FP uncertainty

The generated claim validity ledger includes **{u['raw_generated_claim_classes']}** classes: **{m['generated_validity']['classes_by_status'].get('PDF_ENTAILED',0)}** provisionally labeled `PDF_ENTAILED`, **{m['generated_validity']['classes_by_status'].get('SUPPORTED_NONCOVERING',0)}** labeled `SUPPORTED_NONCOVERING`, and **{m['generated_validity']['classes_by_status'].get('PDF_UNSUPPORTED',0)}** definitively labeled `PDF_UNSUPPORTED`. Their evidence grades are **{m['generated_validity']['support_grades'].get('E3',0)} E3**, **{m['generated_validity']['support_grades'].get('E2',0)} E2**, and **{m['generated_validity']['support_grades'].get('E1_BEST_EFFORT',0)} E1_BEST_EFFORT**.

**This is the main reliability limitation:** {m['generated_validity']['support_grades'].get('E1_BEST_EFFORT',0)} classes lack independently certified full-source support, even though the ledger has not positively isolated an unsupported residual proposition. Therefore **FP=0 is an unproven best-effort estimate** and **Precision=100% must not be reported as verified correctness**. Fully supported noncovering classes require affirmative PDF entailment, not simply topical similarity. The current corpus includes short table cells that were checked with inherited row/column context; some may require more independent review.

## 6. Source atomization audit

The frozen source inventory contains **{u['source_positive_atoms']}** source positives and **{u['source_negative_controls']}** fixed negatives, identical across the intended method-comparison basis. All {u['source_positive_atoms']} positive atoms have a Phase 5 atomization decision. The dispositions are:

| Atomization decision | Count |
|---|---:|
"""
for k,v in sorted(m['source_atomization']['dispositions'].items()):coverage+=f'| `{k}` | {v} |\n'
coverage+=f"""

Two PDF line-wrap corrections restore the literal endpoint `/v1/workspaces/{{workspaceId}}/members` in source atom normalization without replacing the original PDF quotes or changing source IDs or the denominator. This was independently visualized on **physical page 23**. The source count delta is **{m['source_atomization']['source_count_delta']}**. One high-level summary and two normativity-boundary cases remain explicitly uncertain; the retained parent/child and common-boilerplate analyses are *best-effort*, not certified proof that 1,024 is the uniquely correct atomic denominator. Any future correction must be applied across all evaluated methods.

The Phase 5 change ledger records **{m['change_deltas']['FN_TO_TP_ENTAILMENT_CORRECTION']}** FN-to-TP corrections, **{m['change_deltas']['GENERATED_SEMANTIC_CLASS_MERGE']}** generated semantic-class merges, **{m['change_deltas']['TP_EVIDENCE_RELINK_NO_SCORE_CHANGE']}** TP-evidence relinks, and **{m['change_deltas']['SOURCE_LINE_WRAP_CORRECTION']}** source line-wrap fixes. Each category has case-level entries in `07_change_delta.jsonl`.

## 7. Raw semantic duplication and its scope

The duplication formula is `(GO − G) / GO`, using raw occurrence and class counts rather than expanded source coverage. Final raw Duplicate = **{pct('Duplicate')}**, with excess occurrences **{dm['duplicate_excess_occurrences']}**, across-file **{dm['across_file_excess']}**, within-file **{dm['within_file_excess']}**, repeated classes **{dm['repeated_claim_class_count']}**, and multi-file repeated classes **{dm['repeated_classes_spanning_files']}**.

The 23 Phase 5 class merges correct only the pairs that were adjudicated. Other semantically equivalent paraphrases may remain separate classes; this can understate duplication. Conversely, erroneous merges of slightly different actor/condition/outcome predicates would overstate duplication. The value is therefore reproducible for these ledger decisions but is not guaranteed to be unique under all reasonable interpretations.

## 8. Verification matrix and regression probes

The independent checker verifies all raw occurrence-class relationships, unique IDs, source and negative identities, exact four-cell equations, raw duplication partition, original eight-file hashes and recorded nonblank line coverage, PDF 90-page coverage and quotation pages, 979 TP audit entries and 45 FN root-cause records. It also crosschecks all 37 negative controls and validates source line-wrap and class-change delta relationships.

`06_regression_probes_final.jsonl` records full-corpus keyword and actual-location probes for: case title, workspace retention class, repeated same-key case creation, `/members` after PDF wrapping, case revision `If-Match`, `ApprovalDecisionRecorded` and separate publication, and cross-tenant denial. The probes are retrieval diagnostics, **not automatic semantic proof**. Every final FN was reciprocally re-searched and recorded in `06_fn_reciprocal_recheck_final.jsonl`.

The three pages 23, 83, and 85–87 provide especially important register/table inheritance cases; page 89 provides verification-test overlap. The checker confirmed the PDF bytes and text citations on their actual physical page, rather than using a derived summary as source authority.

## 9. Overall confidence and stop rule

**Structural confidence:** The enumerated ledger and all stated arithmetic invariants reconcile; every scored input is present and unchanged; source and generated evidence locators exist.  
**Semantic confidence:** `BEST_EFFORT`, not externally certified. The 34 conservative FN, 11 partial FN, 964 machine-adjudicated E2 TPs, 3,218 E1-grade generated-class validity records, and source atomization boundary cases limit interpretation. These uncertainties may move Precision, Recall, F1 or Duplicate in either direction; no error interval or guaranteed lower bound is claimed.  
**Production meaning:** This is an evaluation of generated specification coverage against one controlled fictional PDF; it is not a measurement of deployed software, security enforcement, production availability or provider accuracy.  
**Comparisons:** No comparison artifact is created because only one complete eight-file set was explicitly selected for scoring in this run.  
**Completion:** All six requested phases are closed. No archive is created; all JSONL, JSON, Markdown and Python outputs are individually available.

## Reproducibility

Execute `python compute_metrics.py` from this output directory with the unchanged original inputs mounted in the parent directory. The checker independently recomputes and rewrites the metrics and validation JSON files. `06_recheck_fn_retrieval.py` documents the additional full-corpus FN retrieval audit introduced in Phase 6. Full source and generated ledgers remain in their documented filenames. The original eight scored Markdown inputs are never rewritten.
"""
(p/'08_coverage_and_limitations.md').write_text(coverage,encoding='utf-8')

status={
 'phase':6,'phase_status':'PHASE_COMPLETED_BEST_EFFORT','evaluation_status':'FINAL_BEST_EFFORT',
 'all_six_phases_closed':True,'all_structural_assertions_passed':allchecks,
 'independently_computed_metrics_file':'06_metrics_final.json',
 'standalone_recomputation_script':'compute_metrics.py',
 'source_requirement_inventory_reused':True,
 'source_ledger_denominator_changes':m['source_atomization']['source_count_delta'],
 'semantic_certification':'NOT_INDEPENDENTLY_VERIFIED',
 'input_count':u['source_positive_atoms'],
 'notes_en':'Final means six-phase process complete; best-effort metrics retain semantic uncertainty, including generated-class E1 support.'
}
(p/'06_phase_status_final.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
print('Wrote reports',len(page),'and',len(coverage),'characters')
