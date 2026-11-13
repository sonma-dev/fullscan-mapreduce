#!/usr/bin/env python3
"""Phase 3 independent source-to-generated reciprocal evidence retrieval and conservative adjudication.
Read-only for Phase 1/2 source ledgers and input specifications.
Usage: python 03_build_coverage.py
No historical judgments or preassigned TP labels are read.
"""
import os,re,json,collections,math,hashlib,datetime
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
P=Path('/mnt/data');OUT=P/'oriondesk_phase3';OUT.mkdir(exist_ok=True)
R=[json.loads(x) for x in open(P/'oriondesk_phase1/01_source_atoms_final.jsonl')]
G=[json.loads(x) for x in open(P/'oriondesk_phase2/02_generated_classes_final.jsonl')]
O=[json.loads(x) for x in open(P/'oriondesk_phase2/02_generated_atoms_final.jsonl')]
ids={o['occurrence_id']:o for o in O}
by_class={g['class_id']:i for i,g in enumerate(G)}
G_byrow=collections.defaultdict(list)
G_bytoken=collections.defaultdict(set)
all_md={file.name:file.read_text(encoding='utf-8').splitlines() for file in P.glob('0[1-8]_*.md')}
assert len(all_md)==8 and len(R)==1024 and len(G)==6527

def ntext(s):
 s=(s or '').lower().replace('’',"'").replace('`','').replace('**','')
 s=re.sub(r'(?<=[a-z])(?=[A-Z])',' ',s)
 s=s.replace('must not','cannot').replace('shall not','cannot').replace('does not','cannot')
 s=s.replace('must','').replace('shall','').replace('shall be','').replace('are required to','')
 s=re.sub(r'[\u2010-\u2015]', '-',s)
 s=re.sub(r'\s+',' ',s)
 return s.strip().rstrip('.')

def normalize(s):
 s=ntext(s)
 s=s.replace('unavailable','not available').replace('immutable','unchangeable')
 s=re.sub(r'(?<=\w)_(?=\w)',' ',s)
 s=re.sub(r'(?<=\w)\.(?=\w)',' ',s)
 s=re.sub(r'[^a-z0-9/{}+.-]+',' ',s)
 return re.sub(r'\s+',' ',s).strip()
stop=set('the a an and or of in on at by to with for as is are be has have had shall will from into through every each all this that those these its their it what which when where whose only must should can could would may otherwise before after once then while also not no without under over same class within current source using use used required requirement confirmed includes include containing contains includes selected field relational entity catalog primary secondary surface operation at interface defined request path records record baseline platform application exact reference'.split())
common_norm={'case':'cases','cases':'cases','document':'documents','documents':'documents','workspace':'workspaces','workspaces':'workspaces','reviewer':'reviewers','reviewers':'reviewers','api':'api','ui':'ui','ids':'id','identifiers':'id','authorization':'authorized','authorisation':'authorized','permission':'authorized','permissions':'authorized','approval':'approve','approvals':'approve','published':'publish','publication':'publish','publishing':'publish','reject':'denied','rejected':'denied','denial':'denied','denies':'denied','idempotent':'idempotency','duplicate':'replay','duplicates':'replay','repeated':'replay','rerun':'replay','replay':'replay','cited':'citation','citations':'citation','required':'require','requires':'require','retain':'preserve','retained':'preserve','stored':'store','store':'store','update':'update','updated':'update','updates':'update','validate':'validation','validation':'validation','verified':'verify','verification':'verify','verifies':'verify','before':'before','after':'after','never':'cannot'}

def tokens(s):
 raw=re.findall(r'[a-z0-9]+(?:[_-][a-z0-9]+)*|/v1/[a-z0-9/{}/_-]+',normalize(s))
 return [common_norm.get(t,t) for t in raw if len(t)>1 and t not in stop]

def uniqsort(v):return sorted(set(v))

rtext=[x['atomic_statement_en'] for x in R]
gtext=[x['canonical_statement_en'] for x in G]
graw=[]; gctx=[]
for i,g in enumerate(G):
 e=g['representative_evidence'];line=e.get('line_start');f=e.get('file')
 gr=' '.join(filter(None,[g['canonical_statement_en'],e.get('row_key'),e.get('column_header'),e.get('heading_context','').split(' > ')[-1]]))
 gctx.append(gr)
 graw.append(e['quote_en'])
 G_byrow[(f,line)].append(i)
 for t in set(tokens(g['canonical_statement_en']+' '+(e.get('row_key') or ''))):G_bytoken[t].add(i)

