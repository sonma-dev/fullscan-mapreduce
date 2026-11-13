#!/usr/bin/env python3
"""OrionDesk phase 2: evidence-preserving best-effort Markdown atomic extraction.

Each definitive generated occurrence has an original physical line and a table cell
locator when applicable. The extractor is intentionally conservative about approved
claims in the Stage-8 unresolved register. This does not adjudicate PDF support.
"""
from __future__ import annotations
import collections, hashlib, json, os, re, shutil
from pathlib import Path
from difflib import SequenceMatcher
from datetime import datetime, timezone

ROOT=Path('/mnt/data')
OUT=ROOT/'oriondesk_phase2_current'
PRIOR=ROOT/'oriondesk_phase1_current'
FILES=[
'01_screen_functions(7).md','02_api(7).md','03_data(7).md',
'04_batch_functions(7).md','05_business_rules(7).md',
'06_exception_handling(8).md','07_processing_flows(8).md',
'08_architecture_decision(7).md']
CODE_RE = re.compile(r'`[^`]*`')
CITE_RE = re.compile(r'\s*\[(?:Sources?|Source):?[^\]]*\]\s*|\s*\[pp?\.\s*\d+[^\]]+\]\s*', re.I)
BOILER_REF=re.compile(r'\s*\(?\[?(?:pp?\.|Sources?\s*:|See\s+(?:§|section|pp?\.)|c\d+:f\d+)[^\n]*$',re.I)
ID_RE=re.compile(r'\b(?:PDF|SCR|SF|OQ|API|DAT|BAT|BR|ERR|EH|FLOW|AD|TST|SEC|RES|T)-\d{1,4}\b')
ENDPOINT_RE=re.compile(r'\b(?:GET|POST|PUT|PATCH|DELETE)\s+/(?:v1|internal)/[A-Za-z0-9_{}?=./-]+')
FIELD_RE=re.compile(r'`([a-z][a-z0-9_]*(?:\.[a-z_]+)?)`')
STATUS_RE=re.compile(r'\b(?:20[0124]|40[149]|422|429|404|409|503|500)\b|\b(?:[A-Z]+(?:_[A-Z]+){1,})\b')
TOKEN_RE=re.compile(r'[A-Za-z][a-z0-9_\-.]*|\d+(?:\.\d+)?')
SOURCE_PHRASES=('sources:', 'source:', 'all citations below', 'source: pp.', 'sources: pp.',
                'source p.', 'inventory evidence:', 'in table citations',
                'finding shorthand', 'the source explicitly states')
META_PREFIX=('this file,', 'this specification', 'this register', 'the source states',
             'all numbers are', 'all source citations', 'the source confirms',
             'source file', 'the sources', 'all references', 'all citations',
             'these citations', 'finding shorthand')
DECISION_VOCAB=('needs confirmation','unresolved','tbd','to confirm','not selected','not supplied',
                'not confirmed','unapproved','proposal','unadopted','open question','mapping open',
                'unknown','undecided','not specified','requires confirmation', 'pending')
ACTION_VOCAB=('must','shall','requires','required','cannot','never','no ','do not','does not',
              'prohibit','forbid','only','reject','return','include','contains','preserve',
              'enforce','store','captures','record','apply','provide','bind','verify',
              'use ','uses ','is ','are ','remains ','keep ','blocks','retain','recheck',
              'check ','allowed','follows','produce','capture','route','display',
              'support','protect','prevent','permit','has ','have ','must not',
              'authorize','separate','source', 'scope', 'validated','append-only',
              'immutable','idempotent','current','policy','audit','revision',
              'read-only','encrypted','private','async','transactional')
COLUMN_SKIP=('source','source /','source page','needs confirmation','open decision',
             'open physical','open schema','unresolved','remaining',
             'questions to confirm','references', 'related specifications','citation',
             'related api','source evidence','evidence','missing wire',
             'related specifications and requirement ids','related screen',
             'affected scope and earlier identifiers','affected scope and implementation dependency',
             'earlier dependencies','both source positions','evidence conflict',
             'evidence and unresolved','evidence and required','source conflict or missing',
             'required clarification','required amendment','required decision / dependency',
             'earlier links','open id','missing operational','formal schema status',
             'open conditions','open mapping','physical decisions','open decision',
             'logical data purpose and api dependency', 'register evidence',
             'type, default and missing', 'type/requiredness/default decision',
             'unresolved attributes','unresolved measurement',
             'needs confirmation beside','physical/wire status',
             'extra note for missing', 'source test / affected',
             'applicable condition / unresolved', 'needed evidence')

sources=[json.loads(x) for x in open(PRIOR/'09_excluded_units.jsonl',encoding='utf-8') if x.strip()]
atoms=[]; excludes=list(sources); audit=[]; line_coverage=[]; grouped=[]
exidx=0

def strip_ref(s):
    s=s.strip(); s=re.sub(r'\s+\[(?:pp?\.|Source:)[^\]]+\]\.?$', '', s, flags=re.I)
    s=re.sub(r'\s*\((?:pp?\.|Source:)\s*[0-9][^)]*\)\.?$', '', s, flags=re.I)
    s=re.sub(r'\s*\[[^\]]*(?:c\d+:f\d+|r\d+:c\d+)[^\]]*\]\.?$', '', s)
    s=re.sub(r'\s*\(?\b(?:pp?\.\s*)?\d{1,3}(?:[–-]\d{1,3})?(?:,\s*\d+[–-]?\d*)*\s*\[c\d+:[^\]]+\]\)?\.?$', '', s)
    return s.strip(' .')

def clean_md(s):
    s=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',s)
    s=re.sub(r'\*\*|__|`','',s)
    return re.sub(r'\s+',' ',s).strip()

