#!/usr/bin/env python3
"""Phase 2 best-effort evidence-preserving generated-claim extraction and raw class construction.
All output files are English; original input filenames and physical lines are retained.
"""
import collections, csv, hashlib, itertools, json, math, os, re, sys, unicodedata
from pathlib import Path
from difflib import SequenceMatcher

ROOT=Path('/mnt/data'); OUT=ROOT/'oriondesk_phase2'; OUT.mkdir(exist_ok=True)
FILES=[
 '01_screen_functions(3).md','02_api(3).md','03_data(3).md',
 '04_batch_functions(4).md','05_business_rules(3).md','06_exception_handling(4).md',
 '07_processing_flows(5).md','08_architecture_decision(3).md']
ID_RE=re.compile(r'\b(?:SCR(?:-COM|-X)?|API(?:-PROC|-COM|-GAP|-CASE|-EVID)?|DAT(?:-REL|-LC|-CODE|-FILE|-COM|-EVT)?|BAT(?:-OPS|-COM)?|BR|ERR(?:-OPS|-COM)?|FLOW(?:-TX|-COM)?|AD|AC-[A-Z]+|P-[A-Z]+|OQ-[A-Z]+|CON-[A-Z]+|TST|SEC|PDF)-\d{1,5}(?:-F\d+|-A\d+|-S\d+)?\b')
ENDPOINT_RE=re.compile(r'(?i)\b(?:GET|POST|PATCH|PUT|DELETE)\s+/(?:v1|internal)/[\w{}/.-]+')
EVENT_RE=re.compile(r'\b(?:CaseCreated|DocumentNormalized|AgentPlanApproved|WorkflowStageAdvanced|SearchIndexCommitted|ApprovalDecisionRecorded|TenantDeletionVerified|BaselineCommitted|UserReviewOpened|ModelInvocationCompleted|ConnectorSyncStarted|AccessDenied)\b')
LITERAL_RE=re.compile(r'\b(?:CASE_VERSION_CONFLICT|IDEMPOTENCY_CONFLICT|CONNECTOR_REAUTH_REQUIRED|NO_SUPPORTED_EVIDENCE|MODEL_OUTPUT_INVALID|AUTO_ALLOW|HUMAN_REVIEW|REQUEST_MORE_EVIDENCE|QUARANTINED|PUBLISHED|NEEDS_REVIEW|RESTRICTED|CONFIDENTIAL|INTERNAL|PUBLIC|NEW|TRIAGED|IN_PROGRESS|PENDING_APPROVAL|RESOLVED|CLOSED)\b')
CITE_RE=re.compile(r'\[(?:DDS|\w+\.md)\](?:\([^)]*\))?|\[DDS\],?[^.;|]*|\[\d+\]')
LINK_RE=re.compile(r'\[([^\]]+)\]\([^\)]*\)')
EMPH_RE=re.compile(r'(?<!\w)\*\*(.*?)\*\*')
REFERENCE_RE=re.compile(r'(?i)^(?:\*\*)?(?:Source|Sources|Earlier|Related|Reference|Cross-reference|Trace|Handoff status|Open|Previous|Status)\s*[:：]')
UNDECIDED_RE=re.compile(r'(?i)\b(?:needs confirmation|\bNC\b|\bTBD\b|not selected|not supplied|not confirmed|unresolved|unknown|undefined|to be decided|remains open|not established|unadopted proposal)\b')
PROPOSAL_RE=re.compile(r'(?i)(?:^|\s)(?:proposal|proposed|if approved|unadopted|illustration[- ]only|illustrated? only|reference example|fictional example|sample only)\b')
ACTION_RE=re.compile(r'(?i)\b(?:shall|must|require[sd]?|only|never|always|do not|does not|cannot|may not|no (?:unauthorized|unapproved|implicit|arbitrary)|return[s]?|reject[s]?|enforce[s]?|preserve[s]?|prevent[s]?|validate[sd]?|use[s]?|allow[s]?|apply|applies|record[s]?|store[s]?|persist[s]?|retain[s]?|create[s]?|update[s]?|display[s]?|show[s]?|handle[s]?|contain[s]?|include[s]?|bind[s]?|scope[d]?|compute[s]?|derive[s]?|support[s]?|produce[s]?|send[s]?|scan[s]?|read[s]?|write[s]?|publish(?:es)?|advance[s]?|block[s]?|deny|restrict[s]?|route[s]?|check[s]?|audit[s]?|point[s]?|map[s]?|track[s]?|filter[s]?|protect[s]?|set[s]?|generate[s]?|open[s]?|trigger[s]?|invoke[s]?|satisfy|commit[s]?|synchronize[s]?|replay[s]?|expire[s]?|timeout[s]?|terminate[s]?|report[s]?|verify|immutable|idempotent|atomic|authoritative|confirmed|out of scope|deferred|equal|before|after|without|within|forbidden|prohibited|not permitted)\b')
CROSS_REF_ONLY=re.compile(r'^\s*(?:(?:[A-Z]{2,}[-/0-9A-Z]+|OQ-[\w/-]+|CON-[\w/-]+|AD-[\w/-]+)(?:[,;/\s]|$))+\s*$')
META_COLUMNS=re.compile(r'(?i)(?:^|\b)(source|sources|citation|evidence|earlier|related|notes? and source|source pages|reference|open question|unresolved|gap id|item id|identifier|status|proposal status|handoff|links? to|consolidated items|cross[- ]reference|scope and source)\b')
IDENTITY_COLUMNS=re.compile(r'(?i)^(?:requirement id|id|rule id|data id|flow id|job id|exception id|api id|field id|item id|boundary id|term|profile|category|code|source term|actor|field|name)$')
DERIVED_STATUSES={'CONFIRMED','NC','TBD','NEEDS CONFIRMATION','PROPOSAL','RESOLVED','D','I','C','E','P','T'}
BANNED_SECTIONS=re.compile(r'(?i)^(?:open[- ]decision register|open questions|unresolved items|conflicts and required amendments|appendix .*open|proposal inventory|traceability indexes|traceability matrices|traceability table|decision register|handoff trace|open decision cross-reference)')
UNAPPROVED_PHRASES=re.compile(r'(?i)\b(?:recommend(?:ed)?|suggest(?:ed)?|proposal|proposed|option(?:al)?\s+if\s+approved|unadopted|not approved|illustrat(?:ed|ive) only)\b')


