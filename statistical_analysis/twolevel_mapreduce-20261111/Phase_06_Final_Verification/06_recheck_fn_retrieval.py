#!/usr/bin/env python3
"""Perform source-specific full-corpus reciprocal search for all final FN cases."""
import json,re,unicodedata,collections
from pathlib import Path
p=Path(__file__).resolve().parent
attached=p.parent

def read(n):return [json.loads(x) for x in (p/n).read_text(encoding='utf-8').splitlines() if x.strip()]
def write(n,records):
 with (p/n).open('w',encoding='utf-8') as f:
  for x in records:f.write(json.dumps(x,ensure_ascii=False)+'\n')
def norm(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s or '')).strip().lower()
manifest=json.loads((p/'01_input_manifest_final.json').read_text())
source={x['source_id']:x for x in read('01_source_atoms_final.jsonl')}
ledger=read('03_fn_root_cause_audit_final.jsonl')
textlines=[]
for x in manifest['scored_inputs']:
 name=x['actual_filename']
 for lineno,line in enumerate((attached/name).read_text(encoding='utf-8').splitlines(),1):
  if line.strip():textlines.append((name,lineno,line.strip(),norm(line)))
stop=set('the and for all each with from into that this those where which such should shall are must cannot other than shall when then same only also without before after case source application system data design base expected id response current every component actor scope runtime provides including required requires document record within used uses using about valid relevant default according register boundary interface operations operation behavior controls applies specific certain original supported include out model implementation source target policy event request request errors framework test tests requirement'.split())
rechecked=[]
for item in ledger:
 if item['final_scoring_cell']!='FN':continue
 src=source[item['source_id']]
 statement=src['atomic_statement_en']; quote=src.get('quote_en') or statement
 tokens=[x for x in re.findall(r'[A-Za-z][A-Za-z0-9_-]{3,}',statement) if x.lower() not in stop]
 # Choose distinctive exact identifiers and technical terms; do not derive any score from matches.
 paths=re.findall(r'/((?:v1|internal)/[A-Za-z0-9{}?_.\-/]+)',statement+' '+quote)
 exact_paths=['/'+s.rstrip('.,;') for s in paths]
 literals=re.findall(r'\b(?:[A-Z][A-Z0-9_]{4,}|(?:[A-Za-z]+(?:Id|Key|Created|Recorded|Committed)))\b',statement)
 identifiers=list(dict.fromkeys(exact_paths + literals))
 values=collections.Counter(t.lower() for t in tokens)
 ranked=sorted(values, key=lambda k:(-len(k),-values[k],k))
 keys=list(dict.fromkeys(identifiers + ranked[:7]))[:12]
 if not keys:keys=[w for w in re.findall(r'[\w-]+',statement) if len(w)>3][:8]
 hits=[]; counts={k:0 for k in keys}
 for fname,lineno,line,fold in textlines:
  matched=[k for k in keys if k.lower() in fold]
  if not matched:continue
  for k in matched:counts[k]+=1
  scored=sum(min(4,len(k)/4) for k in matched)
  hits.append((scored,len(matched),fname,lineno,line,matched))
 hits.sort(key=lambda x:(-x[0],-x[1],x[2],x[3]))
 examples=[{'file':h[2],'line_start':h[3],'line_end':h[3],'quote_en':h[4][:500],'matched_exact_or_alias_keys':h[5]} for h in hits[:10]]
 full_statement_hits=[h for h in hits if len(norm(statement))>=35 and norm(statement) in h[4].lower()]
 add={
  'source_id':item['source_id'],
  'searched_exact_identifiers_and_alias_terms_en':keys,
  'per_key_corpus_line_hit_counts':counts,
  'all_eight_files_line_searched':True,
  'actual_generated_line_examples':examples,
  'full_statement_contiguous_line_hits':len(full_statement_hits),
  'preserved_final_disposition':item['fn_review_disposition'],
  'source_statement_en':statement,
  'limitation_en':'Full-corpus lexical reverse retrieval and inherited-context candidates were inspected to document explicit source terms. A search hit does not prove every condition; no score is silently changed.'
 }
 rechecked.append(add)
 item['exact_and_alias_keys_checked']=keys
 item['phase6_reciprocal_source_line_audit']={'audit_file':'06_fn_reciprocal_recheck_final.jsonl','actual_line_examples':examples[:3],'full_statement_contiguous_line_hits':len(full_statement_hits)}
write('06_fn_reciprocal_recheck_final.jsonl',rechecked)
write('03_fn_root_cause_audit_final.jsonl',ledger)
print('Independent final FN reciprocal audits:',len(rechecked))
print('Final FN with full-line statement matches:',[(r['source_id'],r['full_statement_contiguous_line_hits']) for r in rechecked if r['full_statement_contiguous_line_hits']])
print('Final FN with zero generated key-hit lines:',[r['source_id'] for r in rechecked if not r['actual_generated_line_examples']])
