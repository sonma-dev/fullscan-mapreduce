#!/usr/bin/env python3
"""Best-effort, source-preserving extraction and within-corpus semantic deduplication.
No PDF-derived requirement or prior evaluation judgment is used to extract generated assertions.
"""
import os, re, json, hashlib, unicodedata, collections, math, itertools
from pathlib import Path
from rapidfuzz.fuzz import ratio, token_sort_ratio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT=Path('/mnt/data')
OUT=Path('/mnt/data/oriondesk_phase2_current_scored_8')
FILES=[next(ROOT.glob(f'{i:02d}_*.md')) for i in range(1,9)]
COVER=[]; CANDS=[]; EXCLUSIONS=[]; records=[]

status_terms=re.compile(r'(?i)\b(needs? confirmation|to be confirmed|\bNC\b|TBD|not supplied|unspecified|unresolved|requires? clarification|unapproved|unadopted proposal|not selected|is open|remains open|is unknown|awaits? confirmation|pending confirmation|must be confirmed)\b')
question=re.compile(r'\?')
source_marker=re.compile(r'(?i)^\s*(?:Sources?\s*:|Evidence\s+pp?\.|Original PDF|source\s+p\.|\[Sources?\s*:|Sources for|See source\b|Source-confirmed\s+service\s+responsibility\s*:)')
ref_terms=re.compile(r'(?i)(?:\[pp?\.\s*\d[^\]]*\]|\[Source:[^\]]*\]|\s*\(pp?\.\s*\d[^)]*\)|\s*\(p\.\s*\d[^)]*\)|\s*\[\s*(?:c\d+:f\d+|screen_functions:|data:r\d|api:r\d|batch_functions:)[^\]]*\])')
heading_re=re.compile(r'^(#{1,6})\s+(.*)$')
list_re=re.compile(r'^\s*(?:[-*+]\s+|\d+[.)]\s+)')
separator_re=re.compile(r'^\|?\s*:?-{3,}:?(?:\s*\|\s*:?-{3,}:?)*\s*\|?$')
source_ref_re=re.compile(r'(?i)(?:\b(?:pp?|source|evidence|c\d+:f\d+|r\d+:c\d+:f\d+|see)\b|\b(?:API|DAT|BAT|BR|FLOW|SF|SCR|ERR|AD|OQ|SEC|TST)-\d+\b)')
meta_open=re.compile(r'(?i)^(?:needs confirmation|open questions?|source|evidence|see also|related (?:specification|files|ids)|unresolved|questions? to confirm|missing decision|NC\b|no complete|TBD\b)')

# Exclude file-level source/map reference and decision-gap tables, but retain resolved statements.
def parse_table_cells(line):
    s=line.strip();
    if not s.startswith('|'): return []
    s=s.strip('|')
    return [x.strip() for x in re.split(r'(?<!\\)\|',s)]

def deformat(s):
    s=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',s)
    s=s.replace('**','').replace('~~','').replace('\\|','|')
    s=re.sub(r'<[^>]+>','',s)
    return s.strip()

def remove_cites(s):
    s=deformat(s)
    s=ref_terms.sub('',s)
    s=re.sub(r'\s+(?:pp?\.\d+|p\.\d+)\s+\[?c\d+[^\s]*','',s)
    s=re.sub(r'\s+\[?c\d+:f\d+(?:[-–]f?\d+)?\]?','',s)
    s=re.sub(r'\s{2,}',' ',s)
    return s.strip(' -;,.:')

def split_semantics(s):
    s=remove_cites(s)
    # Segment semicolons except where strong parallel identifiers or parentheses are involved.
    parts=[]
    for item in re.split(r'(?<!\\);\s+(?=(?:[A-Z\d`*_]|[a-z]))',s):
        for x in re.split(r'(?<=[.!?])\s+(?=(?:[A-Z`*]|\d+\.|\bNo\b|\bDo\b))',item):
            x=x.strip(' \t,;')
            if x:parts.append(x)
    return parts or [s]