def clean(s):
 s=LINK_RE.sub(r'\1', s);s=s.replace('**','').replace('`','').replace('\\|','|')
 s=re.sub(r'<a\s+id="[^"]+"\s*></a>', '',s)
 s=re.sub(r'\[DDS\](?:,?\s*pp?\.[^.;|]*)?', '',s)
 s=re.sub(r'(?i)\s*\[DDS\]\s*', ' ',s)
 s=re.sub(r'\s+', ' ',s).strip(' \t—|')
 return s

def ismeta(s):
 st=clean(s)
 if not st: return True
 if re.match(r'^\[.+\]:\s*',s):return True
 if REFERENCE_RE.match(s.strip()):return True
 if st.lower().startswith(('source:', 'sources:', 'source ', 'sources ', 'source document:', 'source baseline:', 'scope:', 'earlier:', 'open:', 'related:', 'reference:','needs confirmation —','proposal —','no choice of','there is no confirmed')):return True
 if re.fullmatch(r'\w{1,15}\s*[-–]+\s*\w{1,20}', st) and not re.search(r'\s',st): return True
 if CROSS_REF_ONLY.match(st):return True
 return False

def split_cells(line):
 # Pipes escaped by backslash are preserved.
 s=line.strip(); s=s[1:] if s.startswith('|') else s; s=s[:-1] if s.endswith('|') else s
 cells=re.split(r'(?<!\\)\|',s)
 return [c.strip() for c in cells]

def is_separator(cells): return bool(cells) and all(re.fullmatch(r':?-{3,}:?',c.strip()) for c in cells)

def split_assertions(text):
 """Conservative split at independent sentences and semicolon clauses only."""
 # avoid splitting versions and decimal values; split at . following lowercase etc.
 s=clean(text);s=re.sub(r'\s*<br\s*/?>\s*','; ',s)
 if len(s)<2:return []
 pieces=re.split(r'(?<=\w)[.;](?:\s+)(?=[A-Z`0-9]|No\s|Do\s|If\s|The\s|Every\s)',s)
 out=[]
 for p in pieces:
  # A semicolon separates independently testable obligations in many summary tables.
  if len(p)>100 and ';' in p:
   sub=re.split(r';\s*(?=[A-Za-z0-9`])',p)
  else: sub=[p]
  out.extend(x.strip(' -.;') for x in sub if x.strip(' -.;'))
 return out

def normalize(s):
 s=clean(s).lower();s=unicodedata.normalize('NFKC',s)
 s=re.sub(r'\b(?:shall|must)\b',' ',s)
 s=re.sub(r'\b(?:a|an|the)\b',' ',s)
 s=re.sub(r'\b(?:confirm(?:ed)?|is supported|source[- ]confirmed)\b',' ',s)
 s=s.replace('must not','not').replace('shall not','not').replace('do not','not').replace('does not','not').replace('cannot','not')
 s=re.sub(r'\b(?:is|are|be|to|that|which)\b',' ',s)
 s=re.sub(r'[^a-z0-9_/{}.+%:-]+',' ',s)
 s=re.sub(r'\s+',' ',s).strip();return s

def anchor_of(s,scope='',row_id=''):
 # Canonical targets are preferred over local document-specific assigned IDs.
 e=ENDPOINT_RE.search(s)
 if e: return 'endpoint:'+e.group(0).lower()
 ev=EVENT_RE.search(s)
 if ev:return 'event:'+ev.group(0).lower()
 lit=LITERAL_RE.search(s)
 if lit and len(s)<110:return 'literal:'+lit.group(0).lower()
 c=re.search(r'(?i)\b(?:case|document|workspace|tenant|source|evidence|approval|review|run|model|connector|cache|audit|token|evaluation|index|retention|export|deletion|policy|object|tool|worker|SSE|UI|API|batch|event|RLS|ACL)s?\b',s)
 if c:return 'domain:'+c.group(0).lower()
 if row_id:return 'row:'+row_id.upper()
 return 'scope:'+normalize(scope)[:90]

