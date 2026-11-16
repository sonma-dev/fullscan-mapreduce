#!/usr/bin/env python3
"""Phase 2: best-effort exhaustive cell/line inspection and source-grounded raw claim extraction.
All generated deliverables use English. No PDF is used to create generated commitments.
"""
import re, json, hashlib, unicodedata, collections, math, os
from pathlib import Path
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

ROOT=Path('/mnt/data'); OUT=ROOT/'orion_phase2'; OUT.mkdir(exist_ok=True)
FILES=[
'01_screen_functions(1).md','02_api(1).md','03_data(1).md',
'04_batch_functions(1).md','05_business_rules(1).md',
'06_exception_handling(3).md','07_processing_flows(2).md','08_architecture_decision(2).md']
METHOD='supplied_eight_file_set'
META_COL=re.compile(r'^(?:id|job id|api id|data id|flow id|rule id|exception id|field id|item id|conflict id|question id|source|status|status and source|source and status|status / source|evidence|source evidence|citation|status and evidence|related specification ids and evidence|related specifications and requirement ids|earlier (?:mapping|trace)|earlier specifications|reference|trace|related contracts|related references|related spec(?:ification)?s|open(?:ing)? (?:decision|question)|questions to confirm|question|needs confirmation|missing interface|reason for remaining unresolved|impact and pending confirmation|affected scope and implementation gate|source / status)$',re.I)
IDONLY=re.compile(r'^(?:<a\s+[^>]*></a>\s*)?(?:(?:SCR|API|DAT|BAT|BR|ERR|FLOW|AD|OQ|CON|AC|SEC|TST|DAT-REL|DAT-COM|SCR-COM|FLOW-TX)[-\w/]+|\d{1,3}|[A-Z]-\d{2,3})\s*$',re.I)
EXCL_HEAD=re.compile(r'(?:consistency and open questions|open.decision register|proposal register|proposal status|unresolved items|source conflicts and required amendments|cross.specification conflicts|conflicts and required amendments|conflicts and pending decisions|dependencies and later handoffs|dependencies on later specifications|handoffs and dependencies|missing evidence and required confirmation|confirmation order implied|review coverage and complete open.question traceability|proposal.*dependencies|source conflicts|reconciliation.*questions|items resolved by the specifications|explicitly unadopted proposals|specification basis and status|specification basis and requirement status)',re.I)
EXCL_PREFIX=re.compile(r'^(?:\*\*)?(?:needs confirmation|proposal|unadopted proposal|tbd|open decision|open question|pending|unresolved(?:\s+decision)?)(?:\*\*)?(?:\s*[-—:]|\s*$)',re.I)
UNDEF=re.compile(r'\b(?:needs? confirmation|\bNC\b|\bTBD\b|unresolved|not specified|not established|undefined|not supplied|pending approval|to be defined|to confirm|not confirmed|remains open|not selected|unknown|requires confirmation|not yet approved)\b',re.I)
DEF_POS=re.compile(r'\b(?:must|shall|required|requires?|never|only|cannot|can\s*not|do not|does not|no\s+\w+\s+(?:may|shall|must)|prohibited|forbidden|reject|deny|validate|retain|record|store|persist|enforce|preserve|return|emit|publish|commit|create|read|write|use|apply|check|verify|capture|include|exclude|support|protect|limit|constrain|prevent|run|start|open|display|show|accept|handle|attach|derive|calculate|replay|route|process|perform|restore|report|close|reopen|delete|purge|advance|ensure|treat|maintain|provide|produce|contains?|consists?\s+of|is|are|may|can|should|supports?|confirmed)\b',re.I)
BIB_ONLY=re.compile(r'^\s*(?:\*\*?(?:Source|Sources|Related|Earlier|Trace|Source baseline|Reference|Status)(?:s)?\*\*?\s*:|\[DDS\]\s*:|\[\w[\w-]*\]\s*:)',re.I)
REF_ONLY=re.compile(r'^(?:\[?DDS\]?|\[?Source\]?|\[?\d+(?:[–-]\d+)?\]?|\[?pp?\.\s*\d+[-–,\d ]*\]?|\[?§\s*\d+(?:\.\d+)*\]?|[A-Za-z0-9_()./\-]+\.md(?:#[\w\-]+)?|[A-Za-z0-9_()./\-]+\.pdf)\s*$',re.I)
REGEX_TABLE_LINE=re.compile(r'^\s*\|')
SEPARATOR_RE=re.compile(r'^\s*\|[\s\-:|]+\|\s*$')
NUM_RE=re.compile(r'(?<!\w)(?:\d+(?:\.\d+)?\s*(?:MB|GB|ms|s|seconds|hours|days|%|tokens|calls|minutes|dimensions|retries|requests|per\s+\w+)|\d{3})\b',re.I)
PATH_RE=re.compile(r'(?:GET|POST|PUT|PATCH|DELETE)\s+/(?:v\d+|internal)/[A-Za-z0-9_{}./?&=\-]+|/(?:v\d+|internal)/[A-Za-z0-9_{}./?&=\-]+')
CODE_RE=re.compile(r'\b(?:[A-Z]{2,}(?:_[A-Z0-9]+)+|[A-Za-z]+(?:Created|Committed|Recorded|Requested|Advanced|Promoted|Deleted|Normalized|Verified)|TST-\d+|T-\d{2})\b')
ID_RE=re.compile(r'\b(?:SCR|API|DAT|BAT|BR|ERR|FLOW|AD|OQ|CON|AC|SEC|TST|EVT|REQ)[-_][A-Z0-9-]+\b',re.I)
BACKTICK=re.compile(r'`([^`]{1,180})`')

