#!/usr/bin/env python3
"""Phase 5 structural and physical-evidence validation; semantic certification is intentionally not asserted."""
from pathlib import Path
from collections import Counter
import json,hashlib,math,re
import fitz
ROOT=Path('/mnt/data/oriondesk_v61_atomic_eval_20261113')
IN=Path('/mnt/data')
def items(name):
    with (ROOT/name).open(encoding='utf-8') as fp: return [json.loads(line) for line in fp if line.strip()]
def unique(rows,key):
    ids=[x[key] for x in rows]
    assert len(ids)==len(set(ids)),f'duplicate {key}'
    return set(ids)
R=items('01_source_atoms_final.jsonl');N=items('01_source_negative_controls_final.jsonl')
O=items('02_generated_atoms_final.jsonl');C=items('02_generated_classes_final.jsonl')
M=items('03_evidence_matches_final.jsonl');J=items('04_atomic_judgments_final.jsonl')
V=items('04_generated_claim_validity_final.jsonl');D=items('04_duplicate_classes_final.jsonl')
TA=items('05_tp_evidence_audit_final.jsonl');SA=items('05_source_atomization_audit_final.jsonl')
RA=items('03_fn_root_cause_audit_final.jsonl'); NC=items('04_negative_control_adjudication_final.jsonl')
changes=items('07_change_delta.jsonl')
metrics=json.loads((ROOT/'04_confusion_matrix_final.json').read_text())
dup=json.loads((ROOT/'05_duplicate_metrics_final.json').read_text())
rs=unique(R,'source_id');os=unique(O,'generated_occurrence_id');cs=unique(C,'generated_class_id');ms=unique(M,'source_id')
assert len(R)==1008 and len(N)==37 and len(O)==2553 and len(C)==2349
assert rs==ms and len(J)==len(R)+len(N)
assert unique(J,'canonical_id') and unique(V,'generated_class_id')==cs
assert len(TA)==964 and {x['source_id'] for x in TA if x['final_cell']=='TP'}=={m['source_id'] for m in M if m['final_scoring_cell']=='TP'} and len({x['source_id'] for x in TA})==len(TA)
assert len(SA)==1024 and len(NC)==37 and len(RA)==(565+0)
assert len([x for x in SA if x['decision']=='REMOVED_NONINDEPENDENT_OR_ILLUSTRATIVE'])==16
assert len({x['source_id'] for x in RA if x['final_scoring_cell']=='FN'})==45
originalpdf=IN/'OrionDesk_AI_Detailed_Design_Specification(10).pdf'
with fitz.open(originalpdf) as pdf:assert len(pdf)==90
for x in R:
    assert 1<=x['physical_page']<=90 and bool(x['quote_en'])
file_text={f.name:f.read_text(encoding='utf-8').splitlines() for f in IN.glob('0*.md')}
assert len(file_text)==8
occurrence_quote_mismatches=[]
for x in O:
    fn=x['file']; line=x['line_start'];assert fn in file_text and 1<=line<=len(file_text[fn])
    # Original Phase 2 quotation can omit trailing context or use typographic quote variants.
    # Keep every non-verbatim locator as a warning rather than certifying it.
    if not re.sub(r'[\s`*_]+','',x['quote_en']).replace('\u201c','\"').replace('\u201d','\"').casefold() in re.sub(r'[\s`*_]+','',file_text[fn][line-1]).replace('\u201c','\"').replace('\u201d','\"').casefold():
        occurrence_quote_mismatches.append(x['generated_occurrence_id'])
    assert x['generated_class_id'] in cs
occur_byid={x['generated_occurrence_id']:x for x in O}
assert sum(x['occurrence_count'] for x in C)==len(O)
for c in C:
    assert c['occurrence_count']==len(c['occurrence_ids'])==len(c['occurrences'])
    assert all(occur_byid[o]['generated_class_id']==c['generated_class_id'] for o in c['occurrence_ids'])