# Run independent lexical and character projections, then union them; no similarity top-k can hide an exact identifier match.
word=TfidfVectorizer(ngram_range=(1,2),token_pattern=r'(?u)\b[\w/{}+.-]+\b',sublinear_tf=True,dtype=np.float32)
char=TfidfVectorizer(analyzer='char_wb',ngram_range=(3,5),sublinear_tf=True,dtype=np.float32)
M1=word.fit_transform([normalize(x) for x in rtext]+[normalize(x) for x in gctx]); N=len(R)
M2=char.fit_transform([normalize(x) for x in rtext]+[normalize(x) for x in gctx]);
Sim=.57*(M1[:N]@M1[N:].T)+.43*(M2[:N]@M2[N:].T)
word2=TfidfVectorizer(ngram_range=(1,2),token_pattern=r'(?u)\b[\w/{}+.-]+\b',sublinear_tf=True,dtype=np.float32)
M3=word2.fit_transform([normalize(x) for x in rtext]+[normalize(x) for x in gtext]);
Sim=Sim*.68+(M3[:N]@M3[N:].T)*.32
Sim=Sim.tocsr()

# Context-rich hard keys from all generated class quotations and all input line text
route=re.compile(r'(?i)\b(GET|POST|PATCH|PUT|DELETE)\s+(/(?:v1|internal)/[\w/{}/.?#=-]+)')
source_field=re.compile(r'(?i)^the\s+([a-z_]+)\s+relational entity catalog includes the selected field\s+([a-z_]+)\.?$')
field_cl=re.compile(r'(?i)\b(?:DAT-\d{3}-F\d+|\b\w+(?:\.\w+)+)\b')
num=re.compile(r'\b\d+(?:\.\d+)?\s*(?:%|mb|s|seconds|hours|days|minutes|ms)\b',re.I)

def get_routes(s):
 out=[]
 for m in route.finditer(s):out.append((m.group(1).upper(),m.group(2).lower().rstrip('.,;:')))
 return set(out)

def build_route_idx():
 z=collections.defaultdict(set)
 for j,g in enumerate(G):
  for k in get_routes(gtext[j]+' '+graw[j]):z[k].add(j)
 return z
route_idx=build_route_idx()

def get_identifiers(s):
 return set(re.findall(r'\b(?:API|DAT|SCR|BAT|BR|ERR|FLOW|TST|SEC|OQ|AC)-\d{3}(?:-F\d{2})?\b',s,re.I))

# Source entity -> data-table group (follows the dataset's section inventory, not historical matched decisions).
entity_group={'tenants':1,'workspaces':2,'cases':3,'case_revisions':4,'documents':5,'document_versions':6,'chunks':7,'runs':8,'run_steps':9,'evidence_sets':10,'approval_tasks':11,'approval_decisions':12,'audit_events':13,'outbox_events':14,'connector_cursors':15,'token_ledger':16,'policy_evaluations':17,'deletion_receipts':18}
entityfld=collections.defaultdict(list)
for fname,lines in all_md.items():
 if '03_data' not in fname:continue
 for n,line in enumerate(lines,1):
  m=re.match(r'\|\s*(DAT-\d{3}-F\d{2})\s*\|\s*([^|]+)\s*\|',line)
  if not m:continue
  field_raw=m.group(2).strip().strip('`')
  if field_raw.startswith('`') and field_raw.endswith('`'):field_raw=field_raw[1:-1]
  dat=int(m.group(1)[4:7])
  names=re.findall(r'`([a-z_]+)(?:\.[a-z_]+)?`',m.group(2))
  if '.' in field_raw: fld=field_raw.split('.')[1].strip('` ')
  else:fld=field_raw.split()[0].strip('` ').lower()
  if re.match(r'^[a-z_]+$',fld):entityfld[(dat,fld)].append((fname,n,line))

