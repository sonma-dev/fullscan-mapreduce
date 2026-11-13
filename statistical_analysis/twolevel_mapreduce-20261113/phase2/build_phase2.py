#!/usr/bin/env python3
"""One-pass, conservative, provenance-preserving English Markdown claim inventory.

The method deliberately favors bounded, explicit extraction over unsupported semantic certainty.
It never reads Phase 1 source atoms for generated-claim extraction or matching.
"""
from __future__ import annotations
import re,json,hashlib,os,shutil,collections,itertools,unicodedata
from pathlib import Path
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

BASE=Path('/mnt/data')
OUT=BASE/'oriondesk_v61_atomic_eval_20261113'
P1=BASE/'oriondesk_v61_phase1_20261113'
OUT.mkdir(exist_ok=True)
for name in ['01_source_atoms_final.jsonl','01_source_negative_controls_final.jsonl','01_pdf_page_coverage_final.jsonl','01_pdf_coverage_and_source_exclusions.md','01_source_atomization_challenge_final.jsonl','01_pdf_quote_verification_final.jsonl','01_source_evidence_verification_final.json','01_input_manifest_final.json','01_phase_status_final.json','verify_phase1.py']:
 if (P1/name).exists():
  a=P1/name; b=OUT/name
  if not b.exists() or hashlib.sha256(a.read_bytes()).digest()!=hashlib.sha256(b.read_bytes()).digest():shutil.copy2(a,b)

INPUTS=['01_screen_functions(8).md','02_api(8).md','03_data(8).md','04_batch_functions(8).md','05_business_rules(8).md','06_exception_handling(9).md','07_processing_flows(9).md','08_architecture_decision(8).md']
method='supplied_set_1'
ABBREVS={'e.g.','i.e.','pp.','p.','vs.','r1.0','wcag2.2','sec.','fig.','no.','et al.'}
RE_CITE=re.compile(r'\s*\[(?:(?:Source|PDF|Current PDF|Additional source|Register evidence|pp?\.|source|p\.|Source findings|Sources):?)[^\]\n]*\]\s*$',re.I)
RE_MARKUP=re.compile(r'\*\*|(?<!\w)\*(?!\w)|`')
RE_META_START=re.compile(r'^(?:\*\*)?(?:Needs confirmation|TBD|Unadopted proposal|Proposal|Open question|No new proposal|No proposals|Source findings|These (?:are|rows)|References? (?:to|connect)|The (?:source|following|columns|table)|All citations|This (?:file|specification)|Status and|Source:|See |Note:)',re.I)
RE_OPEN_ONLY=re.compile(r'\b(?:TBD|Needs confirmation|not selected|unselected|not yet selected|not approved|open|unknown|unspecified|unresolved|would require|requires confirmation|to confirm|questions? to confirm)\b',re.I)
RE_NONDEF=re.compile(r'\b(?:may be|could be|should be considered|proposed|illustrative|hypothetical|example only|not implemented|needs confirmation|not selected|unadopted|unapproved alternative)\b',re.I)
RE_COMMIT=re.compile(r'\b(?:must|shall|requires?|required|cannot|never|prohibit(?:ed|s)?|deny|denied|reject|rejected|retain|preserve|validate|record|enforce|write|read|return|returns|submit|provide|invoke|assign|guard|protect|ensure|exclude|block|blocks|fail|fails|sign|signed|open|opens|rebuild|rebuilds|scan|scans|extract|extracts|trigger|triggers|complete|completes|check|created?|creates|start|starts|save|store|stores|attach|attached|contains|include|includes|use|uses|target|keeps?|becomes?|provide|provides|apply|applies|support|supports|accepted|accepts|issues|issued|limits?|bound|binds?|check|checks|before|after|without|only|when|on |if |automatic|automatically|cap|separate|distinct|immutable|append.only|release.blocking|encrypted|signed|scoped|immutable|200|201|202|204|400|401|403|404|409|422|429|99\.9|RPO|RTO|P95|PKCE|SSE|RFC3339|RLS|SQL|HTTP|ACL|UUID)\b',re.I)
RE_CONTEXT_ID=re.compile(r'\b(?:SF|SCR|API|DAT|BAT|BR|ERR|FLOW|AD|RES|TST|SEC|T)-\d{1,3}[a-z]?(?:\.\d+)?\b',re.I)
RE_ENDPOINT=re.compile(r'(?:GET|POST|PUT|PATCH|DELETE)\s+(/(?:v1|internal)/[^\s,;)]+)')
RE_PATH=re.compile(r'/(?:v1|internal)/[A-Za-z0-9_/{}/.?=&-]+')
RE_ATOMIZED_STATUS=re.compile(r'(?:^|;\s*)(?:Needs confirmation|TBD|open|unselected|not selected|pending decision|not supplied)(?:\b|:)',re.I)
RE_FIELD_ID=re.compile(r'\b(?:tenant_id|workspace_id|actor_id|event_id|trace_id|correlation_id|occurred_at|aggregate_revision|schema_version|plan_revision|artifact_hash|case_id|run_id|source_id|source_hash|evidence_set_id|caseId|runId|If-Match|Idempotency-Key|Last-Event-ID)\b')
RE_CODE_LANG=re.compile(r'^```\s*(\w+)?')
STOP=set('the a an and or of on in at by to from with for is are as be been being into than that those which where whose this these who it its their they we you our all each every only no not can may will would should must do does did has have had if then else when after before under over upon per via using use used requires required necessary target targets scope type status value data source purpose object inputs outputs content context time date version example specific named current cases case run operation entity available supported open confirmed implementation reference remains applies rules true false'.split())


def write_jsonl(path,objs):
 with open(path,'w',encoding='utf8') as w:
  for o in objs:w.write(json.dumps(o,ensure_ascii=False,sort_keys=True)+'\n')