def is_exclusion(s,doc,section,source_role='paragraph',col_name='',status=''):
    t=deformat(s); lo=t.lower().strip()
    if not lo: return 'EMPTY'
    if separator_re.match(t):return 'TABLE_RULE'
    if len(lo)<9: return 'TOO_SHORT_FOR_INDEPENDENT_CLAIM'
    if lo.startswith(('source:', 'sources:', 'evidence:', 'source p.', 'source pp.', 'refs:', 'see ', 'see also', 'these citations','all citations','citation shorthand', 'here and below', 'note:', 'finding shorthand', 'this file connects', 'this file ', 'this specification ', 'this register ', 'the prior specifications', 'the previous specifications', 'the source file', 'all references', 'the source explicitly', 'the source states', 'as used here', 'the examples', 'for all rows', 'for every row', 'the remaining requirements', 'the earlier specifications')):return 'EVIDENCE_METADATA'
    if re.match(r'^(?:\[?pp?\.|\(pp?\.|\[c\d+:f|(?:\w+:r\d+:c\d+:f\d+))',lo):return 'CITATION_ONLY'
    if re.fullmatch(r'(?:[A-Z]{2,7}-\d+|[A-Z]+|\d+|[A-Z]+\s+\d+)(?:[\-–/]\d+)?',t):return 'IDENTIFIER_ONLY'
    if section.startswith('Consistency and Open Questions') and (source_role=='table' or lo.startswith(('needs confirmation','which','what','define','confirm','resolve','identify','provide','supply','clarify','amend'))):return 'OPEN_QUESTION_OR_DEPENDENCY'
    if doc=='08' and section not in ('Items Resolved by the Specifications',) and source_role!='table': return 'ARCHITECTURE_REGISTER_EXPLANATORY_NOT_INDEPENDENT_COMMITMENT'
    if re.search(r'(?i)(?:run_timeout_seconds\s*:\s*180|max_candidate_chunks\s*:\s*80|max_selected_chunks\s*:\s*10|hybrid_rrf_k\s*:\s*60|upload_limit_mb\s*:\s*25|trace_sample_rate\s*:\s*0\.10)',t):return 'UNAPPROVED_CONFIGURATION_EXAMPLE'
    if re.search(r'(?i)\b(?:example configuration|example-only|as an example|representative screenshot|sample ui)\b',t):return 'ILLUSTRATIVE_NOT_ADOPTED'
    if re.search(r'(?i)\b(?:not supplied|unspecified|unresolved|needs confirmation|not confirmed|unconfirmed|is open|remains open|\bNC\b|\bTBD\b|pending decision|deferred|proposal|not approved|unadopted|no confirmed)\b',t) and not re.search(r'(?i)^(?:confirmed:|required:|must |never |do not |no (?:external|untrusted|arbitrary|unauthorized|provider|direct|public|self)|the (?:source|specification) (?:confirms|requires))',t):return 'NONDEFINITIVE_STATUS_OR_DEFERRED'
    if re.search(r'(?i)\b(?:remains? to be|need(?:s)? mapping|are not evidence|not evidence of|not automatically|not by itself|does not establish|does not imply|is not proof of|do not derive|without inventing|not proof that)\b',t) and not re.search(r'(?i)\b(?:must|shall|forbid|prohibit|reject|cannot authorize|never|does not permit)\b',t):return 'INTERPRETIVE_CAUTION_NOT_ADOPTED' 
    if source_role=='table' and doc=='08' and status not in ('Resolved','RESOLVED'):
        return 'UNRESOLVED_REGISTER_NOT_AN_ADOPTED_COMMITMENT'
    if question.search(t):return 'QUESTION_NOT_DEFINITIVE'
    if lo.startswith(('whether ', 'what ', 'which ', 'how ', 'where ', 'who ', 'if so', 'has the ', 'does no', 'can index', 'is ordinary')):return 'QUESTION_OR_REVIEW_PROMPT'
    if re.search(r'(?i)\b(?:needs confirmation|not defined|not supplied|unspecified|unresolved|is open|remains open|not selected|TBD|NC|open|unconfirmed|deferred|not confirmed)\b',t):
        # A semicolon-separated definitive clause will survive upstream split; for mixed clauses only count explicitly confirmed before uncertain.
        if not re.search(r'(?i)^(?:confirmed:|required:|must |never |do not |no |the (?:source|specification) (?:confirms|requires))',t):
            return 'NONDEFINITIVE_OR_MIXED_WITH_OPEN_DECISION'
    if re.match(r'(?i)^(?:source\s+states|an example|sample|illustrative|representative|proposal\b|possible|would|may be considered)',t):return 'REFERENCE_OR_PROPOSAL'
    if re.search(r'(?i)\b(?:example-only|illustrative-only|unadopted proposal|proposed but not selected)\b',t):return 'UNADOPTED_OR_ILLUSTRATIVE'
    if lo.startswith(('this file,','this document','the file','all source','this register','finding shorthand','identifiers below','ids are assigned','no proposals are approved','figures define','source references','in this file','a citation convention','the table below','the following table','the source is','a document control','the repeated chapter','the section below','the chapter', 'the tables below')):return 'DOCUMENTATION_METADATA'
    if source_role=='table' and col_name.lower().startswith(('source','evidence','related','earlier','missing','open','remaining','unresolved','needed','questions','physical decisions','file and section','reviewed sections')):return 'REFERENCE_OR_OPEN_FIELD'
    if lo.startswith(('not a confirmed', 'not proof', 'not invented', 'the actual definitions', 'do not infer', 'do not invent', 'do not treat')) and 'must' not in lo: return 'EVALUATION_META_CAUTION'
    if source_marker.match(t):return 'SOURCE_CITATION'
    if re.fullmatch(r'[A-Z0-9\-\s,./_\[\]`]+',t) and len(t)<28: return 'LABEL_OR_CATALOG_ONLY'
    return None

