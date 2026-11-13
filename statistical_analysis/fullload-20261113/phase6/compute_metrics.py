#!/usr/bin/env python3
"""Independent phase-6 recomputation over one canonical effective-proposition universe.

Usage: python compute_metrics.py [--root /path/to/final-directory] [--output /path/to/report.json]
No expected score totals are embedded. This checker verifies item-level arithmetic,
provenance locators and declared proof availability; it cannot certify logical entailment.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,re,sys
from pathlib import Path

REQUIRED_ROLES=['01_screen_functions','02_api','03_data','04_batch_functions','05_business_rules','06_exception_handling','07_processing_flows','08_architecture_decision']
PREDICATES=('target','action','actor','condition','scope','timing','constraint','exception','outcome','version')
CELLS={'TP':(1,1),'FN':(1,0),'FP':(0,1),'TN':(0,0)}

def load_jsonl(d:Path,n:str):
    return [json.loads(s) for s in (d/n).read_text(encoding='utf-8').splitlines() if s.strip()]

def by_unique(items,key):
    out={}
    for x in items:
        k=x[key]
        if k in out:raise AssertionError(f'duplicate {key}: {k}')
        out[k]=x
    return out

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def recompute(d:Path)->dict:
    src=load_jsonl(d,'01_source_atoms_final.jsonl'); neg=load_jsonl(d,'01_source_negative_controls_final.jsonl')
    occ=load_jsonl(d,'02_generated_atoms_final.jsonl'); g=load_jsonl(d,'02_generated_classes_final.jsonl')
    bridges=load_jsonl(d,'03_semantic_coverage_bridges_final.jsonl'); evidence=load_jsonl(d,'03_evidence_matches_final.jsonl')
    fn_aud=load_jsonl(d,'03_fn_root_cause_audit_final.jsonl');tp_aud=load_jsonl(d,'05_tp_evidence_audit_final.jsonl')
    source_aud=load_jsonl(d,'05_source_atomization_audit_final.jsonl')
    validity=load_jsonl(d,'04_generated_claim_validity_final.jsonl');classes_dup=load_jsonl(d,'04_duplicate_classes_final.jsonl')
    universe=load_jsonl(d,'03_canonical_universe_final.jsonl');judgments=load_jsonl(d,'04_atomic_judgments_final.jsonl')
    neg_aud=load_jsonl(d,'05_negative_control_audit_final.jsonl')
    delta=load_jsonl(d,'07_change_delta.jsonl')
    R=by_unique(src,'source_id');N=by_unique(neg,'negative_control_id');O=by_unique(occ,'occurrence_id')
    G=by_unique(g,'class_id');V=by_unique(validity,'generated_class_id')
    E=by_unique(evidence,'source_id');B=by_unique(bridges,'source_id')
    TP_A=by_unique(tp_aud,'source_id');S_A=by_unique(source_aud,'source_id')
    FN_A=by_unique(fn_aud,'source_id');DUP=by_unique(classes_dup,'class_id')
    NEG_A=by_unique(neg_aud,'negative_control_id');U=by_unique(universe,'canonical_id');J=by_unique(judgments,'canonical_id')
    assert set(R).isdisjoint(N),'R and N overlap'
    assert set(R)==set(E)==set(S_A),'source inventories/audit incomplete'
    assert set(G)==set(V)==set(DUP),'generated class inventory/validity/duplication incomplete'
    assert set(U)==set(J),'canonical universe differs from judgment ledger'
    assert set(NEG_A)==set(N),'negative control audit incomplete'
    assert all(x['method']=='provided_eight_documents' for x in occ+g+validity+evidence), 'cross-method contamination'
    assert all(x.get('eligibility') in ('DEFINITIVE','ELIGIBLE') for x in occ),'ineligible occurrence counted'
    assert set(x['class_id'] for x in occ)==set(G)
    membership=collections.defaultdict(list)
    for x in occ:membership[x['class_id']].append(x['occurrence_id'])
    for cid,row in G.items():
        assert set(row['occurrence_ids'])==set(membership[cid])
        assert row['occurrence_count']==len(membership[cid])
        assert set(V[cid]['occurrence_ids'])==set(membership[cid])
        assert set(DUP[cid]['occurrence_ids'])==set(membership[cid])
    assert len(O)>=len(G)
    # Evidence quote and source page checks. PDF is the only normative source.
    import fitz
    pdfpath=d/'OrionDesk_AI_Detailed_Design_Specification.pdf'
    assert pdfpath.exists(),f'original PDF copy missing: {pdfpath}'
    pdf=fitz.open(pdfpath);assert len(pdf)==90
    pages=[p.get_text('text') for p in pdf]
    assert all(t.strip() for t in pages),'unreadable PDF page'
    inputdir=d.parent
    files={}
    for prefix in REQUIRED_ROLES:
        options=list(inputdir.glob(prefix+'*.md'))
        assert len(options)==1,(prefix,options)
        files[options[0].name]=options[0].read_text(encoding='utf-8').splitlines()
    line_count=sum(len(lines) for lines in files.values())
    for x in occ:
        assert x['file'] in files
        ln=x['line_start'];end=x['line_end'];assert 1<=ln<=end<=len(files[x['file']])
        assert x['quote_en'].strip() in '\n'.join(files[x['file']][ln-1:end]), (x['occurrence_id'],'quote mismatch')
    for x in src:
        assert 1<=x['physical_page']<=len(pages)
        assert x.get('pdf_evidence'),'source atom has no PDF evidence'
    for x in neg:
        assert x.get('pdf_evidence'), 'negative control without PDF evidence'
        assert 1<=x['pdf_page']<=len(pages)
    by_cell=collections.Counter()
    positive=set();asserted_controls=set();unsupported=set()
    for cid,x in U.items():
        y=J[cid]
        assert x['scoring_cell']==y['scoring_cell']
        assert x['actual_label']==y['actual_label'] and x['predicted_label']==y['predicted_label']
        c=x['scoring_cell'];assert c in CELLS and CELLS[c]==(x['actual_label'],x['predicted_label'])
        by_cell[c]+=1
        k=x['unit_kind']
        if k=='PDF_POSITIVE':
            assert cid in R and x['origin_source_ids']==[cid] and not x['origin_negative_control_ids']
            assert E[cid]['scoring_cell']==c
            if c=='TP':positive.add(cid)
            else:assert c=='FN'
        elif k=='BOUNDED_PDF_NEGATIVE':
            assert cid in N and x['origin_negative_control_ids']==[cid] and not x['origin_source_ids']
            if c=='FP':asserted_controls.add(cid)
            else:assert c=='TN'
        elif k=='GENERATED_ONLY_UNENTAILED':
            assert c=='FP' and not x['origin_source_ids'] and not x['origin_negative_control_ids']
            assert x['origin_generated_class_ids']
            assert all(V[q]['validity_label']=='PDF_UNSUPPORTED' for q in x['origin_generated_class_ids'])
            unsupported.add(cid)
        else:raise AssertionError(('unsupported unit_kind',k))
    assert len(U)==len(R)+len(N)+len(unsupported),'canonical universe size not R+N+F'
    assert by_cell['TP']==len(positive) and by_cell['FN']==len(R)-len(positive)
    assert by_cell['TN']==len(N)-len(asserted_controls)
    assert by_cell['FP']==len(unsupported)+len(asserted_controls)
    assert by_cell['TP']+by_cell['FP']==sum(x['predicted_label']==1 for x in U.values())
    assert len(unsupported)==sum(x['validity_label']=='PDF_UNSUPPORTED' for x in validity)
    assert set(x['origin_generated_class_ids'][0] for x in U.values() if x['unit_kind']=='GENERATED_ONLY_UNENTAILED') ==set(v['generated_class_id'] for v in validity if v['validity_label']=='PDF_UNSUPPORTED')
    assert not asserted_controls.intersection(unsupported),'asserted negative double-counted'
    # TP predicate evidence and reverse-FN audit: structural checks only.
    assert set(B)<=positive,'source bridge is not a TP'
    assert all(cid in TP_A for cid in positive)
    assert all(cid in FN_A for cid in set(R)-positive)
    assert sum(x['final_cell']=='TP' for x in tp_aud)==len(positive)
    assert all(x.get('pdf_evidence') and x.get('generated_evidence') for x in tp_aud if x['final_cell']=='TP')
    assert all(x.get('coverage_mode') and x.get('source_membership_and_entailment_bridge_en') for x in tp_aud if x['final_cell']=='TP')
    for cid in positive:
        match=E[cid]
        assert match.get('entailment_grade') in ('E2','E3')
        assert match.get('generated_evidence') and match.get('pdf_evidence')
        assert set(match.get('generated_class_ids',[]))<=set(G)
        pred=match.get('predicate_check_en',{})
        assert all(t in pred and pred[t].get('status') in ('MET','NOT_APPLICABLE') for t in PREDICATES),(cid,'incomplete predicate checklist')
        if match['entailment_grade']=='E2':
            assert match.get('full_predicate_proof_en'),cid
            assert cid in B or match['coverage_mode']=='DIRECT_EQUIVALENCE',cid
        assert TP_A[cid]['final_cell']=='TP'
    allowed={'TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'}
    fncounts=collections.Counter()
    candidateloc_missing=[]
    for cid in set(R)-positive:
        a=FN_A[cid];assert a['final_scoring_cell']=='FN'
        assert a['fn_review_disposition'] in allowed
        assert a.get('pdf_evidence') and a.get('unmet_predicates_en')
        assert a.get('universal_context_conjunction_checked') and a.get('exact_and_alias_keys_checked')
        if not a.get('best_generated_candidates'):candidateloc_missing.append(cid)
        fncounts[a['fn_review_disposition']]+=1
    assert sum(fncounts.values())==by_cell['FN']
    for cid,a in FN_A.items():
        if a['fn_review_disposition']=='MATCHER_FALSE_NEGATIVE_CORRECTED':
            assert cid in positive,'corrected FN still scored FN'
    # Verify all source-atomization records reference extant source IDs.
    assert set(S_A)==set(R)
    changed=[x for x in source_aud if x.get('change_applied')]
    assert all(x.get('new_source_ids') for x in changed)
    # Negative controls must have a real PDF-scoped nonassertion audit.
    assert all(NEG_A[cid]['final_scoring_cell']==('FP' if cid in asserted_controls else 'TN') for cid in N)
    # Raw duplicate class partition.
    within=across=repeat=multi=0
    for cid,x in DUP.items():
        ex=x['duplicate_excess_count'];assert ex==len(membership[cid])-1
        assert x['within_file_excess']+x['across_file_excess']==ex
        within+=x['within_file_excess'];across+=x['across_file_excess']
        repeat+=int(len(membership[cid])>=2)
        multi+=int(bool(x['spans_multiple_files']) and len(membership[cid])>=2)
        if ex:
            part=x.get('excess_occurrence_partition',[])
            assert len(part)==ex
    excess=len(O)-len(G)
    assert within+across==excess
    TP=by_cell['TP'];FN=by_cell['FN'];TN=by_cell['TN'];FP=by_cell['FP']
    prec=TP/(TP+FP) if TP+FP else None
    rec=TP/(TP+FN) if TP+FN else None
    f1=2*TP/(2*TP+FP+FN) if 2*TP+FP+FN else None
    duplicate=excess/len(O) if O else None
    counts=collections.Counter(x['validity_label'] for x in validity)
    assert counts['PDF_UNSUPPORTED']==len(unsupported)
    # PDF reference quote: some text-cell wraps are represented in the original PDF as separate text lines.
    norm=lambda s:re.sub(r'\s+',' ',s).strip().lower()
    pdfquote_match=sum(norm(x['quote_en']) in norm(pages[x['physical_page']-1]) for x in src)
    md_evidence_locs=0;md_evidence_match=0
    for row in evidence:
        for ev in row.get('generated_evidence',[]):
            if ev.get('file') in files and isinstance(ev.get('line_start'),int):
                md_evidence_locs+=1
                ln=ev['line_start'];en=ev.get('line_end',ln)
                if 1<=ln<=en<=len(files[ev['file']]) and ev.get('quote_en','').strip() in '\n'.join(files[ev['file']][ln-1:en]):md_evidence_match+=1
    summary={
      'prefix':'provided_eight_documents','status':'FINAL_BEST_EFFORT','protocol_version':'6.1',
      'universe':{'source_positive_atoms':len(R),'source_negative_controls':len(N),
        'raw_generated_claim_classes':len(G),'generated_positive_occurrences':len(O),
        'covered_source_atoms':len(positive),'asserted_negative_controls':len(asserted_controls),
        'unsupported_generated_only_propositions':len(unsupported),
        'canonical_predicted_positive_units':TP+FP,'canonical_decision_units':len(U),
        'negative_universe_scope':'PDF-grounded, predeclared bounded controls only'},
      'confusion':{'TP':TP,'TN':TN,'FP':FP,'FN':FN},
      'metrics':{'Precision':prec,'Recall':rec,'F1':f1,'Duplicate':duplicate},
      'duplicate':{'eligible_generated_occurrences':len(O),'unique_generated_claim_classes':len(G),
        'duplicate_excess_occurrences':excess,'within_file_excess':within,'across_file_excess':across,
        'repeated_claim_class_count':repeat,'repeated_classes_spanning_multiple_files':multi},
      'generated_validity_counts':dict(sorted(counts.items())),
      'FN_root_cause_counts':dict(sorted(fncounts.items())),
      'audits':{'tp_final_proof_rows':sum(x['final_cell']=='TP' for x in tp_aud),
        'tp_downgraded_proof_rows':sum(x['final_cell']=='FN' for x in tp_aud),
        'fn_initially_challenged_rows':len(fn_aud),
        'fn_corrected_to_tp_rows':sum(x['fn_review_disposition']=='MATCHER_FALSE_NEGATIVE_CORRECTED' for x in fn_aud),
        'source_atomization_audit_rows':len(source_aud),'source_atomization_changed_records':len(changed),
        'negative_control_audit_rows':len(neg_aud),'phase_change_delta_rows':len(delta),
        'source_PDF_quote_whitespace_exact_matches':pdfquote_match,
        'source_PDF_quote_total':len(src),
        'generated_match_evidence_quote_matches':md_evidence_match,
        'generated_match_evidence_quote_locations':md_evidence_locs,
        'FN_without_generated_candidate_locator':len(candidateloc_missing),
        'FN_without_generated_candidate_ids':candidateloc_missing[:50]},
      'input_coverage':{'pdf_physical_pages':len(pdf),'pdf_nonempty_text_pages':sum(bool(p.strip()) for p in pages),
        'scored_markdown_roles':len(files),'scored_markdown_lines':line_count,
        'scored_files':[{ 'file':f,'line_count':len(v),'sha256':sha(inputdir/f)} for f,v in sorted(files.items())],
        'original_pdf_sha256':sha(pdfpath)},
      'metric_interpretation':'Precision, Recall and F1 use the effective canonical proposition universe, not raw generated-class precision. Duplicate uses eligible raw occurrences and semantic classes. TN covers only fixed negative controls. Structural checks cannot certify the completeness of semantic entailment.',
      'semantic_certification':'NOT_CERTIFIED: PDF-source predicates, 191 conservative FNs and many generated validity classes remain subject to independent semantic interpretation; the arithmetic is independently reproducible.'}
    return summary

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--output',type=Path,default=None)
    args=ap.parse_args()
    result=recompute(args.root)
    result_json=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:args.output.write_text(result_json,encoding='utf-8')
    print(result_json)