def strip_cite(t):
 t=t.strip()
 # Trailing source footnotes are not part of an eligible assertion.
 for _ in range(3):
  nt=RE_CITE.sub('',t).strip()
  if nt==t:break
  t=nt
 t=re.sub(r'\s+\[(?:Source|pp?\.|PDF|Current PDF)[^\]]+$','',t)
 return t.strip()

def clean(t):
 t=strip_cite(t)
 t=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',t)
 t=RE_MARKUP.sub('',t)
 t=t.replace('**','').replace('“','"').replace('”','"').replace('’',"'").strip(' \t—–;-')
 return re.sub(r'\s+',' ',t).strip()

def table_cells(s):
 # Split unescaped pipe while retaining the physical original.
 return [x.strip() for x in re.split(r'(?<!\\)\|',s.strip().strip('|'))]

def sentence_chunks(t):
 t=clean(t)
 if not t:return []
 # Explicit unresolved spans after labels are held out rather than predicting a default.
 t=re.split(r'\b(?:\*\*)?Needs confirmation\s*(?:—|:|beside|for)\b',t,maxsplit=1,flags=re.I)[0]
 if not t:return []
 # Semi-colon often separates independently testable commitments in this corpus.
 a=re.split(r';\s*(?![^{}]*\})',t)
 all_chunks=[]
 for s in a:
  s=s.strip()
  if not s:continue
  # Split only at sentence boundaries; keep decimal points and abbreviations.
  pieces=re.split(r'(?<=[.!?])\s+(?=(?:[A-Z]|\d+\.|\*\*))',s)
  for p in pieces:
   p=p.strip()
   if p:all_chunks.append(p)
 return all_chunks

def exclusion_reason(t,context='',col_header='',role=''):
 t=t.strip()
 if not t:return 'EMPTY_OR_STRUCTURE'
 s=clean(t)
 if not s:return 'SOURCE_CITATION_ONLY'
 if re.search(r'\b(?:remains? (?:open|unselected|undefined|unresolved|unspecified)|is (?:open|unselected|undefined|unresolved)|are (?:open|unselected|undefined|unresolved)|requires? confirmation|needs? confirmation|not (?:specified|selected|supplied|established|confirmed)|\bopen\.?$)\b',s,re.I) and not re.search(r'\b(?:must|cannot|never|prohibited|binding|mandatory|preserve|retain|reject|no implicit)\b',s,re.I):return 'UNRESOLVED_CONTRACT_NOT_ADOPTED'
 if role=='diagram':return 'DIAGRAM_OR_SUPPORTING_CODE_NOT_INDEPENDENT_CLAIM'
 if role=='example_code':return 'ILLUSTRATIVE_CODE_NOT_SELECTED_COMMITMENT'
 if re.fullmatch(r'(?:[-+*/|=_.:;\d\\s]|\w{1,3}){1,12}',s):return 'STRUCTURAL_OR_FRAGMENT'
 if re.match(r'^(?:(?:Source|Sources|PDF|Reference(?:s)?|Additional source|Source findings|Evidence):?\s*\[|\[[\w:-]+\])',s,re.I):return 'EVIDENCE_REFERENCE_ONLY'
 if re.fullmatch(r'(?:\w+\s*){1,2}',s) and not RE_COMMIT.search(s):return 'INSUFFICIENT_STANDALONE_ASSERTION'
 if re.match(r'^(?:No|Not) (?:additional|new|complete|independent|previous|screen|specific|production)',s,re.I) and not re.search(r'\b(?:must|may|allowed|cannot|never)\b',s,re.I):return 'EVIDENCE_LIMITATION_NOT_IMPLEMENTATION'
 if RE_META_START.search(s) and not re.search(r'\b(?:must|shall|cannot|never|before|after|required|preserve|deny|prohibit|do not)\b',s,re.I):return 'META_OR_UNRESOLVED_CONTRACT'
 if re.search(r'(?:must define|define (?:the|which|how|exact|whether)|which (?:provider|actor|schema|role)|what (?:is|are)|confirm whether|what (?:should|must))',s,re.I):return 'OPEN_DECISION_NOT_APPROVED'
 if re.search(r'\b(?:Needs confirmation|TBD|unadopted proposal|unselected alternative)\b',s,re.I) and not re.search(r'\b(?:must|never|cannot|prohibited|mandatory|binding|confirmed|require[ds])\b',s,re.I):return 'OPEN_DECISION_NOT_APPROVED'
 if re.search(r'^(?:p{1,2}\.|\[|§|`?\w+_)?\d+(?:–\d+)?\s*$',s):return 'LOCATOR_ONLY'
 if re.search(r'(?:screen_functions|processing_flows|batch_functions|business_rules|exception_handling|api|data):r\d+:c\d+:f\d+',s,re.I) and not re.search(r'\b(?:must|shall|prohibited|cannot|before|after)\b',s,re.I):return 'SOURCE_PROVENANCE_ONLY'
 if not RE_COMMIT.search(s) and not RE_ENDPOINT.search(s) and len(s)<110:
  # Short, explicit outcome/constraint cell fragments inherit table-row meaning.
  if col_header.lower() not in {'prose','sql'} and re.search(r'(?:confirmed|behavior|result|success|required|status|permission|constraint|scope|effect|response|output|invariant|definition|rule|action|process|condition|content|fields|trigger|control|guard|reference|record)',col_header,re.I) and len(s)>20 and not RE_OPEN_ONLY.search(s):pass
  else:return 'TOPIC_OR_NARRATIVE_WITHOUT_BINDING_COMMITMENT'
 if len(s)<13 and not re.match(r'^(?:20[0129]|40[049]|42[29])\b',s):return 'FRAGMENT_WITHOUT_STANDALONE_REQUIREMENT'
 return None