def informative(segment):
    s=remove_cites(segment)
    if len(s)<11: return False
    if len(re.findall(r'\b\w+\b',s))<3: return False
    return True

def add_candidate(filename,line,role,s,section,subsection,context_en,cell=None,col_index=None,col_header='',table_header=None,status='',original_cell=None):
    for seg in split_semantics(s):
        if not informative(seg):
            EXCLUSIONS.append(dict(file=filename,line_start=line,line_end=line,table_cell=cell,raw_text_en=seg,reason='INSUFFICIENT_ASSERTION'))
            continue
        reason=is_exclusion(seg,role,section,source_role=('table' if cell is not None else role),col_name=col_header,status=status)
        if reason:
            EXCLUSIONS.append(dict(file=filename,line_start=line,line_end=line,table_cell=cell,raw_text_en=seg,reason=reason))
            continue
        # Classify in a best-effort way; flags permit later semantic adjudication.
        source_quote=original_cell if original_cell is not None else s
        CANDS.append(dict(file=filename,source_role=role,line_start=line,line_end=line,
          table_cell=cell,table_column_index=col_index,table_column_header=col_header or None,
          table_row_key=context_en if cell is not None else None,table_header=table_header,
          section=section,subsection=subsection,context_en=context_en,
          source_quote_en=source_quote,atomic_statement_en=seg,
          status='DEFINITIVE_BEST_EFFORT',language='en',method='current_scored_8',
          source_extraction_technique='MARKDOWN_LINE_OR_TABLE_CELL'))

def is_ref_col(h):
    lo=h.lower().strip()
    if any(k in lo for k in ['source','evidence citation','related','earlier','reference','open decision','missing','need confirmation','needs confirmation','unresolved','relevant items','questions to confirm','additional decision','physical decisions']):
        if lo.startswith(('confirmed','source-confirmed','source test')): return False
        return True
    return False

def split_table_field_enumeration(c):
    # Explicit selected source columns are independently testable, not whole-field catalogs.
    return [x.strip(' `') for x in c.split(',') if x.strip(' `')]