def tokenize_pieces(s):
    """Split only at proven top-level sentence/semicolon boundaries; respect code spans."""
    s=strip_ref(s)
    s=re.sub(r'^p\.\d+\s+c\d+:f\d+\.?\s*','',s)
    # Remove source suffixes while retaining the literal raw evidence externally.
    s=re.sub(r'\s*(?:\[Source:[^\]]+\]|\[Sources:[^\]]+\])$', '', s,flags=re.I)
    pieces=[]; buf=[]; code=False; braces=0; parens=0
    for i,c in enumerate(s):
        if c=='`': code=not code
        if not code:
            if c=='{': braces+=1
            elif c=='}': braces=max(0,braces-1)
            elif c=='(': parens+=1
            elif c==')': parens=max(0,parens-1)
        cut=False
        if not code and braces==0 and parens==0:
            if c==';' and i>0: cut=True
            elif c=='.' and i+1<len(s) and s[i+1].isspace() and not (i>=1 and s[i-1].isdigit()):
                prior=''.join(buf).strip().lower()
                if not re.search(r'(?:\bp|\bpp|\bno|\betc|\beg|\bi\.e|\br\d|\ba\d|\bv\d|\b§\d)$', prior): cut=True
        if cut:
            p=''.join(buf).strip(' ;.\t');buf=[]
            if p:pieces.append(p)
        else:buf.append(c)
    p=''.join(buf).strip(' ;.\t')
    if p:pieces.append(p)
    return pieces

def split_enum(s):
    """Split explicit lists only for clearly testable fields/values, never paraphrase arbitrary conjoined clauses."""
    s=s.strip()
    if re.search(r'\b(?:tenant_id|workspace_id|case_id|actor_id|created_at|updated_at)\b',s) and len(s)<85 and s.count('`')>=4:
        return [x.strip() for x in re.split(r',\s*(?=`)',s) if x.strip()]
    return [s]

def classify(text,filename, section, col='', row_status='', from_ad=False, from_table=False):
    s=clean_md(text).strip(); low=s.lower()
    if not s or len(s)<3:return ('EMPTY_OR_FRAGMENT','Empty or nonpropositional fragment.')
    if re.fullmatch(r'[-+—\d\s.<>|/:`_,]+',s):return ('STRUCTURAL','No independently asserted implementation predicate.')
    if low.startswith(SOURCE_PHRASES) or low.startswith(META_PREFIX):return ('SOURCE_CITATION_OR_CONTEXT','Bibliographic or document-context statement, not a new design commitment.')
    if re.search(r'^(?:no design proposals|screen and sf identifiers|the (?:specification|source|example|citation|document) (?:is|was|has)|these are (?:assigned|analytical|reference)|no confirmed (?:endpoint|route|screen))', low):return ('DOCUMENT_METADATA','Instruction-file context or analytical labels, not a separate implementation predicate.')
    if re.fullmatch(r'(?:\[[^\]]+\]|(?:API|DAT|BR|BAT|SF|SCR|ERR|FLOW|AD|TST|RES)-\d+|\w+)',s) and not re.search(r'\b(?:must|shall|require|forbid)\b', low):
        return ('REFERENCE_OR_LABEL','Bare identifier or label; contains no independent definitive assertion.')
    if re.match(r'(?:needs confirmation|tbd|pending|open question|question to confirm|unknown|not supplied)\s*[:—-]',low):
        return ('NONDEFINITIVE','Explicitly unresolved or information-requesting text.')
    if low.startswith(('?', 'what ', 'which ', 'how ', 'who ', 'when ', 'whether ')) or low.endswith('?'):
        return ('OPEN_QUESTION','Question is not an approved commitment.')
    if (any(x in low for x in ('trace_sample_rate:', 'run_timeout_seconds:', 'max_candidate_chunks:', 'max_selected_chunks:', 'hybrid_rrf_k:', 'auto_publish_classification:', 'example configuration', 'sample config'))):
        return ('EXAMPLE_NONNORMATIVE','Reference-only configuration sample is not an adopted implementation policy.')
    if ('representative cards' in low or 'representative views' in low or 'representative image' in low or 'screenshot shows' in low or 'sample id' in low or 'these examples are' in low):
        return ('ILLUSTRATIVE_CONTEXT','Representative UI cards and sample IDs are not adopted defaults or requirements.')
    if 'fictional' in low and ('value' in low or 'reference image' in low or 'example' in low):
        return ('ILLUSTRATIVE_CONTEXT','Representative content does not establish a fixed requirement.')
    if ('example' in low or 'illustrative' in low or 'placeholder' in low) and not re.search(r'(?:not|cannot|never|must|do not)',low):
        return ('EXAMPLE_NONNORMATIVE','Illustrative-only example; no default or final contract is adopted.')
    if col and any(col.lower().strip().startswith(y) for y in COLUMN_SKIP):
        return ('TABLE_REFERENCE_OR_GAP','Column is designated for sources, unresolved dependencies, coverage crosswalk, or missing-schema information, not an adopted standalone implementation commitment.')
    if from_ad and (row_status in ('TBD','Needs confirmation','Unadopted proposal','Proposal','Pending')):
        if re.search(r'\b(?:remain binding|remain confirmed|remains mandatory|still required|must not|cannot|never|is required|remain forbidden|remain prohibited)\b',low):
            return ('DEFINITIVE','An explicit separable currently binding constraint survives unresolved status.')
        return ('NONDEFINITIVE_AD','Architecture-decision register row is unresolved or unadopted.')
    if ('not selected' in low or 'unapproved' in low or 'needs confirmation' in low or 'unspecified' in low or 'not supplied' in low or 'remains open' in low) and not re.search(r'\b(?:never|cannot|do not|must not|must|requires|is required|confirmed|forbidden)\b',low):
        return ('NONDEFINITIVE','Describes a missing/unselected contract, not a completed implementation claim.')
    if any(z in low for z in ('is not an approved', 'not a confirmed', 'not evidence that')):
        if re.search(r'\b(?:do not|cannot|must not)\b',low):return('DEFINITIVE','Explicit normative boundary or prohibition.')
        return('NONDEFINITIVE','Caution against inferred behavior without an independently adopted choice.')
    if from_table and not from_ad:
        if re.fullmatch(r'(?:API|DAT|BR|BAT|SF|SCR|ERR|FLOW|AD|TST|RES|T|SEC|OQ|API-OQ|DAT-OQ|BR-OQ|BAT-OQ|ERR-OQ|FLOW-OQ)-\d+(?:[–-]\d+)?(?:,?\s*/?\s*(?:API|DAT|BR|BAT|SF|SCR|ERR|FLOW|AD|TST|RES|T|SEC|OQ|API-OQ|DAT-OQ|BR-OQ|BAT-OQ|ERR-OQ|FLOW-OQ)-\d+)*',s):
            return ('REFERENCE_OR_LABEL','Only cross-reference identifiers are listed.')
        if low in ('none','nc','no','yes','tbd','resolved','confirmed','needs confirmation'):
            return ('REFERENCE_OR_LABEL','Status value, not an independently scoped product requirement.')
        # The table row and column provide binding context to values and short
        # predicates, including 201/409, actor grants, state transitions, fields.
        # Open/unspecified columns were filtered above and are not adopted.
        if (not any(x in low for x in ('needs confirmation', 'tbd', 'nc;', 'not supplied',
             'not selected', 'not specified', 'unresolved', 'open decision',
             'no approved', 'not confirmed', 'unspecified', 'requires confirmation'))
             and not low.endswith((' nc', ' n/c')) and len(s)>3):
            return ('DEFINITIVE','Table heading, row key and column name complete the short field, status, scope, or outcome predicate.')
    if re.fullmatch(r'\(?[\w/.\-\s]{1,30}\)?',s) and not re.search(r'\b(?:required|shall|must|only|denied|immutable|append|async|read-only|forbid)\b',low):
        return ('LABEL_OR_VALUE','Short table value without independently testable predicate.')
    if re.search(r'\b(?:is a blocker|not implementation discretion|unresolved choice|cannot be inferred|must not infer)\b',low):return ('DEFINITIVE','Binding constraint on implementation inference.')
    if re.search(r'\b(?:must|shall|requires|required|cannot|never|do not|must not|only after|only if|before|without|no |deny|reject|retain|preserv|record|store|validat|return|enforc|support|guard|capture|recomput|limit|restrict|check|block|prohibit|immutable|append.only|versioned|approved|independent|scope|rollback|transaction|idempot|backoff|replay|fallback|separat|current|audit|signed|calibrat|clock|exclud|defer|include|show|display)\b',low):
        return ('DEFINITIVE','Explicit affirmative design commitment, guard, limit, or negative boundary.')
    if re.search(r'\b(?:is|are|has|have|uses|use|creates|contains|returns|reads|writes|provides|starts|ends|allows|ensures|receives|captures|follows|stores|exposes|sends|produce|delivers)\b',low):
        return ('DEFINITIVE','Descriptive but definitive design contract in confirmed section/context.')
    if ENDPOINT_RE.search(s) or re.search(r'`[^`]*`',text) or re.search(r'\b(?:RPO|RTO|SLO|P95|WCAG|TLS|RLS|OIDC|PKCE|ACL|MCP|A2A)\b',s):
        return ('DEFINITIVE','Concrete design interface, condition, or scoped requirement value.')
    return ('NONPROPOSITIONAL','No affirmative independently testable design commitment identified.')

