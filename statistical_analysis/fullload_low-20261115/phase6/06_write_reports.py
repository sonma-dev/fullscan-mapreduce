#!/usr/bin/env python3
"""Render Phase-6 English reports from independently recomputed, item-level ledgers."""
from pathlib import Path
import json
from collections import Counter
P=Path(__file__).resolve().parent
m=json.loads((P/'06_metrics_final.json').read_text(encoding='utf-8'))
p5=json.loads(Path('/mnt/data/oriondesk_phase5/04_confusion_matrix_final.json').read_text(encoding='utf-8'))

def pct(x):return ('N/A' if x is None else f'{100*x:.2f}%')

def write(n,txt):
 (P/n).write_text(txt.strip()+'\n',encoding='utf-8')

def md_table(headers,rows):
 return '| '+' | '.join(headers)+' |\n|'+ '|'.join('---' for _ in headers)+'|\n' + '\n'.join('| '+' | '.join(map(str,row))+' |' for row in rows)

c=m['confusion'];u=m['universe'];d=m['duplicate_metrics'];a=m['audit'];cover=m['coverage']
mc=md_table(['Cell','Actual','Predicted','Count'],[['TP',1,1,c['TP']],['FN',1,0,c['FN']],['FP',0,1,c['FP']],['TN',0,0,c['TN']],['Total','—','—',u['canonical_decision_units']]])
metrics=md_table(['Metric','Exact decimal','Display'],[
 ['Precision',f"{m['metrics']['Precision']:.12f}",pct(m['metrics']['Precision'])],
 ['Recall',f"{m['metrics']['Recall']:.12f}",pct(m['metrics']['Recall'])],
 ['F1',f"{m['metrics']['F1']:.12f}",pct(m['metrics']['F1'])],
 ['Semantic duplicate rate',f"{m['metrics']['Duplicate']:.12f}",pct(m['metrics']['Duplicate'])]])

write('04_confusion_matrix_final.json',json.dumps({
 'protocol_version':'6.1','method':m['method'],'phase':6,'status':m['status'],
 'universe':u,'confusion':c,'metrics':m['metrics'],
 'class_validity_counts':a['generated_validity_counts'],
 'fn_root_causes':a['final_FN_root_cause_counts'],
 'evidence_certification':'NOT_CERTIFIED',
 'reconciliation':'Independent item-level recomputation with all structural checks passing; see 06_metrics_final.json',
 'note_en': 'FP denotes source-unsupported generated-only canonical propositions under conservative adjudication, not necessarily a proven design defect.'
 },ensure_ascii=False,indent=2))
write('04_confusion_matrix_final.md',f"""
# Phase 6 — Final Best-Effort Canonical Four-Cell Matrix

**Status:** `{m['status']}`  
**Protocol:** 6.1  
**Evaluated method:** `supplied_set_01` (one complete attached eight-file set)  
**Source of counts:** Final canonical judgment rows, recomputed by `compute_metrics.py`. No historical total is used as input.

{mc}

{metrics}

**Universe:** `R={u['source_positive_atoms']}`, `N={u['bounded_negative_controls']}`, `F={u['generated_only_unsupported_propositions']}`, `B={u['asserted_negative_controls']}`, and `|U|={u['canonical_decision_units']}`. `|P|=TP+FP={u['canonical_predicted_positive_units']}`.

```text
TP + FN = {c['TP']} + {c['FN']} = {u['source_positive_atoms']} = |R|
TN + |B| = {c['TN']} + {u['asserted_negative_controls']} = {u['bounded_negative_controls']} = |N|
FP - |B| = {c['FP']} - {u['asserted_negative_controls']} = {u['generated_only_unsupported_propositions']} = |F|
|U| = |R| + |N| + |F| = {u['source_positive_atoms']} + {u['bounded_negative_controls']} + {u['generated_only_unsupported_propositions']} = {u['canonical_decision_units']}
|P| = TP + FP = {c['TP']} + {c['FP']} = {u['canonical_predicted_positive_units']}
```

This is **one effective proposition universe**, not a union of source-side coverage counts with an unrelated raw generated-class denominator. The raw generated class count `{u['raw_generated_classes']}` does **not** equal canonical predicted-positive count `{u['canonical_predicted_positive_units']}` and is not forced to do so. The 37 negative controls are a bounded original-PDF-grounded diagnostic set; their TN count does not describe all absent features.

**Certification limitation:** Structural arithmetic is reproducible. Full semantic correctness of all E2/E3 bridges, source atomization decisions, and PDF-unsupported classifications has not been independently certified. The scores are `FINAL_BEST_EFFORT`, not verified implementation quality or production performance.
""")
write('05_duplicate_metrics_final.json',json.dumps(d,ensure_ascii=False,indent=2))
write('05_duplicate_metrics_final.md',f"""
# Final Raw Generated Semantic Duplication

**Status:** `{m['status']}`. Raw generated duplicates are independent of the expanded source-coverage projection.

{md_table(['Quantity','Count'],[['Definitive eligible occurrences `GO`',d['eligible_generated_occurrences']],['Raw canonical classes `G`',d['raw_unique_generated_classes']],['Excess occurrences',d['duplicate_excess_occurrences']],['Within-file excess',d['within_file_excess']],['Across-file excess',d['across_file_excess']],['Repeated classes',d['repeated_claim_class_count']],['Repeated classes spanning multiple input files',d['repeated_classes_across_files']]])}

Duplicate = `(GO - G) / GO` = `({d['eligible_generated_occurrences']} - {d['raw_unique_generated_classes']}) / {d['eligible_generated_occurrences']}` = **{pct(d['duplicate_rate'])}**.

The within-file and across-file partitions are independently derived by sorting each class's occurrences by actual input-file order, physical line and table cell, selecting the earliest representative, and classifying subsequent excess occurrences. This semantic-class rate may still undercount paraphrases that have not been safely merged. It is not the proportion of duplicated PDF-positive atoms.
""")