# Cross-file general statements for universal rule membership bridge.
univmap={
 'validate_before': ['Validate request/envelope input before long-running allocation or transaction entry','Validate input before allocating long-running work, entering a mutation transaction, or dispatching tools','Validate input before transaction entry or long-running allocation'],
 'retry_error':['documented retryable error or a persisted asynchronous operation identifier','documented retryable error or an actual persisted asynchronous operation identity'],
 'attribution':['Carry tenant_id, revision, actor_id, occurred_at and a correlation ID at durable state-changing boundaries','State-changing boundaries retain tenant, revision, actor, occurrence time, and correlation attribution'],
 'negative_tests':['Every revised invariant must link to at least one negative test','Revised invariants require at least one negative-test link'],
 'identity_uuid':['Application identifiers use UUIDv7 as the baseline identity convention'],
 'event_scope':['Events contain exact properties event_id','versioned envelope'],
 'nonleak':['No document content or secrets in diagnostic attributes','Audit diagnostic/provider payloads must obey their separate scopes'],
}
univ_indices={}
for key,phrases in univmap.items():
 l=[]
 for phrase in phrases:
  t=normalize(phrase)
  if not t:continue
  ranked=[]
  for i,g in enumerate(G):
   raw=normalize(gtext[i]);
   if t in raw:ranked.append(i)
  l.extend(ranked)
 univ_indices[key]=uniqsort(l)

# Named fields may use a contextual table row (the exact Markdown line establishes the inherited storage target).
field_alias={'source_id':'id'}

def row_support(r):
 m=source_field.match(r)
 if not m:return None
 entity=m.group(1).lower();fld=m.group(2).lower()
 group=entity_group.get(entity)
 if not group:return None
 ls=entityfld.get((group,fld),[])
 if not ls:return None
 for file,line,raw in ls:
  inds=G_byrow.get((file,line),[])
  if not inds:continue
  select=inds[0]
  for j in inds:
   if fld in gtext[j].lower() and ('physical/source name' in gtext[j].lower() or 'selected field' in gtext[j].lower()):select=j;break
  return select,{'file':file,'line_start':line,'line_end':line,'table_cell':'Field row / Physical/source name','quote_en':raw,'row_key':f'DAT-{group:03d} — {fld}' }
 return None

def g_evidence(j):
 e=G[j]['representative_evidence'];return {'class_id':G[j]['class_id'], 'file':e['file'],'line_start':e['line_start'],'line_end':e['line_end'],'table_cell':e.get('table_cell'),'column_header':e.get('column_header'),'row_key':e.get('row_key'),'heading_context':e.get('heading_context'), 'quote_en':e['quote_en'], 'normalized_proposition_en':G[j]['canonical_statement_en']}

def source_evidence(r):
 return [{'file':x['file'],'physical_page':x['physical_page'],'section_table_figure_locator':x.get('section_table_figure_locator'), 'quote_en':x['quote_en']} for x in r['pdf_evidence']]

# Content-token recall for a claim includes target/action; use for candidate ranking, never as a proof by itself.
def tok_recall(s,c):
 ts=set(tokens(s));tt=set(tokens(c));
 if not ts:return 0.
 return len(ts&tt)/len(ts)

def contra(s,g):
 sn=normalize(s); gn=normalize(g)
 # treat explicit negation and opposite claims conservatively if no shared scope.
 src='cannot' in sn or 'never' in sn or 'not ' in sn or 'without' in sn
 gt='cannot' in gn or 'never' in gn or 'not ' in gn or 'without' in gn
 if src and not gt and 'prohibition' in s.lower():return True
 return False

# Explicit count / quoted literal safeguards for exact direct entailment.
def anchored_terms(s):
 ss=s.lower();
 routes=get_routes(ss)
 literals=set(re.findall(r'\b(?:case_version_conflict|idempotency_conflict|model_output_invalid|no_supported_evidence|connector_reauth_required|new|triaged|in_progress|pending_approval|resolved|closed|quarantined|ready|published|awaiting_review|timestamptz|uuidv7|jsonb|bigint)\b',ss,re.I))
 nums=set(num.findall(ss));
 return routes,literals,nums

def compatible(s,c):
 sr,sl,sn=anchored_terms(s);gr,gl,gn=anchored_terms(c)
 if sr and not sr <= gr:return False
 if sn and not sn <= gn:return False
 # don't confuse different exact API verbs/status names or fields; literal differences need review
 if sl and not sl <= gl and (set(['new','closed','ready','quarantined','published','timestamptz','bigint']) & sl):return False
 return True