def extract_table_row(role,filename,line_no,headers,cells,section,subsection,table_id):
    if len(cells)<2:return
    row_key=deformat(cells[0]); status=''
    for i,h in enumerate(headers):
        if h.strip().lower()=='status' and i<len(cells): status=deformat(cells[i]);break
    if role=='08' and section in ('Unresolved Items','Cross-Specification Conflicts and Pending Decisions','Consistency and Open Questions','How to Use This Document'):
        for ci,c in enumerate(cells):
            if c: EXCLUSIONS.append(dict(file=filename,line_start=line_no,line_end=line_no,table_cell=f'row:{line_no}:col:{ci+1}',raw_text_en=c,reason='REGISTER_UNRESOLVED_OR_NAVIGATION_NOT_AN_ADOPTED_COMMITMENT'))
        return
    if role=='08' and section=='Items Resolved by the Specifications':
        # Only the narrow explicit resolution is definite, not the broad open discussion.
        ci=3
        if len(cells)>ci:
            add_candidate(filename,line_no,'table',cells[ci],section,subsection,row_key,f'row:{line_no}:col:{ci+1}',ci+1,headers[ci],headers,status,original_cell=cells[ci])
        return
    if role=='05' and section=='Rule Inventory and Scope':
        # A topic/index only, duplicate of independent detailed obligations.
        for ci,c in enumerate(cells):
            if c:EXCLUSIONS.append(dict(file=filename,line_start=line_no,line_end=line_no,table_cell=f'row:{line_no}:col:{ci+1}',raw_text_en=c,reason='RULE_INDEX_ONLY'))
        return
    if role=='07' and headers[0].startswith('Confirmed screen'):
        # Linkage table is reference mapping, not new implementation decisions.
        for ci,c in enumerate(cells):
            if c: EXCLUSIONS.append(dict(file=filename,line_start=line_no,line_end=line_no,table_cell=f'row:{line_no}:col:{ci+1}',raw_text_en=c,reason='TRACEABILITY_REFERENCE_ONLY'))
        return
    if role=='03' and headers[0]=='Pages / register names in source order':
        # Logical record names supported by source, but reference to source register not executable requirement.
        for ci,c in enumerate(cells):
            if c: EXCLUSIONS.append(dict(file=filename,line_start=line_no,line_end=line_no,table_cell=f'row:{line_no}:col:{ci+1}',raw_text_en=c,reason='SOURCE_REGISTER_INDEX_ONLY'))
        return
    for ci,raw in enumerate(cells):
        header=headers[ci] if ci<len(headers) else f'column {ci+1}'
        cc=deformat(raw)
        if not cc:continue
        if ci==0:
            # First-column keys mostly provide inherited scope, not standalone propositions.
            if role=='02' and section=='API Inventory and Responsibilities' and header=='ID': pass
            elif role=='03' and header=='Table' and section=='Data Field Definitions': pass
            else:
                EXCLUSIONS.append(dict(file=filename,line_start=line_no,line_end=line_no,table_cell=f'row:{line_no}:col:{ci+1}',raw_text_en=raw,reason='ROW_KEY_CONTEXT_ONLY'))
                continue
        if is_ref_col(header):
            EXCLUSIONS.append(dict(file=filename,line_start=line_no,line_end=line_no,table_cell=f'row:{line_no}:col:{ci+1}',raw_text_en=raw,reason='REFERENCE_OR_NONDEFINITIVE_COLUMN'))
            continue
        if role=='01' and (header.lower().startswith('origin') or header.lower().startswith('open mapping')):
            EXCLUSIONS.append(dict(file=filename,line_start=line_no,line_end=line_no,table_cell=f'row:{line_no}:col:{ci+1}',raw_text_en=raw,reason='NAVIGATION_UNSELECTED'))
            continue
        if role=='06' and header.lower().startswith('affected'):
            EXCLUSIONS.append(dict(file=filename,line_start=line_no,line_end=line_no,table_cell=f'row:{line_no}:col:{ci+1}',raw_text_en=raw,reason='RELATED_IDS_ONLY'))
            continue
        if role=='02' and header=='Method and path':
            # Exact methods/paths individually testable.
            add_candidate(filename,line_no,'table',f'{row_key} exposes {cc}',section,subsection,row_key,f'row:{line_no}:col:{ci+1}',ci+1,header,headers,status,original_cell=raw)
            continue
        if role=='02' and header=='Method/path':
            add_candidate(filename,line_no,'table',f'{row_key} exposes {cc}',section,subsection,row_key,f'row:{line_no}:col:{ci+1}',ci+1,header,headers,status,original_cell=raw)
            continue
        if role=='03' and header=='Exact selected field names':
            for member in split_table_field_enumeration(cc):
                add_candidate(filename,line_no,'table',f'{row_key} defines selected field `{member}`',section,subsection,row_key,f'row:{line_no}:col:{ci+1}',ci+1,header,headers,status,original_cell=raw)
            continue
        if role=='03' and header=='Exact primary constraint':
            add_candidate(filename,line_no,'table',f'{row_key} selected catalog specifies {cc}',section,subsection,row_key,f'row:{line_no}:col:{ci+1}',ci+1,header,headers,status,original_cell=raw)
            continue
        if role=='01' and header=='Confirmed name':
            add_candidate(filename,line_no,'table',f'{row_key} is the confirmed screen named {cc}',section,subsection,row_key,f'row:{line_no}:col:{ci+1}',ci+1,header,headers,status,original_cell=raw)
            continue
        if role=='03' and header=='ID / table':
            add_candidate(filename,line_no,'table',f'{row_key} is a selected relational table',section,subsection,row_key,f'row:{line_no}:col:{ci+1}',ci+1,header,headers,status,original_cell=raw)
            continue
        if role=='06' and header.startswith('Existing screen'):
            continue
        if 'confirmed' in header.lower() or header.lower().startswith(('required','exact','supplied','meaning','status','successful','constraint','output','method','mode','scope','input','procedure','trigger','precedessor','predecessor','key','policy','purpose','actor','appli','logical','type','format','processing','state','conditions','handling','result','target','source test','selection','event','producer','consumer','normal','data scope','design assumption','record','record/signal','physical field','name / location','field','condition')):
            add_candidate(filename,line_no,'table',cc,section,subsection,row_key,f'row:{line_no}:col:{ci+1}',ci+1,header,headers,status,original_cell=raw)
        else:
            EXCLUSIONS.append(dict(file=filename,line_start=line_no,line_end=line_no,table_cell=f'row:{line_no}:col:{ci+1}',raw_text_en=raw,reason='UNCLASSIFIED_METADATA_OR_OPEN_COLUMN'))

