#!/usr/bin/env python3
"""Independent structural recomputation of OrionDesk evaluation v6.1.

Reads item-level final JSONL ledgers. It does NOT use prior summary counts as inputs.
It checks evidence locations and provenance but cannot itself prove semantic entailment.
Python 3, standard library only; optional PyMuPDF for PDF quotation audit.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, math, pathlib, re, sys

REQUIRED = [
 '01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl',
 '02_generated_atoms_final.jsonl','02_generated_classes_final.jsonl',
 '03_canonical_universe_final.jsonl','03_evidence_matches_final.jsonl',
 '03_semantic_coverage_bridges_final.jsonl','03_fn_root_cause_audit_final.jsonl',
 '04_generated_claim_validity_final.jsonl','04_atomic_judgments_final.jsonl',
 '04_duplicate_classes_final.jsonl','04_generated_only_unsupported_final.jsonl',
 '05_tp_evidence_audit_final.jsonl','05_source_atomization_audit_final.jsonl',
 '07_change_delta.jsonl','09_excluded_units.jsonl','02_generated_line_coverage.jsonl',
]
ROLE_PREFIXES = ('01_screen_functions','02_api','03_data','04_batch_functions',
 '05_business_rules','06_exception_handling','07_processing_flows','08_architecture_decision')

def load_jsonl(path):
    result=[]
    for n,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if line.strip():
            try: result.append(json.loads(line))
            except Exception as exc: raise AssertionError(f'{path.name}:{n} invalid JSON: {exc}')
    return result

def unique_index(rows,key):
    idx={}
    for x in rows:
        k=x[key]
        assert k not in idx, f'duplicate {key}={k}'
        idx[k]=x
    return idx

def ratio(a,b):return a/b if b else None

def normalized(s):return re.sub(r'\s+',' ',str(s)).strip()

def scan_quote(text,q):
    a=normalized(text).casefold(); b=normalized(q).casefold()
    return bool(b) and (b in a or re.sub(r'[^\w]+','',b) in re.sub(r'[^\w]+','',a))

def check_evidence(entry, input_files, issues, kind, srcid, max_issues=30):
    ev=entry.get('generated_evidence',[])
    if isinstance(ev,dict):ev=[ev]
    for x in ev:
        if not isinstance(x,dict):continue
        name=x.get('file')
        if name not in input_files:
            issues.append({'id':srcid,'kind':kind,'problem':'missing_generated_file','file':name});continue
        st=x.get('line_start');en=x.get('line_end',st)
        lines=input_files[name]
        if not isinstance(st,int) or not isinstance(en,int) or st<1 or en>len(lines) or st>en:
            issues.append({'id':srcid,'kind':kind,'problem':'invalid_line_range','file':name,'start':st,'end':en});continue
        q=x.get('quote_en',x.get('raw_quote_en',''))
        if q and not scan_quote(' '.join(lines[st-1:en]),q):
            issues.append({'id':srcid,'kind':kind,'problem':'quote_not_on_reported_line','file':name,'start':st,'excerpt':str(q)[:130]})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger-dir',default=str(pathlib.Path(__file__).resolve().parent))
    parser.add_argument('--original-dir',default=str(pathlib.Path(__file__).resolve().parent.parent))
    parser.add_argument('--output-dir',default=str(pathlib.Path(__file__).resolve().parent))
    args=parser.parse_args();base=pathlib.Path(args.ledger_dir);root=pathlib.Path(args.original_dir);out=pathlib.Path(args.output_dir)
    out.mkdir(parents=True,exist_ok=True)
    for f in REQUIRED:assert (base/f).is_file(),f'Missing mandatory ledger: {f}'
    rows={f:load_jsonl(base/f) for f in REQUIRED}
    R=unique_index(rows['01_source_atoms_final.jsonl'],'source_id')
    N=unique_index(rows['01_source_negative_controls_final.jsonl'],'negative_control_id')
    GO=unique_index(rows['02_generated_atoms_final.jsonl'],'occurrence_id')
    GC=unique_index(rows['02_generated_classes_final.jsonl'],'class_id')
    U=unique_index(rows['03_canonical_universe_final.jsonl'],'canonical_id')
    J=unique_index(rows['04_atomic_judgments_final.jsonl'],'canonical_id')
    matches=unique_index(rows['03_evidence_matches_final.jsonl'],'source_id')
    bridges=unique_index(rows['03_semantic_coverage_bridges_final.jsonl'],'source_id')
    validity=unique_index(rows['04_generated_claim_validity_final.jsonl'],'generated_class_id')
    NA=unique_index(rows['05_tp_evidence_audit_final.jsonl'],'source_id')
    unsupported=rows['04_generated_only_unsupported_final.jsonl']
    fn_audit=rows['03_fn_root_cause_audit_final.jsonl']
    fn_by_id=unique_index(fn_audit,'source_id')
    dup=unique_index(rows['04_duplicate_classes_final.jsonl'],'class_id')
    assert not (set(R)&set(N)), 'R/N IDs overlap'
    assert len(U)==len(J), 'U and judgment size mismatch'
    assert set(U)==set(J), 'U and judgment IDs mismatch'
    assert set(matches)==set(R), 'Source coverage evidence incomplete'
    assert set(validity)==set(GC), 'Generated validity coverage incomplete'
    assert set(dup)==set(GC), 'Duplicate classes coverage incomplete'
    assert all(v['prefix']=='supplied_eight_file_set' for v in J.values()), 'Method leakage in canonical ledger'
    assert all(v['prefix']=='supplied_eight_file_set' for v in GO.values()), 'Method leakage in generated occurrences'
    assert all(v['prefix']=='supplied_eight_file_set' for v in GC.values()), 'Method leakage in generated classes'
    assert all(v['prefix']=='supplied_eight_file_set' for v in validity.values()), 'Method leakage in generated validity'
    occurrences_by_class=collections.defaultdict(list)
    for oid,g in GO.items():
        cid=g['class_id'];assert cid in GC,f'unknown class for {oid}'
        occurrences_by_class[cid].append(oid)
    for cid,cls in GC.items():
        ids=cls['occurrence_ids'];assert len(ids)==len(set(ids))
        assert set(ids)==set(occurrences_by_class[cid]),f'wrong class membership {cid}'
        assert cls['occurrence_count']==len(ids),f'wrong occurrence count {cid}'
        assert len(ids)>=1
        assert dup[cid]['occurrence_count']==len(ids)
    assert sum(len(x['occurrence_ids']) for x in GC.values())==len(GO)
    assert len(GO)>=len(GC)
    # Verify each canonical proposition's ground truth and prediction exactly once.
    canonical_R=set();canonical_N=set();canonical_F=set();asserted_N=set();A=set()
    counts=collections.Counter()
    for k,v in J.items():
        u=U[k]
        for attr in ('actual_label','predicted_label','scoring_cell','canonical_type'):
            assert v[attr]==u[attr],f'judgment/universe {k} {attr} mismatch'
        a=v['actual_label'];p=v['predicted_label'];cell=v['scoring_cell']
        assert a in (0,1) and p in (0,1)
        assert cell=={(1,1):'TP',(1,0):'FN',(0,1):'FP',(0,0):'TN'}[a,p]
        counts[cell]+=1
        typ=v['canonical_type']
        if typ=='PDF_POSITIVE':
            ids=v['origin_source_ids'];assert len(ids)==1 and ids[0] in R
            sid=ids[0];assert sid not in canonical_R;canonical_R.add(sid)
            assert a==1;assert matches[sid]['scoring_cell']==cell
            if cell=='TP':
                A.add(sid)
                assert v['entailment_grade'] in ('E2','E3'),f'wrong TP grade {sid}'
                assert v['generated_evidence'] and v['origin_generated_class_ids'],f'no TP generated proof {sid}'
                assert sid in NA and NA[sid]['audit_outcome']=='CONFIRMED_TP',f'TP audit missing {sid}'
                if v['entailment_grade']=='E2' and v['coverage_mode']!='DIRECT':assert sid in bridges
            else:
                assert sid in fn_by_id,f'FN audit missing {sid}'
                arow=fn_by_id[sid]
                assert arow['final_scoring_cell']=='FN'
                assert arow['fn_review_disposition'] in ('TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED')
                assert arow.get('pdf_evidence') and arow.get('best_generated_candidates')
                assert arow.get('specific_reason_en')
        elif typ=='PDF_NEGATIVE_CONTROL':
            ids=v['origin_negative_control_ids'];assert len(ids)==1 and ids[0] in N
            nid=ids[0];assert nid not in canonical_N;canonical_N.add(nid)
            assert a==0
            if p==1: asserted_N.add(nid)
        elif typ=='GENERATED_ONLY_UNSUPPORTED':
            assert a==0 and p==1 and cell=='FP', f'unsupported F unit {k}'
            assert v['origin_generated_class_ids'],f'unsupported F no generated class {k}'
            canonical_F.add(k)
        else: raise AssertionError(f'bad canonical type {typ}')
        for cid in v.get('origin_generated_class_ids',[]):assert cid in GC,(k,cid)
    assert canonical_R==set(R) and canonical_N==set(N)
    assert counts['TP']==len(A)
    assert counts['FN']==len(R)-len(A)
    assert counts['TN']==len(N)-len(asserted_N)
    assert counts['FP']==len(canonical_F)+len(asserted_N)
    assert len(J)==len(R)+len(N)+len(canonical_F)
    assert counts.total()==len(J)
    assert counts['TP']+counts['FP']==len(A)+len(asserted_N)+len(canonical_F)
    assert len(unsupported)==len(canonical_F), 'Unsupported generated proposition register differs from F'
    assert len(NA)==counts['TP']+sum(x['audit_outcome']=='CORRECTED_TO_FN' for x in NA.values())
    assert {s for s,x in NA.items() if x['audit_outcome']=='CONFIRMED_TP'}==A
    assert {s for s,x in fn_by_id.items() if x['final_scoring_cell']=='FN'}==canonical_R-A
    assert all(x['final_scoring_cell'] in ('TP','FN','REMOVED_OR_MERGED') for x in fn_audit)
    assert sum(1 for x in fn_audit if x['final_scoring_cell']=='FN')==counts['FN']
    final_fn_causes=collections.Counter(x['fn_review_disposition'] for x in fn_audit if x['final_scoring_cell']=='FN')
    assert sum(final_fn_causes.values())==counts['FN']
    # Source-atomization integrity: all removed atoms absent, all corrected IDs retained.
    atom_audits=rows['05_source_atomization_audit_final.jsonl']
    removed=[]; corrected=[]
    for x in atom_audits:
        if x['audit_decision']=='EXCLUDED_NONNORMATIVE_OR_PARENT':
            for sid in x['old_source_ids']:
                removed.append(sid);assert sid not in R, f'atom excluded yet scored: {sid}'
        elif x['audit_decision']=='CORRECTED_LINE_WRAP':
            for sid in x['new_source_ids']:
                corrected.append(sid);assert sid in R
    assert len(removed)==len(set(removed))
    # Independent duplicates partition by input order, physical line, table-column position.
    sources={}
    for p in root.iterdir():
        if p.is_file() and p.suffix.lower()=='.md':
            for prefix in ROLE_PREFIXES:
                if p.name.startswith(prefix):
                    assert prefix not in sources,f'Multiple input candidates for {prefix}'
                    sources[prefix]=p
    assert set(sources)==set(ROLE_PREFIXES),f'missing scored Markdown roles {set(ROLE_PREFIXES)-set(sources)}'
    source_lines={p.name:p.read_text(encoding='utf-8').splitlines() for p in sources.values()}
    assert set(g['file'] for g in GO.values())==set(source_lines)
    line_entries=rows['02_generated_line_coverage.jsonl']
    assert len(line_entries)==sum(len(lines) for lines in source_lines.values())
    line_keys=set();line_covered_occurrences=[]
    for entry in line_entries:
        k=(entry['file'],entry['line']); assert k not in line_keys
        line_keys.add(k)
        assert k[0] in source_lines and 1<=k[1]<=len(source_lines[k[0]])
        src=source_lines[k[0]][k[1]-1]
        assert hashlib.sha256(src.encode('utf-8')).hexdigest()==entry['line_sha256'], f'line hash mismatch {k}'
        for oid in entry['occurrence_ids']:
            assert oid in GO and GO[oid]['file']==k[0] and GO[oid]['line_start']==k[1], f'line-to-occurrence mismatch {k} {oid}'
            line_covered_occurrences.append(oid)
    assert len(line_covered_occurrences)==len(GO) and set(line_covered_occurrences)==set(GO)
    prefix_order={sources[prefix].name:i for i,prefix in enumerate(ROLE_PREFIXES)}
    within=across=0;repeated=spans=0
    for cid,c in GC.items():
        ids=c['occurrence_ids']
        if len(ids)>1:
            repeated+=1
            if len({GO[i]['file'] for i in ids})>1:spans+=1
        ordered=sorted(ids,key=lambda i:(prefix_order[GO[i]['file']],GO[i]['line_start'],
            (GO[i]['table_cell'] or {}).get('column_index') or 0,i))
        previous_files=set()
        for i,oid in enumerate(ordered):
            f=GO[oid]['file']
            if i:
                if f in previous_files:within+=1
                else:across+=1
            previous_files.add(f)
    assert within+across==len(GO)-len(GC)
    dpath=base/'05_duplicate_metrics_final.json'
    if dpath.exists():
        prev=json.loads(dpath.read_text())
        assert (within,across)==(prev['within_file_excess'],prev['across_file_excess']), 'duplicate partition mismatch'
        assert (repeated,spans)==(prev['repeated_claim_class_count'],prev['repeated_classes_spanning_multiple_files'])
    # Evidence structural auditing: all original evidence locators must be resolvable.
    location_problems=[]
    for x in GO.values():
        check_evidence({'generated_evidence':[{'file':x['file'],'line_start':x['line_start'],
          'line_end':x['line_end'],'raw_quote_en':x['raw_quote_en']}]},source_lines,
          location_problems,'raw_generated_occurrence',x['occurrence_id'])
    for x in NA.values():check_evidence(x,source_lines,location_problems,'TP_proof',x['source_id'])
    for x in matches.values():
        if x['scoring_cell']=='TP':check_evidence(x,source_lines,location_problems,'TP_matching',x['source_id'])
    # Check that the physical PDF really has 90 pages and pages quoted in R are valid.
    pdf_files=list(root.glob('OrionDesk_AI_Detailed_Design_Specification*.pdf'))
    assert len(pdf_files)==1,'Require exactly one original PDF'
    physical_pages=0;pdf_quote_pass=pdf_quote_not_text=[]
    pdf_quote_pass=[];pdf_quote_not_text=[]
    try:
        import fitz
        pdf=fitz.open(pdf_files[0]);physical_pages=pdf.page_count
        assert physical_pages==90,f'PDF has {physical_pages}, expected 90 physical pages'
        pdf_text=[pdf.load_page(i).get_text() for i in range(physical_pages)]
        for sid,x in R.items():
            p=x['physical_page'];assert 1<=p<=physical_pages
            if scan_quote(pdf_text[p-1],x['quote_en']):pdf_quote_pass.append(sid)
            else:pdf_quote_not_text.append({'source_id':sid,'page':p,'quote_en':x['quote_en'][:200],
                   'possible_explanation':'Figure-image text or wrapped/table normalization; requires image-aware validation'})
    except ImportError:
        physical_pages=None
    # Every source page must be accounted for, including nonnormative pages.
    page_coverage=json.loads((base/'01_pdf_page_coverage.json').read_text()) if (base/'01_pdf_page_coverage.json').exists() else None
    if page_coverage is not None:
        assert len(page_coverage)==90 and {r['physical_pdf_page'] for r in page_coverage}==set(range(1,91))
    line_coverage=json.loads((base/'02_generated_corpus_coverage.json').read_text()) if (base/'02_generated_corpus_coverage.json').exists() else None
    # Check delivered final coverage, final phases, and authored-language surface.
    final_page=base/'01_pdf_page_coverage_final.json'
    if final_page.exists():
        revised=json.loads(final_page.read_text(encoding='utf-8'))
        assert len(revised)==90
        page_R=collections.Counter(x['physical_page'] for x in R.values())
        page_N=collections.Counter(x['pdf_page'] for x in N.values())
        assert all(x['positive_atom_count']==page_R[x['physical_pdf_page']] and
                   x['negative_control_count']==page_N[x['physical_pdf_page']] for x in revised)
    report_names=['06_metrics_final.md','08_coverage_and_limitations.md',
                  '04_confusion_matrix_final.md','05_duplicate_metrics_final.md']
    for name in report_names:
        fp=base/name
        assert fp.exists(),f'Missing mandatory final authored report {name}'
        report=fp.read_text(encoding='utf-8')
        assert not re.search(r'[\u3040-\u30ff\u3400-\u9fff]',report),f'Non-English script detected in {name}'
    for name in ('06_metrics_final.md','08_coverage_and_limitations.md'):
        assert 'FINAL_BEST_EFFORT' in (base/name).read_text(encoding='utf-8')
    # No output archives, no unsupported synthesized comparison for a single method.
    assert not any(p.suffix.lower() in ('.zip','.tar','.gz','.7z') for p in base.iterdir() if p.is_file())
    # Final statistics, independently derived and not imported from prior summaries.
    TP=counts['TP'];TN=counts['TN'];FP=counts['FP'];FN=counts['FN']
    precision=ratio(TP,TP+FP);recall=ratio(TP,TP+FN)
    f1=ratio(2*TP,2*TP+FP+FN)
    duplicate=ratio(len(GO)-len(GC),len(GO))
    uncertain_generated=sum(x.get('pdf_support_grade')=='E1_UNCERTAIN' for x in validity.values())
    eligibility_concerns=sum(bool(x.get('eligibility_concern')) for x in validity.values())
    unverified_class_proofs=sum(not x.get('phase5_independent_semantic_certified',False) for x in validity.values())
    grade_counts=dict(collections.Counter(x.get('entailment_grade') for x in matches.values()))
    semantic_limited=(uncertain_generated>0 or unverified_class_proofs>0 or bool(location_problems) or
      bool(pdf_quote_not_text) or any(x.get('proof_review_level')!='INDEPENDENTLY_VERIFIED' for x in NA.values()))
    status='FINAL_BEST_EFFORT' if semantic_limited else 'FINAL_VERIFIED'
    summary={
       'prefix':'supplied_eight_file_set','status':status,'protocol_version':'6.1',
       'universe':{'source_positive_atoms':len(R),'source_negative_controls':len(N),
          'raw_generated_claim_classes':len(GC),'generated_positive_occurrences':len(GO),
          'covered_source_atoms':len(A),'asserted_negative_controls':len(asserted_N),
          'unsupported_generated_only_propositions':len(canonical_F),
          'canonical_predicted_positive_units':TP+FP,'canonical_decision_units':len(J),
          'negative_universe_scope':'PDF-grounded predeclared bounded controls only'},
       'confusion':{'TP':TP,'TN':TN,'FP':FP,'FN':FN},
       'metrics':{'Precision':precision,'Recall':recall,'F1':f1,'Duplicate':duplicate},
       'duplicate':{'eligible_generated_occurrences':len(GO),'unique_generated_claim_classes':len(GC),
          'duplicate_excess_occurrences':len(GO)-len(GC),'within_file_excess':within,
          'across_file_excess':across,'repeated_claim_class_count':repeated,
          'repeated_classes_spanning_multiple_files':spans},
       'fn_root_causes':dict(sorted(final_fn_causes.items())),
       'audits':{'source_atomization_review_records':len(atom_audits),
          'source_atoms_excluded_in_corrections':len(removed),'source_line_wrap_corrections':len(corrected),
          'initial_FN_challenge_records':len(fn_audit),
          'matcher_FN_candidates_corrected_to_TP':sum(x['fn_review_disposition']=='MATCHER_FALSE_NEGATIVE_CORRECTED' for x in fn_audit),
          'final_TP_proof_records':len(A),'TP_review_ledger_rows':len(NA),
          'TP_ledger_review_not_independently_certified':sum(x.get('proof_review_level')!='INDEPENDENTLY_VERIFIED' for x in NA.values()),
          'generated_class_E1_support_uncertainty':uncertain_generated,
          'generated_class_eligibility_concerns':eligibility_concerns,
          'generated_class_semantic_proof_uncertified':unverified_class_proofs,
          'source_evidence_quotes_found_in_pdf_text':len(pdf_quote_pass),
          'source_evidence_quotes_not_literal_in_pdf_text':len(pdf_quote_not_text),
          'generated_evidence_location_issues':len(location_problems)},
       'input_coverage':{'pdf_original':pdf_files[0].name,'pdf_physical_pages':physical_pages,
          'markdown_roles':{k:v.name for k,v in sorted(sources.items())},
          'markdown_line_counts':{k:len(source_lines[v.name]) for k,v in sorted(sources.items())},
          'source_pages_represented_in_positive_ledger':len({x['physical_page'] for x in R.values()}),
          'generated_physical_lines_audited':len(line_entries),
          'prior_phase1_page_coverage_available':page_coverage is not None,
          'prior_phase2_line_coverage_available':(base/'02_generated_line_coverage.jsonl').exists()},
       'structural_checks':'PASS' if not location_problems else 'PASS_WITH_EVIDENCE_LOCATION_WARNINGS',
       'metric_interpretation':('Independent arithmetic on one effective canonical proposition universe. '
          'Raw generated class counts are separate and must not equal TP+FP. TN is a fixed bounded diagnostic count. '
          'Provisional metrics do not certify semantic completeness or precision; FP=0 is only zero established unsupported propositions.')
    }
    (out/'06_metrics_final.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    checks={'status':status,'all_canonical_equations_pass':True,'all_unique_membership_tests_pass':True,
         'all_FN_have_final_disposition':True,'all_final_TP_have_proof_audit':True,
         'generated_quote_or_line_issues':location_problems[:80],
         'generated_quote_or_line_issue_count':len(location_problems),
         'pdf_quotes_not_literal_in_text_layer':pdf_quote_not_text[:35],
         'pdf_quotes_not_literal_count':len(pdf_quote_not_text),
         'final_FN_source_ids':sorted(canonical_R-A),
         'generated_class_support_grades':dict(collections.Counter(x.get('pdf_support_grade') for x in validity.values())),
         'source_entailment_grades':grade_counts,
         'warning':'Evidence availability and structural arithmetic cannot certify all full-predicate semantic entailments.'}
    (out/'06_validation_results.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':status,'confusion':summary['confusion'],'metrics':summary['metrics'],
        'evidence_location_issues':len(location_problems),'pdf_text_quote_misses':len(pdf_quote_not_text),
        'source_pages_covered':summary['input_coverage']['source_pages_represented_in_positive_ledger'],
        'class_E1_uncertain':uncertain_generated},indent=2))
    return 0

if __name__=='__main__':sys.exit(main())