def table_claim(row,head,ci,raw,anchor,title,section):
 h=head[ci] if ci<len(head) else f'column_{ci+1}'
 hc=clean(h); x=clean(raw); rowlabel=clean(row[0]) if row else ''
 if len(row)>1 and len(rowlabel)<4: rowlabel+=' '+clean(row[1])[:100]
 if not x or x.upper() in DERIVED_STATUSES or x in ['—','-','None','n/a','NC.']:return None,'EMPTY_OR_STATUS_ONLY'
 if re.fullmatch(r'\*?\*?[*: -]*',x):return None,'FORMAT_ONLY'
 if re.fullmatch(r'[\d,]+',x) and not re.search(r'(status|result|limit|cap|count|value|response)',hc,re.I):return None,'BARE_NUMBER'
 if (META_COLUMNS.search(hc) and not re.search(r'(?i)^(?:confirmed|normative|required) (?:behavior|result|constraint)',hc)) or re.search(r'(?i)^(?:cross.layer mapping|related contracts|enforcing screens/actions|source and link|source evidence|referenced .*ids|needs confirmation|unresolved .*contract|open contract|impact and pending confirmation|consolidated items|previous mapping|earlier mapping|status and source|pending question|open decision|historical mapping)$',hc):return None,'METADATA_OR_CROSS_REFERENCE_COLUMN'
 if ci==0 and len(row)>1:return None,'ROW_KEY_CONTEXT_ONLY'
 if re.search(r'(?i)^(?:Related contracts|Earlier trace|References|Status and source|Open question|Missing interface|Remaining contract gap|Open contract|Adjacent open decision)$',clean(row[0])):return None,'REFERENCE_OR_GAP_ROW'
 if re.search(r'(?i)^(?:document id|source document|source baseline|source character|specification file|specification basis|scope|identifier convention|identifier preservation|citation convention|previous specifications|completed preceding specifications|source file|source|design baseline|protocol version|status and source|reference|methodology|applicable version|previous specification|baseline|previous stage)$',clean(row[0])):return None,'DOCUMENT_METADATA_ROW'
 if IDENTITY_COLUMNS.match(hc):return None,'ROW_IDENTIFIER_OR_LABEL'
 if ismeta(x):return None,'REFERENCE_ONLY'
 if re.search(r'(?i)^(?:needs confirmation|proposal|TBD|unadopted|not confirmed|not specified|not established|not supplied|undefined|unresolved)',x):return None,'UNADOPTED_OR_OPEN'
 if re.search(r'(?i)^\*?\*?(?:illustration|proposal|NC)\b',raw.strip()):return None,'ILLUSTRATED_OR_UNDECIDED'
 if re.search(r'(?i)\b(?:remains (?:unresolved|NC|TBD)|contract NC|not supplied|exact .* unresolved)\b',x) and not re.search(r'(?i)\b(?:must|never|do not|only if|confirmed|required|cannot)\b',x): return None,'UNRESOLVED_CONTRACT'
 if re.search(r'(?i)(?:\bproposal\b|\bnot approved\b)',x) and not re.search(r'(?i)^(?:Confirmed|Mandatory)\b',x):return None,'UNADOPTED_PROPOSAL'
 # For identity fields in field-definition tables, permit substantive types and validity constraints in typed columns.
 short=re.fullmatch(r'(?:\d{3}|\d+(?:\.\d+)?\s*(?:MB|days?|hours?|minutes?)|(?:GET|POST|PATCH|PUT|DELETE) /[\w/{}/.-]+|[A-Z_]{4,50}|UUID|UUIDv7|BIGINT|TEXT|TIMESTAMPTZ)',x)
 if len(x)<18 and not ACTION_RE.search(x) and not short:return None,'UNSUPPORTED_SHORT_CELL'
 if short and re.match(r'(?i)^(?:confirmed result|result|success(?:ful)? response|method|method and path|method/path|type|value|response|http status|code|constraint)',hc): pass
 elif not ACTION_RE.search(x) and len(x)<26:return None,'NONASSERTIVE_CELL'
 prefix=(rowlabel[:145]+' — ') if rowlabel else ''
 # Make table context explicit. The cell evidence remains the original quoted text.
 st=f'{prefix}{hc}: {x}'
 return st, None

def row_id_from(row):
 for c in row[:3]:
  m=ID_RE.search(clean(c))
  if m:return m.group(0)
 return ''