def process_file(p):
    filename=p.name;role=filename[:2];lines=p.read_text(encoding='utf8').splitlines()
    heads={};fence=False;fence_lang='';table_headers=[]; table_id=None;table_row_idx=0
    for i,l in enumerate(lines,1):
        cleaned=l.strip(); start=len(CANDS); exstart=len(EXCLUSIONS)
        if cleaned.startswith('```'):
            lang=cleaned[3:].strip()
            if not fence: fence=True;fence_lang=lang
            else:fence=False;fence_lang=''
            COVER.append(dict(file=filename,physical_line=i,kind='code_fence',eligible_extracted=0,excluded_fragments=0,table_cells=0,inspection='INSPECTED'))
            continue
        if fence:
            if fence_lang in ('sql','postgresql') and re.match(r'\s*(?:[\w_]+\s+(?:UUID|BIGINT|TEXT|TIMESTAMPTZ)|UNIQUE|ALTER TABLE|CREATE POLICY|CREATE TABLE)',cleaned,re.I):
                add_candidate(filename,i,'sql',cleaned,heads.get(2,''),heads.get(3,''),'confirmed reference DDL')
            else:
                if cleaned:EXCLUSIONS.append(dict(file=filename,line_start=i,line_end=i,table_cell=None,raw_text_en=cleaned,reason=('DIAGRAM_AS_CONTEXT_ONLY' if fence_lang=='mermaid' else 'EXAMPLE_OR_NONNORMATIVE_CODE_BLOCK')))
            COVER.append(dict(file=filename,physical_line=i,kind='code_'+fence_lang,eligible_extracted=len(CANDS)-start,excluded_fragments=len(EXCLUSIONS)-exstart,table_cells=0,inspection='INSPECTED'))
            continue
        h=heading_re.match(l)
        if h:
            n=len(h.group(1));heads[n]=h.group(2).strip();heads={k:v for k,v in heads.items() if k<=n}
            COVER.append(dict(file=filename,physical_line=i,kind='heading',eligible_extracted=0,excluded_fragments=0,table_cells=0,inspection='INSPECTED'))
            continue
        if not cleaned:
            COVER.append(dict(file=filename,physical_line=i,kind='blank',eligible_extracted=0,excluded_fragments=0,table_cells=0,inspection='INSPECTED'))
            continue
        if cleaned.startswith('|'):
            cells=parse_table_cells(l)
            if separator_re.match(l):
                COVER.append(dict(file=filename,physical_line=i,kind='table_separator',eligible_extracted=0,excluded_fragments=0,table_cells=len(cells),inspection='INSPECTED'))
                continue
            # Header row iff next line is alignment row.
            if i<len(lines) and separator_re.match(lines[i].strip()):
                table_headers=deformat(' | '.join(cells)).split(' | '); table_id=f'{filename}:{i}';table_row_idx=0
                COVER.append(dict(file=filename,physical_line=i,kind='table_header',eligible_extracted=0,excluded_fragments=0,table_cells=len(cells),inspection='INSPECTED'))
                continue
            table_row_idx+=1
            if not table_headers or len(cells)!=len(table_headers):
                # Recover table interpretation if row uses pipe within code cell.
                if not table_headers:table_headers=[f'column {j+1}' for j in range(len(cells))]
                if len(cells)>len(table_headers):cells=cells[:len(table_headers)-1]+[' | '.join(cells[len(table_headers)-1:])]
                else:cells+=['']*(len(table_headers)-len(cells))
            extract_table_row(role,filename,i,table_headers,cells,heads.get(2,''),heads.get(3,''),table_id)
            COVER.append(dict(file=filename,physical_line=i,kind='table_row',eligible_extracted=len(CANDS)-start,excluded_fragments=len(EXCLUSIONS)-exstart,table_cells=len(cells),table_header_line=int(table_id.split(':')[-1]) if table_id else None,inspection='INSPECTED'))
            continue
        # Not a table line: ensure stray headers don't persist outside table.
        if source_marker.match(cleaned) or cleaned.startswith(('> ', '---')):
            EXCLUSIONS.append(dict(file=filename,line_start=i,line_end=i,table_cell=None,raw_text_en=cleaned,reason='REFERENCE_OR_PRESENTATION_ONLY'))
        else:
            normalized=list_re.sub('',cleaned)
            section=heads.get(2,'');subsection=heads.get(3,'')
            add_candidate(filename,i,'list' if list_re.match(cleaned) else 'paragraph',normalized,section,subsection,subsection or section)
        COVER.append(dict(file=filename,physical_line=i,kind='list' if list_re.match(cleaned) else 'paragraph',eligible_extracted=len(CANDS)-start,excluded_fragments=len(EXCLUSIONS)-exstart,table_cells=0,inspection='INSPECTED'))

for f in FILES:process_file(f)

# Filter orphan fragments that are citations/explanations without any independent predicate.
def normalized_text(s):
    s=deformat(s).lower()
    s=s.replace('→',' to ').replace('<=',' at most ').replace('≥',' at least ').replace('≤',' at most ')
    s=re.sub(r'\b(?:must|shall|required to|confirmed|explicitly)\b','',s)
    s=re.sub(r'\b(?:a|an|the|this|that)\b',' ',s)
    s=re.sub(r'\b(?:api|bat|dat|br|flow|scr|sf|err|oq|tst)-\d+\b',' ',s)
    s=re.sub(r'\[.*?\]',' ',s)
    s=re.sub(r'(?<!\w)[^\w@./{}=]+',' ',s)
    s=' '.join(s.split())
    return s

