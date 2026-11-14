#!/usr/bin/env python3
"""Independent item-ledger recomputation for OrionDesk evaluation protocol 6.1.

Usage: python compute_metrics.py --ledger-dir /path/to/phase6 --input-dir /path/to/uploads
No historical expected totals are hard-coded. Arithmetic and structural checks are
not substitutes for a semantic proof of entailment.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, re, sys
from pathlib import Path
from datetime import datetime, timezone

REQUIRED_LEDGER_FILES = [
    '01_source_atoms_final.jsonl', '01_source_negative_controls_final.jsonl',
    '02_generated_atoms_final.jsonl', '02_generated_classes_final.jsonl',
    '03_canonical_universe_final.jsonl', '03_evidence_matches_final.jsonl',
    '03_semantic_coverage_bridges_final.jsonl', '03_fn_root_cause_audit_final.jsonl',
    '04_generated_claim_validity_final.jsonl', '04_atomic_judgments_final.jsonl',
    '04_duplicate_classes_final.jsonl', '05_duplicate_metrics_final.json',
    '05_tp_evidence_audit_final.jsonl', '05_source_atomization_audit_final.jsonl',
    '07_change_delta.jsonl'
]
SCORING_ROLES = ['01_screen_functions', '02_api', '03_data',
    '04_batch_functions', '05_business_rules', '06_exception_handling',
    '07_processing_flows', '08_architecture_decision']
PREDICATES = ['actor','target','action','scope','condition','exception',
              'timing','outcome','version','polarity']
FINAL_FN_DISPOSITIONS = {'TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED'}


def jsonl(path):
    with path.open('r', encoding='utf-8') as f:
        for i,line in enumerate(f,1):
            if line.strip():
                try: yield json.loads(line)
                except Exception as exc: raise ValueError(f'{path.name}:{i}: {exc}')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def one_per(rows,key,label,errors):
    data={}
    for item in rows:
        k=item.get(key)
        if k is None: errors.append(f'{label}: missing {key}'); continue
        if k in data: errors.append(f'{label}: duplicate {k}')
        data[k]=item
    return data


def sane_fraction(a,b,zero=None): return a/b if b else zero


def norm(s):
    return re.sub(r'\s+',' ',str(s or '').replace('**','').replace('`','')).strip().lower()


def content_match(snippet, line):
    q=norm(snippet); t=norm(line)
    return bool(q) and (q in t or (len(q)>35 and q[:35] in t))


def check_evidence_locator(item, originals, errors, warnings, label, strict_line=False):
    file=item.get('file')
    if file not in originals:
        errors.append(f'{label}: unknown generated file {file!r}')
        return False
    line=item.get('line_start')
    if not isinstance(line,int) or not (1 <= line <= len(originals[file])):
        errors.append(f'{label}: invalid physical line {file}:{line}')
        return False
    end=item.get('line_end',line)
    if end is None: end=line
    if not isinstance(end,int) or not (line <= end <= len(originals[file])):
        errors.append(f'{label}: invalid line range {file}:{line}-{end}')
        return False
    text='\n'.join(originals[file][line-1:end])
    if not text.strip():
        errors.append(f'{label}: points to blank line {file}:{line}')
        return False
    table=item.get('table_cell')
    if table:
        col=table.get('column_index')
        if col is not None and (not isinstance(col,int) or col < 1 or '|' not in text):
            errors.append(f'{label}: invalid column-index table context {file}:{line}:{col}')
            return False
        if col is None and ('row_key' in table or 'column_heading' in table) and '|' not in text:
            warnings.append(f'{label}: legacy table-context locator points to prose {file}:{line}')
    quote=item.get('quote_en') or item.get('generated_quote_en')
    if strict_line and quote and not content_match(quote,text):
        warnings.append(f'{label}: quotation not literally recoverable at {file}:{line}')
    return True


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--ledger-dir', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--input-dir', type=Path, default=Path(__file__).resolve().parent.parent)
    p.add_argument('--no-write', action='store_true')
    args=p.parse_args()
    d=args.ledger_dir.resolve(); root=args.input_dir.resolve()
    errors=[]; warnings=[]; checks={}; diagnostics={}
    for n in REQUIRED_LEDGER_FILES:
        if not (d/n).is_file(): errors.append('Mandatory ledger missing: '+n)
    if errors: raise RuntimeError('; '.join(errors))

    R=one_per(jsonl(d/'01_source_atoms_final.jsonl'),'source_id','R',errors)
    N=one_per(jsonl(d/'01_source_negative_controls_final.jsonl'),'negative_control_id','N',errors)
    GO=one_per(jsonl(d/'02_generated_atoms_final.jsonl'),'occurrence_id','GO',errors)
    GC=one_per(jsonl(d/'02_generated_classes_final.jsonl'),'class_id','G',errors)
    U=one_per(jsonl(d/'03_canonical_universe_final.jsonl'),'canonical_id','U',errors)
    J=one_per(jsonl(d/'04_atomic_judgments_final.jsonl'),'canonical_id','judgments',errors)
    E=one_per(jsonl(d/'03_evidence_matches_final.jsonl'),'source_id','source evidence',errors)
    BR=one_per(jsonl(d/'03_semantic_coverage_bridges_final.jsonl'),'source_id','source bridges',errors)
    FN_A=one_per(jsonl(d/'03_fn_root_cause_audit_final.jsonl'),'source_id','FN audit',errors)
    TP_A=one_per(jsonl(d/'05_tp_evidence_audit_final.jsonl'),'source_id','TP proof audit',errors)
    GV=one_per(jsonl(d/'04_generated_claim_validity_final.jsonl'),'class_id','generated validity',errors)
    AT=one_per(jsonl(d/'05_source_atomization_audit_final.jsonl'),'source_id','atomization',errors)
    DUP=one_per(jsonl(d/'04_duplicate_classes_final.jsonl'),'class_id','duplicate classes',errors)
    changes=list(jsonl(d/'07_change_delta.jsonl'))
    stated_duplicate=read(d/'05_duplicate_metrics_final.json')
    methods={o.get('method') for o in GO.values()}|{c.get('method') for c in GC.values()}|{j.get('method') for j in J.values()}
    if None in methods or len(methods)!=1: errors.append(f'Method isolation broken: {methods}')
    method=next(iter(methods)) if len(methods)==1 else 'UNKNOWN'

    # Re-open exact scored Markdown inputs, preserving copy suffixes.
    input_names=sorted({o['file'] for o in GO.values()})
    original={}
    for name in input_names:
        path=root/name
        if not path.is_file(): errors.append('Scored input missing: '+name); continue
        original[name]=path.read_text(encoding='utf-8-sig').splitlines()
    for role in SCORING_ROLES:
        choices=[n for n in input_names if Path(n).name.startswith(role) and Path(n).suffix=='.md']
        if len(choices)!=1: errors.append(f'Ambiguous/missing scored role {role}: {choices}')
    if len(input_names)!=len(SCORING_ROLES): errors.append(f'Expected {len(SCORING_ROLES)} scored roles, got {len(input_names)} inputs')
    file_order={next((n for n in input_names if n.startswith(role)),role):i for i,role in enumerate(SCORING_ROLES)}
    inspected_lines=0; inspected_cells=0
    if (d/'02_line_cell_coverage_final.jsonl').is_file():
        line_cov=list(jsonl(d/'02_line_cell_coverage_final.jsonl'))
        idx={(x.get('file'),x.get('physical_line')):x for x in line_cov}
        if len(idx)!=len(line_cov):errors.append('Duplicate physical line coverage records')
        for f,lines in original.items():
            for li,raw in enumerate(lines,1):
                row=idx.get((f,li))
                if not row:errors.append(f'Uninspected physical input line: {f}:{li}');continue
                if row.get('raw_line_en')!=raw:errors.append(f'Line coverage text changed: {f}:{li}')
                inspected_lines+=1
        if len(idx)!=sum(map(len,original.values())):
            errors.append('Line coverage inventory cardinality differs from originals')
    else: warnings.append('Physical line coverage ledger unavailable')
    if (d/'02_table_cell_coverage_final.jsonl').is_file():
        table_rows=list(jsonl(d/'02_table_cell_coverage_final.jsonl'))
        for item in table_rows:
            f=item.get('file');ln=item.get('physical_line'); col=item.get('table_cell',{}).get('column_index')
            if f not in original or not isinstance(ln,int) or not (1<=ln<=len(original[f])):
                errors.append(f'Invalid table coverage locator {f}:{ln}')
            elif '|' not in original[f][ln-1] or not isinstance(col,int):
                errors.append(f'Invalid source Markdown table-cell row {f}:{ln}:{col}')
            inspected_cells+=1
        # Require only that earlier phase enumerated actual cells; do not claim independent semantic line-by-line comprehension.
    else: warnings.append('Table cell coverage ledger unavailable')

    # Validate source identity and physical page enumeration.
    pdfs=sorted(root.glob('OrionDesk_AI_Detailed_Design_Specification*.pdf'))
    if len(pdfs)!=1: errors.append(f'PDF original not uniquely identified: {[x.name for x in pdfs]}')
    pdf_filename=pdfs[0].name if len(pdfs)==1 else None
    pdf_page_count=None; pdf_page_text=[]
    if pdf_filename:
        try:
            import fitz
            with fitz.open(pdfs[0]) as doc:
                pdf_page_count=len(doc)
                pdf_page_text=[page.get_text('text') for page in doc]
                if any(len(x.strip())<10 for x in pdf_page_text):errors.append('An original PDF physical page has unreadable text')
        except Exception as exc:errors.append(f'Cannot inspect original PDF: {exc}')
    pg_cov=list(jsonl(d/'01_pdf_page_coverage.jsonl')) if (d/'01_pdf_page_coverage.jsonl').exists() else []
    if pdf_page_count is not None:
        if sorted(x.get('physical_page') for x in pg_cov)!=list(range(1,pdf_page_count+1)):
            errors.append('PDF physical-page coverage ledger incomplete')
    if any(not x.get('page_readable') for x in pg_cov):errors.append('PDF source page marked unreadable')

    # Disjoint canonical ID universes and complete enumerated U.
    if set(R)&set(N):errors.append('Source-positive/negative ID overlap')
    if set(U)!=set(J):errors.append('Canonical U differs from final judgments')
    if not (set(R)|set(N))<=set(U):errors.append('Source/negative controls missing from U')
    if set(R)&set(U)-set(R):pass # no-op; IDs are disjoint by source namespace
    if any(k in GC for k in U):errors.append('Raw generated class ID collides with canonical unit')
    for sid in R:
        if sid not in E:errors.append(f'Missing source-evidence match {sid}')
        if sid not in AT:errors.append(f'Missing atomization audit for surviving {sid}')
    for gid in GC:
        if gid not in GV:errors.append(f'Missing generated class validity {gid}')

    # Per occurrence membership, one class per occurrence and no invisible generated records.
    assigned=collections.Counter()
    for cid,c in GC.items():
        if c['method']!=method:errors.append(f'Cross-method class {cid}')
        members=c.get('occurrence_ids',[])
        if not members:errors.append(f'Class with no occurrence: {cid}')
        if c.get('occurrence_count')!=len(members):errors.append(f'Class occurrence count mismatch: {cid}')
        for oid in members:
            assigned[oid]+=1
            if oid not in GO:errors.append(f'Nonexistent occurrence: {cid}/{oid}')
            elif GO[oid].get('semantic_class_id')!=cid:errors.append(f'Occurrence has inconsistent class: {oid}')
        if c.get('representative_occurrence_id') not in members:errors.append(f'Class representative not in membership: {cid}')
    for oid,o in GO.items():
        if assigned[oid]!=1:errors.append(f'Occurrence not assigned to exactly one class: {oid} ({assigned[oid]})')
        if o['method']!=method:errors.append(f'Cross-method occurrence {oid}')
        check_evidence_locator(o,original,errors,warnings,'GO/'+oid)
        if o.get('quote_en') and not content_match(o['quote_en'], original.get(o.get('file'),[''])[o['line_start']-1] if o.get('file') in original and 1<=o.get('line_start',0)<=len(original[o['file']]) else ''):
            warnings.append(f'Occurrence quotation not literally recoverable at {oid}')

    # Verify uniqueness, cross-direction links, and fixed negative controls.
    cells=collections.Counter()
    TPids=set();FNids=set();TNids=set();Bids=set();Fids=set()
    for uid,j in J.items():
        u=U[uid]
        if j.get('method')!=method or u.get('method')!=method:errors.append(f'Cross-method canonical unit {uid}')
        if j.get('scoring_cell')!=u.get('scoring_cell') or j.get('actual_label')!=u.get('actual_label') or j.get('predicted_label')!=u.get('predicted_label'):
            errors.append(f'Judgment/universe mismatch {uid}')
        actual=j.get('actual_label'); predicted=j.get('predicted_label'); cell=j.get('scoring_cell')
        expected={(1,1):'TP',(1,0):'FN',(0,1):'FP',(0,0):'TN'}.get((actual,predicted))
        if cell!=expected:errors.append(f'Invalid canonical binary cell {uid} {actual}/{predicted}/{cell}')
        cells[cell]+=1
        if uid in R:
            if actual!=1 or j.get('origin_source_ids')!=[uid]:errors.append(f'Malformed source unit {uid}')
            if cell=='TP':TPids.add(uid)
            if cell=='FN':FNids.add(uid)
        elif uid in N:
            if actual!=0 or j.get('origin_negative_control_ids')!=[uid]:errors.append(f'Malformed negative unit {uid}')
            if cell=='TN':TNids.add(uid)
            else:Bids.add(uid)
        else:
            if cell!='FP' or actual!=0 or predicted!=1: errors.append(f'Unsupported-only unit is not FP {uid}')
            if not j.get('origin_generated_class_ids'):errors.append(f'FP lacks originating generated class {uid}')
            if uid in GC:errors.append(f'Unsupported unit collides with generated class ID {uid}')
            Fids.add(uid)
        if uid in R and cell in ('TP','FN'):
            ev=j.get('pdf_evidence') or []
            if not ev:errors.append(f'Source judgment lacks PDF evidence: {uid}')
            for z in ev:
                pg=z.get('physical_page')
                if z.get('file')!=pdf_filename or not isinstance(pg,int) or not (1<=pg<=(pdf_page_count or 0)):
                    errors.append(f'Invalid PDF evidence page/file for {uid}')
    if set(U)!=(set(R)|set(N)|Fids):errors.append('Canonical universe does not enumerate exactly R+N+F')
    if Bids & Fids:errors.append('Duplicate asserted negative control in generated-only FP')

    # TP evidence quality: full-predicate map must be present; certification is counted, not presumed.
    proof_status=collections.Counter(); proof_semantic_certified=0; tp_missing_fieldproof=0
    tp_E2=0; tp_E3=0; bridge_modes=collections.Counter()
    for sid in TPids:
        j=J[sid];t=TP_A.get(sid)
        if not t or t.get('final_cell')!='TP': errors.append(f'Final TP missing retained proof record: {sid}');continue
        grade=j.get('entailment_grade')
        if grade not in ('E2','E3'):errors.append(f'TP non-entailing grade {sid}:{grade}')
        if grade=='E2':tp_E2+=1
        else:tp_E3+=1
        bridge_modes[j.get('coverage_mode')]+=1
        ids=j.get('origin_generated_class_ids') or []
        if not ids or not all(cid in GC for cid in ids):errors.append(f'TP missing eligible class reference: {sid}')
        if not j.get('generated_evidence'):errors.append(f'TP has no generated evidence: {sid}')
        if not j.get('pdf_evidence'):errors.append(f'TP has no PDF evidence: {sid}')
        m=t.get('predicate_check_map') or {}
        if any(k not in m or m[k].get('status') not in ('met','not_applicable') or not m[k].get('proof_en') for k in PREDICATES):
            errors.append(f'TP predicate evidence map incomplete: {sid}');tp_missing_fieldproof+=1
        for proof in t.get('generated_evidence_checks',[]):
            check_evidence_locator(proof,original,errors,warnings,'TP/'+sid,strict_line=True)
        if grade=='E2' and sid not in BR:errors.append(f'E2 TP lacks semantic bridge row {sid}')
        if sid in BR and BR[sid].get('entailment_grade') not in ('E2','E3'):
            errors.append(f'Bridge has invalid grade {sid}')
        if t.get('complete_semantic_entailment_certified') is True:proof_semantic_certified+=1
        proof_status[t.get('review_disposition')]+=1

    # Corrected TP candidate may have been removed by source atomization.
    for sid,t in TP_A.items():
        final=t.get('final_cell')
        if final=='TP' and sid not in TPids:errors.append(f'Proof asserts TP not in final judgments: {sid}')
        if final in ('REMOVED_OR_MERGED','FN') and sid in TPids:errors.append(f'Final TP removed or downgraded in audit: {sid}')

    fn_cause=collections.Counter()
    for sid in FNids:
        a=FN_A.get(sid)
        if not a:errors.append(f'Missing FN root-cause row {sid}');continue
        if a.get('final_scoring_cell')!='FN' or a.get('fn_review_disposition') not in FINAL_FN_DISPOSITIONS:
            errors.append(f'Invalid final FN root cause {sid}')
        fn_cause[a['fn_review_disposition']]+=1
        if not a.get('exact_and_alias_keys_checked') or not a.get('universal_context_conjunction_checked'):
            errors.append(f'FN lacks reciprocal search details {sid}')
        candidates=a.get('best_generated_candidates') or []
        if not candidates:errors.append(f'FN has no inspected generated candidate: {sid}')
        if not a.get('unmet_predicates_en'):errors.append(f'FN missing specific unmet predicate: {sid}')
        if a.get('pdf_evidence') is None:errors.append(f'FN missing source quote: {sid}')
        for z in candidates[:10]:
            if z.get('file') and z.get('line_start'):
                check_evidence_locator(z,original,errors,warnings,'FN/'+sid)
    for sid,a in FN_A.items():
        c=a.get('final_scoring_cell')
        if c=='FN' and sid not in FNids: errors.append(f'Root-cause audit final FN not in universe {sid}')
        if c=='TP' and sid not in TPids: errors.append(f'Corrected provisional FN not in final TP set {sid}')
        if c=='REMOVED_OR_MERGED' and sid in R: errors.append(f'Removed/merged FN still scored in R {sid}')
    if sum(fn_cause.values())!=len(FNids):errors.append('Final FN category total mismatch')

    # Verify the original and removed source atomization records, not just the current denominator.
    atomization_decisions=collections.Counter(x.get('decision') for x in AT.values())
    removed={sid for sid,a in AT.items() if a.get('decision')=='REMOVED_FROM_POSITIVE_SCORING_UNIVERSE'}
    if (set(AT)-removed)!=set(R):errors.append('Atomization retained IDs do not equal final source atoms')
    if removed & set(R):errors.append('Removed atom appears in scored positives')
    if removed and not changes:errors.append('Source atomization changes absent from change delta')

    # Negative-control assertions with independently enumerated expected result.
    if (d/'04_negative_control_assertion_audit.jsonl').exists():
        audit=one_per(jsonl(d/'04_negative_control_assertion_audit.jsonl'),'negative_control_id','negative assertion audit',errors)
        if set(audit)!=set(N):errors.append('Negative assertion audit not exhaustive')
        for nid,a in audit.items():
            if bool(a.get('asserted_by_generated_definitive_corpus'))!=(nid in Bids):
                errors.append(f'Negative assertion contradicts score {nid}')

    # Generated-class validity: undefined/uncertain semantics cannot be scored as true FP=0 certification.
    generated_validity=collections.Counter(x.get('validity_status') for x in GV.values())
    invalid_labels=set(generated_validity)-{'PDF_ENTAILED','PDF_UNSUPPORTED','SUPPORTED_NONCOVERING'}
    if invalid_labels:errors.append(f'Invalid generated validity label(s): {invalid_labels}')
    referenced_unsupported_ids={x.get('unsupported_canonical_id') for x in GV.values() if x.get('validity_status')=='PDF_UNSUPPORTED' and x.get('unsupported_canonical_id')}
    if not referenced_unsupported_ids <= Fids:errors.append('Generated unsupported class not mapped to F')
    generated_semantic_certified=sum(x.get('semantic_certification')=='VERIFIED' for x in GV.values())
    reverse_quote_unreconciled=0
    if (d/'05_generated_reverse_evidence_audit_final.jsonl').exists():
        reverse=list(jsonl(d/'05_generated_reverse_evidence_audit_final.jsonl'))
        if {x.get('class_id') for x in reverse}!=set(GC):errors.append('Generated PDF reverse audit does not cover every raw class')
        reverse_quote_unreconciled=sum(not x.get('verified_original_locator') for x in reverse)
    else: warnings.append('Generated reverse evidence audit missing')
    generated_pdf_quote_not_literal=[]
    for cid,v in GV.items():
        matches=False
        for src_ev in v.get('pdf_support_evidence') or []:
            pg=src_ev.get('physical_page')
            if isinstance(pg,int) and 1 <= pg <= len(pdf_page_text):
                quote=norm(src_ev.get('quote_en'));page_text=norm(pdf_page_text[pg-1])
                if quote and (quote in page_text or (len(quote)>35 and quote[:35] in page_text)):
                    matches=True;break
        if not matches:
            generated_pdf_quote_not_literal.append({'class_id':cid,
                'pdf_candidate_evidence':(v.get('pdf_support_evidence') or [])[:2],
                'reason_en':'Candidate source quote not literally recovered in its stated PDF page text extraction; figure/image text and layout differences require visual verification. This does not establish substantive semantic support.'})

    # Independently derive raw duplication and within/across partition from original occurrences.
    within=across=repeated=multifile=0
    for cid,c in GC.items():
        occurrences=sorted((GO[oid] for oid in c['occurrence_ids'] if oid in GO),
           key=lambda o:(file_order.get(o['file'],10**6),o['line_start'],
                         (o.get('table_cell') or {}).get('column_index',0),o['occurrence_id']))
        seen_files=set(); one_w=one_a=0
        for i,o in enumerate(occurrences):
            if i>0:
                if o['file'] in seen_files:within+=1;one_w+=1
                else:across+=1;one_a+=1
            seen_files.add(o['file'])
        repeated+=len(occurrences)>1;multifile+=len(seen_files)>1
        if len(occurrences)>1:
            dc=DUP.get(cid)
            if not dc:errors.append(f'Duplicate class ledger missing {cid}')
            elif dc.get('within_file_excess')!=one_w or dc.get('across_file_excess')!=one_a:
                errors.append(f'Duplicate partition disagrees with originals {cid}')
    GO_count=len(GO);G_count=len(GC);excess=GO_count-G_count
    if within+across!=excess:errors.append('Raw duplicate partition does not reconcile')
    if (stated_duplicate.get('eligible_generated_occurrences')!=GO_count or
        stated_duplicate.get('raw_unique_generated_claim_classes')!=G_count or
        stated_duplicate.get('within_file_excess')!=within or
        stated_duplicate.get('across_file_excess')!=across):
        errors.append('Phase 5 duplication summary does not match independent enumeration')

    TP=len(TPids); FN=len(R)-TP; TN=len(N)-len(Bids); FP=len(Bids)+len(Fids)
    if FN!=len(FNids) or TN!=len(TNids) or FP!=cells['FP'] or TP!=cells['TP']:
        errors.append('Four-cell set equations do not reconcile with judgments')
    if sum(cells.values())!=len(U) or len(U)!=len(R)+len(N)+len(Fids):
        errors.append('Canonical universe total incorrect')
    pcount=TP+FP
    if pcount!=sum(j['predicted_label']==1 for j in J.values()):
        errors.append('Effective predicted-positive count discrepancy')
    precision=sane_fraction(TP,TP+FP)
    recall=sane_fraction(TP,TP+FN)
    f1=sane_fraction(2*TP,2*TP+FP+FN)
    duplicate=sane_fraction(excess,GO_count)

    # PDF evidence integrity: page present and extractable; exact quote recovery is only a locator heuristic.
    original_pdf_quotes=0; literal_pdf_quotes=0
    for s in R.values():
        ev=s.get('pdf_evidence') or []
        if not ev:errors.append(f'PDF source atom without evidence: {s["source_id"]}')
        for entry in ev:
            page=entry.get('physical_page'); file=entry.get('file')
            if file!=pdf_filename or not isinstance(page,int) or not (1<=page<=(pdf_page_count or 0)):
                errors.append(f'Invalid source atom PDF locator: {s["source_id"]}')
            original_pdf_quotes+=1
            if isinstance(page,int) and 1<=page<=len(pdf_page_text):
                quote=norm(entry.get('quote_en'))
                pt=norm(pdf_page_text[page-1])
                if quote and (quote in pt or (len(quote)>30 and quote[:30] in pt)):
                    literal_pdf_quotes+=1
    # Physical line source-text sweep / exact-match regression probes.
    probe_specs={
      'case_title_field': [r'\bcase includes title\b',r'\btitle\b'],
      'workspace_retention_class': [r'workspace settings includes retention class',r'retention class'],
      'idempotent_same_key_case_creation': [r'create case twice with same key',r'identical response'],
      'event_envelope_schema_version': [r'canonical event envelope includes schema_version',r'\bschema_version\b'],
      'approval_exact_artifact_hash': [r'approval applies only to the exact content hash',r'reviewed artifact hash']
    }
    probe_rows=[];probe_exceptions=[]
    for pname,patterns in probe_specs.items():
        matches=[s for s in R.values() if re.search(patterns[0],s.get('atomic_statement_en',''),re.I)]
        if not matches:
            matches=[s for s in R.values() if re.search(patterns[-1],s.get('atomic_statement_en',''),re.I)][:6]
        exact_generated=[]
        for fname,lines in original.items():
            for i,line in enumerate(lines,1):
                if re.search(patterns[-1],line,re.I):
                    exact_generated.append({'file':fname,'line_start':i,'snippet':line[:220]})
        for s in matches:
            sid=s['source_id'];j=J[sid]
            row={'probe':pname,'source_id':sid,'source_statement_en':s['atomic_statement_en'],
                 'final_scoring_cell':j['scoring_cell'],'exact_generated_line_count':len(exact_generated),
                 'generated_line_examples':exact_generated[:5],
                 'diagnostic_only':True,'semantic_certification':'NOT_AUTOMATICALLY_PROVED'}
            probe_rows.append(row)
            if j['scoring_cell']=='FN' and len(exact_generated)>0:
                probe_exceptions.append({'source_id':sid,'probe':pname,'reason_en':
                    'A generated text hit exists for an FN; manual full-predicate re-adjudication is required before asserting verified absence.'})
    # Broad direct exact-path/status exceptions for source FNs (not auto corrections).
    for sid in FNids:
        atom=R[sid]
        st=atom.get('atomic_statement_en','')
        literals=re.findall(r'(?:GET|POST|PATCH|PUT|DELETE)\s+(/(?:v1|internal)/[\w/{}/?-]+)',st)
        for lit in literals:
            hits=[(fname,i) for fname,lines in original.items() for i,line in enumerate(lines,1) if lit in line]
            if hits:probe_exceptions.append({'source_id':sid,'target':lit,'matching_line_count':len(hits),
               'examples':[{'file':fn,'line_start':i} for fn,i in hits[:5]],
               'reason_en':'Exact method/path appears in the generated corpus while the full source predicate is judged FN; compare omitted predicates before final semantic certification.'})

    # English authored reports: a syntax/Unicode screen cannot prove English language semantically.
    authored_report_names=['04_confusion_matrix_final.md','05_duplicate_metrics_final.md',
                           '05_evidence_and_corrections_report.md',
                           '06_metrics_final.md','08_coverage_and_limitations.md']
    for n in authored_report_names:
        if not (d/n).is_file():errors.append('Missing authored report: '+n)
        else:
            txt=(d/n).read_text(encoding='utf-8')
            if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',txt):errors.append(f'Non-English CJK text in authored report {n}')

    final_individual_artifacts=[
      '06_metrics_final.json','06_metrics_final.md','06_independent_checks.json',
      '06_regression_probes_final.jsonl','06_fn_full_corpus_search_final.jsonl',
      '06_quote_recovery_exceptions_final.jsonl','08_coverage_and_limitations.md',
      '09_excluded_units.jsonl','06_phase_status.json','06_final_file_inventory.json',
      '04_confusion_matrix_final.json','04_confusion_matrix_final.md',
      '05_duplicate_metrics_final.json','05_duplicate_metrics_final.md',
      'compute_metrics.py'
    ]
    for name in final_individual_artifacts:
        if not (d/name).is_file():errors.append('Missing required final output: '+name)
    if list(d.glob('*.zip')) or list(d.glob('*.tar')) or list(d.glob('*.tar.gz')):
        errors.append('Forbidden archive artifact found in final output directory')
    strict_check_count={
        'source_positive_atom_ids_unique':len(R),
        'fixed_negative_control_ids_unique':len(N),
        'generated_occurrence_ids_unique':len(GO),
        'generated_class_ids_unique':len(GC),
        'canonical_unique_units':len(J),
        'input_files':len(original),
        'actual_markdown_lines_inspected_by_coverage_ledger':inspected_lines,
        'actual_markdown_table_cells_inspected_by_coverage_ledger':inspected_cells,
        'pdf_pages':pdf_page_count,
        'retained_tp_with_audit_record':len(TPids & {sid for sid,r in TP_A.items() if r.get('final_cell')=='TP'}),
        'retained_fn_with_root_cause_record':len(FNids & {sid for sid,r in FN_A.items() if r.get('final_scoring_cell')=='FN'}),
        'tp_with_independently_certified_complete_entailment':proof_semantic_certified,
        'generated_claims_with_independently_certified_semantics':generated_semantic_certified,
        'source_atom_pdf_quote_locator_total':original_pdf_quotes,
        'source_atom_pdf_quote_literal_text_recovered':literal_pdf_quotes,
        'generated_reverse_pdf_locator_boolean_not_verified':reverse_quote_unreconciled,
        'generated_pdf_support_quote_not_literal_recovered':len(generated_pdf_quote_not_literal),
        'diagnostic_probe_exception_count':len(probe_exceptions),
    }
    metrics={
      'protocol_version':'6.1','phase':6,'method':method,
      'status':'FINAL_BEST_EFFORT' if not errors else 'STRUCTURAL_VALIDATION_FAILED',
      'semantic_certification':'NOT_VERIFIED',
      'universe':{
        'source_positive_atoms':len(R),'source_negative_controls':len(N),
        'raw_generated_claim_classes':G_count,'generated_positive_occurrences':GO_count,
        'covered_source_atoms':TP,'asserted_negative_controls':len(Bids),
        'unsupported_generated_only_propositions':len(Fids),
        'canonical_predicted_positive_units':pcount,'canonical_decision_units':len(U),
        'negative_universe_scope':'Predeclared PDF-grounded bounded controls; does not represent all possible absent requirements.'},
      'confusion':{'TP':TP,'TN':TN,'FP':FP,'FN':FN},
      'metrics':{'Precision':precision,'Recall':recall,'F1':f1,'Duplicate':duplicate},
      'duplication':{'eligible_generated_occurrences':GO_count,'unique_generated_claim_classes':G_count,
        'duplicate_excess_occurrences':excess,'repeated_claim_class_count':repeated,
        'repeated_classes_spanning_multiple_files':multifile,'within_file_excess':within,
        'across_file_excess':across},
      'final_FN_root_causes':dict(sorted(fn_cause.items())),
      'source_atomization':{'retained':len(R),'removed_from_original_inventory':len(removed),
        'removed_ids':sorted(removed),'review_records':len(AT)},
      'generated_class_validity':dict(sorted(generated_validity.items())),
      'evidence_reliability':strict_check_count,
      'interpretation':('Arithmetic is independently recomputed from one canonical effective-proposition '
        'universe, not the raw generated-class universe. Unverified generated-class PDF support '
        'makes the apparent zero FP and 100% precision provisional only. TP proof records are '
        'structurally present but not independently semantically certified. TN is bounded; '
        'duplicate rate is raw occurrence/class based. Calculated recall is not certified true coverage.'),
    }
    # The script fails on hard structural anomalies, but records semantic exceptions.
    checks={
      'strict_errors':errors[:1000], 'strict_error_count':len(errors),
      'warnings':warnings[:200], 'warning_count':len(warnings),
      'all_structural_checks_passed':not errors,
      'proof_coverage_status':'ITEM_LEVEL_RECORDED_BUT_NOT_SEMANTICALLY_CERTIFIED',
      'remaining_high_risk_exact_or_conceptual_match_probes':probe_exceptions,
      'tp_E2_records':tp_E2,'tp_E3_records':tp_E3,'tp_coverage_modes':dict(bridge_modes),
      'tp_semantically_certified_count':proof_semantic_certified,
      'generated_classes_semantically_certified_count':generated_semantic_certified,
      'generated_validity_distribution':dict(generated_validity),
      'source_quote_literal_recovery_warning':(
          'Layout-extraction literal matching is a locator diagnostic, not an exhaustive PDF quotation proof.'),
      'source_file_sha256':hashlib.sha256(pdfs[0].read_bytes()).hexdigest() if pdf_filename else None,
      'scored_input_sha256':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in original},
    }
    if not args.no_write:
        with (d/'06_quote_recovery_exceptions_final.jsonl').open('w',encoding='utf-8') as f:
            for x in generated_pdf_quote_not_literal:f.write(json.dumps(x,ensure_ascii=False)+'\n')
        (d/'06_metrics_final.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (d/'06_independent_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        with (d/'06_regression_probes_final.jsonl').open('w',encoding='utf-8') as f:
            for x in probe_rows: f.write(json.dumps(x,ensure_ascii=False)+'\n')
    print(json.dumps({'result':metrics['status'],'confusion':metrics['confusion'],
          'metrics':metrics['metrics'],'duplicate':metrics['duplication'],
          'strict_errors':len(errors),'warnings':len(warnings),
          'probe_exceptions':len(probe_exceptions),'source_pdf_pages':pdf_page_count,
          'generated_classes_without_certified_semantics':len(GC)-generated_semantic_certified},indent=2))
    if errors:
        print('STRUCTURAL ERRORS:',*errors[:35],sep='\n- ',file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':sys.exit(main())