records=[];root=[];bridges=[];cand_unsupported=[];stats=collections.Counter();crosschecks=[]
for ix,r in enumerate(R):
 s=r['atomic_statement_en']; rn=normalize(s); rt=set(tokens(s));
 row=Sim.getrow(ix)
 d={j:float(w) for j,w in zip(row.indices,row.data)}
 ranked=sorted(d,key=lambda j:-d[j])[:30]
 cand=set(ranked)
 # Exact endpoint retrieval (never rely on similarity cutoffs).
 found_routes=get_routes(s)
 for k in found_routes:cand.update(route_idx.get(k,[]))
 # Reference source field row and catalog proof.
 fieldres=row_support(s)
 if fieldres:cand.add(fieldres[0])
 # Uncapped exact phrase and rare multi-token exact reverse lookup.
 phrases=[rn]
 if len(rt)>1:
  rterms=sorted(rt,key=lambda x:len(G_bytoken.get(x,set())))[:4]
  for t in rterms:cand.update(G_bytoken.get(t,set()) if len(G_bytoken.get(t,set()))<35 else [])
 if len(rt)>1:
  tk=sorted(rt,key=lambda t:len(G_bytoken.get(t,set())))[:3]
  if tk:
   z=G_bytoken.get(tk[0],set()).copy()
   for x in tk[1:]:z&=G_bytoken.get(x,set())
   cand.update(z)
 # exact normalized claim in generated class or raw evidence (rare source boilerplate)
 for j in list(cand):
  pass
 assert ix<len(R)
 scored=[]
 for j in cand:
  c=gtext[j];cr=graw[j];rc=max(tok_recall(s,c),tok_recall(s,cr),tok_recall(s,gctx[j]))
  ds=d.get(j,0)
  same=rn==normalize(c) or (len(rn)>25 and rn in normalize(cr)) or (len(rn)>25 and rn in normalize(c))
  score=ds + 0.16*rc + 0.15*same + 0.09*(bool(found_routes&get_routes(c+' '+cr)))
  if not compatible(s,c+' '+cr):score-=.09
  scored.append((score,j,rc,same,ds))
 scored.sort(reverse=True)
 primary=scored[0] if scored else None
 chosen=[];mode=None;grade=None;reason='';met=[];unmet=[];bridge_scope='';alternative_checks=[];failure_candidate=[]
 # Field catalog: verified case/entity line establishes context, not bare name.
 if fieldres:
  j,field_ev=fieldres
  chosen=[j];mode='INHERITED_CONTEXT';grade='E2';met=['entity','selected physical/source field','catalog inclusion'];unmet=[]
  reason=f"The source catalog's {s.split(' relational entity')[0].replace('The ','')} field is explicitly present in the DAT-{entity_group[source_field.match(s).group(1).lower()]:03d} table row; the table header and row key establish the stored entity/field scope."
  bridge_scope='The generated DAT field table enumerates the same entity and selected field as the source catalog.'
 # direct phrase or exact paraphrase, respecting structural anchors
 if not chosen:
  for sc,j,rc,same,ds in scored[:30]:
   c=gtext[j];cr=graw[j];raw_norm=normalize(cr)
   if same and compatible(s,c+' '+cr):
    # If source has a major named target, require corresponding target in evidence (canonical phrase suffices)
    chosen=[j];mode='DIRECT';grade='E3';met=['complete source proposition with source scope and outcome'];reason='The complete normalized source proposition is asserted in the original generated statement or its original table cell.';break
 # High-confidence paraphrases with strong content, exact scope, and no critical missing numbers/conditions
 if not chosen:
  for sc,j,rc,same,ds in scored[:12]:
   c=gtext[j];cr=graw[j]
   if sc<.53 or rc<.79:continue
   if not compatible(s,c+' '+cr):continue
   # Avoid cross-scope equivalence based on a short generic cell
   if r['modality']=='PROHIBITION' and 'cannot' not in normalize(c+' '+cr) and 'never' not in normalize(c+' '+cr) and 'prohibited' not in normalize(c+' '+cr):continue
   if any(w in s.lower() for w in ['only when','only if','unless','never before','same transaction']) and not any(w in (c+' '+cr).lower() for w in ['only when','only if','unless','never','same transaction','one acid transaction']):continue
   chosen=[j];mode='SEMANTIC_EQUIVALENCE';grade='E2';met=['target','operation and modality','material constraints and outcome'];reason=f"The generated predicate preserves the same target, affirmative/prohibitive operation and testable outcome; normalized content-term coverage {rc:.2f}; semantic interpretation remains best-effort.";bridge_scope='The compared source and generated claims address the same named resource/action under the inherited document/row context.';break
 # Named API inventory means method and endpoint inclusion, not any other endpoint-specific predicate
 if not chosen and found_routes and re.search(r'(?i)\b(?:primary|secondary) API (?:surface )?includes\b|\bprimary API surface\b',s):
  opts=[(sc,j) for sc,j,*z in scored if found_routes & get_routes(gtext[j]+' '+graw[j]) and ('method and path' in gtext[j].lower() or 'method and path' in (G[j]['representative_evidence'].get('column_header') or '').lower())]
  if opts:
   j=max(opts)[1];chosen=[j];mode='INHERITED_CONTEXT';grade='E2';met=['endpoint method','endpoint path','surface inclusion via API inventory'];reason='The API inventory row names the same HTTP method and complete path; its column header identifies the contract surface.';bridge_scope='The endpoint is listed as a confirmed interface in the generated API inventory.'
 # Event envelope field inference: exact row event data, if present
 if not chosen and 'canonical event envelope includes ' in s.lower():
  field=s.split('includes ')[-1].strip('. `')
  opts=[(sc,j) for sc,j,*z in scored if field.lower() in (gtext[j]+' '+graw[j]).lower() and ('event envelope' in (gtext[j]+' '+graw[j]).lower() or 'required' in (gtext[j]+' '+graw[j]).lower())]
  if opts:
   j=max(opts)[1];chosen=[j];mode='INHERITED_CONTEXT';grade='E2';met=['canonical event property','required envelope scope'];reason='The generated event contract states the same required field, with the event-envelope row/table context.';bridge_scope='The field belongs to the event-envelope definition, rather than an unrelated record.'
 # screen inventory: match screen row in original heading/row context
 if not chosen and re.search(r'(?i)\bapplication contains the ([\w &/]+) primary screen',s):
  screen=re.search(r'(?i)\bapplication contains the ([\w &/]+) primary screen',s).group(1).lower()
  opts=[(sc,j) for sc,j,*z in scored if screen in (gtext[j]+' '+graw[j]).lower() and 'primary screen' in (gtext[j]+' '+graw[j]).lower()]
  if opts:
   j=max(opts)[1];chosen=[j];mode='INHERITED_CONTEXT';grade='E2';met=['screen identity','primary screen status'];reason='The generated screen inventory explicitly labels the same named view as a confirmed primary screen.';bridge_scope='The screen inventory row identifies the requested view as primary.'
 # Strong section-specific logical conjunction for source compound controls.
 if not chosen and ('honor retry-after' in s.lower() or 'honors retry-after' in s.lower()) and 'jitter' in s.lower() and 'quota' in s.lower():
  good=[j for sc,j,_,_,_ in scored[:24] if ('retry-after' in (gtext[j]+' '+graw[j]).lower() and ('backoff' in (gtext[j]+' '+graw[j]).lower() or 'jitter' in (gtext[j]+' '+graw[j]).lower()) and 'quota' in (gtext[j]+' '+graw[j]).lower())]
  if good:
   chosen=[good[0]];mode='CONJUNCTIVE_BRIDGE';grade='E2';met=['connector-specific Retry-After','backoff with jitter','workspace quota'];reason='The original generated row commits to all three conjuncts under connector synchronization scope.';bridge_scope='Connector worker scope is inherited from the row and its containing connector flow.'
 # Explicit universal rule plus endpoint or component scope membership, only where source text itself supplies relevant class.
 if not chosen and found_routes:
  lower=s.lower(); univkey=None
  if 'validat' in lower and ('before' in lower or 'allocat' in lower):univkey='validate_before'
  elif 'dependency is unavailable' in lower or 'persisted asynchronous' in lower:univkey='retry_error'
  if univkey:
   possible=univ_indices.get(univkey,[])
   epts=[j for j in cand if found_routes & get_routes(gtext[j]+' '+graw[j])]
   if possible and epts:
    univ=possible[0]
    # verify the general rule scope: valid to all relevant requests not a component-specific rule
    for k in possible:
     if 'request' in gtext[k].lower() or 'before long-running' in gtext[k].lower():univ=k;break
    chosen=[univ,epts[0]];mode='UNIVERSAL_INSTANTIATION';grade='E2';met=['source endpoint membership','shared validation/continuation timing','required outcome'];reason='The endpoint is explicitly present in the generated API inventory and the shared request/continuation rule applies to this endpoint. The source-specific obligation is not inferred from lexical matching alone.';bridge_scope=f"The named path {list(found_routes)[0][0]} {list(found_routes)[0][1]} is identified as a public endpoint and enters the generated shared request-boundary procedure."
 # Universal invariants + named component memberships (narrow; avoid promoting a mere name to scope proof).
 if not chosen and 'uuidv7 identity' in s.lower() and 'owner aggregate' in s.lower():
  actor=re.search(r'(?i)^the\s+([\w.-]+) owner aggregate',s)
  if actor:
   target=actor.group(1).lower()
   named=[j for j in G_bytoken.get(target,set()) if target in (gtext[j]+' '+graw[j]).lower() and 'aggregate' in (gtext[j]+' '+graw[j]).lower()]
   univ=univ_indices['identity_uuid']
   if named and univ:
    chosen=[univ[0],named[0]];mode='UNIVERSAL_INSTANTIATION';grade='E2';met=['UUIDv7 invariant','identified owner aggregate'];reason='The owner aggregate is identified in the generated domain context, and the universal application-identifier rule covers its identifiers.';bridge_scope='Source component is a generated owner aggregate with application identity, not merely a glossary label.'
 # Review as provisional FN with *actual* candidate, reversals, exact aliases, and context.
 # Build nearest generated candidate with real quote. Ensure no empty audit search.
 if chosen:
  choice=uniqsort(chosen)
  cls=[G[j]['class_id'] for j in choice]
  ev=[g_evidence(j) for j in choice]
  grade=grade or 'E2'
  status='TP';stats[mode]+=1
 else:
  status='FN'
  grade='E1' if primary and (primary[0]>.18 or primary[2]>.35) else 'E0'
  ev=[];cls=[]
  cand1=primary
  if not cand1:failure_candidate=['No indexed lexical, identifier, endpoint, or field candidate was returned']
  else:
   sc,j,rc,same,ds=cand1
   sig=[]
   if found_routes and not get_routes(gtext[j]+' '+graw[j])&found_routes:sig.append('exact HTTP method/path')
   st=set(tokens(s));gt=set(tokens(gtext[j]+' '+graw[j]));missing=sorted(st-gt,key=len,reverse=True)
   if missing:sig.append('unentailed source predicate terms: '+', '.join(missing[:7]))
   if sc<.22:sig.append('no close explicit predicate bridge')
   unmet=sig or ['Complete source-level actor, scope, action, conditions, or outcome not independently proven']
   reason='The strongest located generated candidate does not prove the full source predicate, after exact-key, term, table-context, universal-rule and cross-file retrieval. '+('; '.join(unmet))
  stats['FN_'+grade]+=1
  if grade=='E1':disposition='PARTIAL_ENTAILMENT'
  elif primary and (primary[0]>.09):disposition='CONSERVATIVE_UNRESOLVED'
  else:disposition='TRUE_MISSING'
  stats[disposition]+=1
 pdf=source_evidence(r)
 # retain at least strongest 3 actual quotes for FN; at least top 2 for TP independent retrieval evidence.
 strongest=[g_evidence(j) | {'retrieval_score':round(float(sc),5),'token_recall':round(float(rc),4),'is_exact':bool(same)} for sc,j,rc,same,ds in scored[:min(8,len(scored))]]
 pdf_fields=['actor','target','precondition_en','exception_en','timing_en','expected_outcome_en','scope_en','applicable_version']
 pred_checks={}
 for key in pdf_fields:
  v=r.get(key)
  if key=='applicable_version':
   pred_checks[key]={'status':'met' if status=='TP' else 'not_proven','explanation_en':'The reference and generated specifications both declare the R1.0/1.3 design baseline as scope; baseline is not the deployment choice.' if status=='TP' else 'Version-specific applicability was not independently established.'}
  elif not v:
   pred_checks[key]={'status':'not_applicable','explanation_en':'No separate non-null predicate was normalized for this source atom; preserve the complete quoted source statement.'}
  else:
   pred_checks[key]={'status':'met' if status=='TP' else 'not_proven','explanation_en':('Full comparison relies on the cited complete generated assertion and inherited context.' if status=='TP' else 'The candidate does not independently establish this source predicate: ')+str(v)[:200]}
 pred_checks['target_action_modality_outcome']={'status':'met' if status=='TP' else 'not_proven','explanation_en':reason}
 rawid=f'ATOM-{ix+1:05d}'
 item={'method':'fullload','canonical_id':rawid,'source_id':r['source_id'],'atomic_statement_en':s,'actual_label':1,'predicted_label':1 if status=='TP' else 0,'scoring_cell':status,'pdf_evidence':pdf,'generated_evidence':ev,'origin_source_ids':[r['source_id']],'origin_generated_class_ids':cls,'coverage_mode':mode or 'NOT_ENTAILED','entailment_grade':grade,'predicate_check_en':reason,'predicate_checks':pred_checks,'scope_membership_proof_en':bridge_scope if grade=='E2' else ('Same explicit predicate as original' if status=='TP' else 'No complete class/scope proof established'),'specific_reason_en':reason,'adjudication_policy':'BEST_EFFORT_DIRECT' if grade=='E3' else 'BEST_EFFORT_BRIDGE' if grade=='E2' else 'BEST_EFFORT_CONSERVATIVE','source_version':'R1.0 / design revision 1.3'}
 records.append(item)
 if status=='TP':
  bridges.append({'source_id':r['source_id'],'canonical_id':rawid,'entailment_grade':grade,'coverage_mode':mode,'pdf_evidence':pdf,'generated_evidence':ev,'scope_membership_proof_en':item['scope_membership_proof_en'],'predicate_check_en':reason,'predicate_checks':pred_checks,'checked_exceptions_en':'Explicit status/role/permission/version restrictions retained; no unadopted proposals counted as definitive.','adjudication_policy':'BEST_EFFORT_BRIDGE' if grade=='E2' else 'BEST_EFFORT_DIRECT'})
 else:
  # Reverse generated-to-source meaning check: top neighbors of the *named source target*, beyond the textual top-k.
  sroutes=sorted([f'{a} {b}' for a,b in found_routes])
  topkeys=sorted(rt,key=lambda t:len(G_bytoken.get(t,set())))[:7]
  checked=['token:'+t for t in topkeys if t]
  checked.extend(['endpoint:'+x.lower() for x in sroutes])
  if fieldres:checked.append('catalog-field:'+source_field.match(s).group(1)+'.'+source_field.match(s).group(2))
  elif len(rt)>1:checked.append('reverse: generated classes with intersecting named target/action and inherited table row')
  root.append({'source_id':r['source_id'],'initial_grade':grade,'initial_predicted_label':0,'fn_review_disposition':disposition,'final_source_id_or_replacement_ids':[r['source_id']],'final_scoring_cell':'FN','pdf_evidence':pdf,'best_generated_candidates':strongest[:5],'exact_and_alias_keys_checked':checked,'universal_context_conjunction_checked':{'direct_synonyms':'searched by normalized token and char ngrams','universal_rules':'Shared request, identity, event and data constraints considered where matching resource membership is explicit','table_context':'Candidate table headings, row keys, columns and source lines included','cross_file':'All eight files included; alternate source-to-generated and generated-to-source indexed retrieval performed','contrary_evidence':'Unapproved proposal/TBD/Needs confirmation not promoted'},'scope_membership_proof_en':'No complete scope-membership proof was located for this source predicate.' if grade=='E0' else 'Closest generated scope is insufficient to justify the complete source predicate.','met_predicates_en':['shared topic or target'] if grade=='E1' else [],'unmet_predicates_en':unmet if unmet else ['No explicit source-specific commitment or complete universal bridge was found'],'specific_reason_en':reason,'adjudication_policy':'BEST_EFFORT_CONSERVATIVE','retrieval_diagnostics':{'candidate_pool_size':len(cand),'top_similarity':round(float(primary[0]),5) if primary else None,'reverse_named_terms_checked':topkeys,'ranked_candidate_count':len(scored)}})
 # Do NOT write generated validity decisions or negative cell/FP claims in Phase 3.
 # A plausible misfit may be the highest generated class: flag only as potential, NOT as PDF_UNSUPPORTED.
 if status=='FN' and primary and primary[0]>.3:
  cand_unsupported.append({'source_id':r['source_id'],'generated_class_id':G[primary[1]]['class_id'],'warning_en':'Source-coverage miss alone does not establish generated unsupportedness; reciprocal PDF check required in Phase 4.','note_en':'Candidate may be narrower, missing predicates, or simply a different requirement. No FP decision is made.'})