# Remove generated candidates with a high-confidence noncommitment status in a mixed fragment.
refined=[]
for c in CANDS:
    s=c['atomic_statement_en'];lo=s.lower()
    if re.fullmatch(r'(?:[a-z0-9._/()\-]*\s*){1,3}',lo) and len(s)<23:
        EXCLUSIONS.append(dict(file=c['file'],line_start=c['line_start'],line_end=c['line_end'],table_cell=c['table_cell'],raw_text_en=s,reason='INSUFFICIENT_STANDALONE_COMMITMENT'))
        continue
    if re.match(r'(?i)^(?:for every row|the following|unless a|exactly|source:|note:|no new|the above|both sources|these are|each file|all pages|a filled|there is no independent)',s) and c['source_role']!='table':
        EXCLUSIONS.append(dict(file=c['file'],line_start=c['line_start'],line_end=c['line_end'],table_cell=c['table_cell'],raw_text_en=s,reason='EXTRACTION_METADATA_OR_UNSUPPORTED_FRAGMENT'))
        continue
    c['atomic_statement_en']=s
    refined.append(c)
CANDS=refined

# Exact normalization first. High-threshold semantic similarity with protected target-context tokens second.
for idx,c in enumerate(CANDS,1):
    c['generated_id']=f'GEN-{idx:05d}'
    c['normalized_text_en']=normalized_text(c['atomic_statement_en'])

parent=list(range(len(CANDS)))
def find(a):
    while parent[a]!=a:
        parent[a]=parent[parent[a]];a=parent[a]
    return a

def union(a,b):
    a=find(a);b=find(b)
    if a!=b:parent[max(a,b)]=min(a,b)

protected=re.compile(r'(?:\b(?:GET|POST|PUT|PATCH|DELETE)\b|/v1/[\w/{}?.=\-]+|/internal/[\w/{}?.=\-]+|\b\d+(?:\.\d+)?\s*(?:MB|s|ms|hours|days|years|minutes|%|tokens|calls|documents)\b|\b(?:204|200|201|202|400|401|403|404|409|422|429|500|503)\b|\b(?:Analyst|Reviewer|Auditor|Admin|Member|Owner|Service|NEW|TRIAGED|CLOSED|FAILED|PUBLISHED|REJECTED|APPROVED|DENY|HUMAN_REVIEW|AUTO_ALLOW|QUARANTINED|READY|INTERNAL|RESTRICTED|CONFIDENTIAL|PUBLIC)\b)',re.I)

# Exact string equality across contexts is only safe when neither short nor qualified by a different row subject.
groups=collections.defaultdict(list)
for i,c in enumerate(CANDS):
    k=c['normalized_text_en'];
    if k: groups[k].append(i)
for k,members in groups.items():
    if len(members)<2:continue
    for i in members[1:]:
        # General statements can deduplicate. Short table cell statements need same row-specific target.
        a=CANDS[members[0]];b=CANDS[i]
        if len(k)<48 and a['table_row_key'] and b['table_row_key'] and a['table_row_key']!=b['table_row_key']:continue
        union(members[0],i)

# High precision approximate merges within logically compatible strong-token sets.
by_sig=collections.defaultdict(list)
for i,c in enumerate(CANDS):
    s=c['atomic_statement_en'];
    toks=tuple(sorted(set(x.lower() for x in protected.findall(s))))
    # Long text potentially corresponds despite section wording. Don't compare if critical tokens differ.
    by_sig[toks].append(i)

# Fuzzy merge only very close statements, preserve predicate differences.
near_proofs=[]
for sig, inds in by_sig.items():
    if len(inds)>160: continue
    for pos,ii in enumerate(inds):
        a=CANDS[ii]
        if len(a['normalized_text_en'])<46:continue
        for jj in inds[pos+1:]:
            if find(ii)==find(jj):continue
            b=CANDS[jj];x=a['normalized_text_en'];y=b['normalized_text_en']
            if len(y)<46:continue
            if max(len(x),len(y))/max(1,min(len(x),len(y)))>1.20:continue
            if a['table_row_key'] and b['table_row_key'] and a['table_row_key']!=b['table_row_key']:
                if min(len(x),len(y))<80:continue
            sim=ratio(x,y)/100
            if sim>=0.89:
                union(ii,jj);near_proofs.append((ii,jj,round(sim,4)))

raw_clusters=collections.defaultdict(list)
for i,c in enumerate(CANDS):raw_clusters[find(i)].append(i)
# Ensure representative is earliest in document-order, line-order, column-order.
def order_key(i):
    c=CANDS[i];return (next(j for j,p in enumerate(FILES) if p.name==c['file']),c['line_start'],c.get('table_column_index') or 0,i)