# Preserve Markdown pipe cell offsets; don't split escaped pipes or pipes within inline code.
def split_cells(line):
    cells=[]; buf=[]; escaped=False; incode=False
    for c in line:
        if c=='`' and not escaped: incode=not incode
        if c=='|' and not escaped and not incode:
            cells.append(''.join(buf).strip()); buf=[]
        else: buf.append(c)
        if c=='\\' and not escaped: escaped=True
        else: escaped=False
    cells.append(''.join(buf).strip())
    if len(cells)>=2 and cells[0]=='': cells=cells[1:]
    if cells and cells[-1]=='': cells=cells[:-1]
    return cells

def clean(s):
    s=re.sub(r'<a\s+[^>]*>\s*</a>',' ',s,flags=re.I)
    s=re.sub(r'\[([^\]]+)\]\([^()]*?\)',r'\1',s)
    s=re.sub(r'\[DDS\](?:\s*,?\s*pp?\.\s*[\d–\- ,;§.]+)?',' ',s)
    s=re.sub(r'(?<!\w)\*\*(?!\s)(.*?)(?<!\s)\*\*',r'\1',s)
    s=s.replace('\\|','|').replace('**','').replace('__','').replace('\\_','_')
    return re.sub(r'\s+',' ',s).strip(' \t\r\n')

def normalize(s):
    s=clean(s).lower().replace('’',"'")
    s=re.sub(r'\b(?:shall|is required to|are required to)\b','must',s)
    s=re.sub(r'\b(?:must not|shall not|is prohibited from|may not)\b','cannot',s)
    s=re.sub(r'\b(?:confirmed requirement|confirmed behavior|confirmed|source supported|source-confirmed)\b',' ',s)
    s=re.sub(r'\s*\[(?:dds|source)[^\]]*\]',' ',s)
    s=re.sub(r'(?<!\w)(?:scr|api|dat|bat|br|err|flow|ad|oq|con|ac)[-_](?:com[-_])?\d{1,4}(?:[-_][a-z0-9]+)?\b',' ',s)
    s=s.replace('`','').replace('**','')
    s=re.sub(r'[^\w/%:.?{}<>+=\- ]+',' ',s)
    s=re.sub(r'\s+',' ',s).strip(' .;:')
    return s

def valid_clause(s):
    x=clean(s)
    if len(x)<8 or x in ['—','-','None','N/A','NC','Confirmed','TBD','Unspecified','No','Yes','D','I','C','P','S','E','X']:
        return False,'SHORT_OR_PLACEHOLDER'
    if REF_ONLY.fullmatch(x) or IDONLY.fullmatch(x) or BIB_ONLY.match(x):
        return False,'CITATION_OR_IDENTIFIER_ONLY'
    if EXCL_PREFIX.match(x):return False,'OPEN_OR_PROPOSAL_CLAIM'
    if re.match(r'^(?:the )?source does not (?:confirm|define|establish|provide|specify)\b',x,re.I):return False,'ABSENT_SOURCE_CONTRACT_NOT_IMPLEMENTATION_COMMITMENT'
    if re.search(r'\bproposal\b',x,re.I) and not re.match(r'^(?:do not|never|must not|cannot)\b',x,re.I):return False,'PROPOSED_UNAPPROVED_MATERIAL'
    if UNDEF.search(x) and not re.match(r'^(?:do not|never|must not|cannot)\b',x,re.I):return False,'MIXED_UNRESOLVED_MATERIAL'
    if re.match(r'^(?:source|earlier|related|see|see also|based on|reference|sources|from|earlier trace|open:|dependencies|status)\s*:',x,re.I):return False,'CITATION_OR_METADATA'
    if re.search(r'\b(?:the source (?:does not|doesn.t|has not)|source (?:does not|doesn.t) (?:define|supply)|not (?:a|an|the) (?:confirmed|approved|selected)|not (?:defined|specified|provided|established)|needs to be (?:defined|confirmed)|requires (?:further )?confirmation|\bunresolved\b|\bunknown\b)\b',x,re.I):
        # May still be a meaningful negated prohibition if in front of the uncertain fragment.
        if not re.match(r'^(?:do not|must not|never|cannot)\b',x,re.I):return False,'UNRESOLVED_OR_META_ASSERTION'
    if re.match(r'^(?:OQ-|CON-|P-|AD-)\w+\b',x):return False,'REGISTER_ONLY'
    if len(x)>3000:return False,'LONG_CONTEXT_OR_REPRESENTATION'
    if re.fullmatch(r'(?:[A-Za-z]+[-_]\d+(?:[/,; ]+)?){1,12}',x):return False,'CROSS_REFERENCE_ONLY'
    if re.search(r'\b(?:no body described|no endpoint/guard/control provided|not defined in the source|no source supplied|no confirmed contract)\b',x,re.I):return False,'MISSING_CONTRACT_NOT_COMMITMENT'
    if len(x)<=16 and not (re.search(r'\b(?:201|202|200|409|422|429|404|UUID|BIGINT|TEXT|NOT NULL|PRIMARY KEY|UNIQUE|DEFAULT|INTERNAL|NEW)\b',x) or x.startswith('GET ') or x.startswith('POST ')):
        return False,'VALUE_WITHOUT_ASSERTION'
    return True,None

def split_clauses(text):
    # Use explicit semicolon and full-sentence boundaries; avoid splitting inline API code and decimals.
    txt=clean(text)
    txt=re.sub(r'^\s*(?:\d+[.)]|\*\s+|[-+]\s+)\s*','',txt)
    txt=re.sub(r'^(?:\*\*)?(?:Confirmed(?:\s+(?:behavior|requirement|rule|data|result))?|Procedure|Requirement|Outcome|Validation|Success)(?:\*\*)?\s*:\s*','',txt,flags=re.I)
    # Multi independent semicolon conditions; only split when semicolon separates substantive clauses.
    segs=re.split(r';\s+(?=(?:[A-Z`]|\b(?:and|no|do|must|the|a|each|only|when|for|if|source|current|where|in|with|without|before|after)\b))',txt)
    out=[]
    for seg in segs:
        parts=re.split(r'(?<=[.!?])\s+(?=(?:[A-Z][a-z]|`|\d+\.|No\s|Only\s|Do\s|Must\s|The\s))',seg)
        for x in parts:
            x=x.strip(' \t;')
            if x:out.append(x)
    return out