occ=[]; exclusions=[]; coverage=[]; cellcoverage=[]; stats={}; inputhash={}; flagged=[]
for fidx,f in enumerate(FILES):
 p=ROOT/f;rawbytes=p.read_bytes();inputhash[f]=hashlib.sha256(rawbytes).hexdigest()
 lines=p.read_text(encoding='utf-8-sig').splitlines()
 headingstack=[];tableheaders=None; tabletitle='';table_count=0;code=False;code_lang='';section_substantive=0
 filecnt=collections.Counter()
 def add(text,quote,kind,start,end,cell=None,header='',row='',title='',context='',row_id='',code_mark=''):
  global occ
  if not clean(text):return None
  stmt=clean(text)
  stmt=re.sub(r'^(?:Confirmed\s*[:.]\s*)','',stmt,flags=re.I)
  if len(stmt)<8:return None
  target=anchor_of(stmt,context,row_id)
  rid=ID_RE.findall(stmt)
  rec={
   'occurrence_id':f'GEN-{len(occ)+1:05d}', 'method':'fullload',
   'atomic_statement_en':stmt,'quote_en':quote.strip(),
   'evidence':{'file':f,'line_start':start,'line_end':end,'table_cell':cell,
       'column_header':header or None,'row_key':row or None,'table_title':title or None,'heading_context':context or None,'quote_en':quote.strip()},
   'source_file':f,'line_start':start,'line_end':end,'table_cell':cell,
   'column_header':header or None,'row_key':row or None,
   'heading_context':context,'claim_origin_kind':kind,
   'target_key':target,'identifier_keys':list(dict.fromkeys(rid)),
   'endpoint_keys':list(dict.fromkeys(ENDPOINT_RE.findall(stmt))),
   'event_keys':list(dict.fromkeys(EVENT_RE.findall(stmt))),
   'literal_keys':list(dict.fromkeys(LITERAL_RE.findall(stmt))),
   'content_key':normalize(stmt),'eligibility':'DEFINITIVE_BEST_EFFORT',
   'source_validation':'NOT_YET_PERFORMED_PHASE_2'
  }
  occ.append(rec);filecnt['claims']+=1
  return rec['occurrence_id']
 def exclude(start,end,kind,quote,why,cell=None,head=None):
  rr={'file':f,'line_start':start,'line_end':end,'table_cell':cell,'column_header':head,'content_kind':kind,'quote_en':quote.strip(),'exclusion_reason':why}
  exclusions.append(rr);filecnt['exclusions']+=1
 def current_ctx():return ' > '.join(h for _,h in headingstack)
 for i,line in enumerate(lines,1):
  s=line.strip();kind='prose'; ids=[];seen_cells=0
  if not s: kind='blank';coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':[],'status':'STRUCTURAL_BLANK'});continue
  if re.fullmatch(r'\s*\|?\s*(?::?-{3,}:?\s*\|\s*)+\s*',s):
   kind='table_separator';coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':[],'status':'STRUCTURAL_SEPARATOR'});continue
  if s.startswith('```'):
   kind='code_fence';code=not code;code_lang=s.strip('`').strip() if code else ''
   coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':[],'status':'STRUCTURAL_CODE_FENCE'});continue
  if code:
   kind='code';stmt=clean(s)
   # source-confirmed SQL DDL and examples; no automatic inference that snippets are full production schemas
   if not re.search(r'(?i)(?:proposed partial json mappings|unadopted|proposal)',current_ctx()) and not re.search(r'(?i)(?:needs confirmation|<case-create body)',stmt) and code_lang in {'sql','http','json','yaml','yml','protobuf','typescript','python','bash','text'} and len(stmt)>5 and re.search(r'(?i)\b(?:CREATE|ALTER|CHECK|POLICY|NOT NULL|DEFAULT|PRIMARY KEY|UNIQUE|REFERENCES|HTTP/1.1|"[a-z_]+"\s*:|(?:GET|POST|PATCH|PUT|DELETE) /)',stmt):
    rid=add('Reference contract syntax — '+stmt,s,'CONFIRMED_REFERENCE_CODE',i,i,context=current_ctx(),code_mark=code_lang)
    if rid:ids.append(rid)
   if not ids:exclude(i,i,'code',s,'NON-NORMATIVE_OR_CONTEXTUAL_CODE')
   coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':ids,'status':'ELIGIBLE' if ids else 'EXCLUDED'});continue
  if s.startswith('#'):
   kind='heading'; hlevel=len(s)-len(s.lstrip('#')); htxt=clean(s[hlevel:]);
   headingstack=[x for x in headingstack if x[0]<hlevel]+[(hlevel,htxt)]
   tableheaders=None;tabletitle=''
   exclude(i,i,'heading',s,'STRUCTURAL_HEADING_CONTEXT')
   coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':[],'status':'CONTEXT_ONLY'});continue
  ctx=current_ctx(); in_open=bool(re.search(r'(?i)(?:open[- ]decision register|open questions|unresolved items|traceability|cross reference|proposal|conflicts and required amendments)',ctx))
  if s.startswith('|'):
   kind='table';row=split_cells(s)
   if is_separator(row):
    coverage.append({'file':f,'line':i,'kind':'table_separator','claim_ids':[],'status':'STRUCTURAL_SEPARATOR'});continue
   if (i<len(lines) and lines[i].lstrip().startswith('|') and is_separator(split_cells(lines[i]))):
    tableheaders=[clean(x) for x in row];tabletitle=ctx;table_count+=1
    for ci,x in enumerate(row):cellcoverage.append({'file':f,'line':i,'cell':ci+1,'column_header':clean(x),'status':'TABLE_HEADER'})
    coverage.append({'file':f,'line':i,'kind':'table_header','claim_ids':[],'status':'CONTEXT_ONLY'});continue
   if not tableheaders:
    # malformed or layout-independent table; retain row context
    tableheaders=[f'Column {j+1}' for j in range(len(row))];tabletitle=ctx
   rid=row_id_from(row)
   idsource=clean(row[0]) if row else '';mark_rows=[]
   for ci,x in enumerate(row):
    h=tableheaders[ci] if ci<len(tableheaders) else f'Column {ci+1}'
    cell_status='EXCLUDED';reasons=[];cellids=[]
    if in_open or (f.startswith('08_') and re.search(r'(?i)(?:items resolved by the specifications|cross-specification conflicts|consistency and open questions|missing evidence and required|confirmation order implied|resolved documentation|documentation handoff|conflicts and|source conflicts|traceability|earlier|open question|unresolved)',tabletitle)) or re.search(r'(?i)(?:open[- ]decision register|unresolved|traceability|conflict trace|specification basis|specification status|status definitions|documentation handoffs|resolved documentation handoffs|appendix note|earlier-to-later mapping)',tabletitle):
     reason='UNDECIDED_OR_CROSS_REFERENCE_TABLE'
    elif re.search(r'(?i)^\s*(?:OQ-|CON-|P-|API-GAP-|AD-R|CF-)',clean(row[0])) and not re.search(r'(?i)confirmed',h):
     reason='UNAPPROVED_ID_ROW'
    else:
     candidate,reason=table_claim(row,tableheaders,ci,x,rid,tabletitle,ctx)
     if candidate:
      # Split row cell independently; preserve inherited context for each fragment.
      xp=clean(x);parts=split_assertions(xp)
      if len(parts)==1:parts=[xp]
      for part in parts:
       # In a cell, retain complete scope of ID + header, not just the fragment.
       if re.search(r'(?i)^(?:Needs confirmation|NC|TBD|Proposal|Unadopted|not selected|not supplied|unknown|undefined)\b',part):continue
       if len(part)<7 or re.fullmatch(r'\[DDS\].*',part):continue
       if re.search(r'(?i)^(?:not supplied|not specified|not confirmed|unknown|undefined|unresolved|none defined|no complete|exact .* (?:NC|unknown|undefined|unresolved))\b',part) and not re.search(r'(?i)\b(?:must|never|shall|cannot|do not|not permitted)\b',part):continue
       if re.search(r'(?i)\b(?:\bNC\b|needs confirmation|unresolved|not supplied|not confirmed|undefined)\b',part) and not re.search(r'(?i)\b(?:must|shall|only|never|cannot|do not|prohibited|required|enforced)\b',part):continue
       # first column may be a textual condition (e.g. state), and cell > 1 result holds contract
       stmt=f'{clean(row[0])[:150]} — {h}: {part}' if clean(row[0]) else f'{h}: {part}'
       newid=add(stmt,x,'TABLE_CELL_CONTRACT',i,i,cell=f'R{i}C{ci+1}',header=h,row=idsource,title=tabletitle,context=ctx,row_id=rid)
       if newid:cellids.append(newid)
      if cellids:cell_status='ELIGIBLE';reason=''
      else:reason='NO_INDEPENDENT_DEFINITIVE_CLAUSE'
    if not cellids:
     exclude(i,i,'table_cell',x,reason or 'NOT_DEFINITIVE',f'R{i}C{ci+1}',h)
    ids.extend(cellids)
    cellcoverage.append({'file':f,'line':i,'cell':ci+1,'column_header':h,'status':cell_status,'claim_ids':cellids,'reason':reason})
   coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':ids,'status':'ELIGIBLE' if ids else 'EXCLUDED'});continue
  # prose / paragraph / list / bold labels.
  if re.match(r'(?:\d+\.|[-*+]\s|>\s)',s):kind='list'
  if s.startswith('**'):kind='bold_or_prose'
  if re.match(r'^\[.+\]:',s):
   exclude(i,i,kind,s,'REFERENCE_DEFINITION');coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':[],'status':'EXCLUDED'});continue
  if re.search(r'(?i)(?:specification basis and status|document control and source metadata|traceability cross[- ]reference|resolved documentation handoffs)',ctx) and not re.search(r'(?i)(?:must|never|do not|required|shall)',s):
   exclude(i,i,kind,s,'SPECIFICATION_METADATA_CONTEXT');coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':[],'status':'EXCLUDED'});continue
  if ismeta(s):
   exclude(i,i,kind,s,'CITATION_OR_META');coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':[],'status':'EXCLUDED'});continue
  if re.match(r'(?i)^\s*(?:\*\*)?(?:Needs confirmation|Proposal|Unadopted proposal|Open question|Open contracts|Proposal Status|Handoff status)',s):
   exclude(i,i,kind,s,'UNDECIDED_OR_UNADOPTED');coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':[],'status':'EXCLUDED'});continue
  if f.startswith('08_') and re.search(r'(?i)(?:Items Resolved by the Specifications|Cross-Specification Conflicts and Pending Decisions|Consistency and Open Questions|Missing Evidence and Required Confirmation Material|Confirmation Order Implied by Dependencies)',ctx):
   exclude(i,i,kind,s,'DOCUMENTATION_OR_PENDING_DECISION_METADATA');coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':[],'status':'EXCLUDED'});continue
  if in_open and not re.search(r'(?i)\b(?:must|confirmed|never|do not|shall|required)\b',s):
   exclude(i,i,kind,s,'OPEN_DECISION_CONTEXT');coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':[],'status':'EXCLUDED'});continue
  original=s
  # leave inline word "proposal" only if separable confirmed constraint; do not score proposal itself
  s=re.sub(r'^(?:\d+\.\s*|[-*+]\s+|>\s*)','',s)
  s=re.sub(r'\*\*(?:Confirmed|Supported|Required|Mandatory)\s*[:.]?\*\*\s*','',s,flags=re.I)
  # Entirely contextual section label / paragraph
  parts=split_assertions(s)
  for part in parts:
   if len(part)<10 or ismeta(part):continue
   if PROPOSAL_RE.match(part) or re.search(r'(?i)^\s*\*?\*?Proposal\b',part):continue
   if re.search(r'(?i)^(?:Needs confirmation|NC|TBD|Not confirmed|Not defined|Whether|Which|What exact|What |The following statuses|The inventory uses|The file is|This register consolidates|The source document|This file documents|It does not inspect|Broad questions can|The traceability tables|The following constraints are|No confirmed|No exact|No complete|No numeric|The row|This section|The mapping|The next sections)\b',part) and not re.search(r'(?i)\b(?:must|shall|never|do not|cannot)\b',part):continue
   if '→' in part and len(part)<70 and not ACTION_RE.search(part):continue
   if not ACTION_RE.search(part) and len(part)<95:continue
   if re.search(r'(?i)^(?:The source does not|No (?:confirmed|exact|complete|numeric)|Whether|No supplied|\d+\s+identified)',part) and not re.search(r'(?i)\b(?:must|do not|cannot|never|required)\b',part):continue
   if re.match(r'(?i)^\s*(?:OQ-|CON-|AC-|AD-)',part) and not ACTION_RE.search(part):continue
   if re.match(r'(?i)^(?:SCR|API|DAT|BAT|BR|ERR|FLOW)-[A-Z0-9-]+\s+[—-]\s+[^.]{0,90}$',part) and ('. ' in s or ';' in s):continue
   st=clean(part)
   if len(st)<12:continue
   rid=add(st,original,kind.upper(),i,i,context=ctx)
   if rid:ids.append(rid)
  if not ids:exclude(i,i,kind,original,'NONDEFINITIVE_CONTEXT_OR_META')
  coverage.append({'file':f,'line':i,'kind':kind,'claim_ids':ids,'status':'ELIGIBLE' if ids else 'EXCLUDED'})
 filecnt['lines']=len(lines);filecnt['table_cells']=sum(1 for x in cellcoverage if x['file']==f)
 filecnt['table_cells_eligible']=sum(1 for x in cellcoverage if x['file']==f and x['status']=='ELIGIBLE')
 filecnt['substantive_lines']=sum(1 for x in coverage if x['file']==f and x['kind'] not in ('blank','table_separator','table_header','heading','code_fence'))
 filecnt['lines_with_claims']=sum(1 for x in coverage if x['file']==f and x['claim_ids'])
 filecnt['heading_lines']=sum(1 for x in coverage if x['file']==f and x['kind']=='heading')
 filecnt['table_header_lines']=sum(1 for x in coverage if x['file']==f and x['kind']=='table_header')
 filecnt['excluded_substantive_lines']=sum(1 for x in coverage if x['file']==f and x['kind'] not in ('blank','table_separator','table_header','heading','code_fence') and not x['claim_ids'])
 stats[f]=dict(filecnt)