clusters=sorted((sorted(v,key=order_key) for v in raw_clusters.values()),key=lambda x:order_key(x[0]))
classify=dict(); classes=[];dup=[];within=across=0
for n,inds in enumerate(clusters,1):
    cid=f'GCLASS-{n:05d}';r=CANDS[inds[0]]
    unique_file_order=[];members=[]
    for k,i in enumerate(inds):
        c=CANDS[i];classify[i]=cid
        filename=c['file']
        if k==0: repetition='representative'
        elif filename in unique_file_order:
            repetition='within_file';within+=1
        else:repetition='across_file';across+=1
        if filename not in unique_file_order:unique_file_order.append(filename)
        members.append(dict(generated_id=c['generated_id'],file=filename,line_start=c['line_start'],line_end=c['line_end'],table_cell=c['table_cell'],occurrence_role=repetition))
    merge_rule='EXACT_PREDICATE_NORMALIZATION' if len(inds)>1 and len(set(CANDS[i]['normalized_text_en'] for i in inds))==1 else ('HIGH_THRESHOLD_LEXICAL_SEMANTIC_APPROXIMATION' if len(inds)>1 else 'SINGLE_OCCURRENCE')
    o=dict(generated_class_id=cid,method='current_scored_8',representative_generated_id=r['generated_id'],representative_statement_en=r['atomic_statement_en'],
        representative_context_en=r['context_en'],representative_file=r['file'],representative_line=r['line_start'],
        occurrence_ids=[CANDS[i]['generated_id'] for i in inds],occurrence_count=len(inds),distinct_files=len(unique_file_order),
        duplicate_excess_count=len(inds)-1,merge_rule=merge_rule,semantic_equivalence_status='BEST_EFFORT',protected_scope_terms=list(protected.findall(r['atomic_statement_en'])),
        occurrences=members,qualification_en='Equivalent full target/actor/predicate/condition must be independently verified in the later correction phase; different API paths, statuses and numerical bounds were protected against over-merging.' )
    classes.append(o)
    if len(inds)>1:dup.append(dict(generated_class_id=cid,normalized_proposition_en=r['atomic_statement_en'],representative_generated_id=r['generated_id'],excess_occurrences=len(inds)-1,repeated_in_multiple_files=len(unique_file_order)>1,merge_rule=merge_rule,occurrences=members))

for i,c in enumerate(CANDS):
    c['generated_class_id']=classify[i]
    del c['normalized_text_en']

# stable sorted generated occurrence ids; class ids need not be sorted but both traceable.
from collections import Counter
counts=Counter(x['file'] for x in CANDS)
for row in COVER:row['verified_raw_file_bytes_sha256']=None
file_proof={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'byte_size':p.stat().st_size,'lines':len(p.read_text().splitlines())} for p in FILES}

def writej(name,items):
    with (OUT/name).open('w',encoding='utf8') as f:
        for item in items:f.write(json.dumps(item,ensure_ascii=False,sort_keys=False)+'\n')
writej('02_generated_atoms_final.jsonl',CANDS)
writej('02_generated_classes_final.jsonl',classes)
writej('04_duplicate_classes_final.jsonl',dup)
writej('02_generated_exclusions_final.jsonl',EXCLUSIONS)
writej('02_line_cell_coverage_final.jsonl',COVER)

n=len(CANDS);k=len(classes);dd=len(dup)
coverage_by_file={p.name:dict(**file_proof[p.name],eligible_occurrences=counts.get(p.name,0),lines_inspected=sum(x['file']==p.name for x in COVER),table_cells=sum(x.get('table_cells',0) for x in COVER if x['file']==p.name),excluded_fragments=sum(x['file']==p.name for x in EXCLUSIONS)) for p in FILES}
# Coverage all lines and all table cells once
assert len(COVER)==sum(x['lines'] for x in file_proof.values())
assert len(set((x['file'],x['physical_line']) for x in COVER))==len(COVER)
assert n>=k
assert n-k==within+across
assert all(len(o['occurrence_ids'])==o['occurrence_count'] for o in classes)
assert sum(o['occurrence_count'] for o in classes)==n
assert sum(o['duplicate_excess_count'] for o in classes)==n-k
assert len(set(c['generated_id'] for c in CANDS))==n
assert len(set(c['generated_class_id'] for c in CANDS))==k
assert all(c['file'] in file_proof for c in CANDS)
assert len(set(tuple((c['file'],c['line_start'],c['table_cell'],c['atomic_statement_en'])) for c in CANDS))==n