fn=a['final_FN_root_cause_counts']
valid=a['generated_validity_counts']
probes=a['regression_probes']
probe_table=md_table(['Probe','Source ID','Original input','Result'],[[x['probe'],x['source_id'],x['original_file'],'PASS' if x['passed'] else 'FAIL'] for x in probes])
input_table=md_table(['Role / supplied input','Physical lines'],[
 [fn,len((Path('/mnt/data')/fn).read_text(encoding='utf-8').splitlines())] for fn in cover['scored_markdown_files']])
write('08_coverage_and_limitations.md',f"""
# Coverage, Evidence Quality, and Limitations — Phase 6

## Scope and final status

- **Protocol:** OrionDesk Six-Turn Semantic-Entailment Atomic Requirement Evaluation Protocol, version 6.1.
- **Method:** `supplied_set_01` (one unambiguously mapped eight-document set; no cross-method comparison is applicable).
- **Final status:** `{m['status']}`. All six phases were closed once, and this phase is complete. Full-predicate independent semantic certification is **NOT** claimed.
- **Authoritative requirements:** Original 90-page English `OrionDesk_AI_Detailed_Design_Specification(10).pdf` only. The eight scored Markdown files are generated outputs, not authorities for source requirements.
- **Original files were not modified.** Final deliverables are English-language individual files; no archive is supplied.

## Physical source and input coverage

The original PDF contains exactly **{cover['pdf_physical_pages']} physical pages**. Every page yielded readable text in the final PyMuPDF check ({cover['pdf_readable_pages']}/90). The exact English source quotation for **{cover['pdf_positive_exact_page_quote_matches']} of {u['source_positive_atoms']}** retained PDF-positive atoms was found on its recorded original physical page. This verifies quotation location, not the claim's normative force or optimal atomization. Figures, tables, original page layout and reference diagrams were considered in the earlier page-level audit; a separate full independent multimodal human audit is not claimed.

{input_table}

The original eight scored Markdown files contain **{cover['markdown_lines']:,} physical lines** and the Phase-2 coverage ledger contains **{cover['line_coverage_records']:,} physical line dispositions** with no omitted line. The Phase-2 table parser counted **6,308 table-cell positions** (a parser-specific measure; naïve pipe splitting is not an equivalent cell count). The Phase-6 recomputation reopened every used original generated line and confirmed **{cover['tp_original_generated_quote_checks']} source-line quote matches** among final TP proofs. All **{cover['tp_pdf_locator_checks']} TP PDF evidence page references** were within 1–90.

## Canonical universe and arithmetic

{mc}

`|R|={u['source_positive_atoms']}`; `|N|={u['bounded_negative_controls']}`; `|F|={u['generated_only_unsupported_propositions']}`; `|B|={u['asserted_negative_controls']}`. Therefore `|U|=|R|+|N|+|F|={u['canonical_decision_units']}`. The bounded negative controls include only explicit PDF prohibitions, exclusions or release deferrals and do not represent the population of all possible negatives.

{metrics}

A single universal generated rule can cover several independently testable PDF-positive requirements when its scope and conditions fully apply. Thus TP is **not** required to equal the number of raw generated classes. In this method `|GO|={u['raw_generated_occurrences']}`, `|G|={u['raw_generated_classes']}`, whereas effective predicted-positive canonical units `|P|={u['canonical_predicted_positive_units']}`. Do not use raw class-level denominators for conventional Precision, Recall or F1.

## FN correction, remaining root causes and source atomization

- Initial Phase-3 FN candidates reviewed: **{a['initial_FN_candidates_audited']}** records, including later corrected cases and removed source parents.
- Corrected initial matcher false negatives across Phases 3, 5 and 6: **{a['corrected_matcher_false_negative_rows']}**. Phase 6 identified and corrected **10 additional explicit full-predicate matches** found during independent high-risk and regression review, documented in `06_phase6_corrected_retrieval_matches.jsonl`. Corresponding source-to-generated, bridge, FN, TP, validity, judgment and class metadata records were reconciled.
- Source atomization audit: **{a['source_atomization_review_rows']}** decisions; **{a['source_atomization_removed_atoms']}** nonindependent parent/summary atoms removed in Phase 5 with prior/replacement IDs and original PDF quotations. The common positive inventory is **{u['source_positive_atoms']}** after these changes, not a historical fixed total of 1,024.
- Final FN total: **{c['FN']}**. The dispositions remain deliberately distinct:

{md_table(['Final FN root-cause disposition','Count','Interpretation'],[['TRUE_MISSING',fn.get('TRUE_MISSING',0),'A scored-corpus obligation remains absent under recorded search.'],['PARTIAL_ENTAILMENT',fn.get('PARTIAL_ENTAILMENT',0),'Related definitive commitment exists but a substantive predicate is missing.'],['CONSERVATIVE_UNRESOLVED',fn.get('CONSERVATIVE_UNRESOLVED',0),'Full entailment remains unproved despite retrieved alternatives; not a certified omission.']])}

The **{fn.get('CONSERVATIVE_UNRESOLVED',0)} conservative FN** decisions and **{fn.get('PARTIAL_ENTAILMENT',0)} partially covered FN** decisions are not proof that these requirements are absent from the generated specification. Their closest actual candidates, searched aliases, applicability checks and unmet predicate descriptions remain in `03_fn_root_cause_audit_final.jsonl`. More semantic review could move counts in either direction.

## TP proof and generated-claim validity

There are **{a['final_TP_audit_rows']}** final TP evidence-audit rows, one for each final TP; each includes an original PDF locator, a real generated-file/line excerpt, a predicate-check map, source scope and coverage mode. These consist of **396 E3** and **188 E2** graded records after Phase-6 corrections. `E2` denotes an evidenced contextual/universal/conjunctive entailment, not partial credit. The automated checks show that original evidence strings and file/line positions exist, but the map's `met` status is **not equivalent** to external human verification of every semantic predicate.

The **{u['raw_generated_classes']}** generated classes are independently adjudicated in the generated-validity ledger:

{md_table(['Generated-class validity','Class count'],[['PDF_ENTAILED',valid.get('PDF_ENTAILED',0)],['SUPPORTED_NONCOVERING',valid.get('SUPPORTED_NONCOVERING',0)],['PDF_UNSUPPORTED',valid.get('PDF_UNSUPPORTED',0)]])}

A generated class labeled `SUPPORTED_NONCOVERING` may be backed by a narrower source rule without satisfying any independently retained source-positive atom. Its count (**{valid.get('SUPPORTED_NONCOVERING',0)}**) is an audit signal about source-atomization and matching completeness. The **{valid.get('PDF_UNSUPPORTED',0)}** PDF-unsupported generated classes yield **{c['FP']}** conservatively scored generated-only FP units after distinct canonical merging and negative-control deduplication. These are **not** all confirmed design errors; a source-supported narrower alternative or implicit context could still change some of their classifications. No negative counterfactual control was asserted (`B=0`, `TN=37`).

## Diagnostic exact-match and reciprocal regression probes

The following tests check the corresponding live source Markdown line, case/field/API/test context and current canonical label. These probe identities were confirmed in this input corpus rather than imposed as a goldset.

{probe_table}

In addition, an exact normalized full-quote/statement scan over every remaining FN and the full eight-file text found no verbatim sentence-copy conflict. This **does not** establish the absence of semantic equivalents; the Phase-6 high-risk challenge explicitly uncovered ten nonverbatim, context-dependent equivalents and corrected them. Other high-risk FNs, E2 bridges and FP residual predicates still require independent domain-specific validation for a `FINAL_VERIFIED` claim.

## Duplicate partition

The final raw claim inventory has **{d['eligible_generated_occurrences']}** occurrences and **{d['raw_unique_generated_classes']}** classes. Excess occurrences = **{d['duplicate_excess_occurrences']}** = **{d['within_file_excess']}** within-file + **{d['across_file_excess']}** across-file. Repeated classes: **{d['repeated_claim_class_count']}**, including **{d['repeated_classes_across_files']}** spanning multiple documents. Duplicate rate **{pct(d['duplicate_rate'])}**. Some unmerged meaning-preserving paraphrases may remain, so this rate is best-effort.

## Exclusions, reproducibility and interpretation

The consolidated `09_excluded_units.jsonl` records **{a['exclusion_rows']:,}** excluded spans, including PDF context/headings and generated headings, source citations, open questions, unadopted proposals, table structure and examples without independent commitments. The Phase-6 generated-class metadata reconciliation changes only stale status labels, not raw occurrence identity, source atoms, negative controls, FP residuals or class membership.

Reproduce: `python compute_metrics.py --base <directory containing final ledgers> --inputs <directory containing the original PDF and eight scored Markdown inputs> --write`. The script verifies item-level counts, origin partitions, class/occurrence membership, duplicate partitions, audit coverage, source pages, original generated line evidence, original PDF quotations and seven live regression probes. The script was executed successfully with **zero structural validation errors**.

**Limitations:** Structural agreement, exact quotations, TF-IDF/BM25-like retrieval and recorded predicate flags do not certify complete semantic equivalence; many generated validity judgments use heuristic or contextual source evidence. Evaluation covers only the fictional R1.0 / revision 1.3 design baseline, not real implementation safety, performance, business value or deployment readiness. The resulting point estimates are provisional best-effort measures subject to future human semantic reassessment in either direction; no fabricated statistical confidence interval is attached.
""")