records=[]; excluded=[]; cover=[]; manifest=[]
counts=collections.defaultdict(lambda:collections.Counter())

for fi, filename in enumerate(FILES):
    data=(ROOT/filename).read_bytes()
    lines=data.decode('utf-8-sig').splitlines()
    manifest.append({'filename':filename,'role':f'{fi+1:02d}','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'physical_lines':len(lines)})
    heads=['']*6; current_table=None; in_fence=False; fence_lang=''; prev_header=''; table_row_no=0
    for li,raw in enumerate(lines,1):
        s=raw.strip()
        heading=re.match(r'^(#{1,6})\s+(.*)',s)
        if heading:
            lev=len(heading.group(1)); heads[lev-1]=clean(heading.group(2))
            for k in range(lev,6):heads[k]=''
        context=' > '.join([h for h in heads if h]); major=heads[1]; own=heads[-1] or heads[2]
        bad_section=bool(EXCL_HEAD.search(context)) or (fi==7 and ('Unresolved Items' in context or 'Open-Decision' in context or ('How to Use This Document' in context and 'Work That Can Proceed' not in context)))
        def record_coverage(unit_kind,idx,text,status,reason=None,refs=None,header=None,row=None):
            cov={'file':filename,'line':li,'unit_kind':unit_kind,'cell_index':idx,'header':header,'row_anchor':row,'text_en':text,'inspection_status':status,'reason_code':reason,'generated_occurrence_ids':refs or []}
            cover.append(cov)
            counts[filename][f'{unit_kind}:{status}']+=1
            if status=='EXCLUDED_NONDEFINITIVE' and text.strip():excluded.append({'file':filename,'line_start':li,'line_end':li,'table_cell':None if idx is None else {'column_index':idx,'header':header,'row_anchor':row},'quote_en':text,'exclusion_reason':reason,'section_context':context})
            return cov
        def add_claim(clause,quote,unit_type,colidx=None,colhdr=None,row_anchor=None,field_target=None,conditional_context=None,status='DEFINITIVE',code_lang=None):
            clause=clean(clause)
            ok,reason=valid_clause(clause)
            if not ok:return None,reason
            norm=normalize(clause)
            if len(norm)<5:return None,'EMPTY_NORMALIZATION'
            # Reconstruction retains inherited context for short, generic table values.
            ref_scope=clean(field_target or row_anchor or (heads[3] or heads[2] or heads[1]))
            if re.fullmatch(r'(?:SCR|API|DAT|BAT|BR|ERR|FLOW|AD)[-_][A-Z0-9-]+',ref_scope):ref_scope=clean(heads[2] or heads[1])
            conditional_context=clean(conditional_context or '')
            if conditional_context and norm!=normalize(conditional_context):
                statement=f'When {conditional_context}: {clause}'
            elif unit_type=='TABLE_CELL' and len(norm)<110 and ref_scope and normalize(ref_scope) not in norm:
                statement=f'{ref_scope}: {clause}'
            elif unit_type=='CODE' and ref_scope:
                statement=f'{ref_scope}: {clause}'
            else: statement=clause
            record={'method':METHOD,'file':filename,'file_order':fi,'line_start':li,'line_end':li,'table_cell':None if colidx is None else {'column_index':colidx,'column_header':colhdr,'row_anchor':row_anchor},'section_context':context,'unit_type':unit_type,'exact_quote_en':quote,'selected_clause_en':clause,'normalized_proposition_en':statement,'normalized_key':normalize(statement),'status':status,'scope_inherited_en':ref_scope or None,'conditional_context_en':conditional_context or None,'code_language':code_lang,'source_line_sha256':hashlib.sha256(raw.encode()).hexdigest()[:20]}
            records.append(record)
            return record,None

        if not s:
            record_coverage('BLANK',None,raw,'STRUCTURAL','BLANK_LINE');continue
        if heading:
            record_coverage('HEADING',None,raw,'CONTEXT_ONLY','HEADING_HIERARCHY');continue
        if s.startswith('```') or s.startswith('~~~'):
            if in_fence: in_fence=False;fence_lang=''
            else:in_fence=True;fence_lang=s[3:].strip().lower()
            record_coverage('FENCE',None,raw,'STRUCTURAL','CODE_FENCE');continue
        if in_fence:
            if bad_section or fence_lang in ['mermaid','plantuml','dot','text','jsonc']:
                record_coverage('CODE',None,raw,'EXCLUDED_NONDEFINITIVE','DIAGRAM_OR_UNRESOLVED_CODE');continue
            # Only accepted source-backed DDL/examples with meaningful assertions; exclude mere punctuation.
            if fence_lang in ['sql']:
                text=re.sub(r'(--.*$)|[,()]\s*$','',s).strip()
                if text.upper() in ['CREATE TABLE CASES','ALTER TABLE CASES ENABLE ROW LEVEL SECURITY','CREATE POLICY TENANT_SCOPE ON CASES USING',');',''] or text in ['{','}','[',']']:
                    if text.upper().startswith('ALTER TABLE'):r,_=add_claim(text,s,'CODE',code_lang=fence_lang)
                    else:r=None
                else:r,_=add_claim(text,s,'CODE',code_lang=fence_lang)
            elif fence_lang in ['http','json','yaml','yml']:
                # Example should not become invented production contract. Known case conflict shape can be evidence-only.
                r=None
            else:r=None
            record_coverage('CODE',None,raw,'EXTRACTED' if r else 'EXCLUDED_NONDEFINITIVE','REFERENCE_DDL_FIELD' if r else 'CODE_EXAMPLE_OR_SYNTAX',[r['occurrence_id']] if r and 'occurrence_id' in r else [])
            continue
        if SEPARATOR_RE.fullmatch(s):
            record_coverage('TABLE_SEPARATOR',None,raw,'STRUCTURAL','TABLE_RULE');continue
        if REGEX_TABLE_LINE.match(s):
            cells=split_cells(raw)
            if not cells:
                record_coverage('TABLE',None,raw,'EXCLUDED_NONDEFINITIVE','EMPTY_TABLE');continue
            # Header if next nonempty physical line is separator.
            nextline=lines[li] if li<len(lines) else ''
            is_header=bool(SEPARATOR_RE.fullmatch(nextline.strip()))
            if is_header:
                current_table={'headers':[clean(c) for c in cells],'start':li,'name':context,'row_no':0}
                for ci,c in enumerate(cells,1):record_coverage('TABLE_HEADER',ci,c,'CONTEXT_ONLY','TABLE_COLUMN_HEADING',header=clean(c))
                continue
            if current_table is None or len(cells)>len(current_table.get('headers',[]))+2:
                current_table={'headers':[f'column_{i}' for i in range(1,len(cells)+1)],'start':li,'name':context,'row_no':0}
            current_table['row_no']+=1
            headers=current_table['headers']; table_row_no=current_table['row_no']
            anchor_parts=[clean(c) for c in cells[:2] if clean(c)]
            row_anchor=' / '.join(anchor_parts)[:245]
            # first short identifier and next descriptive cell; derive context of field from closest heading.
            key=clean(cells[0]); second=clean(cells[1]) if len(cells)>1 else ''
            if IDONLY.fullmatch(key) and second:
                field_target=re.sub(r'^\w[-\w]{2,16}\s*[—–-]\s*','',second).split(' — ')[0].split(' – ')[0].strip()[:130]
            else:field_target=key[:145]
            conditional=None
            if any(re.search(r'^(?:condition|trigger|current state|failure or result|result condition|input condition|source condition|when|failure category|boundary/result|category|situation|event|state|precondition)$',clean(h),re.I) for h in headers[:2]):
                conditional=key
            for ci,c in enumerate(cells,1):
                h=clean(headers[ci-1]) if ci<=len(headers) else f'column_{ci}'
                cc=clean(c)
                if not cc:
                    record_coverage('TABLE_CELL',ci,c,'EXCLUDED_NONDEFINITIVE','EMPTY_CELL',header=h,row=row_anchor);continue
                if bad_section or (li<=30 and re.search(r'\b(?:specification basis|statuses|how to use)\b',context,re.I) and 'Work That Can Proceed' not in context):
                    record_coverage('TABLE_CELL',ci,c,'EXCLUDED_NONDEFINITIVE','UNRESOLVED_OR_PROPOSAL_REGISTER',header=h,row=row_anchor);continue
                if ci==1 and len(cells)>1:
                    record_coverage('TABLE_CELL',ci,c,'CONTEXT_ONLY','ROW_IDENTITY_OR_CONDITION_CONTEXT',header=h,row=row_anchor);continue
                if re.search(r'(?i)\b(?:status|source|reference|evidence|earlier|open question|trace|question|decision to confirm|gap|needs confirmation|unresolved|related|proposal|verification reference|citation|prerequisite to confirm|open contract)\b',h) and (not re.search(r'\b(?:result|response|expected outcome|type|behavior)\b',h,re.I) or re.search(r'\b(?:source|status|needs confirmation|unresolved|proposal|references|related|earlier|trace)\b',h,re.I)):
                    record_coverage('TABLE_CELL',ci,c,'EXCLUDED_NONDEFINITIVE','METADATA_OR_UNRESOLVED_COLUMN',header=h,row=row_anchor);continue
                if (h.lower() in ['contract category','category','item','specification file','identifier convention','event literal','field and meaning','parameter / datum','parameter','profile'] and len(cc)<55 and not DEF_POS.search(cc)) or META_COL.fullmatch(h):
                    record_coverage('TABLE_CELL',ci,c,'EXCLUDED_NONDEFINITIVE','METADATA_COLUMN',header=h,row=row_anchor);continue
                if re.search(r'acceptance|test|verification|boundary criteria',context,re.I) and re.search(r'^(?:scenario|prerequisite(?:s)?|input(?:s)?(?: / condition)?|trigger|test stimulus|preconditions? and action|test action|test setup|prerequisites / action|input / scenario|test id|test title)$',h,re.I):
                    record_coverage('TABLE_CELL',ci,c,'CONTEXT_ONLY','TEST_TRIGGER_CONTEXT_NOT_INDEPENDENT_IMPLEMENTATION_CLAIM',header=h,row=row_anchor);continue
                if EXCL_PREFIX.match(cc) or re.match(r'^(?:\*\*)?(?:Proposal|Needs confirmation|TBD|NC)\b',cc,re.I):
                    record_coverage('TABLE_CELL',ci,c,'EXCLUDED_NONDEFINITIVE','PROPOSAL_OR_UNAPPROVED_SUBCLAIM',header=h,row=row_anchor);continue
                if re.match(r'^(?:OQ|CON|P|AD)-[A-Z0-9-]+\s*:',cc) and UNDEF.search(cc):
                    record_coverage('TABLE_CELL',ci,c,'EXCLUDED_NONDEFINITIVE','REGISTER_REFERENCE',header=h,row=row_anchor);continue
                parts=split_clauses(cc)
                good=[]; reasons=[]
                for part in parts:
                    if EXCL_PREFIX.match(part) or (re.search(r'\bproposal\b',part,re.I) and not re.match(r'^(?:do not|never|must not|cannot)\b',part,re.I)) or re.match(r'^(?:\bno\b|the\s+)?(?:exact|complete|full|specific|actual|chosen|selected|approved|initial|default|physical|public|wire|complete|complete production).*\b(?:NC|unresolved|not supplied|unknown|not defined)\b',part,re.I) or (UNDEF.search(part) and not re.match(r'^(?:do not|must not|cannot|never|no\s+\w+\s+may)\b',part,re.I)):
                        reasons.append('NONDEFINITIVE_PARTIAL_CELL');continue
                    if not DEF_POS.search(part) and len(part)<24 and re.search(r'\b(?:mapping|example|screen|figure|source|chapter)\b',h,re.I):
                        reasons.append('NONASSERTIVE_CELL');continue
                    r,why=add_claim(part,c,'TABLE_CELL',ci,h,row_anchor,field_target,conditional if ci>1 and conditional else None)
                    if r:good.append(r)
                    else: reasons.append(why)
                if good:
                    record_coverage('TABLE_CELL',ci,c,'EXTRACTED','PARTIAL_CELL_WITH_OPEN_MATERIAL' if reasons else 'ELIGIBLE_DEFINITIVE',[],header=h,row=row_anchor)
                else:record_coverage('TABLE_CELL',ci,c,'EXCLUDED_NONDEFINITIVE',reasons[0] if reasons else 'NO_ELIGIBLE_DEFINITIVE_CLAUSE',header=h,row=row_anchor)
            continue
        # prose / lists
        if bad_section:
            record_coverage('PROSE',None,raw,'EXCLUDED_NONDEFINITIVE','UNRESOLVED_OR_PROPOSAL_SECTION');continue
        if s.startswith(('[DDS]:','[SCR-', '[API-', '[DAT-', '[BR-', '[BAT-', '[ERR-', '[FLOW-')):
            record_coverage('PROSE',None,raw,'EXCLUDED_NONDEFINITIVE','REFERENCE_DEF');continue
        if s.startswith(('[',)) and re.match(r'^\[[^\]]+\]:\s+',s):
            record_coverage('PROSE',None,raw,'EXCLUDED_NONDEFINITIVE','REFERENCE_DEF');continue
        if BIB_ONLY.match(s) or EXCL_PREFIX.match(s) or re.match(r'^(?:\*\*)?(?:Needs confirmation|Proposal|Open|Earlier|Source|Source:|Sources:|Earlier trace|See also|Related:|Cited source|Trace):',s,re.I):
            record_coverage('PROSE',None,raw,'EXCLUDED_NONDEFINITIVE','OPEN_METADATA_OR_CITATION');continue
        if s.startswith('<!--') or s.startswith('<a '):
            record_coverage('PROSE',None,raw,'STRUCTURAL','HTML_ANCHOR');continue
        # skip diagram edge text and section navigation
        if re.fullmatch(r'[-*_\s]{3,}',s) or re.match(r'^\s*\[.+\]\(.+\)\s*$',s):
            record_coverage('PROSE',None,raw,'STRUCTURAL','MARKDOWN_SEPARATOR_OR_LINK');continue
        parts=split_clauses(s)
        good=[]; reasons=[]
        for part in parts:
            if EXCL_PREFIX.match(part) or (re.search(r'\bproposal\b',part,re.I) and not re.match(r'^(?:do not|never|must not|cannot)\b',part,re.I)): reasons.append('OPEN_OR_PROPOSAL');continue
            if UNDEF.search(part) and (re.match(r'^(?:the source|source|no|exact|complete|physical|the\s+exact|this is|not|these|such|what|whether|which|who|how|a|an)\b',part,re.I) and not re.match(r'^(?:no .* (?:is allowed|may be|shall|must)|do not|must not|never|cannot)\b',part,re.I)):
                reasons.append('UNRESOLVED_OR_EXAMPLE');continue
            if not DEF_POS.search(part) and len(part)<100:
                reasons.append('NONASSERTIVE_PROSE');continue
            r,why=add_claim(part,raw,'PROSE')
            if r:good.append(r)
            else:reasons.append(why)
        record_coverage('PROSE',None,raw,'EXTRACTED' if good else 'EXCLUDED_NONDEFINITIVE','PARTIAL_WITH_EXCLUSIONS' if good and reasons else ('ELIGIBLE_DEFINITIVE' if good else (reasons[0] if reasons else 'NO_ELIGIBLE_CLAUSE')))

# Attach unique occurrence ID based on exact file order and physical position, not a semantic key.
for i,r in enumerate(records,1):r['occurrence_id']=f'GEN-{i:05d}'
refmap=collections.defaultdict(list)
for r in records:refmap[(r['file'],r['line_start'],r['table_cell']['column_index'] if r['table_cell'] else None)].append(r['occurrence_id'])
for cov in cover:
    if cov['inspection_status']=='EXTRACTED': cov['generated_occurrence_ids']=refmap.get((cov['file'],cov['line'],cov['cell_index']),[])

# exact + guarded high-confidence semantic deduplication.
CRIT=re.compile(r'(?:/(?:v\d+|internal)/[\w{}./?=&\-]+|\b[A-Z]{2,}(?:_[A-Z0-9]+)+\b|\b(?:\d+(?:\.\d+)?\s*(?:MB|GB|ms|seconds|hours|days|%|tokens|calls)|201|202|200|409|422|429|404|1536|24|16|8)\b|`[^`]+`)',re.I)

def critical_tokens(rec):
    # Collect specific API paths, status codes, numbers and entity fields, but not arbitrary local requirement ids.
    s=rec['selected_clause_en']; back=[x.lower() for x in BACKTICK.findall(s) if not ID_RE.fullmatch(x)]
    paths=re.findall(r'/(?:v\d+|internal)/[\w{}./?=&\-]+',s)
    codes=[x for x in re.findall(r'\b[A-Z]{2,}(?:_[A-Z0-9]+)+\b',s) if x not in ['NEEDS_CONFIRMATION','NOT_NULL','SOURCE_SUPPORTED']]
    nums=re.findall(r'\b\d+(?:\.\d+)?\s*(?:MB|GB|ms|seconds|hours|days|%|tokens|calls|dimensions)\b',s,re.I)
    # Raw integer codes if likely HTTP statuses, use ranges.
    codes += re.findall(r'\b(?:201|202|200|409|422|429|404)\b',s)
    # Code/DDL field names are critical; an identical type on created_at and updated_at is not one field duty.
    if rec['unit_type']=='CODE' and rec['code_language']=='sql':
        field=re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s+(?:UUID|TEXT|BIGINT|TIMESTAMPTZ|BOOLEAN|INTEGER|VARCHAR|NUMERIC)\b',s,re.I)
        if field:back.append('sql-field:'+field.group(1).lower())
    return sorted(set(paths+codes+nums+back))

for r in records:r['constraint_signature']=critical_tokens(r)

N=len(records)
parent=list(range(N)); sizes=[1]*N; reasons={}
def find(x):
    while parent[x]!=x:
        parent[x]=parent[parent[x]]; x=parent[x]
    return x

def merge(i,j,why):
    x,y=find(i),find(j)
    if x==y:return False
    if x>y:x,y=y,x
    parent[y]=x;sizes[x]+=sizes[y];reasons[(i,j)]=why
    return True

# All exact normalized statements are equivalent, with critical tokens retained by the statement.
by=collections.defaultdict(list)
for i,r in enumerate(records):
    by[r['normalized_key']].append(i)
for bucket in by.values():
    if len(bucket)>1:
        for i in bucket[1:]:merge(bucket[0],i,'EXACT_NORMALIZED_PROPOSITION')

# Near-equal syntactic paraphrases, limited and guarded to avoid erasing independent
# actor, target, method, status, numeric and authorization differences.
keys=list(by)
# Narrow nearest-neighbour pass over UNIQUE normalized strings only (approximately 6-10k).
if len(keys)>1:
    vector=TfidfVectorizer(analyzer='char',ngram_range=(3,5),min_df=1,sublinear_tf=True,dtype='float32' if False else __import__('numpy').float32)
    X=vector.fit_transform(keys)
    # direct matrix computation in blocks avoids dense N^2; keep high-similarity only.
    knn=NearestNeighbors(n_neighbors=min(6,len(keys)),algorithm='brute',metric='cosine',n_jobs=1)
    knn.fit(X)
    distances, neighbors=knn.kneighbors(X)
    for a,ks in enumerate(neighbors):
        for delta,b in zip(distances[a],ks):
            if b>=a or delta>0.075:continue  # similarity >= .925
            ka,kb=keys[a],keys[b]
            if abs(len(ka)-len(kb))>60:continue
            ia=by[ka][0];ib=by[kb][0]
            ra,rb=records[ia],records[ib]
            if ra['constraint_signature']!=rb['constraint_signature']:continue
            if len(ka)<38 or len(kb)<38:continue
            if bool(re.search(r'\b(?:may|optional|can)\b',ka))!=bool(re.search(r'\b(?:may|optional|can)\b',kb)):continue
            if bool(re.search(r'\b(?:cannot|never|prohibit|deny|reject|without|not)\b',ka))!=bool(re.search(r'\b(?:cannot|never|prohibit|deny|reject|without|not)\b',kb)):continue
            # No automatic alias inference for a different exact method/path or different context in short table statements.
            if ra['unit_type']=='TABLE_CELL' or rb['unit_type']=='TABLE_CELL':
                if len(ka)<75 and ra['scope_inherited_en']!=rb['scope_inherited_en']:continue
            merge(ia,ib,'NEAR_IDENTICAL_FULL_PREDICATE_WITH_MATCHED_CONSTRAINTS')

members=collections.defaultdict(list)
for i,r in enumerate(records):members[find(i)].append(i)
classes=[]
for root,inds in sorted(members.items(),key=lambda kv:min(kv[1])):
    classid=f'GCLASS-{len(classes)+1:05d}'
    inds.sort(key=lambda i:(records[i]['file_order'],records[i]['line_start'],records[i]['table_cell']['column_index'] if records[i]['table_cell'] else 0,i))
    first=records[inds[0]]
    for i in inds:records[i]['class_id']=classid
    distinctfiles=list(dict.fromkeys(records[i]['file'] for i in inds))
    within=0;across=0;observed=set()
    for idx in inds[1:]:
        f=records[idx]['file'];
        if f in observed:within+=1
        else:across+=1
        observed.add(f)
    # Need representative file in observed before evaluating subsequent.
    within=across=0;observed={records[inds[0]]['file']}
    dup_details=[]
    for idx in inds[1:]:
        f=records[idx]['file']; part='within_file' if f in observed else 'across_file'
        if part=='within_file':within+=1
        else:across+=1
        observed.add(f)
        dup_details.append({'occurrence_id':records[idx]['occurrence_id'],'file':f,'line_start':records[idx]['line_start'],'excess_partition':part})
    core=clean(first['selected_clause_en'])
    cls={'class_id':classid,'method':METHOD,'canonical_claim_en':first['normalized_proposition_en'],'representative_occurrence_id':first['occurrence_id'],'representative_file':first['file'],'representative_line':first['line_start'],'representative_table_cell':first['table_cell'],'representative_exact_quote_en':first['exact_quote_en'],'normalized_predicate_key':first['normalized_key'],'critical_constraints':first['constraint_signature'],'occurrence_ids':[records[i]['occurrence_id'] for i in inds],'occurrence_count':len(inds),'file_count':len(distinctfiles),'files':distinctfiles,'excess_within_file':within,'excess_across_file':across,'excess_occurrences':len(inds)-1,'excess_partition_details':dup_details,'merge_rationale_en':'Exact full normalized predicate or guarded near-identical full predicate; literal scope, path, codes and constraints preserved. Not equivalent merely by shared topic.','semantic_merge_confidence':'HIGH' if len(set(records[i]['normalized_key'] for i in inds))==1 else 'BEST_EFFORT_NEAR_IDENTICAL'}
    classes.append(cls)

# Lookup keys for reciprocal phase3 matching.
def index_keys(r):
    textv=' '.join([r['selected_clause_en'],r['normalized_proposition_en']]); keys=set()
    for x in ID_RE.findall(textv):keys.add('id:'+x.lower())
    for x in PATH_RE.findall(textv):keys.add('api:'+x.lower().strip())
    for x in CODE_RE.findall(textv):keys.add('code:'+x.lower())
    for x in BACKTICK.findall(textv):
        xx=x.strip();
        if 1<len(xx)<85:keys.add('literal:'+xx.lower())
    for x in re.findall(r'\b(?:tenant_id|workspace_id|case_id|artifact_hash|title|revision|retention class|idempotency.key|if.match|retry.after|last.event.id)\b',textv,re.I): keys.add('field:'+x.lower())
    for x in re.findall(r'\b(?:TST-\d+|T-\d{2}|SEC-\d+|BR-\d+|API-\d+|SCR-\d+|DAT-\d+)\b',textv,re.I):keys.add('test_or_trace:'+x.lower())
    return sorted(keys)
lookup_idx=collections.defaultdict(list)
lookup_rows=[]
for c in classes:
    rep=records[next(i for i,r in enumerate(records) if r['occurrence_id']==c['representative_occurrence_id'])]
    keyset=set()
    for oi in c['occurrence_ids']:
        # all occurrences since aliases/source IDs can appear in non-representative quotes
        rr=records[int(oi.split('-')[1])-1]
        keyset.update(index_keys(rr))
    for k in sorted(keyset):lookup_idx[k].append(c['class_id'])
    lookup_rows.append({'method':METHOD,'class_id':c['class_id'],'lookup_keys':sorted(keyset),'source_occurrence_count':c['occurrence_count']})

# Summaries and smoke checks
assert len(set(r['occurrence_id'] for r in records))==len(records)
assert len(set(c['class_id'] for c in classes))==len(classes)
assert set(r['file'] for r in records)==set(FILES)
assert sum(c['occurrence_count'] for c in classes)==len(records)
assert sum(c['excess_occurrences'] for c in classes)==len(records)-len(classes)
assert all(c['excess_occurrences']==c['excess_within_file']+c['excess_across_file'] for c in classes)
assert sum(1 for r in records if r['class_id'])==len(records)
assert all(r['line_start']>=1 and r['line_start']<=manifest[r['file_order']]['physical_lines'] for r in records)
assert all(len(cov['generated_occurrence_ids'])>0 for cov in cover if cov['inspection_status']=='EXTRACTED')
assert all(cov['file'] in FILES for cov in cover)

# language checks
for r in records:
    if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',r['normalized_proposition_en']):raise ValueError('Non-English generated assertion found')

stats={
 'protocol_version':'6.1','phase':2,'method':METHOD,
 'status':'PHASE_COMPLETED_BEST_EFFORT',
 'inputs':manifest,'source_positive_atoms_reference':'../orion_phase1/01_source_atoms_final.jsonl',
 'source_negative_controls_reference':'../orion_phase1/01_source_negative_controls_final.jsonl',
 'eligible_generated_occurrences':len(records),'raw_semantic_classes':len(classes),
 'excess_duplicate_occurrences':len(records)-len(classes),
 'preliminary_duplicate_rate':(len(records)-len(classes))/len(records) if records else None,
 'repeated_classes':sum(c['occurrence_count']>1 for c in classes),
 'repeated_classes_across_files':sum(c['file_count']>1 for c in classes),
 'within_file_excess':sum(c['excess_within_file'] for c in classes),
 'across_file_excess':sum(c['excess_across_file'] for c in classes),
 'inspected_physical_lines':sum(d['physical_lines'] for d in manifest),
 'inspected_line_and_cell_units':len(cover),
 'substantive_nondefinitive_or_other_excluded_units':len(excluded),
 'individual_file_inspection_stats':{f:dict(counts[f]) for f in FILES},
 'contextual_scope_policy_en':'Restore meaning from nearest heading, table column, row key, and condition; reject proposals and unresolved decisions. Confirmed fragments in mixed rows can remain eligible.',
 'semantic_dedup_policy_en':'Exact full normalized predicate deduplication plus constrained near-identical character ngram matching (>=0.925) with matching status codes, endpoint paths, literal fields and numerical constraints. Semantically distant paraphrases are not automatically merged.',
 'limitations_en':['Best-effort rule-aided semantic segmentation, with physical-line and table-cell accountability; full human semantic equivalence certification is not asserted.','Some mixed status cells and universal boilerplate require a later reciprocal semantic audit.','Near-identical matching favors avoiding false merges over aggressive paraphrase clustering; duplication may be underestimated.','Some shorthand table cells may remain a candidate for parent-context refinement; their exact source and inherited row/column context are recorded.','This phase does not compute confusion cells or PDF-to-generated entailment.']
}

def write_jsonl(name,items):
    with (OUT/name).open('w',encoding='utf-8') as f:
        for v in items:f.write(json.dumps(v,ensure_ascii=False,separators=(',',':'))+'\n')
write_jsonl('02_generated_atoms_final.jsonl',records)
write_jsonl('02_generated_classes_final.jsonl',classes)
write_jsonl('04_duplicate_classes_final.jsonl',classes)
write_jsonl('02_generated_exclusions_final.jsonl',excluded)
write_jsonl('02_line_cell_coverage_final.jsonl',cover)
write_jsonl('02_reciprocal_lookup_keys_final.jsonl',lookup_rows)
(OUT/'02_reciprocal_key_to_classes_final.json').write_text(json.dumps(lookup_idx,indent=1,ensure_ascii=False),encoding='utf-8')
(OUT/'02_phase2_status.json').write_text(json.dumps(stats,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
with (OUT/'09_excluded_units.jsonl').open('w',encoding='utf-8') as o:
    with (ROOT/'orion_phase1/09_excluded_units.jsonl').open('r',encoding='utf-8') as f:
        for line in f:o.write(line)
    for x in excluded:o.write(json.dumps({'unit_origin':'GENERATED_MD','exclusion':x},ensure_ascii=False,separators=(',',':'))+'\n')

report=f'''# Phase 2 — Generated Corpus Inspection and Raw Semantic Duplication

**Protocol:** 6.1  
**Status:** `{stats['status']}`  
**Method identifier:** `{METHOD}` (one complete supplied eight-document set; no prefix inferred)

## Inputs inspected

| Role | Unchanged uploaded filename | Physical lines | SHA-256 |
|---|---|---:|---|
'''
for d in manifest:report+=f"| {d['role']} | `{d['filename']}` | {d['physical_lines']:,} | `{d['sha256']}` |\n"
report+=f'''
## Extracted inventories

- Eligible generated occurrences (`GO`): **{len(records):,}**.
- Raw unique semantic classes (`G`): **{len(classes):,}**.
- Excess occurrences: **{len(records)-len(classes):,}**.
- Preliminary duplicate rate: **{stats['preliminary_duplicate_rate']:.6%}**.
- Repeated classes: **{stats['repeated_classes']:,}**; across-file repeated classes: **{stats['repeated_classes_across_files']:,}**.
- Within-file excess occurrences: **{stats['within_file_excess']:,}**; across-file excess occurrences: **{stats['across_file_excess']:,}**.
- Physical lines inspected: **{stats['inspected_physical_lines']:,}**; line/cell units classified: **{len(cover):,}**.
- Excluded nondefinitive, metadata, and supporting units: **{len(excluded):,}** (including table-cell exclusions; overlap with source/metadata context is explicit).

## Extraction rules

All eight unchanged source Markdown files were decoded as UTF-8 and inspected from the first to last physical line. Markdown tables were split into cells with escaped-pipe and inline-code awareness. Each retained cell receives its physical line, column index, column header and original row anchor. Prose and semicolon-separated assertions were extracted into source-quoted atomic candidates. Nested section and conditional table context is preserved, not inferred from stand-alone literals alone. Code blocks are classified separately; verifiable reference DDL terms are eligible while illustrative, unresolved or decorative code is excluded.

Unapproved proposals, TBD/Needs confirmation statements, open questions, conflict registers, unsupported inferences and bare citations do not become definitive generated claims. Where a line contains both resolved and unresolved subclaims, only the resolvable independent portion is eligible. Examples and baseline screenshots are not adopted as production configuration.

Raw classes are grouped by normalized target/operation/scope where structurally explicit. Exact normalized predicates merge. Very close textual variants merge only with preserved critical paths, fields, statuses and numeric constraints. Nonidentical actor, resource, operation, precondition or outcome remains separate. Duplicate excess is assigned deterministically to the earliest occurrence, and split into within-file vs across-file as required by the protocol.

## Structural checks

All eight scored roles were present. Every extracted occurrence has one valid original file line and belongs to exactly one semantic class. No occurrence belongs to two classes, no class has zero members, all references point to the uploaded filenames, and the duplicate partition reconciles to the occurrence/class count. Each inspected line/table cell has a recorded classification and all extracted units have at least one occurrence ID.

## Limitations and next phase

This is a fully enumerated **best-effort** extraction, not certified manual semantic atomization. Some subtle paraphrases are intentionally left as separate classes unless the full semantic predicates are defensibly equivalent; the reported duplicate rate is provisional. Class correctness against the PDF and source-atom coverage are not decided here. They require item-level PDF evidence and reciprocal source/generated retrieval in phases 3–5. No TP, TN, FP, FN or coverage percentage is reported in this phase.

## Deliverables

- `02_generated_atoms_final.jsonl` — eligible definitive occurrences, original quotations, physical locations and class assignments.
- `02_generated_classes_final.jsonl` — canonical within-method raw semantic classes and all member occurrence IDs.
- `04_duplicate_classes_final.jsonl` — class-level repetition and within/across-file partition.
- `02_generated_exclusions_final.jsonl` — explicitly excluded nondefinitive source units.
- `02_line_cell_coverage_final.jsonl` — physical-line and table-cell inspection register, including structural units.
- `02_reciprocal_lookup_keys_final.jsonl` and `02_reciprocal_key_to_classes_final.json` — bidirectional retrieval aids for phase 3.
- `09_excluded_units.jsonl` — phase-1 PDF exclusions and phase-2 excluded generated units.
- `02_phase2_status.json` — machine-readable completeness, counts, assumptions and limitations.
'''
(OUT/'02_phase2_report.md').write_text(report,encoding='utf-8')
print('PHASE_2_COMPLETE')
print(json.dumps({k:v for k,v in stats.items() if k in ['status','eligible_generated_occurrences','raw_semantic_classes','excess_duplicate_occurrences','preliminary_duplicate_rate','repeated_classes','repeated_classes_across_files','within_file_excess','across_file_excess','inspected_physical_lines','inspected_line_and_cell_units','substantive_nondefinitive_or_other_excluded_units']},indent=2))