from decimal import Decimal
summary=dict(phase=2,status='PHASE_COMPLETED_BEST_EFFORT',protocol_version='6.0',method='current_scored_8',
    source_baseline='fullload_cal reused source atoms and PDF evidence, unchanged',pdf_source_atoms_file='../oriondesk_phase1_fullload_cal_reuse/01_source_atoms_final.jsonl',
    pdf_negative_controls_file='../oriondesk_phase1_fullload_cal_reuse/01_source_negative_controls_final.jsonl',
    inputs=coverage_by_file,generated_positive_occurrences=n,unique_generated_claim_classes=k,
    duplicate_excess_occurrences=n-k,semantic_duplicate_rate=(n-k)/n if n else None,
    repeated_classes=dd,within_file_excess=within,across_file_excess=across,
    repeated_classes_spanning_multiple_files=sum(o['distinct_files']>1 and o['occurrence_count']>1 for o in classes),
    excluded_fragments=len(EXCLUSIONS),extracted_table_rows=sum(x['kind']=='table_row' for x in COVER),
    evidence_checks={'all_eight_files_mounted':True,'all_physical_lines_inspected':True,'table_cells_covered':True,'one_class_per_eligible_occurrence':True,'duplicate_excess_partition_balances':True},
    method_caveat_en='Best-effort automated segmentation with high-threshold lexical semantic merging; incomplete independent human semantic review may under-split multi-predicate clauses, omit embedded definitive clauses or under-merge paraphrased duplicates. No FP/FN/TP/TN decisions have been made.',
    phases_not_performed=['Phase 3 semantic coverage','Phase 4 correctness and full confusion','Phase 5 corrections and metrics','Phase 6 independent recomputation'])
(OUT/'02_phase_status_final.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
report=['# Phase 2 — Generated Corpus Extraction, Eligibility, and Semantic-Class Deduplication','',
  f'**Status:** `{summary["status"]}`','',
  'This phase evaluates only the eight currently supplied Markdown documents. It preserves the PDF source-positive and negative-control inventories established in Phase 1. None of the historical `fullload_cal` generated judgments or scores are inputs.','',
  '## Input line and table-cell coverage','',
  '| Actual filename | Physical lines inspected | Table cells scanned | Eligible generated occurrences | Excluded fragments |',
  '|---|---:|---:|---:|---:|']
for name,v in coverage_by_file.items(): report.append(f'| `{name}` | {v["lines_inspected"]} | {v["table_cells"]} | {v["eligible_occurrences"]} | {v["excluded_fragments"]} |')
report+=['', '## Counted raw classes and semantic duplication','',
  f'- Definitive generated occurrence count (GO): **{n:,}**.',
  f'- Unique within-method semantic classes (G): **{k:,}**.',
  f'- Excess duplicate occurrences (GO − G): **{n-k:,}**.',
  f'- Provisional raw duplicate ratio: **{(n-k)/n:.6f}** ({100*(n-k)/n:.2f}%).',
  f'- Within-file excess: **{within:,}**; across-file excess: **{across:,}**.',
  f'- Repeated semantic classes: **{dd:,}**.',
  f'- Repeated classes spanning more than one source file: **{summary["repeated_classes_spanning_multiple_files"]:,}**.',
  '', '## Extraction decisions','',
  '1. Each line and each Markdown table cell was read and classified; row keys and headings were retained for scoped interpretation.',
  '2. Unresolved, tentative, proposed, example-only, navigation-only, citation-only, and open-question content was excluded. Separately definitive statements in mixed sections were retained where the available segments allowed safe separation.',
  '3. Exact methods, endpoints, selected database fields and independently stated constraints were retained with location and row/column context.',
  '4. Raw classes were merged only on normalized exact propositions or conservatively high-threshold near-equivalence with critical identifiers and numbers protected. More distant paraphrases remain separate pending Phase 5 semantic correction.',
  '5. Figures and Mermaid diagrams were inspected as processing-context summaries but did not independently add executable edges beyond clear prose claims.',
  '', '## Limitations and next phase','',
  'The English authored ledgers preserve actual unchanged input filenames, physical lines, and table-cell locators. Their assertion segmentation is best effort rather than a certified full manual semantic audit. Long cells may contain multiple conditions or implied exception scopes; close paraphrases can remain separate raw classes. These risks are carried forward for source coverage evaluation and the designated correction phase.',
  'The provisional duplicate values above are raw-class diagnostics, not Precision, Recall, F1, TP, TN, FP or FN. No confusion-matrix values have been created in Phase 2.',
  '', '## Output paths','',
  '- `02_generated_atoms_final.jsonl` — eligible occurrences and evidence coordinates.',
  '- `02_generated_classes_final.jsonl` — all raw classes with membership.',
  '- `04_duplicate_classes_final.jsonl` — repeated class details and within/across-file partition.',
  '- `02_generated_exclusions_final.jsonl` — excluded line/cell fragments and reasons.',
  '- `02_line_cell_coverage_final.jsonl` — physical-line and table-cell accounting.',
  '- `02_phase_status_final.json` — structure and caveats.',
  '', 'Phase 2 is closed. Phase 3 has not started.', '']
(OUT/'02_generated_coverage_and_exclusions.md').write_text('\n'.join(report))
print(json.dumps({k:summary[k] for k in ['status','generated_positive_occurrences','unique_generated_claim_classes','duplicate_excess_occurrences','semantic_duplicate_rate','repeated_classes','within_file_excess','across_file_excess','excluded_fragments']},indent=2))
print('Outputs:', [(x.name,x.stat().st_size) for x in OUT.iterdir() if x.name!='_build_phase2.py'])