# record exposed evidence and excluded status

def add_exclusion(filename, li, quote, category, reason, col=None, row_key=None, section=None, cell_idx=None):
    global exidx
    exidx+=1
    e={'excluded_unit_id':f'EXCL-GEN-{exidx:05d}', 'direction':'GENERATED',
       'source':{'file':filename,'line_start':li,'line_end':li,'quote_en':quote,
                 'section':section,'table_cell':col,'table_column_index':cell_idx,'table_row_key':row_key},
       'status':category,'eligibility_reason_en':reason,'eligible_for_prediction':False}
    excludes.append(e)
    return e['excluded_unit_id']

def add_atom(filename, li, snippet, original_full, section, table_cell=None, col_idx=None,
             table_row_key=None, row_context=None, heading=None, kind='PROSE'):
    s=clean_md(snippet)
    if not s:return None
    atom_id=f'GEN-{len(atoms)+1:05d}'
    code=ENDPOINT_RE.findall(s)
    fields=FIELD_RE.findall(snippet)
    codes=STATUS_RE.findall(s)
    role=filename[:2]
    # For tables, attach row key to short predicates and field/value cells.
    if table_cell and table_row_key and len(s)<125 and not s.startswith(table_row_key):
        stmt=f'{clean_md(table_row_key)} — {s}'
    else:stmt=s
    atom={
     'generated_id':atom_id,'method':'current_scored_8','protocol_version':'6.1',
     'atomic_statement_en':stmt,'evidence':{'file':filename,'line_start':li,'line_end':li,
        'quote_en':original_full,'quote_fragment_en':snippet,'table_cell':
        ({'row_line':li,'column_index':col_idx,'column_header_en':table_cell,'cell_quote_en':original_full,'row_key_en':table_row_key} if table_cell else None),
        'section_heading':section},
     'file':filename,'line_start':li,'line_end':li,'table_cell':(
         {'column_index':col_idx,'column_header_en':table_cell,'row_key_en':table_row_key} if table_cell else None),
     'heading_context_en':heading or section,
     'table_row_key_en':table_row_key,'table_row_cells_en':row_context if table_cell else None,'quote_en':original_full,'quote_fragment_en':snippet,
     'source_kind':kind,'definitive_eligibility':True,
     'context_inheritance_en':('Table heading/column/row establishes the actor, target or field scope.' if table_cell else 'Containing Markdown section establishes scope; source citations are not new requirements.'),
     'lookup_keys':{'endpoint_methods_paths':code,'field_names':sorted(set(fields)),'codes_and_statuses':sorted(set(codes)),'source_references':sorted(set(ID_RE.findall(s)))} }
    atoms.append(atom);return atom_id

def markdown_cells(line):
    s=line.strip();cells=[];buff='';code=False;escaped=False
    for c in s:
        if escaped: buff+=c;escaped=False;continue
        if c=='\\': escaped=True;buff+=c;continue
        if c=='`':code=not code
        if c=='|' and not code:
            cells.append(buff.strip());buff=''
        else:buff+=c
    cells.append(buff.strip())
    if s.startswith('|'):cells=cells[1:]
    if s.endswith('|'):cells=cells[:-1]
    return cells

def is_separator(cells):return bool(cells) and all(re.fullmatch(r':?-{3,}:?',x.strip()) for x in cells)