# Classing: conservative full-predicate identity. No evidence-free similarity-based merging.
# 1) exact normalized substantive commitment; class scope is attached when no standalone target.
# 2) For field/type/permission/status, different row identities remain separate unless exact target is identical.
# 3) Numeric/error/method/path and distinct actor/target qualifiers can never be discarded.

def self_contained_core(o):
 """Canonical full predicate after stripping purely editorial table labels.
 Required to contain an explicit natural-language target; deictic clauses are excluded.
 """
 if o['claim_origin_kind'] != 'TABLE_CELL_CONTRACT': return None
 st=o['atomic_statement_en']; m=re.search(r' — [^:]{3,85}: ',st)
 if not m: return None
 body=st[m.end():].strip()
 if len(body)<49 or len(body.split())<7:return None
 if re.match(r'(?i)^(?:it|they|this|these|those|as above|same|current|selected|existing|per|where applicable|only if|not automatically)',body):return None
 if re.search(r'(?i)\b(?:the following|these|such|its|those|that |the above|the source|the row|the field|here|there)\b',body):return None
 if not re.search(r'(?i)\b(?:case|run|document|source|tenant|workspace|retrieval|model|evidence|index|cache|approval|review|policy|audit|user|data|object|token|api|endpoint|operation|event|outbox|actor|file|prompt|provider|generator|agent|connector|state|tool|submission|response|publication|transaction|execution|request|workflow|claim|control|access|read|write|verification|security)\b',body):return None
 if not ACTION_RE.search(body):return None
 return normalize(body)

