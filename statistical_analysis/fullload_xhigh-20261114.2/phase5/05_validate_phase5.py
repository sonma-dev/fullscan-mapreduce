import json, collections, os, re
from pathlib import Path
P=Path('/mnt/data/orion_phase5')
def load(fn):
 return [json.loads(l) for l in (P/fn).open(encoding='utf8') if l.strip()]
R=load('01_source_atoms_final.jsonl');N=load('01_source_negative_controls_final.jsonl');GO=load('02_generated_atoms_final.jsonl');G=load('02_generated_classes_final.jsonl')
J=load('04_atomic_judgments_final.jsonl');C=load('03_canonical_universe_final.jsonl');D=load('04_duplicate_classes_final.jsonl');V=load('04_generated_claim_validity_final.jsonl')
TA=load('05_tp_evidence_audit_final.jsonl');FA=load('03_fn_root_cause_audit_final.jsonl');S=load('05_source_atomization_audit_final.jsonl');DELTA=load('07_change_delta.jsonl')
cm=json.load(open(P/'04_confusion_matrix_final.json'));q=collections.Counter(j['scoring_cell'] for j in J)
checks={
'R_UNIQUE':len(set(x['source_id'] for x in R))==len(R),
'N_UNIQUE':len(set(x['negative_control_id'] for x in N))==len(N),
'G_UNIQUE':len(set(x['class_id'] for x in G))==len(G),
'GO_UNIQUE':len(set(x['occurrence_id'] for x in GO))==len(GO),
'V_ONE_PER_G':set(x['class_id'] for x in V)==set(x['class_id'] for x in G),
'GO_ONE_CLASS_EACH':set(x['semantic_class_id'] for x in GO).issubset(set(x['class_id'] for x in G)),
'G_MEMBERS_MATCH_GO':sum(len(x['occurrence_ids']) for x in G)==len(GO) and sorted(sum((x['occurrence_ids'] for x in G),[]))==sorted(x['occurrence_id'] for x in GO),
'J_UNIQUE':len({x['canonical_id'] for x in J})==len(J),
'C_EQUALS_J':len(C)==len(J) and [x['canonical_id'] for x in C]==[x['canonical_id'] for x in J],
'CANONICAL_TOTAL':len(J)==len(R)+len(N)+sum(1 for x in J if x['unit_kind']=='GENERATED_ONLY_UNSUPPORTED'),
'CONFUSION_EQUATIONS':q['TP']+q['FN']==len(R) and q['TN']==len(N) and q['TP']+q['FN']+q['FP']+q['TN']==len(J),
'TP_AUDIT':len(TA)==q['TP'] and {x['source_id'] for x in TA}=={x['origin_source_ids'][0] for x in J if x['scoring_cell']=='TP'},
'FN_AUDIT':len([x for x in FA if x['final_scoring_cell']=='FN'])==q['FN'],
'SOURCE_ATOMIZATION':{x['source_id'] for x in S}=={x['source_id'] for x in R},
'DUP_ROWS':len(D)==len(G),
'DUP_PARTITION':sum(x['occurrence_count']-1 for x in D)==len(GO)-len(G),
}
# Excerpt validation for every eligible occurrence and 647 TP evidences against original supplied markdown.
mdfiles={p.name:p.read_text(encoding='utf8').splitlines() for p in Path('/mnt/data').glob('*.md') if re.match('0[1-8]_',p.name)}
assert len(mdfiles)==8
n=lambda s:re.sub(r'\s+',' ',re.sub(r'[^a-z0-9]+',' ',str(s).lower())).strip()
occerrors=[]
for x in GO:
 loc=x['evidence_locator']; line=mdfiles[x['file']][loc['line_start']-1]
 if n(x['generated_quote_en']) not in n(line):occerrors.append(x['occurrence_id'])
checks['ALL_ORIGINAL_GENERATED_QUOTATIONS']=len(occerrors)==0
errtp=[]
for x in TA:
 for loc in x['generated_evidence']:
  if n(loc['quote_en']) not in n(mdfiles[loc['file']][loc['line_start']-1]):errtp.append((x['source_id'],loc['line_start']))
checks['ALL_TP_QUOTATIONS_ORIGINAL']=len(errtp)==0
checks['ALL_FN_HAVE_CANDIDATE_QUOTATIONS']=all(x.get('best_generated_candidates') for x in FA if x['final_scoring_cell']=='FN')
checks['DELTA_INCLUDES_CORRECTIONS']=len([x for x in DELTA if x['change_type']=='FN_TO_TP_RECOVERED'])==60
results={'status':'PHASE_COMPLETED_BEST_EFFORT' if all(checks.values()) else 'FAILED_STRUCTURAL_CHECK',
        'semantic_certification':False,'checks':checks,'source_file_count':len(mdfiles),
        'quote_error_count':len(occerrors)+len(errtp),'confusion':dict(q)}
with (P/'05_independent_structural_validation_final.json').open('w') as f:json.dump(results,f,indent=2);f.write('\n')
assert all(checks.values()),[k for k,v in checks.items() if not v]
print(json.dumps(results,ensure_ascii=False))