def split_cell(fragment,row_key,col_name,file):
    """Contextual independent fragments: delimiter clauses and selected fields."""
    text=fragment.strip()
    if not text:return []
    # Field catalog: one atomic field presence per table row, preserve relational owner.
    if file.startswith('03_data') and col_name.lower().startswith('record / field meaning') and re.match(r'^Case\s+`?title`?,\s*`?description`?',text):
        return [f'Case stores {field}' for field in ('title','description','priority','sensitivity label','status','owner','current approved result')]
    if file.startswith('03_data') and col_name.lower().startswith('exact selected field'):
        return [f'`{m}` is a selected field of `{clean_md(row_key).split()[0]}`' for m in FIELD_RE.findall(text)]
    if file.startswith('03_data') and col_name.lower().startswith('exact primary constraint'):
        return tokenize_pieces(text)
    # A method+path is one atomic operation; success mode, actor, method are distinct.
    parts=tokenize_pieces(text)
    if len(parts)==1 and len(parts[0])>100:
        # Split top-level explicit independent conjunctions marked by comma + new imperative,
        # or dot when it is a complete sentence and has a subject.
        pieces=[]
        for p in parts:
            q=re.split(r',\s+(?=(?:do not|must|never|no |return|reject|preserve|record|verify|recheck|block|validate|store|use |keep |show |capture|replay|reviewer|the |a |only |and (?:never|no |must))\b)',p,flags=re.I)
            pieces.extend([v.strip() for v in q if v.strip()])
        if len(pieces)>1 and all(len(z)>16 for z in pieces):parts=pieces
    return parts

def process_file(filename):
    lines=(ROOT/filename).read_text(encoding='utf-8').splitlines()
    section=[]; code=None; code_lang=''; table_header=[]; in_table=False
    counts=collections.Counter()
    for li,line in enumerate(lines,1):
        raw=line.strip(); code_type=''
        if re.match(r'^#{1,6}\s+',raw):
            lvl=len(raw)-len(raw.lstrip('#'))
            section=section[:lvl-1]+[raw.lstrip('#').strip()]
            ids=[add_exclusion(filename,li,line,'HEADING','Section title establishes context but is not independently scored.',section=' / '.join(section))]
            line_coverage.append({'file':filename,'line':li,'kind':'HEADING','nonblank':True,'atoms':[],'exclusions':ids,'cells':[]})
            counts['headings']+=1;in_table=False;table_header=[];continue
        sec=' / '.join(section)
        if not raw:
            line_coverage.append({'file':filename,'line':li,'kind':'BLANK','nonblank':False,'atoms':[],'exclusions':[],'cells':[]})
            continue
        if raw.startswith('```'):
            if code is None: code=li;code_lang=raw[3:].strip().lower();code_type='START'
            else:code_type='END';code=None;code_lang=''
            ids=[add_exclusion(filename,li,line,'CODE_FENCE','Markdown syntax boundary only.',section=sec)]
            line_coverage.append({'file':filename,'line':li,'kind':'CODE_FENCE_'+code_type,'nonblank':True,'atoms':[],'exclusions':ids,'cells':[]})
            continue
        if code is not None:
            # DDL reference is a binding source-selected SQL excerpt; JSON A2A example is not.
            if code_lang=='sql' and filename.startswith('03_data'):
                if raw.startswith(('CREATE TABLE','ALTER TABLE','CREATE POLICY','UNIQUE','CHECK','REFERENCES')):
                    s=raw
                else:s=raw
                if (re.search(r'(?:\b(?:id|tenant_id|workspace_id|status|revision|sensitivity|created_at|updated_at)\b\s+(?:UUID|TEXT|BIGINT|TIMESTAMPTZ))',s)
                   or 'UNIQUE (' in s or 'tenant_id = current_setting' in s or 'ENABLE ROW LEVEL SECURITY' in s):
                    pieces=[s.strip(',;')];n=[]
                    for p in pieces:n.append(add_atom(filename,li,p,line,sec,kind='NORMATIVE_SQL'))
                    line_coverage.append({'file':filename,'line':li,'kind':'NORMATIVE_SQL','nonblank':True,'atoms':n,'exclusions':[],'cells':[]});counts['claims']+=len(n);continue
            ids=[add_exclusion(filename,li,line,'ILLUSTRATIVE_CODE_OR_DIAGRAM','Example payload, code syntax, or explanatory diagram is not independently adopted executable behavior.',section=sec)]
            line_coverage.append({'file':filename,'line':li,'kind':'CODE_NONNORMATIVE','nonblank':True,'atoms':[],'exclusions':ids,'cells':[]});counts['code_excluded']+=1;continue
        if raw.startswith('|') and len(markdown_cells(raw))>=2:
            cs=markdown_cells(raw)
            if is_separator(cs):
                ids=[add_exclusion(filename,li,line,'TABLE_HEADER_SEPARATOR','Markdown table separator is syntax.',section=sec)]
                line_coverage.append({'file':filename,'line':li,'kind':'TABLE_SEPARATOR','nonblank':True,'atoms':[],'exclusions':ids,'cells':[]});continue
            if not in_table:
                table_header=cs;in_table=True
                ids=[add_exclusion(filename,li,line,'TABLE_HEADER','Table column names provide inherited context.',section=sec)]
                line_coverage.append({'file':filename,'line':li,'kind':'TABLE_HEADER','nonblank':True,'atoms':[],'exclusions':ids,'cells':[]});continue
            row_key=cs[0].strip();statuses=next((c for c in cs if c.strip() in ('TBD','Needs confirmation','Unadopted proposal','Proposal','Pending','Resolved')), '')
            ad_nonclaim_section=filename.startswith('08_architecture_decision') and any(x in sec for x in ('Citation convention','Cross-Specification Conflicts and Pending Decisions','Review coverage and traceability','Missing evidence and confirmation sources','Dependency-implied confirmation order'))
            if ad_nonclaim_section:
                ids=[add_exclusion(filename,li,cell,'ARCHITECTURE_REGISTER_CONTEXT','An alias, comparison of unresolved positions, or proposed confirmation order is register context rather than a newly approved standalone product commitment.',col=(table_header[j] if j<len(table_header) else f'Column {j+1}'),row_key=row_key,section=sec,cell_idx=j+1) for j,cell in enumerate(cs) if cell.strip()]
                line_coverage.append({'file':filename,'line':li,'kind':'TABLE_ROW_UNRESOLVED_CONTEXT','nonblank':True,'atoms':[],'exclusions':ids,'cells':[{'column_index':j+1,'column':table_header[j] if j<len(table_header) else f'Column {j+1}','class':'EXCLUDED_REGISTER_CONTEXT','atoms':[],'exclusions':[ids[k]]} for k,j in enumerate([j for j,x in enumerate(cs) if x.strip()])]})
                counts['table_rows']+=1
                continue
            ad_unresolved=filename.startswith('08_architecture_decision') and 'Unresolved Items' in sec
            # If a table changes layout but no heading, reset best effort on mismatch
            if len(cs)!=len(table_header) and len(cs)>len(table_header):
                table_header += [f'Column {j+1}' for j in range(len(table_header),len(cs))]
            row_atoms=[];row_ex=[];cells_audit=[]
            for idx,cell in enumerate(cs):
                col=table_header[idx] if idx<len(table_header) else f'Column {idx+1}'
                if not cell.strip():continue
                is_row_key=(idx==0)
                is_id_only=is_row_key and (re.match(r'^\s*(?:API|DAT|BAT|BR|SCR|SF|ERR|FLOW|AD|TST|RES|T|SEC)-\d+',cell) or len(cell)<45)
                pieces=split_cell(cell,row_key,col,filename)
                if is_id_only and len(cs)>1:
                    ex=add_exclusion(filename,li,cell,'ROW_KEY_CONTEXT','Row key supplies target/scope and is not independently duplicated as a claim.',col=col,row_key=row_key,section=sec,cell_idx=idx+1)
                    row_ex.append(ex);cells_audit.append({'column_index':idx+1,'column':col,'class':'ROW_KEY_CONTEXT','atoms':[],'exclusions':[ex]});continue
                atom_ids=[];ex_ids=[]
                for frag in pieces:
                    category,reason=classify(frag,filename,sec,col,statuses,ad_unresolved,from_table=True)
                    if category=='DEFINITIVE':
                        atom_id=add_atom(filename,li,frag,cell,sec,col,idx+1,row_key,cs,sec,'TABLE_CELL')
                        atom_ids.append(atom_id);row_atoms.append(atom_id)
                    else:
                        ex=add_exclusion(filename,li,frag,category,reason,col=col,row_key=row_key,section=sec,cell_idx=idx+1)
                        ex_ids.append(ex);row_ex.append(ex)
                if not pieces:
                    ex=add_exclusion(filename,li,cell,'EMPTY_CELL','Blank or nonclaim table cell.',col=col,row_key=row_key,section=sec,cell_idx=idx+1)
                    ex_ids.append(ex);row_ex.append(ex)
                cells_audit.append({'column_index':idx+1,'column':col,'class':'PARTIAL_ELIGIBILITY' if atom_ids and ex_ids else ('DEFINITIVE' if atom_ids else 'EXCLUDED'), 'atoms':atom_ids,'exclusions':ex_ids})
            line_coverage.append({'file':filename,'line':li,'kind':'TABLE_ROW','nonblank':True,'atoms':row_atoms,'exclusions':row_ex,'cells':cells_audit})
            counts['table_rows']+=1;counts['claims']+=len(row_atoms);continue
        in_table=False;table_header=[]
        if raw.startswith('---') and not re.search(r'\w',raw):
            ids=[add_exclusion(filename,li,line,'MARKDOWN_DIVIDER','Visual separator.',section=sec)]
            line_coverage.append({'file':filename,'line':li,'kind':'DIVIDER','nonblank':True,'atoms':[],'exclusions':ids,'cells':[]});continue
        text=re.sub(r'^(?:[-*+]\s+|\d{1,3}[.)]\s+)','',raw).strip()
        pieces=tokenize_pieces(text)
        if not pieces:pieces=[text]
        row_atoms=[];row_ex=[]
        for piece in pieces:
            cat,why=classify(piece,filename,sec,from_ad=filename.startswith('08_architecture_decision') and 'Unresolved Items' in sec)
            if cat=='DEFINITIVE':
                aid=add_atom(filename,li,piece,line,sec,kind='PROSE');row_atoms.append(aid)
            else:
                ex=add_exclusion(filename,li,piece,cat,why,section=sec);row_ex.append(ex)
        line_coverage.append({'file':filename,'line':li,'kind':'PROSE','nonblank':True,'atoms':row_atoms,'exclusions':row_ex,'cells':[]})
        counts['prose_lines']+=1;counts['claims']+=len(row_atoms)
    return counts