def class_key(o):
 s=o['content_key']; x=o['atomic_statement_en']; h=o.get('column_header') or ''
 e=ENDPOINT_RE.search(x)
 if e:return ('endpoint:'+e.group(0).lower(),s)
 rowid=o.get('row_key') or '';m=ID_RE.search(rowid)
 if m and re.search(r'(?i)(?:^|\b)(?:type|length|default|required|not null|field|status|constraint|actor|role|result|source|action|trigger|method|success)\b',h):return (m.group(0).lower(),s)
 return ('generic',s)

classes=[];keymap={}; ids_by_class=collections.defaultdict(list)
for o in occ:
 key=class_key(o)
 # Real exact duplicate of normalized full predicate only; conservative avoids merges across different target identifiers.
 if key not in keymap:
  k=f'GCLASS-{len(classes)+1:05d}';keymap[key]=k
  classes.append({'class_id':k,'method':'fullload','canonical_statement_en':o['atomic_statement_en'],
   'normalized_full_predicate':o['content_key'],'target_key':o['target_key'],'occurrence_ids':[],
   'representative_evidence':o['evidence'],'merge_policy':'EXACT_NORMALIZED_FULL_PREDICATE_OR_SELF_CONTAINED_TABLE_PREDICATE_WITH_TARGET_GUARDS',
   'phase2_validity':'UNASSESSED_PDF_ENTAILMENT','semantic_review_status':'CONSERVATIVE_EXACT_ONLY'})
 k=keymap[key];o['class_id']=k;ids_by_class[k].append(o['occurrence_id'])
for c in classes:c['occurrence_ids']=ids_by_class[c['class_id']];c['occurrence_count']=len(c['occurrence_ids'])

# Secondary semantic normalization can merge self-contained identical duties across editorial headings,
# without sacrificing the primary exact-full-predicate groups.
parent={c['class_id']:c['class_id'] for c in classes}
def find_root(z):
 while parent[z]!=z:
  parent[z]=parent[parent[z]];z=parent[z]
 return z
def union(a,b):
 a=find_root(a);b=find_root(b)
 if a!=b:parent[b]=a
seencore={}
for o in occ:
 core=self_contained_core(o)
 if not core:continue
 k=('self_contained_explicit_predicate',core)
 if k in seencore:union(seencore[k],o['class_id'])
 else:seencore[k]=o['class_id']
if any(find_root(k)!=k for k in list(parent)):
 by_old={c['class_id']:c for c in classes}
 canonical_roots={};next_classes=[];new_members=collections.defaultdict(list)
 for o in occ:
  root=find_root(o['class_id'])
  if root not in canonical_roots:
   new_id=f'GCLASS-{len(canonical_roots)+1:05d}'
   canonical_roots[root]=new_id
   template=dict(by_old[root]);template['class_id']=new_id
   next_classes.append(template)
  o['class_id']=canonical_roots[root]
  new_members[o['class_id']].append(o['occurrence_id'])
 classes=next_classes
 for c in classes:
  c['occurrence_ids']=new_members[c['class_id']];c['occurrence_count']=len(c['occurrence_ids'])


# Diagnostic candidates: near-duplicate probable merges for phase 5, not merged automatically.
# TF-IDF localized nearest neighbors; cap computation and only flag plausible near duplicate cases.
try:
 from sklearn.feature_extraction.text import TfidfVectorizer
 from sklearn.neighbors import NearestNeighbors
 texts=[c['normalized_full_predicate'] for c in classes]; n=len(texts)
 if n>0:
  tfidf=TfidfVectorizer(analyzer='char',ngram_range=(3,5), min_df=2, sublinear_tf=True, dtype='float32').fit_transform(texts)
  model=NearestNeighbors(n_neighbors=min(n,4),metric='cosine',algorithm='brute').fit(tfidf)
  dist,ix=model.kneighbors(tfidf)
  for i in range(n):
   for d,j in zip(dist[i,1:],ix[i,1:]):
    if int(j)<=i:continue
    sim=1-float(d)
    if sim < .88:continue
    x=classes[i];y=classes[int(j)]
    if x['target_key'].startswith('endpoint:') and x['target_key'] != y['target_key']:continue
    if re.search(r'(?:\b201\b|\b202\b|\b409\b|\b422\b|\b429\b|\b404\b)',x['canonical_statement_en']) != re.search(r'(?:\b201\b|\b202\b|\b409\b|\b422\b|\b429\b|\b404\b)',y['canonical_statement_en']):continue
    flagged.append({'class_id_1':x['class_id'],'class_id_2':y['class_id'],'char_similarity':round(sim,4),
       'statement_1_en':x['canonical_statement_en'],'statement_2_en':y['canonical_statement_en'],
       'review_reason':'Possible meaning-preserving paraphrase; not automatically merged because full scope, actor, condition, exception, and outcome have not been independently proven equivalent.'})