# Lightweight normalization; do not remove legal/quantitative distinctions or identifiers.
SYNONYMS=[('shall','must'),('mandatory','required'),('has to','must'),('is required to','must'),('must not','prohibited'),('never','prohibited'),('cannot','prohibited'),('no implicit','prohibited implicit'),('before parsing','before parse'),('before generation','before model generation'),('accepted operation','accepted asynchronous operation'),('idempotent','idempotency'),('source acl','originating acl'),('retrieved evidence','evidence'),('model deployment','deployment'),('authorization','authorisation'),('authorize','authorise'),('versioned json','version json'),('publication gate','publish gate'),('outbox event','event outbox')]
def normalize(t):
 t=clean(t).lower()
 t=re.sub(r'\b(?:sf|api|dat|bat|br|err|flow)-\d+[a-z]?(?:\.\d+)?\b',' ',t)
 t=re.sub(r'\b(?:confirmed|reference|specification assigned)\s*[:—-]\s*',' ',t)
 t=re.sub(r'\s+',' ',t)
 for a,b in SYNONYMS:t=t.replace(a,b)
 t=re.sub(r'[^\w/{}.?=+-]+',' ',t)
 return re.sub(r'\s+',' ',t).strip()

DOMAINS={
 'auth':r'pkce|oidc|authentication|authorization|authorise|authenticate|principal|role|tenant|rls|permission|membership',
 'api':r'\b(?:get|post|patch|put|delete)\s+/|/v1/|/internal/|response code|http status|rest',
 'case':r'\bcase\b|cases|revisions|casecreated|case version|case status|closed|triaged',
 'evidence':r'evidence|citation|anchor|chunk|source|ocr|pdf|document|extraction',
 'connector':r'connector|sync|cursor|watermark|backfill|provisioning',
 'index':r'index|retrieval|search|rrf|embedding|vector|cache|rerank',
 'model':r'model|provider|deployment|prompt|token|gateway|generation',
 'workflow':r'orchestrat|agent|mcp|a2a|tool|plan|run_step|checkpoint',
 'review':r'approval|review|reviewer|self.approval|rejection|override',
 'publication':r'publish|publication|final pointer|satisfied gate',
 'events':r'outbox|event|replay|saga|duplicate|idempotency|ledger|transaction',
 'retention':r'hold|delete|purge|retention|export|audit|key|credential|encrypt|redact',
 'operations':r'backpressure|slo|rpo|rto|recovery|chaos|alert|incident|degrad|failover|backup|canary',
 'quality':r'evaluation|benchmark|test|precision|recall|confidence|sign.off|release|security',
 'ui':r'screen|sidebar|navigation|keyboard|focus|wcag|interface|sse|localization',
}
def dom(t):
 t=t.lower()
 scores={k:len(re.findall(v,t,re.I)) for k,v in DOMAINS.items()}
 if not any(scores.values()):return 'other'
 # For mixed claims, use a broad membership set rather than different ID tokens.
 return ','.join(k for k,v in sorted(scores.items(),key=lambda x:-x[1]) if v>0 and v>=max(scores.values())*.55)[:85]

def protected(t):
 # Normalizing only mandatory discriminators prevents merging distinct API, status, numeric, and role commitments.
 s=clean(t)
 endpoints=set(re.findall(r'(?:GET|POST|PUT|PATCH|DELETE)\s+/(?:v1|internal)/[^\s,;|)]+',s))
 codes=set(re.findall(r'\b(?:[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+|(?:HTTP\s*)?[245]\d\d)\b',s))
 # Preserve selected quantitative values but ignore locator page numbers and trace IDs.
 nums=set(re.findall(r'(?<![\w/-])\d+(?:\.\d+)?\s*(?:MB|ms|%|min|hours?|days?|years?|rps|tokens?|pages?|dimensions?|tools?|calls?|jobs?|concurrent|synthetic)?\b',s,re.I))
 roles=set(re.findall(r'\b(?:Analyst|Reviewer|Auditor|Admin|Owner|Member|Service|Operator|SRE)\b',s))
 return {'paths':sorted(endpoints),'codes':sorted(codes),'numeric':sorted(nums),'roles':sorted(roles)}

def hard_conflict(a,b):
 pa,pb=a['protected'],b['protected']
 if pa['paths'] and pb['paths'] and pa['paths']!=pb['paths']:return True
 if pa['codes'] and pb['codes'] and pa['codes']!=pb['codes']:
  # Codes such as ID names are distinctive; differences are potentially serious.
  return True
 if pa['numeric'] and pb['numeric'] and pa['numeric']!=pb['numeric']:return True
 if pa['roles'] and pb['roles'] and pa['roles']!=pb['roles']:return True
 # Distinguish deontic/prohibited versus permissive claims.
 for neg in ['prohibited','must not','cannot','never','deny','not authorized']:
  if (neg in a['normalized_predicate_en']) != (neg in b['normalized_predicate_en']) and neg in ('prohibited','must not','cannot','never'):
   return True
 return False