for f in FILES: grouped.append((f,process_file(f)))

# Semantic classes: deterministic normalized full predicate; joins guarded by surface/target.
def normalized_core(s):
    s=clean_md(s).lower()
    s=re.sub(r'\b(?:confirmed|as confirmed|the source|the following|for this application|is the same|again|additionally)\b',' ',s)
    s=re.sub(r'(?:\[(?:pp?\.|source:)[^\]]*\]|\b(?:pp?\.)\s*\d+[–-]?\d*)',' ',s)
    s=re.sub(r'\b(?:shall|must|should)\b','requires',s)
    s=re.sub(r'\b(?:never|does not|must not|shall not|do not)\b','forbids',s)
    s=re.sub(r'\b(?:all|every|each)\b','every',s)
    s=re.sub(r'\b(?:records|recorded|recording)\b','record',s)
    s=re.sub(r'\b(?:retains|retained|retention)\b','retain',s)
    s=re.sub(r'\b(?:checks|checked|checking)\b','check',s)
    s=re.sub(r'\b(?:validates|validated|validation)\b','validate',s)
    s=re.sub(r'\b(?:returns|returned|response)\b','return',s)
    s=re.sub(r'\b(?:requires|is required|is mandatory)\b','require',s)
    s=re.sub(r'\b(?:cannot|not allowed|unauthorized)\b','forbids',s)
    s=re.sub(r'\s+',' ',re.sub(r'[^a-z0-9_/@.{}:+-]+',' ',s)).strip()
    return s

def scope_signature(a):
    s=a['atomic_statement_en'].lower(); refs=ENDPOINT_RE.findall(s)
    exact_literals=set(re.findall(r'`([^`]+)`',a['quote_fragment_en']))
    exact_literals={x for x in exact_literals if re.search(r'[_/@.]|\d',x)}
    field_anchor=re.search(r'\b([a-z][a-z0-9_]*)\s+(?:is a selected field of|UUID|BIGINT|TEXT|TIMESTAMPTZ)', s)
    if field_anchor:exact_literals.add('FIELD_ANCHOR:'+field_anchor.group(1))
    # Product scopes are significant. Same general rule in two different docs
    # merges only when the proposition itself matches, not just same named topic.
    return {'endpoints':tuple(sorted(refs)), 'literals':tuple(sorted(exact_literals)),
      'numbers':tuple(sorted(re.findall(r'\b\d+(?:\.\d+)?\b',s))),
      'polarity':'PROHIBITION' if re.search(r'\b(?:never|must not|do not|cannot|forbidden|no )\b',s) else 'AFFIRMATIVE'}

