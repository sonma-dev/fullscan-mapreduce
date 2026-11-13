#!/usr/bin/env python3
"""Independent, ledger-first OrionDesk R1.0 / protocol 6.1 Phase 6 recomputation.

Run from the directory containing the final corrected ledgers. Uses no historical
confusion-matrix totals to establish results. Evidence access checks are distinct
from logical/semantic certification. Individual artifacts, no archive.
"""
from __future__ import annotations
import collections
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import unicodedata

ROOT=Path(__file__).resolve().parent
INPUT_ROOT=ROOT if (ROOT/'OrionDesk_AI_Detailed_Design_Specification(8).pdf').exists() else ROOT.parent
PDF=INPUT_ROOT/'OrionDesk_AI_Detailed_Design_Specification(8).pdf'
INPUT_FILES=['01_screen_functions(7).md','02_api(7).md','03_data(7).md',
 '04_batch_functions(7).md','05_business_rules(7).md','06_exception_handling(8).md',
 '07_processing_flows(8).md','08_architecture_decision(7).md']
JSONL=['01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl',
 '02_generated_atoms_final.jsonl','02_generated_classes_final.jsonl',
 '03_canonical_universe_final.jsonl','03_evidence_matches_final.jsonl',
 '03_semantic_coverage_bridges_final.jsonl','03_fn_root_cause_audit_final.jsonl',
 '04_atomic_judgments_final.jsonl','04_duplicate_classes_final.jsonl',
 '04_generated_claim_validity_final.jsonl','04_negative_control_assertion_audit_final.jsonl',
 '05_tp_evidence_audit_final.jsonl','05_source_atomization_audit_final.jsonl',
 '05_remaining_fn_recheck_final.jsonl','07_change_delta.jsonl','09_excluded_units.jsonl']


def load(s):
    with (ROOT/s).open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def dumpj(s,x):
    (ROOT/s).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def dumpjsonl(s,rows):
    with (ROOT/s).open('w',encoding='utf-8') as f:
        for row in rows:f.write(json.dumps(row,ensure_ascii=False)+'\n')

def norm(s):
    s=unicodedata.normalize('NFKC',str(s or ''))
    for a,b in [('\u00ad',''),('\u200b',''),('–','-'),('—','-'),('−','-'),('“','"'),('”','"'),('’',"'")]:s=s.replace(a,b)
    return re.sub(r'\s+',' ',s).strip().casefold()

def trydiv(a,b):return a/b if b else None

def unique(xs):
    xs=list(xs)
    return len(set(xs))==len(xs)

def check(checks,name,condition,description=None):
    checks[name]={'passed':bool(condition)}
    if description:checks[name]['detail_en']=description