except Exception as e:
 flagged=[{'diagnostic_error':str(e)}]

# Raw repeated classes split by within/across first representative definition.
by_id={x['occurrence_id']:x for x in occ};dup=[];within=across=0;multi=0
for c in classes:
 members=[by_id[k] for k in c['occurrence_ids']]
 # Sorted by source file role, physical line, and table cell order.
 members.sort(key=lambda x:(FILES.index(x['source_file']),x['line_start'],int((x.get('table_cell') or 'R0C0').split('C')[-1])))
 rep=members[0];seen_files={rep['source_file']};per_occ=[];within_local=across_local=0
 for m in members:
  if m is rep:role='representative'
  elif m['source_file'] in seen_files:role='within_file_excess';within+=1;within_local+=1
  else:role='across_file_excess';across+=1;across_local+=1
  seen_files.add(m['source_file'])
  per_occ.append({'occurrence_id':m['occurrence_id'],'source_file':m['source_file'],'line':m['line_start'],'cell':m.get('table_cell'),'duplicate_role':role})
 if len(seen_files)>1:multi+=1
 dup.append({'class_id':c['class_id'],'canonical_statement_en':c['canonical_statement_en'],
   'occurrence_count':len(members),'occurrence_ids':[z['occurrence_id'] for z in members],
   'representative_occurrence_id':rep['occurrence_id'],'representative_evidence':rep['evidence'],
   'within_file_excess':within_local,'across_file_excess':across_local,
   'spans_multiple_files':len(seen_files)>1,'occurrence_roles':per_occ,
   'merge_split_reason_en':'Merged exact full-predicate or explicitly self-contained table obligations only where endpoint/field scope guards permitted. Similar but not demonstrably identical modality, scope, actor, condition or outcome remain separate.'})

# Generated retrieval keys: exact identifier -> occurrences, endpoint, events, literals, plus rare word inverted index.
lookups=collections.defaultdict(set)
for o in occ:
 for k in o['identifier_keys']:lookups['id:'+k.lower()].add(o['occurrence_id'])
 for k in o['endpoint_keys']:lookups['endpoint:'+k.lower()].add(o['occurrence_id'])
 for k in o['event_keys']:lookups['event:'+k.lower()].add(o['occurrence_id'])
 for k in o['literal_keys']:lookups['literal:'+k.lower()].add(o['occurrence_id'])
 for tok in set(re.findall(r'[a-z][a-z0-9_]{3,}',o['content_key'])):
  lookups['word:'+tok].add(o['occurrence_id'])


def dumpjsonl(filename,items):
 with (OUT/filename).open('w',encoding='utf-8') as fd:
  for o in items: fd.write(json.dumps(o,ensure_ascii=False,sort_keys=False)+'\n')