write('06_metrics_final.md',f"""
# OrionDesk R1.0 — Final Six-Phase Atomic-Requirement Evaluation

**Status:** `{m['status']}` (Phase 6 completed as `PHASE_COMPLETED_BEST_EFFORT`)  
**Protocol:** 6.1  
**Method:** `supplied_set_01`  
**Document scope:** Original 90-page English PDF versus eight supplied English Markdown specifications. 

## Final four-cell results

{mc}

{metrics}

The canonical decision universe has **{u['canonical_decision_units']}** units: **{u['source_positive_atoms']}** original-PDF-positive atoms, **{u['bounded_negative_controls']}** bounded negative controls and **{u['generated_only_unsupported_propositions']}** generated-only unsupported propositions. Positive predictions count **{u['canonical_predicted_positive_units']}** effective units. The 37 TN are bounded PDF-derived controls, not a global TN population.

## Raw generated duplication

**{d['eligible_generated_occurrences']}** eligible generated occurrences, **{d['raw_unique_generated_classes']}** unique semantic classes, **{d['duplicate_excess_occurrences']}** excess occurrences = **{d['within_file_excess']}** within-file + **{d['across_file_excess']}** across-file. Duplicate rate **{pct(d['duplicate_rate'])}**.

## Key evidence and corrections

- Independently reopened all 90 original PDF pages and all **{cover['markdown_lines']:,}** original Markdown lines. The **{u['source_positive_atoms']}** retained source-atom quotes were located verbatim after whitespace normalization on their stated physical PDF pages.
- Audited **{a['final_TP_audit_rows']}** TP proof rows (396 E3 and 188 E2), and **{c['FN']}** remaining FN disposition rows.
- Remaining FN categories: **{fn.get('TRUE_MISSING',0)}** `TRUE_MISSING`, **{fn.get('PARTIAL_ENTAILMENT',0)}** `PARTIAL_ENTAILMENT`, and **{fn.get('CONSERVATIVE_UNRESOLVED',0)}** `CONSERVATIVE_UNRESOLVED`.
- The Phase-5 source atomization correction removed five nonindependent parent atoms. Independent Phase-6 checks corrected ten additional semantic-matcher false negatives; 301 candidate-FN records are now documented as corrected across phases.
- Seven case/field/API/test regression probes pass, including case-title storage, workspace retention-class settings and idempotent repeat case creation with the same outcome.
- Original scored inputs were not edited. Source IDs and generated occurrence/class IDs remain stable. All corrections and metadata synchronization are traceable in the English delta ledgers.

## Final reliability statement

The computations satisfy the full single-universe equations and duplicate partition arithmetic, with no structural validation failures. They are **not** certified requirement completeness or implementation correctness. The **{fn.get('CONSERVATIVE_UNRESOLVED',0)}** conservative FN judgments and **{c['FP']}** conservatively unsupported generated-only FP judgments may change with additional semantic evidence. The full limitations, input coverage, corrected-FN citations and negative-control scope are documented in `08_coverage_and_limitations.md`.

**Recomputation:** `python compute_metrics.py --base <final output folder> --inputs <original input folder> --write`.

No multi-method comparison is required: one eight-file input method was supplied. No ZIP, TAR or other archive was generated.
""")

write('06_final_status.json',json.dumps({
 'status':m['status'],'phase':6,'phase_status':m['phase_status'],
 'protocol_version':'6.1','method':m['method'],
 'structural_validation_passed':m['structural_validation']['passed'],
 'semantic_certification':'NOT_CERTIFIED',
 'completed_only_phase_6_in_this_turn':True,'archive_created':False,
 'scores':m['confusion'],'metrics':m['metrics']
},ensure_ascii=False,indent=2))

print('Wrote final reports.')