classes=[]; by_key={}; atom_classes={}
for a in atoms:
    core=normalized_core(a['atomic_statement_en'])
    sig=scope_signature(a)
    # Avoid accidental merging separate fields/paths even when statements superficially alike.
    exact=(core,sig['endpoints'],sig['literals'],sig['numbers'],sig['polarity'])
    if exact in by_key:
        cls=classes[by_key[exact]];cls['generated_occurrence_ids'].append(a['generated_id']);cls['occurrences'].append({'generated_id':a['generated_id'],'file':a['file'],'line_start':a['line_start'],'table_cell':a['table_cell']})
        cls['merge_proofs_en'].append({'generated_id':a['generated_id'],'rule':'EXACT_NORMALIZED_PREDICATE','reason_en':'Identical normalized wording, target literals, endpoint, numerical and polarity predicates.'})
    else:
        cid=f'GCLASS-{len(classes)+1:05d}'; by_key[exact]=len(classes)
        cls={'generated_class_id':cid,'method':'current_scored_8','protocol_version':'6.1',
         'canonical_statement_en':a['atomic_statement_en'], 'canonical_normalized_key':core,
         'representative_generated_id':a['generated_id'],
         'generated_occurrence_ids':[a['generated_id']],
         'occurrences':[{'generated_id':a['generated_id'],'file':a['file'],'line_start':a['line_start'],'table_cell':a['table_cell']}],
         'inherited_scope_en':a['heading_context_en'],'signature':sig,
         'merge_proofs_en':[],'semantic_merge_mode':'EXACT_NORMALIZED_AND_GUARDED',
         'cross_file_equivalence_status':'NOT_ASSERTED_WITHOUT_FULL_PREDICATE_EVIDENCE'}
        classes.append(cls)
    a['generated_class_id']=cls['generated_class_id']

# Second, transparent conservative same-file/cross-file near-duplicate merge.
# Only for relatively self-contained claims with identical key target/literals/number and extremely close surface predicates.
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.neighbors import NearestNeighbors
    texts=[c['canonical_normalized_key'] for c in classes]
    vec=TfidfVectorizer(analyzer='char',ngram_range=(3,5),min_df=1,max_features=220000,sublinear_tf=True)
    X=vec.fit_transform(texts)
    nbrs=NearestNeighbors(metric='cosine',algorithm='brute',n_jobs=-1).fit(X)
    dist,inds=nbrs.kneighbors(X,n_neighbors=min(10,len(classes)),return_distance=True)
    # union-find preserves first-seen representative
    par=list(range(len(classes)))
    def find(i):
        while par[i]!=i:par[i]=par[par[i]];i=par[i]
        return i
    def union(x,y):
        a,b=find(x),find(y)
        if a!=b:par[max(a,b)]=min(a,b)
    plausible=[]
    for i in range(len(classes)):
        A=classes[i];sa=A['signature']
        for d,j in zip(dist[i,1:],inds[i,1:]):
            j=int(j)
            if i==j or j<i or d>0.12:continue
            B=classes[j];sb=B['signature']
            if sa!=sb:continue
            # Require nearly identical entire natural-language predicate, including modality.
            p=SequenceMatcher(None,A['canonical_normalized_key'],B['canonical_normalized_key']).ratio()
            # The non-negotiable condition is equivalent full-predicate content;
            # order changes are allowed only under guarded lexical evidence.
            tok_a=set(re.findall(r'[a-z0-9_]+',A['canonical_normalized_key']))
            tok_b=set(re.findall(r'[a-z0-9_]+',B['canonical_normalized_key']))
            jacc=len(tok_a&tok_b)/max(1,len(tok_a|tok_b))
            protected={'unless','before','after','only','without','never','no','except','must','shall','may','can','per',
                       'analyst','reviewer','admin','owner','tenant','workspace','case','cases','run','runs','document','documents','model','tool','approval','publish'}
            if (tok_a & protected)!=(tok_b & protected):continue
            if p<0.86 or jacc<0.70:continue
            if max(len(A['canonical_normalized_key']),len(B['canonical_normalized_key']))>170 and (p<0.955 or jacc<0.90):continue
            # Do not merge terse cells under different row/section contexts.
            if min(len(A['canonical_normalized_key']),len(B['canonical_normalized_key']))<65:
                if A['inherited_scope_en']!=B['inherited_scope_en']:continue
            # A true near-match requires same explicit identifiers even when one cell is contextual.
            ids_a=set(ID_RE.findall(A['canonical_statement_en']));ids_b=set(ID_RE.findall(B['canonical_statement_en']))
            if ids_a!=ids_b and (ids_a or ids_b):continue
            union(i,j);plausible.append({'pair':[A['generated_class_id'],B['generated_class_id']],'cosine':round(1-float(d),5),'sequence_ratio':round(p,5),'token_jaccard':round(jacc,5),'decision':'MERGE_EXACT_SCOPE_NEAR_PARAPHRASE'})
    merged=collections.defaultdict(list)
    for i in range(len(classes)):merged[find(i)].append(i)
    new=[]; cls_remap={}
    for root,idxs in sorted(merged.items()):
        c=classes[root]
        for i in idxs:
            cls_remap[classes[i]['generated_class_id']]=c['generated_class_id']
            if i==root:continue
            other=classes[i]
            c['generated_occurrence_ids']+=other['generated_occurrence_ids']
            c['occurrences']+=other['occurrences']
            c['merge_proofs_en']+=other['merge_proofs_en']
            c['merge_proofs_en'].append({'absorbed_class_id':other['generated_class_id'],'rule':'VERY_HIGH_SIMILARITY_VERIFIED_SCOPE','reason_en':'Full normalized predicate near-identical, with matching endpoint/literal/numeric/polarity signatures and identical explicit identifiers.'})
            c['semantic_merge_mode']='EXACT_AND_HIGH_CONFIDENCE_PARAPHRASE'
        new.append(c)
    classes=new
    for a in atoms:a['generated_class_id']=cls_remap[a['generated_class_id']]
    for c in classes:
        c['occurrences'].sort(key=lambda o:(FILES.index(o['file']),o['line_start'],o['table_cell']['column_index'] if o['table_cell'] else 0,o['generated_id']))
        c['generated_occurrence_ids']=[o['generated_id'] for o in c['occurrences']]
        c['representative_generated_id']=c['generated_occurrence_ids'][0]