dumpjsonl('02_generated_atoms_final.jsonl',occ)
dumpjsonl('02_generated_classes_final.jsonl',classes)
dumpjsonl('04_duplicate_classes_final.jsonl',dup)
dumpjsonl('02_generated_exclusions_final.jsonl',exclusions)
dumpjsonl('02_generated_line_coverage_final.jsonl',coverage)
dumpjsonl('02_generated_table_cell_coverage_final.jsonl',cellcoverage)
dumpjsonl('02_possible_semantic_merge_review.jsonl',flagged)
dumpjsonl('02_generated_lookup_keys_final.jsonl',({'key':key,'occurrence_ids':sorted(v,key=lambda x:int(x.split('-')[1]))} for key,v in sorted(lookups.items())))
summary={
 'protocol_version':'6.1','phase':2,'status':'PHASE_COMPLETED_BEST_EFFORT',
 'method_label':'fullload','method_label_basis':'Single complete eight-role supplied corpus; user requested fullload_cal source inventory reuse. No claim of independent generation-method metadata verification.',
 'scope':'Eight scored Markdown specification inputs only; PDF and protocol are not generated-input files.',
 'input_files':[{'file':f,'sha256':inputhash[f],**stats[f]} for f in FILES],
 'eligible_generated_occurrences':len(occ),'raw_generated_semantic_classes':len(classes),
 'duplicate_excess_occurrences':len(occ)-len(classes),'duplicate_rate_provisional':(len(occ)-len(classes))/len(occ) if occ else None,
 'within_file_excess':within,'across_file_excess':across,
 'repeated_claim_class_count':sum(len(c['occurrence_ids'])>1 for c in classes),
 'repeated_classes_spanning_multiple_files':multi,
 'near_duplicate_classes_flagged_for_later_semantic_review':len(flagged),
 'exclusion_records':len(exclusions),'line_coverage_records':len(coverage),
 'table_cell_coverage_records':len(cellcoverage),
 'table_cells_with_eligible_assertions':sum(r['status']=='ELIGIBLE' for r in cellcoverage),
 'assertions_from_markdown_tables':sum(x['claim_origin_kind']=='TABLE_CELL_CONTRACT' for x in occ),
 'assertions_from_prose_or_lists':sum(x['claim_origin_kind'] not in ('TABLE_CELL_CONTRACT','CONFIRMED_REFERENCE_CODE') for x in occ),
 'confirmations_performed':['All eight actual input files read as UTF-8','Every physical line classified and indexed','Every Markdown table cell has an independent status record','Every eligible occurrence belongs to exactly one generated raw class','Every occurrence/class has original filename and physical line evidence','No source PDF TP/TN/FP/FN metrics generated'],
 'limitations_en':["The role-matched corpus lacks a generation-method tag; fullload is used as this run's method identifier, not independently proven generation provenance.",
 'Splitting multiple duties and excluding unresolved fragments are conservative, automated, context-aware approximations; exhaustive manual semantic review of every candidate was not achieved.',
 'Raw duplicate classes use normalized full predicates with target guards; explicitly self-contained table predicates can be merged across editorial headings. Meaning-preserving paraphrases can remain split and context-sensitive merges still require Phase 5 review; the provisional duplication metric is not semantically certified.',
 'No source-to-generated entailment decisions or four-cell scores were attempted in Phase 2.'],
 'next_phase_executed':False,
}
assert len(set(x['occurrence_id'] for x in occ))==len(occ)
assert len(set(x['class_id'] for x in classes))==len(classes)
assert all(len(c['occurrence_ids'])>=1 for c in classes)
assert within+across==len(occ)-len(classes)
assert sum(stats[f]['lines'] for f in FILES)==len(coverage)
assert all(o['class_id'] in {c['class_id'] for c in classes} for o in occ)
assert len({(z['file'],z['line'],z['cell']) for z in cellcoverage})==len(cellcoverage)
(OUT/'02_phase_status_final.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
md=['# Phase 2 — Generated Definitive Claims and Raw Deduplication','',
'**Protocol:** 6.1  ', '**Phase status:** PHASE_COMPLETED_BEST_EFFORT  ',
'**Evaluated method identifier:** `fullload` (single supplied eight-document corpus; generation provenance is not independently verified).','',
'## Input coverage','', '| Scored input (unchanged filename) | Physical lines | Table cells | Eligible table cells | Eligible occurrences |',
'|---|---:|---:|---:|---:|']
for f in FILES:
 v=stats[f];md.append(f'| `{f}` | {v["lines"]:,} | {v["table_cells"]:,} | {v["table_cells_eligible"]:,} | {v["claims"]:,} |')
md+=['','## Extracted generated commitments','',
 f'- Eligible generated occurrences: **{len(occ):,}**.',
 f'- Raw distinct generated classes (conservative exact-full-predicate model): **{len(classes):,}**.',
 f'- Provisional duplicate-excess occurrences: **{len(occ)-len(classes):,}**.',
 f'- Provisional duplicate rate: **{100*((len(occ)-len(classes))/len(occ) if occ else 0):.2f}%**.',
 f'- Provisional within-file / across-file excess: **{within:,} / {across:,}**.',
 f'- Classes appearing in multiple source files: **{multi:,}**.',
 f'- Flagged near-semantic duplicate pairs (not silently merged): **{len(flagged):,}**.',
 f'- Recorded excluded elements: **{len(exclusions):,}**.','',
 '## Evidence reconstruction and eligibility','',
 'Every physical line is represented in the line coverage ledger and every table cell in the cell coverage ledger. Original filenames, exact physical lines, row identifiers, column headers, heading context, and source quotations are retained on eligible occurrence records. This makes the original row/table meaning available for Phase 3 reciprocal entailment review.',
 '', 'Explicitly unresolved questions, unapproved proposals, bare reference/citation cells, standalone identifiers, and illustrative examples are excluded unless a separable definitive obligation is present. The same source-derived constraint can appear in several files; no separate scored occurrence is invented for a citation-only repetition.',
 '', '## Quality limitations','',
 'This is a complete *mechanical evidence-inventory pass* over the supplied physical lines and table cells, followed by a deliberately conservative approximate semantic extraction. It is **not** an independently certified semantic audit. Compound table rows may contain residual under-split propositions; definitive commitments in short field/status cells may require context-specific manual review. These limitations are documented, not converted into missing-file blockers.',
 '', 'The provisional raw duplication count is especially conservative: only normalized exact full-predicate matches with compatible target context are merged. High-similarity candidate paraphrases are recorded separately and must not be treated as verified duplicate classes until their actor, target, modality, conditions, exception and outcome are checked. Provisional duplicate-rate values must not be represented as final Phase 5 metrics.',
 '', '## Files','',
 '- `02_generated_atoms_final.jsonl` — every eligible generated occurrence, with English proposition, evidence and retrieval keys.',
 '- `02_generated_classes_final.jsonl` — raw class representatives and occurrence membership.',
 '- `04_duplicate_classes_final.jsonl` — raw duplication partitions and merge rationale.',
 '- `02_generated_exclusions_final.jsonl` — nondefinitive, proposal, citation and contextual exclusions.',
 '- `02_generated_line_coverage_final.jsonl` — one record per source physical line.',
 '- `02_generated_table_cell_coverage_final.jsonl` — one record per encountered Markdown table cell.',
 '- `02_generated_lookup_keys_final.jsonl` — exact identifier, event, endpoint, literal and word retrieval index.',
 '- `02_possible_semantic_merge_review.jsonl` — high-similarity class pairs retained as unmerged audit candidates.',
 '- `02_phase_status_final.json` — counts and limitations.',
 '- `02_extract_generated.py` — reproducible local extraction code.',
 '', 'No source coverage (Phase 3), generated-vs-PDF validity (Phase 4), final deduplication (Phase 5), or four-cell metrics (Phases 4–6) were executed.','']
(OUT/'02_phase2_report.md').write_text('\n'.join(md),encoding='utf-8')
print(json.dumps({'status':summary['status'],'occurrences':len(occ),'classes':len(classes),'within':within,'across':across,'files':len(FILES),'lines':len(coverage),'cells':len(cellcoverage),'excluded':len(exclusions),'candidate_pairs':len(flagged),'byfile':{f:stats[f]['claims'] for f in FILES}},indent=2))