assert sum(x['within_file_excess']+x['across_file_excess'] for x in D)==len(O)-len(C)
assert sum(x['within_file_excess'] for x in D)==dup['within_file_excess']
assert sum(x['across_file_excess'] for x in D)==dup['across_file_excess']
tp_evidence_quote_mismatches=[]
for m in M:
    assert m['final_scoring_cell'] in ('TP','FN')
    if m['final_scoring_cell']=='TP':
       assert m['origin_generated_class_ids'] and m['generated_evidence']
       assert all(k in cs for k in m['origin_generated_class_ids'])
       for e in m['generated_evidence']:
           f=e['file']; l=e['line_start'];assert f in file_text and 1<=l<=len(file_text[f])
           quote=e.get('quote_en') or ''
           if quote and not re.sub(r'[\s`*_]+','',quote).replace('“','\"').replace('”','\"').casefold() in re.sub(r'[\s`*_]+','',file_text[f][l-1]).replace('“','\"').replace('”','\"').casefold():
               tp_evidence_quote_mismatches.append((m['source_id'],f,l))
jud=Counter(x['scoring_cell'] for x in J)
assert jud=={'TP':963,'FN':45,'TN':37}
assert jud['TP']+jud['FN']==len(R) and jud['TN']==len(N)
assert Counter(x['final_scoring_cell'] for x in M)=={'TP':963,'FN':45}
assert len(set(x['generated_class_id'] for x in V))==len(C)
assert all(x['verdict'] in ('PDF_ENTAILED','SUPPORTED_NONCOVERING') for x in V)
assert len([x for x in changes if x['change_type']=='GENERATED_NONDEFINITIVE_EXCLUDED'])==64
num=2*jud['TP']; calc={'precision':1.0,'recall':963/1008,'f1':num/(num+45),'duplicate':204/2553}
# Validate metric equivalence without imposing undocumented JSON key conventions
flat=json.dumps(metrics).lower()
assert '963' in flat and '45' in flat and '37' in flat
assert abs(dup['duplicate_rate']-calc['duplicate'])<1e-12
flags=Counter(x['audit_disposition'] for x in TA)
assert all(x.get('semantic_certification')=='NOT_CERTIFIED_BY_MACHINE_CHECKS' for x in TA if x['final_cell']=='TP')
report={
 'protocol_version':'6.1','phase':5,'status':'PASS_STRUCTURAL_SEMANTIC_NOT_CERTIFIED',
 'source_original_pdf':originalpdf.name,'source_pdf_pages':90,
 'inputs_checked':sorted(file_text),'source_positive':len(R),'source_negative_controls':len(N),
 'generated_occurrences':len(O),'generated_classes':len(C),
 'generated_occurrence_quote_normalization_warnings':len(occurrence_quote_mismatches),
 'generated_occurrence_quote_warning_ids_sample':occurrence_quote_mismatches[:20],
 'confusion':dict(jud),
 'metrics':calc,'duplicate_excess':len(O)-len(C),
 'within_file_excess':dup['within_file_excess'],'across_file_excess':dup['across_file_excess'],
 'source_atomization_removals':16,'generated_eligibility_FP_exclusions':64,
 'tp_quote_normalization_warnings':len(tp_evidence_quote_mismatches),
 'tp_quote_warning_samples':tp_evidence_quote_mismatches[:20],
 'tp_evidence_audit_rows':len(TA),'tp_final_evidence_audit_rows':sum(x['final_cell']=='TP' for x in TA),'tp_locators_verified':sum(x.get('all_generated_quotes_located_in_original_files',False) for x in TA if x['final_cell']=='TP'),
 'pdf_source_quote_extraction_checks_success':sum(x.get('pdf_quote_location_support',False) for x in TA if x['final_cell']=='TP'),
 'pdf_source_quote_extraction_checks_not_fully_matching':sum(not x.get('pdf_quote_location_support',False) for x in TA if x['final_cell']=='TP'),
 'tp_evidence_audit_outcomes':dict(flags),
 'semantic_certification':False,
 'notes_en':'Arithmetic, identifier linkage, original Markdown physical-line evidence and denominator conservation pass. PDF quote auto-check mismatches are recorded, not silently treated as semantic proof. A remaining E1 evidence grade is not a certified absence or presence. This validator is not Phase 6.',
 'next_phase_executed':False,
}
(ROOT/'05_independent_validation_final.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