except Exception as err:
    plausible=[{'decision':'SKIPPED_NEAR_PARAPHRASE','reason_en':str(err)}]

# Build duplicate representative/class ledger (all class rows explicitly included)
dups=[]; within=0;across=0;repeated=0;spanning=0
for c in classes:
    occ=c['occurrences']; seen_files=set(); excess=[]
    for i,o in enumerate(occ):
        if i==0:seen_files.add(o['file']);continue
        where='within_file' if o['file'] in seen_files else 'across_file'
        if where=='within_file':within+=1
        else:across+=1
        excess.append({'generated_id':o['generated_id'],'file':o['file'],'line_start':o['line_start'],'table_cell':o['table_cell'],'partition':where,
        'reason_en':'Same class full-predicate assertion repeated after the earliest canonical occurrence.'})
        seen_files.add(o['file'])
    if excess:repeated+=1
    if len(set(x['file'] for x in occ))>1:spanning+=1
    d={'generated_class_id':c['generated_class_id'],'canonical_statement_en':c['canonical_statement_en'],
       'representative_generated_id':c['representative_generated_id'],
       'occurrence_count':len(occ),'eligible_occurrences':occ,
       'excess_count':len(excess),'excess_occurrences_with_partition':excess,
       'spans_multiple_files':len({x['file'] for x in occ})>1,
       'merge_reason_en':'Only identical guarded normalized propositions or narrowly checked near-equivalent predicates are merged; differing constraints, action, scope, or statuses remain separate.'}
    dups.append(d)

# Lookup index: full-text keys against original generated IDs and all 8 files.
idx=collections.defaultdict(set)
for a in atoms:
    keys=a['lookup_keys'];
    for category,values in keys.items():
        for val in values:idx[f'{category}:{val.lower()}'].add(a['generated_id'])
    for token in set(TOKEN_RE.findall(normalized_core(a['atomic_statement_en']))):
        if len(token)>=4 and token not in {'from','that','this','where','with','which','after','before','must','required','source','their','about','same','never','only','have','will','remain'}:
            idx['word:'+token.lower()].add(a['generated_id'])
lookup={'method':'current_scored_8','source':'eight actual uploaded Markdown files',
 'normalization':'case-insensitive exact literal keys plus normalized English tokens; postings list all matching definitive occurrences',
 'keys':{k:sorted(v) for k,v in sorted(idx.items())}}

# File-scoped coverage and exceptions
file_stats=[]
for f,ct in grouped:
    lines=(ROOT/f).read_text().splitlines()
    entries=[x for x in line_coverage if x['file']==f]
    claims=[a for a in atoms if a['file']==f]
    excl=[e for e in excludes if e.get('direction')=='GENERATED' and e['source']['file']==f]
    table_cells=sum(len(x['cells']) for x in entries)
    cell_without_decision=sum(1 for x in entries for cell in x['cells'] if not cell['atoms'] and not cell['exclusions'])
    file_stats.append({'filename':f,'role':f[:2], 'bytes':(ROOT/f).stat().st_size,'sha256':hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),
      'physical_lines':len(lines), 'nonblank_lines':sum(bool(x.strip()) for x in lines),
      'lines_covered':len(entries),'substantive_table_cells_reviewed':table_cells,
      'table_cells_without_decision':cell_without_decision,
      'eligible_generated_occurrences':len(claims),'generated_exclusions':len(excl),
      'table_row_count':ct['table_rows'],'code_excluded':ct['code_excluded'],
      'status':'FULL_LINE_AND_TABLE_CELL_COVERAGE_BEST_EFFORT_SEMANTIC'})

# Schema audit and output
assert len(line_coverage)==sum(x['physical_lines'] for x in file_stats)
assert len(atoms)==sum(x['eligible_generated_occurrences'] for x in file_stats)
assert sum(len(c['generated_occurrence_ids']) for c in classes)==len(atoms)
assert len({a['generated_id'] for a in atoms})==len(atoms)
assert sum(d['excess_count'] for d in dups)==len(atoms)-len(classes)
assert within+across==len(atoms)-len(classes)
assert not any(x['table_cells_without_decision'] for x in file_stats)
assert all(a['generated_class_id'] in {c['generated_class_id'] for c in classes} for a in atoms)
assert all(e.get('source',{}).get('file') in FILES for e in excludes if e.get('direction')=='GENERATED')

def dump_jsonl(name, obj):
    with open(OUT/name,'w',encoding='utf-8') as ff:
        for row in obj: ff.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
def dump_json(name, obj):
    with open(OUT/name,'w',encoding='utf-8') as ff:json.dump(obj,ff,ensure_ascii=False,indent=2);ff.write('\n')
dump_jsonl('02_generated_atoms_final.jsonl',atoms)
dump_jsonl('02_generated_classes_final.jsonl',classes)
dump_jsonl('04_duplicate_classes_final.jsonl',dups)
dump_jsonl('09_excluded_units.jsonl',excludes)
dump_jsonl('02_generated_line_and_cell_coverage_final.jsonl',line_coverage)
dump_jsonl('02_generated_exclusions_final.jsonl',[e for e in excludes if e.get('direction')=='GENERATED'])
dump_jsonl('02_high_similarity_merges_final.jsonl',plausible)
dump_json('02_canonical_lookup_index_final.json',lookup)

metrics={
 'phase':2,'protocol_version':'6.1','method':'current_scored_8',
 'phase_status':'PHASE_COMPLETED_BEST_EFFORT','semantic_certification':'NOT_CERTIFIED_BEST_EFFORT',
 'source_positive_inventory_reused_unchanged':1024,'source_negative_controls_reused_unchanged':37,
 'generated_eligible_occurrences':len(atoms),'raw_generated_semantic_classes':len(classes),
 'raw_duplicate_excess':len(atoms)-len(classes),
 'duplicate_rate_provisional':((len(atoms)-len(classes))/len(atoms) if atoms else None),
 'repeated_claim_class_count':repeated,'repeated_classes_spanning_multiple_files':spanning,
 'within_file_excess':within,'across_file_excess':across,
 'generated_exclusion_records':len(excludes)-len(sources),
 'previous_phase_source_exclusion_record_count':len(sources),
 'total_line_coverage':len(line_coverage),
 'total_nonblank_lines':sum(x['nonblank_lines'] for x in file_stats),
 'total_table_cells_reviewed':sum(x['substantive_table_cells_reviewed'] for x in file_stats),
 'total_table_cells_without_decision':sum(x['table_cells_without_decision'] for x in file_stats),
 'files':file_stats,'phase3_not_started':True,
 'limitations':[
 'Automated clause segmentation and conservative near-paraphrase clustering cannot independently certify full-predicate semantic equivalence.',
 'Some compound Markdown cells are retained as a single scoped proposition if further division would risk losing actor/condition/outcome context.',
 'Cross-document differently worded semantic duplicates may remain split; high lexical similarity alone is not sufficient to merge them.',
 'Status-based exclusions in unresolved decision rows may omit a separable definitive subclaim; reviewed candidates and source line locations are retained for later correction.',
 'The generated claims have not yet been scored against the authoritative PDF. This phase creates no TP/TN/FP/FN scores.'
 ]}
