#!/usr/bin/env python3
"""Validate the supplied OrionDesk Phase-2 item-level ledgers against unchanged inputs."""
from pathlib import Path
from collections import defaultdict
import json, hashlib
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent

def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]

status=json.loads((ROOT/'02_phase2_status.json').read_text(encoding='utf-8'))
occ=jsonl(ROOT/'02_generated_atoms_final.jsonl')
classes=jsonl(ROOT/'02_generated_classes_final.jsonl')
coverage=jsonl(ROOT/'02_line_cell_coverage_final.jsonl')
lookups=jsonl(ROOT/'02_reciprocal_lookup_keys_final.jsonl')
assert len(occ)==status['eligible_generated_occurrences']
assert len(classes)==status['raw_semantic_classes']
assert len(set(o['occurrence_id'] for o in occ))==len(occ)
assert len(set(c['class_id'] for c in classes))==len(classes)
by_occ={o['occurrence_id']:o for o in occ}
by_class={c['class_id']:c for c in classes}
byfile=defaultdict(set)
for item in coverage:byfile[item['file']].add(item['line'])
for m in status['inputs']:
    path=SOURCE/m['filename']; b=path.read_bytes()
    assert hashlib.sha256(b).hexdigest()==m['sha256']
    lines=b.decode('utf-8-sig').splitlines()
    assert len(lines)==m['physical_lines']
    assert byfile[m['filename']]==set(range(1,len(lines)+1))
for o in occ:
    assert o['method']==status['method']
    assert o['occurrence_id'] in by_class[o['class_id']]['occurrence_ids']
    l=(SOURCE/o['file']).read_text(encoding='utf-8').splitlines()[o['line_start']-1]
    assert o['exact_quote_en'].strip() in l
assert sum(c['occurrence_count'] for c in classes)==len(occ)
assert sum(c['excess_occurrences'] for c in classes)==len(occ)-len(classes)
assert sum(c['excess_within_file'] for c in classes)==status['within_file_excess']
assert sum(c['excess_across_file'] for c in classes)==status['across_file_excess']
assert all(c['excess_occurrences']==c['excess_within_file']+c['excess_across_file'] for c in classes)
assert all(c['occurrence_count']==len(c['occurrence_ids']) and all(i in by_occ for i in c['occurrence_ids']) for c in classes)
assert len(lookups)==len(classes)
assert len(coverage)==status['inspected_line_and_cell_units']
assert all(row['generated_occurrence_ids'] for row in coverage if row['inspection_status']=='EXTRACTED')
print('PHASE_2_LEDGER_VALIDATION_PASSED')
print('files:',len(status['inputs']),'lines:',status['inspected_physical_lines'],'units:',len(coverage),'occurrences:',len(occ),'classes:',len(classes))
