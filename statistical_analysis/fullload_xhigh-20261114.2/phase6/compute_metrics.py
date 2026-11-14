#!/usr/bin/env python3
"""OrionDesk Protocol 6.1: independent Phase-6 ledger recomputation.

The program reads final item-level ledgers rather than trusting saved summary totals.
It checks structural provenance and arithmetic. It does NOT certify semantic
entailment, completeness of extraction, or the absence of unsupported claims.

Example:
    python compute_metrics.py --ledger-dir /mnt/data/orion_phase6 \
       --source-dir /mnt/data --output-dir /mnt/data/orion_phase6
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re

REQUIRED = [
    '01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl',
    '02_generated_atoms_final.jsonl','02_generated_classes_final.jsonl',
    '03_canonical_universe_final.jsonl','03_evidence_matches_final.jsonl',
    '03_semantic_coverage_bridges_final.jsonl','03_fn_root_cause_audit_final.jsonl',
    '04_generated_claim_validity_final.jsonl','04_atomic_judgments_final.jsonl',
    '04_duplicate_classes_final.jsonl','05_tp_evidence_audit_final.jsonl',
    '05_source_atomization_audit_final.jsonl','07_change_delta.jsonl',
    '09_excluded_units.jsonl',
]
ROLES = ['01_screen_functions','02_api','03_data','04_batch_functions',
         '05_business_rules','06_exception_handling','07_processing_flows',
         '08_architecture_decision']


def read_jsonl(path: Path):
    with path.open('r', encoding='utf-8') as stream:
        return [json.loads(line) for line in stream if line.strip()]


def norm(s):
    return re.sub(r'[^a-z0-9]+', '', str(s).lower())


def safe_rate(n, d):
    return n / d if d else None


def validate(path: Path, source: Path, coverage: Path | None = None, pdf: Path | None = None):
    missing = [str(path / name) for name in REQUIRED if not (path / name).is_file()]
    if missing:
        raise FileNotFoundError('Required ledgers missing: ' + '; '.join(missing))
    r,n,go,g,universe,em,bridge,fn_audit,v,j,d,tp_audit,atom_audit,delta,excluded = (
        read_jsonl(path / filename) for filename in REQUIRED
    )
    checks, counts, warnings, exceptions = {}, {}, [], []

    def check(name, outcome):
        checks[name] = bool(outcome)
        return outcome

    def unique_dict(rows, field):
        return {row[field]: row for row in rows}

    sr,nn,occ,classes,jud,ev,valid = (
        unique_dict(r,'source_id'), unique_dict(n,'negative_control_id'),
        unique_dict(go,'occurrence_id'),unique_dict(g,'class_id'),
        unique_dict(j,'canonical_id'),unique_dict(em,'source_id'),
        unique_dict(v,'class_id')
    )
    check('01_unique_source_atoms',len(sr)==len(r))
    check('02_unique_negative_controls',len(nn)==len(n))
    check('03_unique_generated_occurrences',len(occ)==len(go))
    check('04_unique_generated_classes',len(classes)==len(g))
    check('05_unique_canonical_judgments',len(jud)==len(j))
    check('06_complete_class_validity',len(valid)==len(v) and set(valid)==set(classes))
    check('07_source_evidence_mapping',len(ev)==len(em) and set(ev)==set(sr))
    check('08_canonical_universe_identity',len(universe)==len(j) and
          {x['canonical_id'] for x in universe}==set(jud))
    check('09_canonical_universe_row_parity', all(
          (x['actual_label'],x['predicted_label'],x['scoring_cell']) ==
          (jud[x['canonical_id']]['actual_label'],jud[x['canonical_id']]['predicted_label'],jud[x['canonical_id']]['scoring_cell'])
          for x in universe if x['canonical_id'] in jud))

    by_unit=defaultdict(list)
    q=Counter()
    for row in j:
        q[row['scoring_cell']]+=1
        by_unit[row['unit_kind']].append(row)
    matches={'TP':(1,1),'FN':(1,0),'TN':(0,0),'FP':(0,1)}
    check('10_label_and_cell_consistency',all(
        matches.get(row['scoring_cell']) ==
        (row['actual_label'],row['predicted_label']) for row in j))
    check('11_exact_source_universe',len(by_unit['PDF_POSITIVE']) == len(r) and
          Counter(x['origin_source_ids'][0] for x in by_unit['PDF_POSITIVE']) == Counter(sr.keys()))
    check('12_exact_negative_universe',len(by_unit['PDF_NEGATIVE_CONTROL']) == len(n) and
          Counter(x['origin_negative_control_ids'][0] for x in by_unit['PDF_NEGATIVE_CONTROL']) == Counter(nn.keys()))
    unexpected=[x for x in j if x['unit_kind'] not in
                ('PDF_POSITIVE','PDF_NEGATIVE_CONTROL','GENERATED_ONLY_UNSUPPORTED')]
    check('13_known_universe_kinds', not unexpected)
    check('14_single_canonical_population',len(j)==len(r)+len(n)+len(by_unit['GENERATED_ONLY_UNSUPPORTED']))
    check('15_one_universe_equations',q['TP']+q['FN']==len(r) and
          (q['TN']+sum(x['scoring_cell']=='FP' for x in by_unit['PDF_NEGATIVE_CONTROL']))==len(n) and
          q['FP']==len(by_unit['GENERATED_ONLY_UNSUPPORTED'])+
                      sum(x['scoring_cell']=='FP' for x in by_unit['PDF_NEGATIVE_CONTROL']) and
          sum(q.values())==len(j))

    membership=Counter()
    for row in g:
        for oid in row['occurrence_ids']:membership[oid]+=1
    check('16_occurrence_membership_one_to_one',len(membership)==len(go) and
          all(membership.get(x['occurrence_id'])==1 and
              x['semantic_class_id'] in classes and
              x['occurrence_id'] in classes[x['semantic_class_id']]['occurrence_ids'] for x in go))
    check('17_class_cardinality',sum(len(x['occurrence_ids']) for x in g)==len(go))
    check('18_duplicate_ledger_membership',len(d)==len(g) and
          {x['class_id'] for x in d}==set(classes) and all(
          len(x['occurrence_ids'])==x['occurrence_count'] and
          x['occurrence_ids']==classes[x['class_id']]['occurrence_ids']
          for x in d))

    # Apply the protocol's earliest-occurrence-representative rule independently.
    md_files={}
    role_map={}
    for role in ROLES:
        actual=[x for x in source.iterdir() if x.is_file() and
                x.name.startswith(role) and x.suffix=='.md']
        if len(actual)==1:
            role_map[role]=actual[0]
            md_files[actual[0].name]=actual[0].read_text(encoding='utf-8').splitlines()
    check('19_eight_unique_markdown_inputs',len(role_map)==8)
    check('20_occurrence_input_paths_exist',all(x['file'] in md_files for x in go))
    input_lines=sum(map(len,md_files.values()))
    check('21_markdown_eight_document_8330_line_census',input_lines==8330)

    bad_occ=[]
    for row in go:
        fn=row['file'];ln=row['line_start'];txt=row['generated_quote_en']
        if fn not in md_files or not isinstance(ln,int) or ln<1 or ln>len(md_files[fn]) or norm(txt) not in norm(md_files[fn][ln-1]):
            bad_occ.append(row['occurrence_id'])
    check('22_every_generated_quote_verbatim',not bad_occ)
    counts['invalid_generated_quote_locations']=len(bad_occ)

    def source_locators_valid(evlist):
        return (bool(evlist) and all(
            isinstance(e,dict) and e.get('file') and
            isinstance(e.get('physical_page'),int) and 1<=e['physical_page']<=90 and
            bool(e.get('quote_en')) for e in evlist))

    tp_rows=[x for x in j if x['scoring_cell']=='TP']
    fn_rows=[x for x in j if x['scoring_cell']=='FN']
    tp_ids={x['origin_source_ids'][0] for x in tp_rows}
    fn_ids={x['origin_source_ids'][0] for x in fn_rows}
    tp_map={x['source_id']:x for x in tp_audit}
    fn_rows_by_source={x['source_id']:x for x in fn_audit}
    check('23_complete_tp_audit',len(tp_audit)==len(tp_rows) and set(tp_map)==tp_ids)
    check('24_final_fn_audit_closed',sum(x['final_scoring_cell']=='FN' for x in fn_audit)==len(fn_rows) and
          fn_ids=={x['source_id'] for x in fn_audit if x['final_scoring_cell']=='FN'})
    check('25_all_source_atomization_rows',len(atom_audit)==len(r) and
          {x['source_id'] for x in atom_audit}==set(sr))
    check('26_negative_controls_well_sourced',all(source_locators_valid(x.get('pdf_evidence')) for x in n))
    check('27_source_atoms_well_sourced',all(source_locators_valid(x.get('pdf_evidence')) for x in r))

    bad_tp_quote=[];empty_tp_proof=[];weak_tp_maps=[]
    for row in tp_audit:
        evidence=row.get('generated_evidence') or []
        if not evidence or not source_locators_valid(row.get('pdf_evidence')) or not row.get('predicate_check_map'):
            empty_tp_proof.append(row['source_id'])
        for e in evidence:
            f,l=e.get('file'),e.get('line_start');quote=e.get('quote_en')
            if f not in md_files or not isinstance(l,int) or l<1 or l>len(md_files[f]) or not quote or norm(quote) not in norm(md_files[f][l-1]):
                bad_tp_quote.append((row['source_id'],f,l))
        pm=row.get('predicate_check_map',{})
        if any(p.get('status') not in ('met','not_applicable') or not p.get('proof_en') for p in pm.values()):
            weak_tp_maps.append(row['source_id'])
    check('28_every_tp_has_source_generated_and_predicate_proof_record',not empty_tp_proof)
    check('29_every_tp_quote_reloads_from_original_markdown',not bad_tp_quote)
    check('30_tp_structured_predicates_no_missing_proof_field',not weak_tp_maps)
    counts['tp_audit_source_missing']=len(empty_tp_proof)
    counts['tp_quote_location_defects']=len(bad_tp_quote)
    counts['tp_predicate_field_defects']=len(weak_tp_maps)

    fn_bad=[];fn_missing_justification=[]
    for row in fn_audit:
        if row['final_scoring_cell']!='FN':continue
        cands=row.get('best_generated_candidates') or []
        if not cands or not row.get('specific_reason_en') or not row.get('unmet_predicates_en'):
            fn_missing_justification.append(row['source_id'])
        for c in cands:
            e=c.get('evidence',{})
            f,l=e.get('file'),e.get('line_start');quote=e.get('quote_en')
            if f not in md_files or not isinstance(l,int) or l<1 or l>len(md_files[f]) or not quote or norm(quote) not in norm(md_files[f][l-1]):
                fn_bad.append((row['source_id'],f,l))
    check('31_every_fn_has_specific_unmet_predicate_and_candidates',not fn_missing_justification)
    check('32_every_fn_best_candidate_original_markdown_quote',not fn_bad)
    counts['fn_missing_justification']=len(fn_missing_justification)
    counts['fn_candidate_quote_location_defects']=len(fn_bad)

    # PDF page evidence is rechecked against the actual uploaded PDF's unsorted extraction.
    pdf_info={'available':False,'pages':None,'text_quote_matches':None,
              'raster_visual_quotations':None,'text_quote_failures':None,
              'hash_matches_phase1':None,'pages_with_nonempty_text':None}
    if pdf and pdf.exists():
        try:
            import fitz
            dpf=fitz.open(pdf)
            extracted=[norm(pg.get_text(sort=False)) for pg in dpf]
            pdf_info['available']=True
            pdf_info['pages']=len(dpf)
            pdf_info['pages_with_nonempty_text']=sum(bool(x) for x in extracted)
            pdf_info['sha256']=sha256(pdf.read_bytes()).hexdigest()
            pdf_check_rows=[e for x in r for e in x['pdf_evidence']] + [e for x in n for e in x['pdf_evidence']]
            visual=[e for e in pdf_check_rows if e.get('evidence_type')=='PDF_EMBEDDED_RASTER_VISUAL_READ']
            miss=[e for e in pdf_check_rows if e.get('evidence_type')!='PDF_EMBEDDED_RASTER_VISUAL_READ' and
                  norm(e['quote_en']) not in extracted[e['physical_page']-1]]
            pdf_info['text_quote_matches']=len(pdf_check_rows)-len(visual)-len(miss)
            pdf_info['raster_visual_quotations']=len(visual)
            pdf_info['text_quote_failures']=len(miss)
            check('33_original_pdf_90_pages',len(dpf)==90)
            check('34_all_pdf_pages_text_readable',sum(bool(x) for x in extracted)==90)
            check('35_original_pdf_quote_integrity',not miss)
            if coverage and coverage.exists():
                p1=json.loads(coverage.read_text(encoding='utf-8'))
                pdf_info['hash_matches_phase1']=p1.get('pdf',{}).get('sha256')==pdf_info['sha256']
                check('36_pdf_matches_phase1_fixed_source',pdf_info['hash_matches_phase1'])
            else:check('36_pdf_matches_phase1_fixed_source',False)
            if visual and len(visual)==3:
                warnings.append('Three source-positive quotations are from embedded raster labels on physical PDF page 8; their provenance is recorded as visual inspection in Phase 1 and not reproducible by PDF text extraction.')
        except Exception as exc:
            exceptions.append('Original PDF inspection failed: '+str(exc))
            check('33_original_pdf_90_pages',False)
            check('34_all_pdf_pages_text_readable',False)
            check('35_original_pdf_quote_integrity',False)
            check('36_pdf_matches_phase1_fixed_source',False)
    else:
        warnings.append('Original PDF was unavailable for independent byte and page inspection.')
        for i in range(33,37):check(f'{i:02d}_pdf_not_available',False)

    # Compute class duplication from the full original occurrence evidence, not saved duplicate totals.
    ordered_files={name:i for i, name in enumerate(p.name for p in role_map.values())}
    within=across=repeated_classes=crossfile_classes=0
    bad_duplicate_partition=[]
    for c in g:
        members=sorted((occ[oid] for oid in c['occurrence_ids']),
           key=lambda x:(ordered_files.get(x['file'],99),x['line_start'],
                         x.get('segment_index') or 0,x['occurrence_id']))
        if len(members)>1:repeated_classes+=1
        if len({x['file'] for x in members})>1:crossfile_classes+=1
        seen={members[0]['file']}
        for item in members[1:]:
            if item['file'] in seen:within+=1
            else:across+=1
            seen.add(item['file'])
    check('37_raw_duplicate_count',within+across==len(go)-len(g))
    check('38_duplicate_partition_audit',all(
        Counter(x.get('excess_classification') for x in row['excess_partition']).get('within_file',0)+
        Counter(x.get('excess_classification') for x in row['excess_partition']).get('across_file',0)==row['occurrence_count']-1
        for row in d))
    check('39_no_unscored_proposals_promoted',all(x.get('eligible_definitive_claim') is True for x in v))

    verdict=Counter(x['fn_review_disposition'] for x in fn_audit if x['final_scoring_cell']=='FN')
    tp_grade=Counter(x['entailment_grade'] for x in tp_audit)
    validity=Counter(x['validity'] for x in v)
    certainty=Counter(x.get('pdf_support_certainty') for x in v)
    delta_types=Counter(x['change_type'] for x in delta)
    check('40_full_audit_disposition_counts',sum(verdict.values())==q['FN'])
    check('41_class_validity_categories_exclusive',sum(validity.values())==len(g) and
          set(validity).issubset({'PDF_ENTAILED','PDF_UNSUPPORTED','SUPPORTED_NONCOVERING'}))
    check('42_generated_unsupported_units_match_judgments',len(by_unit['GENERATED_ONLY_UNSUPPORTED'])==sum(
          x['scoring_cell']=='FP' for x in by_unit['GENERATED_ONLY_UNSUPPORTED']))

    # Exact-match regression probes are discovered by meaning, not historical atom IDs.
    source_to_j={x['origin_source_ids'][0]:x for x in by_unit['PDF_POSITIVE']}
    probes=[
      ('case_title_field',lambda s:'case includes title' in s.lower()),
      ('workspace_retention_class',lambda s:'workspace settings includes retention class' in s.lower()),
      ('case_idempotent_replay',lambda s:'create case twice with same key' in s.lower()),
    ]
    regression=[]
    for name,pred in probes:
        located=[x for x in r if pred(x['atomic_statement_en'])]
        regression.append({'probe':name,'source_ids':[x['source_id'] for x in located],
            'judgments':[source_to_j[x['source_id']]['scoring_cell'] for x in located if x['source_id'] in source_to_j],
            'source_count':len(located),
            'pass':bool(located) and all(source_to_j[x['source_id']]['scoring_cell']=='TP' and
                  bool(source_to_j[x['source_id']]['generated_evidence']) for x in located)})
    check('43_regression_probes_source_to_generated',all(x['pass'] for x in regression))

    # A separate high-risk regression on publication checks, without presupposing an outcome.
    highrisk=[x for x in r if ('reviewed artifact' in x['atomic_statement_en'].lower() and
                              ('hash' in x['atomic_statement_en'].lower() or 'approval' in x['atomic_statement_en'].lower()))]
    counts['source_high_risk_review_binding_atoms']=len(highrisk)
    counts['high_risk_review_binding_tp']=sum(source_to_j[x['source_id']]['scoring_cell']=='TP' for x in highrisk)
    counts['high_risk_review_binding_fn']=sum(source_to_j[x['source_id']]['scoring_cell']=='FN' for x in highrisk)

    # Source identifiers across local phase inputs and no cross-method leakage.
    method_labels=Counter(x.get('prefix') for x in go)
    check('44_single_method_isolation',len(method_labels)==1 and
          set(x.get('prefix') for x in g)==set(method_labels) and
          set(x.get('prefix') for x in v)==set(method_labels))
    check('45_english_evidence_text_present',all(
          isinstance(x.get('atomic_statement_en'),str) and x['atomic_statement_en'].strip()
          for x in r+go+j))

    # Phase2 source-line/cell census is a separate completed audit of parsing coverage.
    cov_path=source/'orion_phase2'/'02_markdown_line_cell_coverage_final.jsonl'
    line_coverage={'available':False,'rows':None,'table_cells':None,'exact_coverage':False}
    if cov_path.exists():
        lcov=read_jsonl(cov_path)
        line_coverage.update({'available':True,'rows':len(lcov),
                              'table_cells':sum(x.get('cells',0) for x in lcov)})
        file_census=Counter(x['file'] for x in lcov)
        line_coverage['exact_coverage']=all(file_census.get(name)==len(lines) for name,lines in md_files.items())
        check('46_all_original_markdown_lines_in_phase2_census',line_coverage['exact_coverage'])
    else:check('46_all_original_markdown_lines_in_phase2_census',False)

    TP,FN,TN,FP=(q['TP'],q['FN'],q['TN'],q['FP'])
    negative_asserted=sum(x['scoring_cell']=='FP' for x in by_unit['PDF_NEGATIVE_CONTROL'])
    score={
      'TP':TP,'FN':FN,'TN':TN,'FP':FP,'R':len(r),'N':len(n),
      'F_generated_only':len(by_unit['GENERATED_ONLY_UNSUPPORTED']),
      'B_asserted_negative_controls':negative_asserted,
      'canonical_universe_size':len(j),'effective_predicted_positive':TP+FP,
      'precision':safe_rate(TP,TP+FP),'recall':safe_rate(TP,TP+FN),
      'f1':safe_rate(2*TP,2*TP+FP+FN),
      'eligible_generated_occurrences':len(go),'unique_generated_claim_classes':len(g),
      'duplicate_excess_occurrences':len(go)-len(g),
      'duplicate_rate':safe_rate(len(go)-len(g),len(go)),
      'within_file_excess':within,'across_file_excess':across,
      'repeated_claim_class_count':repeated_classes,
      'repeated_classes_spanning_multiple_files':crossfile_classes,
    }
    counts.update({
      'pdf_positive_atoms':len(r),'negative_controls':len(n),
      'markdown_documents':len(md_files),'markdown_physical_lines':input_lines,
      'generated_occurrences':len(go),'generated_classes':len(g),
      'generated_claim_validity':dict(validity),
      'generated_claim_support_certainty':dict(certainty),
      'pdf_positive_source_pages_with_atoms':len({e['physical_page'] for x in r for e in x['pdf_evidence']}),
      'source_positive_evidence_locators':sum(len(x['pdf_evidence']) for x in r),
      'negative_control_evidence_locators':sum(len(x['pdf_evidence']) for x in n),
      'initial_fn_audit_rows':len(fn_audit),'remaining_fn_dispositions':dict(verdict),
      'tp_proof_rows':len(tp_audit),'tp_proof_grades':dict(tp_grade),
      'source_atomization_rows':len(atom_audit),'source_atomization_decisions':dict(Counter(x['decision'] for x in atom_audit)),
      'change_delta_rows':len(delta),'change_delta_types':dict(delta_types),
      'excluded_units_rows':len(excluded),
    })
    if certainty.get('NOT_ESTABLISHED_BY_LEXICAL_RETRIEVAL',0):
        warnings.append(f"{certainty['NOT_ESTABLISHED_BY_LEXICAL_RETRIEVAL']} generated classes lack established PDF support beyond weak/lexical retrieval; FP=0 is not a verified absence of unsupported claims.")
    if verdict.get('CONSERVATIVE_UNRESOLVED',0):
        warnings.append(f"{verdict['CONSERVATIVE_UNRESOLVED']} source-positive judgments remain conservative unresolved FN, not proven absences.")
    warnings.append('Every TP has a source/generated quote locator and a predicate-check record; these structured fields are not independent formal semantic proofs.')
    warnings.append('The 37 TN records are bounded controls constructed from explicit prohibitions/deferrals; TN is not a census of all absent requirements.')
    warnings.append('Phase-5 final raw classes may omit unresolved paraphrase duplicates; measured duplicate rate is a conservative estimate, not exhaustive semantic equivalence.')

    verdict_state='PHASE_COMPLETED_BEST_EFFORT' if all(checks.values()) else 'PHASE_COMPLETED_BEST_EFFORT_WITH_STRUCTURAL_EXCEPTIONS'
    # Recompute final values even when provenance warnings exist.
    result={'protocol_version':'6.1','phase':6,'status':verdict_state,
            'semantic_certification':'NOT_CERTIFIED',
            'method':'unlabeled_eight_document_set',
            'source_pdf_file':pdf.name if pdf else None,
            'scores':score,'counts':counts,'original_pdf_inspection':pdf_info,
            'markdown_line_coverage':line_coverage,
            'regression_probes':regression,
            'structural_checks':checks,'structural_pass_count':sum(checks.values()),
            'structural_total_check_count':len(checks),
            'warnings_en':warnings,'exceptions_en':exceptions,
            'accounting_basis_en':'One canonical proposition universe U = R disjoint-union N disjoint-union F. The effective predicted-positive count need not equal the raw generated semantic-class count.',
            'interpretation_en':'Calculated scores are provisional best-effort ledger statistics, not independent semantic certification. In particular, FP=0 and Precision=100% are not verified.',
            }
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--ledger-dir',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--source-dir',type=Path,default=Path('/mnt/data'))
    parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args()
    pdf=args.source_dir/'OrionDesk_AI_Detailed_Design_Specification(2).pdf'
    coverage=args.source_dir/'orion_phase1'/'01_pdf_coverage_final.json'
    result=validate(args.ledger_dir,args.source_dir,coverage,pdf)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    with (args.output_dir/'06_metrics_final.json').open('w',encoding='utf-8') as f:
        json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    s=result['scores']; c=result['counts']
    fmt=lambda k: ('not defined' if s[k] is None else f"{s[k]*100:.6f}%")
    lines=[
      '# OrionDesk AI — Phase 6 Independent Recalculation',
      '', '**Protocol:** 6.1', f"**Status:** `{result['status']}`",
      '**Semantic certification:** `NOT_CERTIFIED`',
      '**Method:** One unlabeled complete eight-document set',
      '', '## Canonical four-cell results',
      '', '| | Predicted positive | Predicted negative |',
      '|---|---:|---:|',
      f"| Actual positive | TP {s['TP']} | FN {s['FN']} |",
      f"| Actual negative | FP {s['FP']} | TN {s['TN']} |",
      '',f"- Source-positive atoms (R): **{s['R']}**.",
      f"- Fixed PDF-negative controls (N): **{s['N']}** (bounded diagnostic inventory).",
      f"- Generated-only unsupported canonical propositions (F): **{s['F_generated_only']} identified** (not proof of absence).",
      f"- Asserted negative controls (B): **{s['B_asserted_negative_controls']} identified**.",
      f"- Universe size: **{s['canonical_universe_size']}** canonical propositions.",
      f"- Precision: **{fmt('precision')}** (provisional).",
      f"- Recall: **{fmt('recall')}** (provisional).",
      f"- F1: **{fmt('f1')}** (provisional).",
      '', '## Raw generated duplication (separate counting unit)',
      '',f"- Eligible occurrences (GO): **{s['eligible_generated_occurrences']}**.",
      f"- Unique raw classes (G): **{s['unique_generated_claim_classes']}**.",
      f"- Excess occurrences: **{s['duplicate_excess_occurrences']}**.",
      f"- Within-file excess: **{s['within_file_excess']}**.",
      f"- Across-file excess: **{s['across_file_excess']}**.",
      f"- Repeated classes: **{s['repeated_claim_class_count']}**; across-file spanning classes: **{s['repeated_classes_spanning_multiple_files']}**.",
      f"- Duplicate rate: **{fmt('duplicate_rate')}** (conservative best effort).",
      '', '## Independent structural checks',
      '', f"Passed: **{result['structural_pass_count']}/{result['structural_total_check_count']}**.",
      'The checks recompute the confusion matrix and duplicate partition from individual rows, validate exact source and negative-control coverage, and reload every generated/TP/FN evidence quote from the original Markdown files.',
      f"The original PDF inspection found **{result['original_pdf_inspection']['text_quote_matches']}** directly matching PDF-text evidence locators and **{result['original_pdf_inspection']['raster_visual_quotations']}** separately tagged embedded-visual locators.",
      '', '## Why this is not semantically certified',
      '', f"- **{c['generated_claim_support_certainty'].get('NOT_ESTABLISHED_BY_LEXICAL_RETRIEVAL',0)}** generated-class validity records lack established full PDF semantic support; therefore zero identified FP and 100% calculated precision do **not** verify all predictions.",
      f"- **{c['remaining_fn_dispositions'].get('CONSERVATIVE_UNRESOLVED',0)}** final FN outcomes remain genuinely ambiguous, not verified omissions.",
      '- All TP records have checked locators and structured predicate-field entries, but the evidence audit is best effort rather than independent expert semantic adjudication.',
      '- Do not force the effective predicted-positive count to equal the raw generated semantic-class count.',
      '', '## Scope boundary',
      '', 'The Phase-6 operation only recomputes and verifies final Phase-5 ledgers. It does not add another evaluation method, modify scored Markdown, produce an archive, or assert a new gold standard.',
      '', 'See `08_coverage_and_limitations.md` for full provenance and limitations.',
    ]
    (args.output_dir/'06_metrics_final.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'scores':s,'checks':f"{result['structural_pass_count']}/{result['structural_total_check_count']}",
                      'failed_checks':[k for k,v in result['structural_checks'].items() if not v]},ensure_ascii=False))

if __name__=='__main__':main()