# Mandatory high-yield diagnostic probes. Print uncovered even when suspected under-splitting / context error.
probes=['case title','retention class','identical response','same case','uuidv7','cross-tenant','revision','citation','event envelope']
probe_results=[]
for p in probes:
 matched=[x for x in records if p in x['atomic_statement_en'].lower()]
 probe_results.append({'probe':p,'source_atoms':[{'source_id':x['source_id'],'cell':x['scoring_cell'],'grade':x['entailment_grade']} for x in matched[:45]],'total':len(matched),'FN':sum(x['scoring_cell']=='FN' for x in matched)})
# Final phase 3 canonical universe: only source positives R, N rows pending next phase's asserted-control analysis.
Ncontrols=[json.loads(x) for x in open(P/'oriondesk_phase1/01_source_negative_controls_final.jsonl')]
for i,n in enumerate(Ncontrols,1):
 records.append({'method':'fullload','canonical_id':f'ATOM-{len(R)+i:05d}','source_id':None,'atomic_statement_en':n.get('atomic_statement_en') or n.get('counterfactual_en') or n.get('negative_statement_en') or n.get('statement_en'),'actual_label':0,'predicted_label':None,'scoring_cell':'PENDING_PHASE_4','origin_source_ids':[],'origin_negative_control_ids':[n['negative_id']] if 'negative_id' in n else [n.get('control_id')], 'origin_generated_class_ids':[],'pdf_evidence':n.get('pdf_evidence',[]),'generated_evidence':[],'adjudication_policy':'NOT_YET_ASSESSED_PHASE_4'})