atoms=[]; excluded=[]; coverage=[]; files=[]; oid=0; exid=0
for fidx,filename in enumerate(INPUTS):
 f=BASE/filename
 assert f.exists() and f.stat().st_size>1000,filename
 original=f.read_text(encoding='utf8'); lines=original.splitlines()
 files.append({'filename':filename,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'physical_lines':len(lines),'bytes':f.stat().st_size,'file_order':fidx+1})
 header_path=[]; table_headers=None; section=''; code_lang=None
 for li,raw in enumerate(lines,1):
  s=raw.strip(); markup='blank' if not s else 'prose'
  if s.startswith('#'):
   level=len(s)-len(s.lstrip('#'))
   header_path=header_path[:level-1]+[clean(s.lstrip('# '))]
   section=' > '.join(header_path)
   table_headers=None
   coverage.append({'file':filename,'line':li,'unit':'heading','status':'STRUCTURE','raw_text_en':raw,'context_en':section,'generated_occurrence_ids':[]})
   continue
  if not s:
   coverage.append({'file':filename,'line':li,'unit':'blank','status':'STRUCTURE','raw_text_en':raw,'context_en':section,'generated_occurrence_ids':[]})
   continue
  mt=RE_CODE_LANG.match(s)
  if mt:
   if code_lang is None:code_lang=(mt.group(1) or '').lower()
   else:code_lang=None
   coverage.append({'file':filename,'line':li,'unit':'code_fence','status':'STRUCTURE','raw_text_en':raw,'context_en':section,'generated_occurrence_ids':[]})
   continue
  if code_lang is not None:
   # SQL establishes literal DDL constraints; YAML/JSON/mermaid usually illustrative and restated.
   if code_lang in {'mermaid','json','yaml','http','shell','bash'}:reason='ILLUSTRATIVE_OR_DIAGRAM_CODE'
   elif code_lang=='sql':reason=None
   else:reason='CODE_UNSELECTED_OR_SUPPORTING'
   if reason:
    exid+=1
    excluded.append({'exclusion_id':f'EXC-GEN-{exid:05d}','origin':'GENERATED','file':filename,'line_start':li,'line_end':li,'table_cell':None,'quote_en':raw,'reason_code':reason,'exclusion_reason_en':'Code/diagram excerpt is not treated as a new independent definitive requirement; surrounding definitive prose is inspected.'})
    coverage.append({'file':filename,'line':li,'unit':'code','status':'EXCLUDED','raw_text_en':raw,'context_en':section,'reason_code':reason,'generated_occurrence_ids':[]})
    continue
   blocks=[{'content':s,'cell':None,'col':'SQL','row_key':'Reference DDL','row_scope':section}]
   markup='sql'
  elif s.startswith('|') and s.endswith('|'):
   cells=table_cells(s)
   if all(re.match(r'^:?-{3,}:?$',x) for x in cells):
    coverage.append({'file':filename,'line':li,'unit':'table_delimiter','status':'STRUCTURE','raw_text_en':raw,'context_en':section,'generated_occurrence_ids':[]});continue
   if table_headers is None or len(cells)!=len(table_headers):
    table_headers=cells
    coverage.append({'file':filename,'line':li,'unit':'table_header','status':'STRUCTURE','raw_text_en':raw,'context_en':section,'generated_occurrence_ids':[]});continue
   markup='table'
   rowkey=clean(cells[0])
   row_status=' '.join(cells[i] for i,h in enumerate(table_headers) if re.search(r'\bStatus\b',h,re.I))
   # Register row unresolved decisions are not standalone approvals.
   unapproved_register=(filename.startswith('08_') and (rowkey.startswith('AD-') or re.search(r'\bPending\b',section,re.I)) and not rowkey.startswith('RES-'))
   blocks=[]
   for ci,(h,cell) in enumerate(zip(table_headers,cells)):
    if ci==0:
     if re.search(r'^(SCR-|API-|DAT-|BAT-|BR-|ERR-|FLOW-|RES-|AD-|TST-|T-|SEC-)',rowkey):
      # row key embeds the subject, not an independent claim by itself
      pass
     continue
    if h.lower()=='markdown file and section contexts':continue
    if re.search(r'\b(?:source|reference|related|timing and evidence|original source|source quote|questions? to confirm|pending question|open question|unresolved|needs confirmation|remaining boundary|locator|status)\b',h,re.I) and h.lower() not in {'source name','source entity','source scope','reference result/output','reference status','source-named screen'}:
     continue
    if unapproved_register and not re.search(r'\b(?:binding|mandatory|prohibited|shall|must|cannot|required|confirmed)\b',cell,re.I):continue
    if not clean(cell):continue
    # Row-level API IDs and paths set subject scope even if content cell only says 201.
    context=rowkey
    meth=RE_ENDPOINT.search(raw)
    if meth and re.match(r'^(API-|\w+\s*\[)',rowkey):context+=f' {meth.group(0)}'
    if h.lower() in {'source','status','reference'}:continue
    blocks.append({'content':cell,'cell':{'column_index':ci+1,'column_header_en':h,'row_key_en':rowkey},'col':h,'row_key':rowkey,'row_scope':section,'row_status':row_status,'unapproved_register':unapproved_register})
   if not blocks:
    coverage.append({'file':filename,'line':li,'unit':'table_row','status':'EXCLUDED','raw_text_en':raw,'context_en':section,'reason_code':'REFERENCE_OR_UNAPPROVED_REGISTER_ROW','generated_occurrence_ids':[]});continue
  else:
   table_headers=None
   markup='list' if re.match(r'^\s*(?:[-*+]\s|\d+[.)]\s)',s) else 'paragraph'
   text0=re.sub(r'^\s*(?:[-*+]\s|\d+[.)]\s)','',s)
   blocks=[{'content':text0,'cell':None,'col':'prose','row_key':'','row_scope':section}]
  line_occ=[]; line_exc=[]
  for block in blocks:
   original_content=block['content']; col=block['col']; key=block['row_key']
   text0=strip_cite(original_content)
   # Ignore independent sentence that only inventories open decisions or examples.
   chunks=sentence_chunks(text0)
   if col.lower()=='selected physical names':
    chunks=[c.strip() for chunk in chunks for c in chunk.split(',') if c.strip()]
   for chunk in chunks:
    if col.lower()=='scope' and re.search(r',\s*mapping open$',chunk,re.I):chunk=re.sub(r',\s*mapping open$','',chunk,flags=re.I)
    # Cut off explicitly unselected subclauses if separable.
    if re.search(r'^(?:needs confirmation|open|tbd|undefined|unselected|not selected|no confirmation|subject to confirmation)\b',chunk,re.I):
     reason='UNRESOLVED_OR_UNADOPTED_NO_PREDICTION'
    else:
     reason=exclusion_reason(chunk,section,col,'')
    if filename.startswith('08_') and key.startswith('AD-') and re.search(r'\b(?:may proceed|on hold|hold boundary|unselected|needs confirmation)\b',chunk,re.I) and not re.search(r'\b(?:must|binding|cannot|never|prohibited)\b',chunk,re.I):reason='OPEN_ARCHITECTURE_DECISION_NOT_ADOPTED'
    if col.lower().startswith('needs confirmation'):reason='UNRESOLVED_ATTRIBUTE_COLUMN'
    if col.lower().strip() in {'trigger','trigger / exception','test trigger','scenario / test','condition / trigger'} and not re.search(r'\b(?:must|shall|cannot|never|prohibited|mandatory|preserve|retain|reject|require[ds])\b',chunk,re.I):reason='TEST_TRIGGER_NOT_INDEPENDENT_OBLIGATION'
    if re.search(r'\b(?:is|are|remain|remains|still) (?:open|unselected|unresolved|undefined)\b',chunk,re.I) and not re.search(r'\b(?:must|cannot|never|prohibited|binding|mandatory|preserve|retain|reject|no implicit)\b',chunk,re.I):reason='OPEN_CONTRACT_UNAPPROVED'
    # Individually testable table declarations inherit entity/column/action context.
    strong_cols={'selected physical names','meaning/type','nullability/default','key/value constraint','scope','source name','source entity','reference result/output','status and constraint'}
    if block['cell'] and col.lower() in strong_cols and reason != 'TEST_TRIGGER_NOT_INDEPENDENT_OBLIGATION' and not re.search(r'\b(?:needs confirmation|tbd|unselected|not selected|unknown|unresolved|is open|are open|remains open|open mapping|no default shown|not supplied|not established)\b',chunk,re.I) and len(chunk.strip())>=2:
     reason=None
    if re.search(r'\b(?:remains? (?:open|unselected|undefined|unresolved)|is (?:open|unselected)|are (?:open|unselected)|needs confirmation|unknown|unspecified|not selected)\b',chunk,re.I) and not re.search(r'\b(?:must|cannot|never|prohibited|binding|mandatory|preserve|retain|reject|no implicit)\b',chunk,re.I):reason='OPEN_CONTRACT_UNAPPROVED'
    if re.search(r'\b(?:open questions|unresolved items|pending decisions|remaining implementation decisions)\b',section,re.I) and not re.search(r'\b(?:must|shall|cannot|never|prohibited|mandatory|binding|preserve|retain|reject|applies|required)\b',chunk,re.I):reason='OPEN_QUESTION_SECTION_NOT_ADOPTED'
    if reason:
     exid+=1
     exc={'exclusion_id':f'EXC-GEN-{exid:05d}','origin':'GENERATED','file':filename,'line_start':li,'line_end':li,'table_cell':block['cell'],'quote_en':chunk,'reason_code':reason,'exclusion_reason_en':'The extracted span is not a definitive standalone implementation requirement under protocol section 3.2.'}
     excluded.append(exc);line_exc.append(exc['exclusion_id'])
     continue
    oid+=1
    # Keep source and row context separately so matcher can inherit it without misattributing a lone cell.
    ctx=section
    if key:
     ctx+=' | '+key
     # Root API path preserved in row/cell context.
     api=RE_ENDPOINT.search(raw)
     if api:ctx+=' | '+api.group(0)
    # Positive commitments within explicit unresolved heading must have their conditions preserved.
    norm=normalize(chunk)
    result={
     'generated_occurrence_id':f'GEN-{oid:05d}', 'prefix':method,
     'source_file':filename,'file':filename,'line_start':li,'line_end':li,
     'table_cell':block['cell'],'source_kind':markup,'section_context_en':section,
     'row_context_en':key or None,'column_context_en':col or None,
     'quote_en':chunk,'original_cell_en':original_content,
     'atomic_statement_en':(key+' — '+chunk if key else chunk),
     'normalized_predicate_en':norm,
     'exact_structural_keys':sorted(set(RE_PATH.findall(raw) + RE_FIELD_ID.findall(raw)+RE_CONTEXT_ID.findall(raw)+[k for k in re.findall(r'\b[A-Z][A-Z0-9_]{3,}\b',chunk) if len(k)>3])),
     'semantic_domain':dom(chunk+' '+(key or '')),
     'protected':protected(chunk),
     'extraction_method':'CONSERVATIVE_ONE_PASS_SENTENCE_SEMICOLON_TABLE_CELL',
     'claim_definitiveness':'DEFINITIVE_SUBCLAIM',
     'eligibility_assessment':'BEST_EFFORT_DEFINITIVE'
    }
    atoms.append(result);line_occ.append(result['generated_occurrence_id'])
  coverage.append({'file':filename,'line':li,'unit':markup,'status':'ELIGIBLE_AND_EXCLUDED' if line_occ and line_exc else 'ELIGIBLE' if line_occ else 'EXCLUDED','raw_text_en':raw,'context_en':section,'generated_occurrence_ids':line_occ,'excluded_ids':line_exc})