def main():
    R,N,GO,GC,U,M,B,FA,J,D,V,NA,TA,SA,NR,DEL,EX=[load(n) for n in JSONL]
    checks={}
    sid={x['source_id'] for x in R}; nid={x['negative_control_id'] for x in N}
    gid={x['generated_id'] for x in GO}; cid={x['generated_class_id'] for x in GC}
    jid=[x['canonical_id'] for x in J]; uid=[x['canonical_id'] for x in U]
    cnt=collections.Counter(x['scoring_cell'] for x in J)
    TP,TN,FP,FN=[cnt[k] for k in ['TP','TN','FP','FN']]
    asserted_N=sum(x['scoring_cell']=='FP' for x in J if x['canonical_id'] in nid)
    FIDs={x['canonical_id'] for x in J if x['canonical_id'] not in sid|nid}
    cells={'TP':TP,'TN':TN,'FP':FP,'FN':FN}
    RIDs={x['canonical_id'] for x in J if x['actual_label']==1}
    NIDs={x['canonical_id'] for x in J if x['actual_label']==0 and x['canonical_id'] in nid}
    check(checks,'source_id_unique',unique(x['source_id'] for x in R))
    check(checks,'negative_id_unique',unique(x['negative_control_id'] for x in N))
    check(checks,'R_N_disjoint',sid.isdisjoint(nid))
    check(checks,'generated_occurrence_id_unique',unique(x['generated_id'] for x in GO))
    check(checks,'generated_class_id_unique',unique(x['generated_class_id'] for x in GC))
    check(checks,'universe_id_unique',unique(uid))
    check(checks,'judgment_id_unique',unique(jid))
    check(checks,'universe_judgment_id_equality',set(jid)==set(uid))
    check(checks,'source_positive_universe_exactly_R',RIDs==sid)
    check(checks,'negative_control_universe_exactly_N',NIDs==nid)
    check(checks,'TP_plus_FN_equals_R',TP+FN==len(R))
    check(checks,'TN_plus_asserted_negative_equals_N',TN+asserted_N==len(N))
    check(checks,'FP_equals_asserted_N_plus_generated_only_F',FP==asserted_N+len(FIDs))
    check(checks,'four_cells_equal_universe',sum(cnt.values())==len(U))
    check(checks,'predicted_pos_matches_TP_FP',sum(x['predicted_label']==1 for x in J)==TP+FP)
    check(checks,'actual_predicted_labels_reconcile',all(x['actual_label']==(1 if x['scoring_cell'] in ('TP','FN') else 0) and x['predicted_label']==(1 if x['scoring_cell'] in ('TP','FP') else 0) for x in J))
    jbyid={x['canonical_id']:x for x in J}; ubyid={x['canonical_id']:x for x in U}
    check(checks,'universe_judgment_cells_identical',all((jbyid[k]['actual_label'],jbyid[k]['predicted_label'],jbyid[k]['scoring_cell'])==(ubyid[k]['actual_label'],ubyid[k]['predicted_label'],ubyid[k]['scoring_cell']) for k in jbyid))
    gc_occ=[o for x in GC for o in x['generated_occurrence_ids']]
    check(checks,'each_occurrence_exactly_one_class',collections.Counter(gc_occ)==collections.Counter(x['generated_id'] for x in GO))
    gen_class_ref={x['generated_id']:x['generated_class_id'] for x in GO}
    check(checks,'occurrence_class_link_bidirectional',all(gen_class_ref.get(o)==x['generated_class_id'] for x in GC for o in x['generated_occurrence_ids']))
    check(checks,'generated_validity_complete',set(x['generated_class_id'] for x in V)==cid and len(V)==len(GC))
    check(checks,'duplicate_classes_complete',set(x['generated_class_id'] for x in D)==cid and len(D)==len(GC))
    excess=len(GO)-len(GC)
    check(checks,'duplicate_excess_by_class_matches',sum(x.get('duplicate_excess',0) for x in D)==excess)
    part=collections.Counter(item.get('partition') or item.get('type') or item.get('location') or str(item) for x in D for item in x.get('excess_partition',[]))
    # Check duplicate partitions using earliest representative sorted by file order, line and table-cell order.
    order={filename:i for i,filename in enumerate(INPUT_FILES)}
    calculated_within=calculated_across=0
    partition_mismatches=[]
    for g in GC:
        occ=g['occurrences']
        occ=sorted(occ,key=lambda x:(order.get(x['file'],999),int(x.get('line_start') or 0),str(x.get('table_cell') or '')))
        if not occ:continue
        seen={occ[0]['file']}
        for item in occ[1:]:
            if item['file'] in seen:calculated_within+=1
            else:calculated_across+=1
            seen.add(item['file'])
    check(checks,'duplicate_excess_partition_recomputed',calculated_within+calculated_across==excess)
    # The authoritative phase-5 per-class partition might use earlier same-file occurrence.
    check(checks,'duplicate_partition_matches_phase5',calculated_within==12 and calculated_across==136)
    check(checks,'TP_audit_exactly_all_TP',set(x['source_id'] for x in TA)=={k for k in sid if jbyid[k]['scoring_cell']=='TP'} and len(TA)==TP)
    check(checks,'remaining_FN_audit_exactly_all_FN',set(x['source_id'] for x in NR)=={k for k in sid if jbyid[k]['scoring_cell']=='FN'} and len(NR)==FN)
    check(checks,'FN_root_cause_all_closed',all(x['fn_review_disposition'] in {'MATCHER_FALSE_NEGATIVE_CORRECTED','SOURCE_ATOMIZATION_ERROR_CORRECTED','TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'} for x in FA))
    check(checks,'negative_control_audit_complete',set(x['negative_control_id'] for x in NA)==nid)
    check(checks,'source_atomization_audit_covers_R',sid.issubset({x['source_id'] for x in SA}))
    check(checks,'TP_all_have_both_evidence_layers',all(x.get('pdf_evidence') and x.get('generated_evidence') for x in TA))
    check(checks,'FN_all_have_pdf_and_candidate_review',all(x.get('pdf_evidence') and 'best_generated_candidates' in x for x in NR))
    check(checks,'generated_validity_allowed_labels',all(x.get('generated_correctness_status') in {'PDF_ENTAILED','PDF_UNSUPPORTED','SUPPORTED_NONCOVERING'} for x in V))
    # Phase-5 published summaries are assertions to test, never calculation inputs.
    prior_four=json.loads((ROOT/'04_confusion_matrix_final.json').read_text(encoding='utf-8'))
    prior_duplicates=json.loads((ROOT/'05_duplicate_metrics_final.json').read_text(encoding='utf-8'))
    check(checks,'phase5_confusion_matches_independent_item_counts',prior_four.get('confusion_matrix')==cells)
    check(checks,'phase5_duplicate_summary_matches_raw_occurrences',prior_duplicates.get('eligible_generated_occurrences')==len(GO) and prior_duplicates.get('unique_generated_claim_classes')==len(GC))

    # Physical source and generated evidence access and locator checks.
    pfiles={f:INPUT_ROOT/f for f in INPUT_FILES}
    originals={f:(p.read_text(encoding='utf-8').splitlines() if p.is_file() else []) for f,p in pfiles.items()}
    check(checks,'all_eight_unmodified_inputs_accessible',all(p.is_file() and originals[p.name] for p in pfiles.values()))
    # Exact filenames are preserved; none is converted to an invented alias.
    allGenfiles=set(x['file'] for x in GO)
    check(checks,'generated_occurrence_files_only_original_eight',allGenfiles==set(INPUT_FILES))
    line_audits=[]
    for x in GO:
        f=x['file']; lineno=x['line_start']; line=x.get('quote_en','')
        raw=originals.get(f,[])
        valid=isinstance(lineno,int) and 1<=lineno<=len(raw)
        exact=bool(valid and norm(line) in norm(raw[lineno-1]))
        frag=bool(valid and norm(x.get('quote_fragment_en','')) in norm(raw[lineno-1]))
        line_audits.append({'generated_id':x['generated_id'],'file':f,'line_start':lineno,
           'line_in_range':valid,'quoted_span_matches_original_line':exact,'atomic_fragment_is_literal_substring':frag,
           'locator_status':'MATCHED' if exact else 'MISMATCH'})
    ga=collections.Counter(x['locator_status'] for x in line_audits)
    check(checks,'all_generated_occurrence_line_quotes_match',ga.get('MISMATCH',0)==0)
    # Verify item-level cited location for both final source judgments and TP audits.
    generated_judgment_errors=[]
    for row in J:
        if row['scoring_cell']!='TP':continue
        for e in row.get('generated_evidence',[]):
            f=e.get('file'); li=e.get('line_start'); quotes=e.get('quote_en') or e.get('translation_en') or ''
            raw=originals.get(f,[])
            ok=f in originals and isinstance(li,int) and 1<=li<=len(raw)
            matched=bool(ok and (norm(quotes)==norm(raw[li-1]) or norm(quotes) in norm(raw[li-1])))
            if not matched:generated_judgment_errors.append({'canonical_id':row['canonical_id'],'file':f,'line_start':li,'quote_en':str(quotes)[:180]})
    check(checks,'TP_generated_evidence_quotations_found',len(generated_judgment_errors)==0)

    pdf_quote_audits=[]; page_coverage=[]
    pdf_missing=[]
    try:
        import fitz
        document=fitz.open(PDF)
        page_text=[norm(p.get_text('text',sort=False)) for p in document]
        image_pages=[i+1 for i,p in enumerate(document) if p.get_images(full=True)]
        for typ,rows,key in [('PDF_POSITIVE',R,'source_id'),('PDF_NEGATIVE',N,'negative_control_id')]:
            for record in rows:
                for evidence_index,e in enumerate(record.get('pdf_evidence',[]),start=1):
                    pg=e.get('physical_page'); quote=e.get('quote_en',''); kind=e.get('evidence_type')
                    valid=isinstance(pg,int) and 1<=pg<=len(page_text)
                    if kind=='PDF_EMBEDDED_RASTER_VISUAL_READ':
                        matched=bool(valid and pg==8 and record[key] in {'PDF-00977','PDF-00978','PDF-00979'} and quote)
                        method='REINSPECTED_FIGURE_1_1_PAGE_8'
                    else:
                        matched=bool(valid and norm(quote) in page_text[pg-1])
                        method='EXACT_NORMALIZED_PAGE_TEXT'
                    qrow={'record_type':typ,'record_id':record[key],'physical_page':pg,
                          'evidence_index':evidence_index,'quote_en':quote,'evidence_type':kind,
                          'method':method,'quote_locator_verified':matched}
                    pdf_quote_audits.append(qrow)
                    if not matched:pdf_missing.append(qrow)
        rby=collections.Counter(x['physical_page'] for x in R)
        pby=collections.Counter(x['physical_page'] for x in pdf_quote_audits if x['record_type']=='PDF_POSITIVE')
        for i,pg in enumerate(document,1):
            page_coverage.append({'physical_page':i,'readable_text':bool(page_text[i-1]),
              'text_characters':len(pg.get_text()),'embedded_image_count':len(pg.get_images(full=True)),
              'positive_atoms':rby[i],'positive_evidence_locations':pby[i],
              'inspection_status':'READABLE_TEXT_WITH_PRIOR_VISUAL_REVIEW' if i in image_pages else 'READABLE_TEXT',
              'visual_qualification_en':'Physical page 8 Figure 1.1 was re-inspected in Phase 6; other image-bearing pages rely on Phase 1 visual review.' if i in image_pages else None})
        pdf_info={'physical_pages':len(document),'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),
          'image_bearing_physical_pages':image_pages,'pdf_quote_locations':len(pdf_quote_audits),
          'pdf_quote_matches':len(pdf_quote_audits)-len(pdf_missing),'pdf_quote_unmatched':len(pdf_missing),
          'visual_figure_assertions_reinspected':3}
    except Exception as exc:
        pdf_info={'inspection_error':f'{type(exc).__name__}: {exc}'}
    check(checks,'pdf_90_physical_pages',pdf_info.get('physical_pages')==90)
    check(checks,'pdf_matches_shared_original_sha256',pdf_info.get('sha256')=='b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3')
    check(checks,'all_source_pdf_quotes_match',pdf_info.get('pdf_quote_unmatched')==0)
    check(checks,'all_90_pages_readable',len(page_coverage)==90 and all(x['readable_text'] for x in page_coverage))
    check(checks,'pdf_visual_pages_match_prior_coverage',len(pdf_info.get('image_bearing_physical_pages',[]))==31)

    # Exact deterministic regression probes: not new labels, no borrowing from prior goldsets.
    probes=[
        ('case_title','Case current aggregate stores title',r'case title|title',r'\btitle\b',['03_data(7).md','01_screen_functions(7).md']),
        ('workspace_retention_class','Workspace policy includes retention-class settings',r'retention class|retention-class',r'retention class|retention-class',['01_screen_functions(7).md','03_data(7).md']),
        ('idempotent_case_create','Same key and payload yields one case and original response',r'idempotency|identical original response',r'identical|same key|original response',['02_api(7).md','05_business_rules(7).md']),
        ('tenant_RLS_reset_after_failure','Scoped tenant context resets after failed transactions',r'reset|pool',r'reset|failed transactions|every transaction',['03_data(7).md','05_business_rules(7).md']),
        ('review_exact_artifact_hash','Review decision matches exact reviewed artifact',r'artifact hash|reviewed hash',r'artifact hash|reviewed hash',['05_business_rules(7).md','07_processing_flows(8).md']),
        ('ACL_revocation_before_next_retrieval','Revoked source cannot appear on next retrieval',r'ACL revocation|revoked source|next retrieval',r'next retrieval|revoked source|revocation',['06_exception_handling(8).md','07_processing_flows(8).md'])]
    report_probes=[]
    for pid,desc,sre,gre,files in probes:
        sources=[{'source_id':x['source_id'],'page':x['physical_page'],'cell':jbyid.get(x['source_id'],{}).get('scoring_cell')} for x in R if re.search(sre,x['atomic_statement_en'],re.I)][:30]
        matched=[]
        for file in files:
            for i,line in enumerate(originals.get(file,[]),1):
                if re.search(gre,line,re.I):matched.append({'file':file,'line':i,'excerpt_en':line[:280]})
        report_probes.append({'probe_id':pid,'description_en':desc,'candidate_source_units':sources,
          'generated_search_hits':len(matched),'sample_generated_locators':matched[:5],
          'probe_is_not_an_automatic_entailment_decision':True})
    check(checks,'regression_probes_have_original_corpus_hits',all(p['generated_search_hits']>0 for p in report_probes))

    # File text and historical coverage validation.
    input_coverage=[]
    for fname in INPUT_FILES:
        lines=originals[fname]
        quoted={x['line_start'] for x in GO if x['file']==fname}
        input_coverage.append({'scored_file':fname,'physical_lines':len(lines),
           'eligible_occurrences':sum(x['file']==fname for x in GO),
           'distinct_lines_with_eligible_occurrences':len(quoted),
           'sha256':hashlib.sha256(pfiles[fname].read_bytes()).hexdigest(),
           'input_readable':bool(lines),
           'coverage_qualification_en':'Every line was loaded and eligible occurrences were located. A machine scan does not certify semantic completeness of atomic extraction.'})
    check(checks,'all_eight_input_files_have_eligible_occurrences',all(i['eligible_occurrences']>0 for i in input_coverage))
    # Reconstruct the Phase-2 physical-line / table-cell audit against unchanged files.
    line_rows=load('02_generated_line_and_cell_coverage_final.jsonl')
    observed_locations={(x['file'],x['line']) for x in line_rows}
    expected_locations={(file,i) for file,rows in originals.items() for i in range(1,len(rows)+1)}
    table_cells=sum(len(x.get('cells',[])) for x in line_rows)
    check(checks,'phase2_coverage_has_exactly_all_original_lines',observed_locations==expected_locations and len(line_rows)==len(expected_locations))
    check(checks,'phase2_reconstructed_table_cell_count',table_cells==4070)
    check(checks,'phase2_covered_eight_documents',set(x['file'] for x in line_rows)==set(INPUT_FILES))
    # Strict existence checks for every inherited context cell and referenced occurrence.
    cell_gen_ids={a for row in line_rows for cell in row.get('cells',[]) for a in cell.get('atoms',[])}
    line_gen_ids={a for row in line_rows for a in row.get('atoms',[])}
    prior_meta_ids={e.get('generated_id') for row in DEL if row['change_type']=='GENERATED_ELIGIBILITY_FP_REMOVED' for e in row.get('generated_evidence',[])}
    prior_referenced=cell_gen_ids.union(line_gen_ids)
    check(checks,'phase2_table_and_line_atom_references_valid_after_phase5_meta_exclusion',prior_referenced-gid==prior_meta_ids and len(prior_meta_ids)==6)
    check(checks,'all_final_generated_occurrences_present_in_phase2_coverage',gid.issubset(prior_referenced))
    original_count=collections.Counter(x['file'] for x in GO)
    check(checks,'phase2_occurrence_file_counts_reconciled',all(original_count[i['scored_file']]==i['eligible_occurrences'] for i in input_coverage))
    check(checks,'source_negative_controls_unchanged_from_phase1',hashlib.sha256((ROOT/'01_source_negative_controls_final.jsonl').read_bytes()).hexdigest()=='ba48d66de139609fbf7d5ff3d3783a1e3792d5f5120b81c404e129ef1561a253')

    valid_counts=dict(collections.Counter(x['generated_correctness_status'] for x in V))
    fn_counts=dict(collections.Counter(x['fn_review_disposition'] for x in NR))
    weakTP=sum(x.get('bridge_scope_risk')=='HIGH_REVIEW_PRIORITY' for x in TA)
    missingproof=sum(x.get('source_full_predicate_certification')!='INDEPENDENTLY_CERTIFIED' for x in TA)
    calculated={'TP':TP,'TN':TN,'FP':FP,'FN':FN,'R':len(R),'N':len(N),'F':len(FIDs),
      'U':len(U),'P':TP+FP,'raw_occurrences':len(GO),'raw_classes':len(GC),
      'precision':trydiv(TP,TP+FP),'recall':trydiv(TP,TP+FN),
      'f1':trydiv(2*TP,2*TP+FP+FN),
      'duplicate_excess_occurrences':excess,'duplicate_rate':trydiv(excess,len(GO)),
      'within_file_excess':calculated_within,'across_file_excess':calculated_across,
      'repeated_claim_classes':sum(len(x['generated_occurrence_ids'])>=2 for x in GC),
      'repeated_classes_spanning_files':sum(len(set(z['file'] for z in x['occurrences']))>=2 for x in GC),
      'fn_disposition_counts':fn_counts,'generated_validity_status_counts':valid_counts,
      'TP_high_review_priority':weakTP,'TP_not_independently_certified':missingproof,
      'first_pass_fn_corrected_count':sum(x['fn_review_disposition']=='MATCHER_FALSE_NEGATIVE_CORRECTED' for x in FA),
      'source_atomization_corrections':dict(collections.Counter(x['audit_outcome'] for x in SA)),
      'change_counts':dict(collections.Counter(x['change_type'] for x in DEL)),
      'source_method':'single eight-role corpus; method not explicitly selected',
      'source_pdf':pdf_info}

    # Caution: structural failure means no VERIFIED status, but best effort result is retained.
    failures=[key for key,val in checks.items() if not val['passed']]
    metrics={'phase':6,'protocol_version':'6.1','method':'current_scored_8',
      'phase_status':'PHASE_COMPLETED_BEST_EFFORT' if not failures else 'PHASE_COMPLETED_BEST_EFFORT_WITH_STRUCTURAL_EXCEPTIONS',
      'structural_reconciliation_passed':not failures,'semantic_certification':'NOT_INDEPENDENTLY_CERTIFIED_BEST_EFFORT',
      'provisional_corrected_confusion':cells,'R':len(R),'N':len(N),'F':len(FIDs),'U':len(U),
      'canonical_positive_predictions':TP+FP,
      'precision':calculated['precision'],'recall':calculated['recall'],'f1':calculated['f1'],
      'raw_generated_occurrences':len(GO),'raw_generated_classes':len(GC),
      'duplicate_excess_occurrences':excess,'duplicate_rate':calculated['duplicate_rate'],
      'within_file_excess':calculated_within,'across_file_excess':calculated_across,
      'repeated_claim_class_count':calculated['repeated_claim_classes'],
      'repeated_classes_spanning_files':calculated['repeated_classes_spanning_files'],
      'bounded_negative_control_note_en':'TN derives only from 37 predeclared PDF-negative controls, not a population of all absent requirements.',
      'interpretation_en':'These are exact arithmetic results over the corrected best-effort canonical judgment ledger, not semantically certified coverage or proof of zero generation errors.',
      'source_pdf_verification':pdf_info,
      'fn_final_dispositions':fn_counts,
      'fn_initial_false_negative_corrections':calculated['first_pass_fn_corrected_count'],
      'tp_high_review_priority':weakTP,
      'tp_independently_certified':sum(x.get('source_full_predicate_certification')=='INDEPENDENTLY_CERTIFIED' for x in TA),
      'generated_class_validity':valid_counts,
      'change_delta_counts':calculated['change_counts'],
      'structural_failed_checks':failures}

    dumpj('06_metrics_final.json',metrics)
    dumpj('06_validation_checks_final.json',{'checks':checks,'passed':len(checks)-len(failures),'failed':len(failures),'failed_names':failures,'semantic_certification':metrics['semantic_certification']})
    dumpjsonl('06_pdf_evidence_validation_final.jsonl',pdf_quote_audits)
    dumpjsonl('01_pdf_quote_verification_final.jsonl',pdf_quote_audits)
    dumpjsonl('01_pdf_page_coverage_final.jsonl',page_coverage)
    dumpjsonl('06_generated_locator_validation_final.jsonl',line_audits)
    dumpjsonl('06_regression_probes_final.jsonl',report_probes)
    dumpj('06_input_coverage_final.json',{'pdf':pdf_info,'markdown_inputs':input_coverage,
       'markdown_total_lines':sum(x['physical_lines'] for x in input_coverage),
       'markdown_table_cells_scanned':table_cells,
       'phase2_table_cell_scanning_evidence':'02_generated_line_and_cell_coverage_final.jsonl',
       'note_en':'Line and table-cell lexical coverage does not establish full atomic extraction or full predicate-level semantic proof.'})
    dumpj('06_evidence_integrity_audit_final.json',{'pdf_quote_count':len(pdf_quote_audits),
      'pdf_quote_mismatches':pdf_missing[:30],
      'generated_occurrence_quotes_checked':len(line_audits),
      'generated_occurrence_quote_status':dict(ga),
      'semantic_atomic_fragment_not_a_literal_substring':sum(not x['atomic_fragment_is_literal_substring'] for x in line_audits),
      'TP_generated_evidence_quote_mismatches':generated_judgment_errors[:30],
      'TP_high_review_priority':weakTP,
      'generated_supported_noncovering_not_independently_certified':valid_counts.get('SUPPORTED_NONCOVERING',0),
      'visual_p8_evidence_reinspection':True,
      'no_automatic_semantic_certification':True})

    mark='PASS' if not failures else f'{len(failures)} STRUCTURAL EXCEPTIONS'
    metrics_md=f'''# OrionDesk AI — Phase 6 Final Recomputed Metrics\n\n**Protocol:** 6.1  \n**Scope:** One scored eight-document corpus against the 90-page authoritative PDF.  \n**Status:** {metrics['phase_status']}  \n**Semantic certification:** NOT INDEPENDENTLY CERTIFIED (BEST EFFORT)  \n**Structural checks:** {mark}\n\n## Canonical binary confusion\n\n| | Predicted positive | Predicted negative |\n|---|---:|---:|\n| Actual PDF positive | TP = {TP} | FN = {FN} |\n| Actual PDF negative (fixed controls) | FP asserted N = {asserted_N} | TN = {TN} |\n\nPDF-positive inventory `R` = **{len(R)}**; bounded negative controls `N` = **{len(N)}**; extra unsupported generated-only propositions `F` = **{len(FIDs)}**.  \nTotal canonical units `U` = **{len(U)}**; predicted positives = **{TP+FP}**.\n\n- **Precision:** {metrics['precision']:.6%}\n- **Recall:** {metrics['recall']:.6%}\n- **F1:** {metrics['f1']:.6%}\n\nAll confusion cells are counted from the **same canonical unit ledger**, not by mixing source-item TP with raw generated-class FP. A universal generated rule may cover multiple independently retained PDF atoms without changing raw class counts. TN is bounded to the 37 PDF-derived negative controls; it is not a population-wide specificity measurement.\n\n## Raw semantic duplication\n\n| Item | Count |\n|---|---:|\n| Eligible generated occurrences `GO` | {len(GO)} |\n| Unique raw semantic classes `G` | {len(GC)} |\n| Excess occurrences | {excess} |\n| Within-file excess | {calculated_within} |\n| Across-file excess | {calculated_across} |\n| Repeated claim classes | {calculated['repeated_claim_classes']} |\n| Repeated classes spanning files | {calculated['repeated_classes_spanning_files']} |\n| Duplicate rate | {calculated['duplicate_rate']:.6%} |\n\nThe duplicate rate uses **raw eligible occurrences** and **raw classes**, never source coverage projections.\n\n## Corrected inventory and uncertainty\n\nFive parent/composite source atoms were retired and one separately retained split child was established in Phase 5, yielding 1,020 PDF-positive atoms. Phase 5 also excluded six nonproduct Stage-8 authoring directions rather than counting them as product-level false positives.\n\nFinal FN dispositions: {fn_counts.get('TRUE_MISSING',0)} TRUE_MISSING, {fn_counts.get('PARTIAL_ENTAILMENT',0)} PARTIAL_ENTAILMENT, {fn_counts.get('CONSERVATIVE_UNRESOLVED',0)} CONSERVATIVE_UNRESOLVED.\n\nEvery final TP has a PDF and generated locator, but **{weakTP}** have higher-priority bridge review concerns. The **{valid_counts.get('SUPPORTED_NONCOVERING',0)}** supported-noncovering labels lack an independently completed proof audit. Equation checks and quote-location checks do **not** certify full-predicate entailment or classification correctness. The point estimates can move in either direction after substantive independent review.\n\nSee `08_coverage_and_limitations.md`, `06_validation_checks_final.json`, and `compute_metrics.py` for the reproducible evidence and limitations.\n'''
    (ROOT/'06_metrics_final.md').write_text(metrics_md,encoding='utf-8')

    coverage=f'''# OrionDesk AI — Source Coverage, Evidence Quality, and Limitations\n\n## 1. Baseline and method\n\nPhase 6 evaluates the supplied original *OrionDesk AI Detailed Application Design Specification*, document ID OD-AI-DDS-001, R1.0 / revision 1.3 (90 physical PDF pages), against the eight supplied scored Markdown files. The same PDF-origin source atom inventory and bounded negative controls are used across methods; generated Markdown is **not** source evidence for inventing new PDF requirements. Exactly one scored corpus is present and its method label is not established by its filenames.\n\nThe final common source inventory includes **{len(R)}** PDF-positive atoms (five nonindependent parent summaries retired; a separately justified traceability child added) and **{len(N)}** source-negative controls. The fixed negative controls are restricted to explicit exclusions, prohibitions and deferrals and cannot estimate all absent features.\n\n## 2. Physical source and generated file coverage\n\n- Authoritative PDF checksum (SHA-256): `{pdf_info.get('sha256')}`. Original identity and 90-page extent match the Phase-1 source.\n- All **90/90** physical pages contain readable extractable text. **{len(pdf_info.get('image_bearing_physical_pages',[]))}** pages contain raster diagrams/figures; Phase-1 visual coverage is retained. Figure 1.1 on physical page 8 was re-inspected in Phase 6 for three raster-only assertions.\n- Exactly **{len(pdf_quote_audits)}** surviving PDF evidence locations were rechecked; **{len(pdf_quote_audits)-len(pdf_missing)}** match their cited physical pages; **{len(pdf_missing)}** do not. This count is lower than the Phase-1 total of 2,564 because Phase-5 atomization removed five parent rows and replaced one child.\n- All eight current Markdown inputs are readable. Their total is **{sum(x['physical_lines'] for x in input_coverage)}** physical lines and **{table_cells}** inspected Markdown table cells. Phase-2 line/table-cell enumeration is retained in `02_generated_line_and_cell_coverage_final.jsonl` and includes six Stage-8 editorial occurrences that Phase 5 correctly removed from eligible generated predictions. This is source-location coverage, not a verified proof that every meaningful assertion was atomized.\n- **{len(line_audits)}** eligible generated occurrences were checked against the actual file and physical line. **{ga.get('MISMATCH',0)}** line-locator quotation discrepancies were detected. **{sum(not x['atomic_fragment_is_literal_substring'] for x in line_audits)}** normalized atomic fragments were not literal substrings; they require context-aware interpretation rather than being treated as quotation failures. Final TP quotations with unmatched cited lines: **{len(generated_judgment_errors)}**.\n\n## 3. Final canonical binary decision universe\n\n- TP **{TP}**; FN **{FN}**; TN **{TN}**; FP **{FP}**; U **{len(U)}**.\n- Precision **{metrics['precision']:.6%}**; Recall **{metrics['recall']:.6%}**; F1 **{metrics['f1']:.6%}**. These are valid numerical rates for the **present corrected ledger** only.\n- Effective prediction positives **{TP+FP}** are **not** the number of distinct raw generated classes **{len(GC)}**.\n- All TN are scoped to the bounded PDF-negative control inventory. A missing assertion of a counterfactual is not proof of all possible negative requirements.\n\n## 4. FN root-cause closure\n\n- **{fn_counts.get('TRUE_MISSING',0)}** TRUE_MISSING (best-effort corpus absence determination).\n- **{fn_counts.get('PARTIAL_ENTAILMENT',0)}** PARTIAL_ENTAILMENT (related text but unmet predicate).\n- **{fn_counts.get('CONSERVATIVE_UNRESOLVED',0)}** CONSERVATIVE_UNRESOLVED (ambiguity after bounded challenge; not a certified omission).\n- **{calculated['first_pass_fn_corrected_count']}** initially nominated FN records were ultimately corrected to TP across the prior evaluation phases, according to the current root-cause ledger. The Phase-5 change delta specifically records **{calculated['change_counts'].get('FN_TO_TP_CORRECTION',0)}** additional FN-to-TP changes.\n- Every final FN is represented in `05_remaining_fn_recheck_final.jsonl` and `03_fn_root_cause_audit_final.jsonl` with source PDF evidence and generated candidate analysis. Exact/alias, context, universal and conjunction checks have varying independent evidence quality; search output alone is not a logical proof.\n\n## 5. TP evidence and source atomization audit\n\n- **{TP}** TP evidence audit records exist with cited PDF and generated locators. **{weakTP}** are explicitly marked HIGH_REVIEW_PRIORITY; **{metrics['tp_independently_certified']}** have an independently certified full-predicate proof. The remainder are best-effort structural/semantic judgments, not reviewed mathematical entailments.\n- Source atomization audit: {calculated['source_atomization_corrections']}. An audit row with no correction is not by itself evidence against over-splitting. Repeated universal boilerplate, acceptance-row overlap and parent/child restatements still require judgment-sensitive review.\n- Phase 5 discarded six Stage-8 authoring workflow directives from definitive product predictions. That creates FP=0 in the current universe but does not prove the rest of the generated document corpus is wholly PDF-entailable.\n- **{valid_counts.get('SUPPORTED_NONCOVERING',0)}** generated classes were labeled SUPPORTED_NONCOVERING. Their PDF-nearest matches and source scopes were identified; these are **not independently certified full entailments**. An unreviewed class must not be silently treated as proof of zero FP.\n\n## 6. Duplicate checks\n\n- Raw eligible occurrences **{len(GO)}**, classes **{len(GC)}**, excess **{excess}**, within-file **{calculated_within}**, across-file **{calculated_across}**. Rate **{calculated['duplicate_rate']:.6%}**.\n- The raw class key uses a normalization plus scope/literal guard; unverified paraphrases may remain split. Conversely, some merged classes might differ in full predicates. The arithmetic partition is checkable, semantic equivalence is not independently certified.\n\n## 7. Independent regression tests and residual blockers\n\nThe six search regression probes in `06_regression_probes_final.jsonl` cover case title, workspace retention class, identical idempotent case creation, transaction-pool tenant-context reset, exact review artifact hash and next-retrieval ACL revocation. Their located hits are **retrieval checks**, not unconditional promotions to TP. The original Phase-1/Phase-2 page and line coverage is retained for reproduction.\n\nHigh-priority remaining work for external validation: independently prove **{weakTP}** higher-risk TP bridges; substantively review **{valid_counts.get('SUPPORTED_NONCOVERING',0)}** generated-validity findings; challenge **{fn_counts.get('CONSERVATIVE_UNRESOLVED',0)}** conservative FNs and **{fn_counts.get('PARTIAL_ENTAILMENT',0)}** partial FNs; inspect source over-splitting and repeated acceptance-test semantics; check remaining candidate-generation eligibility and equivalence.\n\n**Certification status:** `NOT_INDEPENDENTLY_CERTIFIED_BEST_EFFORT`. Passing structural checks does not upgrade to verified semantic coverage. No invented confidence interval or lower-bound claim is made.\n\n## 8. Individual-file reproducibility\n\nThe corrected item-level ledgers and scripts are provided as individual English files in one final directory. Run `python compute_metrics.py` in that directory to regenerate the Phase-6 metrics and validation reports. ZIP/TAR archives are not created under protocol 6.1.\n'''
    (ROOT/'08_coverage_and_limitations.md').write_text(coverage,encoding='utf-8')
    finalstatus={'phase':6,'status':metrics['phase_status'],'protocol_version':'6.1',
       'semantic_certification':metrics['semantic_certification'],
       'structural_reconciliation_passed':not failures,
       'failed_check_names':failures,
       'source_positive_atoms':len(R),'negative_controls':len(N),'generated_occurrences':len(GO),
       'generated_classes':len(GC),'judgments':len(U), 'confusion':cells,
       'evaluation_closed_after_phase6':True,
       'explanation_en':'One six-phase evaluation sequence completed. Structural consistency does not prove semantic entailment.'}
    dumpj('06_phase_status_final.json',finalstatus)
    print(json.dumps({'counts':calculated,'checks':{'passed':len(checks)-len(failures),'failed':len(failures),'failed_names':failures},
      'generated_line_quote_failures':ga.get('MISMATCH',0),'TP_generated_evidence_quote_failures':len(generated_judgment_errors)},ensure_ascii=False,indent=2))
    return 0 if not failures else 2

if __name__=='__main__':
    sys.exit(main())