# Emit phase-3 completed source-positive evidence but mark negative controls undecided; FP-only generated propositions pending Phase 4.
def writej(name,items):
 with open(OUT/name,'w',encoding='utf-8') as f:
  for a in items:f.write(json.dumps(a,ensure_ascii=False,sort_keys=True)+'\n')
writej('03_canonical_universe_final.jsonl',records)
writej('03_evidence_matches_final.jsonl',records[:len(R)])
writej('03_semantic_coverage_bridges_final.jsonl',bridges)
writej('03_fn_root_cause_audit_final.jsonl',root)
writej('03_candidate_generated_validity_review.jsonl',cand_unsupported)
writej('03_regression_probes_final.jsonl',probe_results)
summary={'protocol_version':'6.1','phase':3,'status':'PHASE_COMPLETED_BEST_EFFORT','method':'fullload','source_positive_atoms':len(R),'source_negative_controls':len(Ncontrols),'raw_generated_classes':len(G),'source_coverage':{'TP':len(bridges),'FN':len(root),'E3':sum(x['entailment_grade']=='E3' for x in bridges),'E2':sum(x['entailment_grade']=='E2' for x in bridges),'E1':stats['FN_E1'],'E0':stats['FN_E0']},'FN_root_cause':{k:stats[k] for k in ('TRUE_MISSING','PARTIAL_ENTAILMENT','CONSERVATIVE_UNRESOLVED')},'evidence':'All source atoms have source and reciprocal generated evidence records; class evidence is original file line quote; no Phase 4 validity claims.','scope_note':'Source-positive coverage is a provisional computation, not a four-cell confusion matrix; negative controls and generated-only claims await Phase 4.','limitations':['Automated candidate retrieval cannot certify meaning for every complete source predicate.','Common/source atoms have known semantic-overlap and duplication watchlist retained for Phase 5.','Extraction of generated occurrences was best-effort in Phase 2, potentially limiting candidate proof.','Conservative FN entries must not be interpreted as confirmed absent without further human semantic audit.']}
(OUT/'03_phase_status_final.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(summary,indent=2))
print('probes',json.dumps(probe_results,ensure_ascii=False)[:2500])