# Raw semantic classes: cluster first exact normalized claims, then cautious strongly similar corpus-level phrasings.
# Keep actor/path/code, limit and modal/polarity constraints distinct.
for i,a in enumerate(atoms):a['_idx']=i
parent=list(range(len(atoms)))
def find(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
def union(a,b):
 a=find(a);b=find(b)
 if a!=b:parent[max(a,b)]=min(a,b)
exact={}
for i,a in enumerate(atoms):
 sig=(a['normalized_predicate_en'], (a['row_context_en'] if a['source_kind']=='table' and len(a['quote_en'])<48 else ''), tuple(a['protected']['paths']),tuple(a['protected']['codes']),tuple(a['protected']['numeric']),tuple(a['protected']['roles']))
 if sig in exact:union(exact[sig],i)
 else:exact[sig]=i

# Use TF-IDF nearest neighbors only as a conservative equivalence supplement.
# Document title/ID words are intentionally omitted from similarity vector; no false method-key mergers.
texts=[a['normalized_predicate_en'] for a in atoms]
candidate_pairs=[]; fuzzy_merged=0
if len(texts)>2:
 vec=TfidfVectorizer(analyzer='char',ngram_range=(3,5),min_df=1,max_features=180000,sublinear_tf=True,dtype=__import__('numpy').float64)
 X=vec.fit_transform(texts)
 nn=NearestNeighbors(n_neighbors=min(7,len(texts)),metric='cosine',algorithm='brute',n_jobs=-1).fit(X)
 sims,neighbors=nn.kneighbors(X)
 for i in range(len(atoms)):
  for dist,j in zip(sims[i][1:],neighbors[i][1:]):
   j=int(j)
   if j<=i:continue
   sim=1-float(dist)
   if sim<.77:continue
   aa,bb=atoms[i],atoms[j]
   if hard_conflict(aa,bb):continue
   # Do not equate different table row entities/API subjects on similar phrasing.
   ra,rb=aa['row_context_en'],bb['row_context_en']
   row_a=re.match(r'^(?:API|SCR|FLOW|BAT|ERR|DAT)-\d+[a-z]?',ra or '')
   row_b=re.match(r'^(?:API|SCR|FLOW|BAT|ERR|DAT)-\d+[a-z]?',rb or '')
   if row_a and row_b and aa['file']==bb['file'] and row_a.group(0)!=row_b.group(0):continue
   # Short table cells need row-context equivalence, not just wording.
   if (aa['source_kind']=='table' and len(aa['quote_en'])<48 or bb['source_kind']=='table' and len(bb['quote_en'])<48) and (aa['row_context_en'] or '')!=(bb['row_context_en'] or ''):continue
   # High-confidence near-identical statements only, no broad semantic guess.
   if sim>=.96:
    union(i,j);fuzzy_merged+=1
   elif sim>=.83:
    candidate_pairs.append({'a':aa['generated_occurrence_id'],'b':bb['generated_occurrence_id'],'score':round(sim,4),'a_locator':{'file':aa['file'],'line':aa['line_start'],'table_cell':aa['table_cell']},'b_locator':{'file':bb['file'],'line':bb['line_start'],'table_cell':bb['table_cell']},'review_flag':'POTENTIAL_PARAPHRASE_NOT_MERGED_TO_AVOID_SEMANTIC_OVERMERGE'})

clusters=collections.defaultdict(list)
for i,a in enumerate(atoms):clusters[find(i)].append(a)
# Sort classes by first occurrence, preserve stable IDs. Each eligible occurrence appears in one class.
classes=[]
for n,(k,occ) in enumerate(sorted(clusters.items(),key=lambda kv:kv[1][0]['_idx']),1):
 occ.sort(key=lambda x:x['_idx'])
 cid=f'GCLASS-{n:05d}'
 for a in occ:a['generated_class_id']=cid
 cls={
  'generated_class_id':cid,'prefix':method,
  'canonical_atomic_statement_en':occ[0]['atomic_statement_en'],
  'representative_occurrence_id':occ[0]['generated_occurrence_id'],
  'representative_quote_en':occ[0]['quote_en'],
  'representative_file':occ[0]['file'],'representative_line':occ[0]['line_start'],
  'representative_table_cell':occ[0]['table_cell'],
  'occurrence_ids':[a['generated_occurrence_id'] for a in occ],
  'occurrences':[{'generated_occurrence_id':a['generated_occurrence_id'],'file':a['file'],'line_start':a['line_start'],'line_end':a['line_end'],'table_cell':a['table_cell'],'quote_en':a['quote_en']} for a in occ],
  'occurrence_count':len(occ),'files':sorted(set(a['file'] for a in occ)),
  'semantic_domain':occ[0]['semantic_domain'],
  'semantic_equivalence_basis':'EXACT_NORMALIZED_FULL_CLAIM' if len(set(a['normalized_predicate_en'] for a in occ))==1 else 'STRONG_SURFACE_EQUIVALENCE_WITH_PROTECTED_PREDICATE_GUARDS',
  'exclusions_checked_en':'API paths, explicit role names, numeric bounds, uppercase codes, and prohibition polarity were guarded against incompatible merges.',
  'full_predicate_review_status':'AUTOMATED_CONSERVATIVE_BEST_EFFORT_UNAUDITED_SEMANTICALLY',
 }
 classes.append(cls)

for a in atoms:a.pop('_idx',None)
# Stable, reverse-search-friendly tokens per class.
reverse=collections.defaultdict(set)
for c in classes:
 cid=c['generated_class_id']; a=next(a for a in atoms if a['generated_occurrence_id']==c['representative_occurrence_id'])
 for occ in c['occurrences']:
  rawline=next(x['raw_text_en'] for x in coverage if x['file']==occ['file'] and x['line']==occ['line_start'])
  for x in RE_ENDPOINT.findall(rawline):reverse['PATH:'+x.lower()].add(cid)
  for x in RE_FIELD_ID.findall(rawline):reverse['FIELD:'+x.lower()].add(cid)
  for x in RE_CONTEXT_ID.findall(rawline):reverse['ID:'+x.upper()].add(cid)
 for x in a['exact_structural_keys']:reverse['STRUCT:'+x.lower()].add(cid)
 terms=set(re.findall(r'[a-zA-Z][a-zA-Z_]{3,}',a['normalized_predicate_en']))-STOP
 for x in sorted(terms):reverse['WORD:'+x.lower()].add(cid)

# Per-line/cell coverage: separate cell inventory to ensure no body cells silently skipped.
cell_coverage=[]
for fn in INPUTS:
 lines=(BASE/fn).read_text(encoding='utf8').splitlines()
 header=None
 for i,line in enumerate(lines,1):
  if line.startswith('|') and line.rstrip().endswith('|'):
   cells=table_cells(line)
   if all(re.match(r'^:?-{3,}:?$',x) for x in cells):continue
   if header is None or len(header)!=len(cells):header=cells;continue
   for k,cell in enumerate(cells,1):
    if not cell.strip():continue
    matches=[a['generated_occurrence_id'] for a in atoms if a['file']==fn and a['line_start']==i and a['table_cell'] is not None and a['table_cell']['column_index']==k]
    exc=[x['exclusion_id'] for x in excluded if x['file']==fn and x['line_start']==i and x['table_cell'] is not None and x['table_cell']['column_index']==k]
    cell_coverage.append({'file':fn,'line':i,'row_key_en':clean(cells[0]),'column_index':k,'column_header_en':header[k-1],'original_cell_en':cell,'status':'SCORED_SUBCLAIM' if matches else 'EXCLUDED_OR_CONTEXT','occurrence_ids':matches,'exclusion_ids':exc,'classification_reason_en':'The row/header provides inherited context; reference columns, unresolved terms, and non-assertions are not independently scored.' if not matches else 'An eligible commitment was extracted with its row and header context.'})
  elif line.strip() and not line.strip().startswith('|'):header=None

# Phase1 PDF exclusions preserved; newly generated exclusions appended in a stable combined exclusions ledger.
phase1_excs=[]
if (P1/'09_excluded_units.jsonl').exists():
 for l in (P1/'09_excluded_units.jsonl').read_text().splitlines():
  if l.strip():phase1_excs.append(json.loads(l))
write_jsonl(OUT/'09_excluded_units.jsonl',phase1_excs+excluded)
write_jsonl(OUT/'02_generated_atoms_final.jsonl',atoms)
write_jsonl(OUT/'02_generated_classes_final.jsonl',classes)
write_jsonl(OUT/'04_duplicate_classes_final.jsonl',[{**c,'duplicate_excess':c['occurrence_count']-1,'repeated':c['occurrence_count']>1,'cross_file_repeated':len(c['files'])>1,'representative_selection':'first in input order, then source line, then cell'} for c in classes])
write_jsonl(OUT/'02_generated_exclusions_final.jsonl',excluded)
write_jsonl(OUT/'02_generated_line_coverage_final.jsonl',coverage)
write_jsonl(OUT/'02_generated_table_cell_coverage_final.jsonl',cell_coverage)
write_jsonl(OUT/'02_reverse_lookup_index_final.jsonl',[{'lookup_key':k,'generated_class_ids':sorted(v),'count':len(v)} for k,v in sorted(reverse.items())])
write_jsonl(OUT/'02_duplicate_candidate_review_final.jsonl',candidate_pairs)

# Required partition: classify excess occurrence as within-file if any earlier occurrence same file, else across-file.
within=across=0;repeat_classes=0;cross_classes=0
for c in classes:
 if c['occurrence_count']>1:repeat_classes+=1
 if len(c['files'])>1:cross_classes+=1
 if c['occurrence_count']>1:
  seen=set()
  for o in c['occurrences']:
   if not seen:seen.add(o['file']);continue
   if o['file'] in seen:within+=1
   else:across+=1
   seen.add(o['file'])
assert within+across==len(atoms)-len(classes)
assert sum(c['occurrence_count'] for c in classes)==len(atoms)
assert len({a['generated_occurrence_id'] for a in atoms})==len(atoms)
assert len({c['generated_class_id'] for c in classes})==len(classes)
assert set(a['file'] for a in atoms).issubset(set(INPUTS))
assert len({x['file'] for x in coverage})==8
assert all(a['table_cell'] is None or a['table_cell']['column_header_en'] for a in atoms)
assert all(a['line_end']<=len((BASE/a['file']).read_text().splitlines()) for a in atoms)

per_file=[]
for f in files:
 fn=f['filename'];a=[x for x in atoms if x['file']==fn];e=[x for x in excluded if x['file']==fn];l=[x for x in coverage if x['file']==fn]
 per_file.append({**f,'eligible_occurrences':len(a),'excluded_segments':len(e),'inspected_physical_lines':len(l),'table_cells_inspected':len([x for x in cell_coverage if x['file']==fn]),'table_cells_with_eligible_occurrences':len([x for x in cell_coverage if x['file']==fn and x['status']=='SCORED_SUBCLAIM'])})
 assert len(l)==f['physical_lines']
summary={'phase':2,'protocol_version':'6.1','prefix':method,'method_label':'Unspecified single complete supplied eight-file set; no fullload/onelevel/twolevel method attribution inferred.','status':'PHASE_COMPLETED_BEST_EFFORT','source_positive_count_from_inherited_phase1':sum(1 for l in (OUT/'01_source_atoms_final.jsonl').open()),'source_negative_control_count_from_inherited_phase1':sum(1 for l in (OUT/'01_source_negative_controls_final.jsonl').open()),'scored_input_count':8,'generated_occurrences_GO_m':len(atoms),'generated_classes_G_m':len(classes),'duplicate_excess_occurrences':len(atoms)-len(classes),'duplicate_rate':(len(atoms)-len(classes))/len(atoms) if atoms else None,'within_file_excess':within,'across_file_excess':across,'repeated_classes':repeat_classes,'classes_spanning_files':cross_classes,'excluded_generated_segments':len(excluded),'generated_physical_lines_inspected':len(coverage),'generated_table_cells_inspected':len(cell_coverage),'potential_unmerged_paraphrase_pairs':len(candidate_pairs),'high_confidence_surface_equivalence_merges':fuzzy_merged,'per_file':per_file,'limitations_en':['An automated rule-based sentence/semicolon/table-cell pass cannot certify complete semantic atomicity or independently audit the predicates of every candidate occurrence.','Exact/near-exact normalized duplicates were merged conservatively; nonidentical paraphrases below a high confidence threshold were retained as separate classes. Candidate pairs are available for Phase 5 audit.','Code/diagrams, reference tables, unresolved decisions, and illustrative examples were not promoted to extra independent final commitments unless a clear binding assertion was present.','A source or generated assertion may be under-split, omitted, or mistakenly eligible. Counts are best-effort inventories, not validated coverage, precision, recall, F1, or certified duplication.','No Phase 3 source-to-generated judgments or later-phase scores were performed.']}
(OUT/'02_phase_status_final.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
report=f'''# Phase 2 — Generated-Corpus Atomic Occurrences and Raw Semantic Classes

**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** 6.1  
**Evaluated set:** One supplied complete eight-file set (`{method}`); the original user-provided file names are preserved and no generation-method label is inferred.  
**Shared Phase 1 inventory:** {summary['source_positive_count_from_inherited_phase1']} PDF-positive atoms and {summary['source_negative_control_count_from_inherited_phase1']} PDF-grounded negative controls, copied without modification. These were not read as sources of generated claims.

## Enumerated Phase 2 results

| Measure | Count |
|---|---:|
| Scored Markdown inputs inspected | 8 |
| Physical Markdown lines inspected | {len(coverage):,} |
| Nonempty Markdown table cells inspected | {len(cell_coverage):,} |
| Eligible generated claim occurrences (`GO_m`) | {len(atoms):,} |
| Raw generated semantic classes (`G_m`) | {len(classes):,} |
| Excess duplicate occurrences (`GO_m - G_m`) | {len(atoms)-len(classes):,} |
| Within-file excess | {within:,} |
| Across-file excess | {across:,} |
| Repeated raw classes | {repeat_classes:,} |
| Classes spanning multiple files | {cross_classes:,} |
| Generated exclusions / nondefinitive fragments | {len(excluded):,} |
| Potential semantic-paraphrase candidate pairs not merged | {len(candidate_pairs):,} |

**Provisional raw duplicate rate:** {summary['duplicate_rate']:.6f}, computed solely as `(GO_m - G_m) / GO_m`. This provisional figure is **not** the Phase 5 audited duplication metric.

## Input coverage

| Original scored file | Lines | Table cells | Eligible occurrences | Excluded fragments |
|---|---:|---:|---:|---:|
'''
for f in per_file:report+=f"| `{f['filename']}` | {f['physical_lines']} | {f['table_cells_inspected']} | {f['eligible_occurrences']} | {f['excluded_segments']} |\n"
report+='''
## Evidence, eligibility, and semantic grouping method

1. Retain the unchanged eight scored inputs. Scan every physical line and nonempty Markdown table cell, preserving original file names, line numbers, table row keys, column headings, and source quotations.
2. Form one candidate per conservative sentence/semicolon segment. Preserve shared section and table context and exact field/endpoint/status markers. The original cell is kept alongside the extracted segment to support review of under-splitting and scope.
3. Exclude citations, bare IDs, links, examples without adopted force, unresolved/TBD questions, unadopted alternatives, and purely structural headings. Retain every exclusion with its location, reason and covered text.
4. Group exact normalized predicates and only highly similar surface equivalents, while guarding endpoint method/path, literal errors, numeric constraints, actor labels and prohibition polarity. Preserve every raw occurrence ID exactly once in the class ledger.
5. Retain a reverse lookup index for methods/paths, field names, IDs, status codes and lexical features. Possible paraphrases not safely mergeable by this bounded procedure are separately enumerated, not silently forced into equivalence.

## Structural validation

- Eight distinct scored roles were present and readable, with no replacement of any original Markdown content.
- Every physical line has one line-coverage record. Every nonempty Markdown table body cell has one cell-coverage record, including reference/context-only cells.
- Every eligible `GEN-*` has an existing source file, physical line and table-cell context if applicable; every `GEN-*` belongs to exactly one `GCLASS-*`.
- The class occurrence-count sum equals `|GO_m|` and the duplicate partition sums to `|GO_m| - |G_m|`.
- The Phase 1 PDF-positive and negative-control ledgers are retained unchanged; generated files are not used as authority to add PDF requirements.

## Limitations, not deferred work in this phase

This is a **best-effort** eligible-claim inventory, not a verified independent semantic annotation of every predicate. Long clauses may contain multiple obligations; a context-dependent cell may be only partially independent; close paraphrases may remain separate; unresolved prose may contain eligible subclaims requiring further scrutiny. These material uncertainties are not hidden by arithmetic or source citations. Protocol Phase 5 is the designated correction/audit phase. Phase 3 was not started.
'''
(OUT/'02_generated_corpus_coverage_and_limitations.md').write_text(report,encoding='utf8')
print(json.dumps({'output_dir':str(OUT),'phase':2,'status':summary['status'],'GO':len(atoms),'GC':len(classes),'within':within,'across':across,'exclusions':len(excluded),'table_cells':len(cell_coverage),'candidate_pairs':len(candidate_pairs),'per_file':[{k:x[k] for k in ('filename','eligible_occurrences','physical_lines','table_cells_inspected')} for x in per_file]},indent=2))