dump_json('02_phase_status_final.json',metrics)
dump_json('02_generated_corpus_coverage_final.json',{'phase':2,'protocol_version':'6.1','source_md_input_files':file_stats,
 'source_md_not_modified':True,'current_pdf_positive_source_atoms':1024,'current_pdf_negative_controls':37,
 'line_cell_coverage_reconciles':True,'semantic_certification':'NOT_CERTIFIED_BEST_EFFORT'})

report=f'''# Phase 2 — Generated Corpus Atomization and Raw Semantic Deduplication

**Protocol:** 6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method label:** `current_scored_8` (exactly one complete uploaded eight-document set; generation method not inferred)  
**Input basis:** The eight actual Markdown files listed below, unmodified.  

## Extracted occurrence and class universe

| Measure | Count |
|---|---:|
| Eligible definitive generated occurrences (G_O) | {len(atoms):,} |
| Conservative raw semantic classes (G_C) | {len(classes):,} |
| Duplicate excess occurrences | {len(atoms)-len(classes):,} |
| Provisional raw duplicate fraction | {metrics['duplicate_rate_provisional']:.4%} |
| Duplicate excess within file | {within:,} |
| Duplicate excess across files | {across:,} |
| Repeated classes | {repeated:,} |
| Repeated classes spanning files | {spanning:,} |
| Excluded generated fragments/cells | {len(excludes)-len(sources):,} |
| Covered physical input lines | {len(line_coverage):,} |
| Reviewed substantive table cells | {metrics['total_table_cells_reviewed']:,} |

The class count is a raw within-method semantic-claim count, not the projected canonical positive prediction count from the later evaluation phases. No source/target entailment judgments or confusion matrix are created here.

## Input line and table-cell coverage

| Actual unmodified input filename | Physical lines | Reviewed table cells | Eligible occurrences | Excluded fragments |
|---|---:|---:|---:|---:|
'''
for st in file_stats:
    report+=f"| `{st['filename']}` | {st['physical_lines']:,} | {st['substantive_table_cells_reviewed']:,} | {st['eligible_generated_occurrences']:,} | {st['generated_exclusions']:,} |\n"
report+='''
Every physical line is classified in `02_generated_line_and_cell_coverage_final.jsonl`. For each Markdown table data row, each nonblank cell has an explicit eligible/excluded outcome, column position and inherited row/heading context. Physical line references and exact source quotations are retained in the occurrence ledger. Open-question columns, unadopted proposals, bare headings, source citations, example code and illustration-only diagrams are excluded with locator-level reasons.

## Raw class construction and bounded uncertainty

Initial duplicate merges require exactly the same guarded normalized English predicate and the same protected path, code literal, numeric and prohibition signatures. A separate very-high-similarity pass only merges near-identical full predicates whose literal/signature and identifier scopes agree. This is intentionally conservative: it favors separate classes rather than claiming unsupported equivalence. `02_high_similarity_merges_final.jsonl` lists those decisions. Every class refers to actual `GEN-*` occurrences, and each eligible occurrence belongs to one and only one class.

A `Resolved` claim in the architectural decision register may express a definitive constraint, but `TBD`, `Needs confirmation`, `Proposal` and `Unadopted proposal` do not become implementation authority. Where a sentence mixes confirmed requirements and unresolved implementation detail, only independently separable confirmed material is eligible. The exact original line and cells remain available for challenge.

## Invariants and future semantic evaluation

- `sum(class occurrence counts) = |G_O|`.
- `|G_O| - |G_C| = within-file excess + across-file excess`.
- All eight files, every physical line and every nonblank table-data cell have logged classifications.
- The Phase 1 PDF-positive `R` and fixed PDF-negative `N` inventories are not modified.
- Phase 3 is not performed. No generated item is declared PDF-entailed or unsupported in this phase.

**Accuracy limit:** The parser applies explicit classification and high-specificity normalized deduplication, not an independently human-certified semantic equivalence audit. A compound rule may retain multiple predicates for later comparison, and strongly paraphrased duplicates may be undermerged. These are visible `BEST_EFFORT` limitations rather than verified complete semantic duplication estimates. Phase 5 is the designated correction phase.

## Deliverable files

- `02_generated_atoms_final.jsonl`: source-located definitive generated occurrences.
- `02_generated_classes_final.jsonl`: every raw generated semantic class and its membership.
- `04_duplicate_classes_final.jsonl`: occurrence-by-class duplication and exact within/across partition.
- `02_generated_exclusions_final.jsonl`: generated nondefinitive/excluded cells with reasons.
- `09_excluded_units.jsonl`: retained Phase 1 PDF exclusion records plus generated exclusions.
- `02_generated_line_and_cell_coverage_final.jsonl`: full physical line/table-cell inspection ledger.
- `02_canonical_lookup_index_final.json`: literal, endpoint, code, field, identifier and normalized-token lookup index for later bidirectional retrieval.
- `02_high_similarity_merges_final.jsonl`: guarded approximate-merge decisions.
- `02_generated_corpus_coverage_final.json`: input hashes and coverage checks.
- `02_phase_status_final.json`: execution limits, counts, and audit limitations.
- `build_phase2.py`: reproducible extraction and partition script.
'''
(OUT/'02_generated_corpus_audit_final.md').write_text(report,encoding='utf-8')
print(json.dumps({'status':metrics['phase_status'],'occurrences':len(atoms),'classes':len(classes),'exclusions':len(excludes)-len(sources),'lines':len(line_coverage),'table_cells':metrics['total_table_cells_reviewed'],'within':within,'across':across,'class_merged_pairs':len(plausible)},indent=2))
