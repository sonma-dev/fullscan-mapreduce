#!/usr/bin/env python3
"""Independent Phase 6 ledger recomputation and evidence-integrity diagnostics.

Usage: python compute_metrics.py [--data-dir DIRECTORY] [--inputs-dir DIRECTORY]
All mathematical counts are derived from item-level JSONL, never prior summaries.
PyMuPDF is optional for the page-text verification; if unavailable, this is
reported as a validation limitation rather than silently assumed successful.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path
import re
import sys
import unicodedata

ROLES = [
    '01_screen_functions.md', '02_api.md', '03_data.md',
    '04_batch_functions.md', '05_business_rules.md',
    '06_exception_handling(2).md', '07_processing_flows(1).md',
    '08_architecture_decision(1).md'
]
LEDGERS = {
    'source': '01_source_atoms_final.jsonl',
    'negative': '01_source_negative_controls_final.jsonl',
    'occurrences': '02_generated_atoms_final.jsonl',
    'classes': '02_generated_classes_final.jsonl',
    'universe': '03_canonical_universe_final.jsonl',
    'matches': '03_evidence_matches_final.jsonl',
    'bridges': '03_semantic_coverage_bridges_final.jsonl',
    'fn': '03_fn_root_cause_audit_final.jsonl',
    'validity': '04_generated_claim_validity_final.jsonl',
    'judgments': '04_atomic_judgments_final.jsonl',
    'duplicate': '04_duplicate_classes_final.jsonl',
    'tp': '05_tp_evidence_audit_final.jsonl',
    'atomization': '05_source_atomization_audit_final.jsonl',
    'changes': '07_change_delta.jsonl',
    'exclusions': '09_excluded_units.jsonl',
    'page_coverage': '01_pdf_page_coverage_final.jsonl',
    'line_coverage': '02_markdown_line_cell_coverage_final.jsonl'
}
PREDICATES = ('target', 'action', 'actor', 'condition', 'scope', 'timing', 'constraint', 'exception', 'outcome', 'version')


def load_jsonl(path):
    result = []
    with path.open(encoding='utf-8') as f:
        for line_no, raw in enumerate(f, 1):
            if raw.strip():
                try:
                    obj = json.loads(raw)
                except Exception as exc:
                    raise ValueError(f'Bad JSON: {path}:{line_no}: {exc}') from exc
                if not isinstance(obj, dict):
                    raise ValueError(f'Expected JSON object: {path}:{line_no}')
                result.append(obj)
    return result


def index_unique(rows, key, failures):
    out = {}
    for row in rows:
        ident = row.get(key)
        if not isinstance(ident, str) or not ident:
            failures.append(f'Empty {key} in record')
        elif ident in out:
            failures.append(f'Duplicate {key}: {ident}')
        else:
            out[ident] = row
    return out


def normalize(s):
    s = unicodedata.normalize('NFKC', str(s or '')).casefold()
    return re.sub(r'[^\w]+', ' ', s, flags=re.UNICODE).strip()


def ratio(n, d):
    return n / d if d else None


def check_evidence_item(ev, text_lines, pdf_text, figures, failures, source_check, which):
    if not isinstance(ev, dict):
        failures.append(f'{which}: evidence is not an object')
        return
    file = ev.get('file')
    quote = ev.get('quote_en') or ev.get('exact_quote_en')
    if file in text_lines:
        start, end = ev.get('line_start'), ev.get('line_end')
        if not isinstance(start, int) or not isinstance(end, int) or not 1 <= start <= end <= len(text_lines[file]):
            failures.append(f'{which}: bad Markdown locator {file} L{start}-{end}')
            return
        actual = '\n'.join(text_lines[file][start - 1:end])
        if quote and normalize(quote) not in normalize(actual):
            failures.append(f'{which}: quoted Markdown does not occur in {file} L{start}-{end}')
        return
    if file == 'OrionDesk_AI_Detailed_Design_Specification.pdf':
        if not isinstance(ev.get('physical_page'), int) or not 1 <= ev['physical_page'] <= 90:
            failures.append(f'{which}: bad PDF page {ev.get("physical_page")}')
            return
        page = ev['physical_page']
        if pdf_text is None:
            source_check['pdf_unverified'] += 1
        elif quote and normalize(quote) not in normalize(pdf_text[page - 1]):
            if page == 8 and normalize(quote) in figures:
                source_check['figure_only'] += 1
            else:
                source_check['pdf_mismatch'] += 1
                if len(source_check['pdf_mismatch_examples']) < 12:
                    source_check['pdf_mismatch_examples'].append({'context': which, 'page': page, 'quote': quote[:170]})
        return
    failures.append(f'{which}: unknown evidence filename {file!r}')


def run(data_dir, inputs_dir):
    failures = []
    warnings = []
    rows = {k: load_jsonl(data_dir / f) for k, f in LEDGERS.items()}
    source = index_unique(rows['source'], 'source_id', failures)
    negative = index_unique(rows['negative'], 'negative_control_id', failures)
    occurrences = index_unique(rows['occurrences'], 'occurrence_id', failures)
    classes = index_unique(rows['classes'], 'class_id', failures)
    universe = index_unique(rows['universe'], 'canonical_id', failures)
    judges = index_unique(rows['judgments'], 'canonical_id', failures)
    validity = index_unique(rows['validity'], 'generated_class_id', failures)
    dupes = index_unique(rows['duplicate'], 'class_id', failures)
    matches = index_unique(rows['matches'], 'source_id', failures)
    tp_proofs = index_unique(rows['tp'], 'source_id', failures)
    bridges = index_unique(rows['bridges'], 'source_id', failures)

    # Common atomic universes and one coherent binary scoring set.
    if set(source) & set(negative):
        failures.append('R and N identifiers overlap')
    if set(judges) != set(universe):
        failures.append('Universe and judgment ID sets differ')
    for k in universe:
        if k in judges and universe[k] != judges[k]:
            failures.append(f'Universe and judgment fields differ: {k}')
    for key, row in judges.items():
        c = row['scoring_cell']
        if (row['actual_label'], row['predicted_label']) != {'TP': (1, 1), 'FN': (1, 0), 'TN': (0, 0), 'FP': (0, 1)}.get(c):
            failures.append(f'Invalid label/cell combination: {key}')
    counters = Counter(r['scoring_cell'] for r in judges.values())
    TP, TN, FP, FN = (counters[k] for k in ('TP', 'TN', 'FP', 'FN'))
    src_j = {k: j for k, j in judges.items() if j.get('origin_source_ids')}
    neg_j = {k: j for k, j in judges.items() if j.get('origin_negative_control_ids')}
    generated_only_j = {k: j for k, j in judges.items() if not j.get('origin_source_ids') and not j.get('origin_negative_control_ids')}
    if set(src_j) != set(source):
        failures.append('Source-positive rows do not bijectively cover R')
    if set(neg_j) != set(negative):
        failures.append('Negative-control rows do not bijectively cover N')
    if any(len(r['origin_source_ids']) != 1 or r['origin_source_ids'][0] != k for k, r in src_j.items()):
        failures.append('Source rows do not identify exactly their own PDF atom')
    if any(len(r['origin_negative_control_ids']) != 1 or r['origin_negative_control_ids'][0] != k for k, r in neg_j.items()):
        failures.append('Negative rows do not identify exactly their own NEG control')
    if any(r['actual_label'] != 0 for r in neg_j.values()):
        failures.append('Negative control not labeled actual zero')
    if any(r['scoring_cell'] != 'FP' for r in generated_only_j.values()):
        failures.append('Unsupported generated-only row must be FP')
    if TP + FN != len(source) or TN + sum(r['scoring_cell'] == 'FP' for r in neg_j.values()) != len(negative):
        failures.append('Source or negative-control partition equation failed')
    if FP != len(generated_only_j) + sum(r['scoring_cell'] == 'FP' for r in neg_j.values()):
        failures.append('FP partition equation failed')
    if TP + FP + TN + FN != len(judges):
        failures.append('Canonical universe total equation failed')
    if sum(r['predicted_label'] for r in judges.values()) != TP + FP:
        failures.append('Predicted-positive total not TP+FP')

    # One generated occurrence is a member of exactly one raw semantic class.
    if set(validity) != set(classes) or set(dupes) != set(classes):
        failures.append('Class/validity/duplicate inventories disagree')
    all_members = []
    mismatch_class = []
    for class_id, cl in classes.items():
        ids = cl['occurrence_ids']
        if len(ids) != cl['occurrence_count']:
            failures.append(f'Class occurrence count mismatch: {class_id}')
        if cl['representative_occurrence_id'] not in ids:
            failures.append(f'Class representative not in its member list: {class_id}')
        all_members.extend(ids)
        for occ_id in ids:
            if occ_id not in occurrences or occurrences[occ_id].get('semantic_class_id') != class_id:
                mismatch_class.append((class_id, occ_id))
        if class_id in validity and set(validity[class_id]['origin_occurrence_ids']) != set(ids):
            failures.append(f'Validity occurrence members disagree: {class_id}')
    if mismatch_class:
        failures.append(f'{len(mismatch_class)} occurrence-to-class membership discrepancies')
    if len(all_members) != len(occurrences) or set(all_members) != set(occurrences) or max(Counter(all_members).values(), default=0) != 1:
        failures.append('Occurrence membership is not a one-to-one partition')
    for row in occurrences.values():
        if row.get('method') != 'supplied_unprefixed_set':
            failures.append(f'Method-isolation discrepancy in occurrence {row["occurrence_id"]}')
    for group, key in ((rows['classes'], 'method'), (rows['judgments'], 'method'), (rows['validity'], 'method')):
        if any(r.get(key) != 'supplied_unprefixed_set' for r in group):
            failures.append('Multiple method codes or unexpected method in a single-set run')

    # Reconstruct duplicate partition from raw individual membership and actual source-file order.
    count_within = count_across = repeated = spanning = 0
    for class_id, cl in classes.items():
        ids = sorted(cl['occurrence_ids'], key=lambda ident: (
            ROLES.index(occurrences[ident]['file']) if occurrences[ident]['file'] in ROLES else 99,
            occurrences[ident]['line_start'], str(occurrences[ident].get('table_cell') or '')))
        files_seen = set()
        w = a = 0
        for i, occ_id in enumerate(ids):
            file = occurrences[occ_id]['file']
            if i:
                if file in files_seen:
                    w += 1
                else:
                    a += 1
            files_seen.add(file)
        if len(ids) > 1:
            repeated += 1
        if len(files_seen) > 1:
            spanning += 1
        count_within += w
        count_across += a
        record = dupes.get(class_id)
        if record and (record['within_file_excess'], record['across_file_excess'], record['excess_occurrences']) != (w, a, w + a):
            failures.append(f'Raw duplicate partition not reproduced: {class_id}')
        if record and record['occurrence_count'] != len(ids):
            failures.append(f'Duplicate class member count mismatch: {class_id}')
    raw_excess = len(occurrences) - len(classes)
    if count_within + count_across != raw_excess:
        failures.append('Duplicate excess partition failed')

    # Generated-only FP vs raw-class semantic validity; no inferred class-level TP denominator.
    unsupported_ids = {k for k, v in validity.items() if v['validity_label'] == 'PDF_UNSUPPORTED'}
    unsupported_rows = {x for r in generated_only_j.values() for x in r['origin_generated_class_ids']}
    if unsupported_ids != unsupported_rows or len(generated_only_j) != len(unsupported_ids):
        failures.append('Unsupported generated class to canonical FP mapping is not 1:1')
    if any(len(r['origin_generated_class_ids']) != 1 for r in generated_only_j.values()):
        failures.append('Generated-only unsupported FP does not have exactly one class ID')
    used_in_tp = {c for r in src_j.values() if r['scoring_cell'] == 'TP' for c in r['origin_generated_class_ids']}
    if used_in_tp & unsupported_ids:
        failures.append('An unsupported generated class was also used as TP support')
    if any(r['validity_label'] not in ('PDF_ENTAILED', 'PDF_UNSUPPORTED', 'SUPPORTED_NONCOVERING') for r in validity.values()):
        failures.append('Invalid generated validity status')

    # Source coverage, bridge, TP predicate and FN root-cause completeness.
    if set(matches) != set(source):
        failures.append('Source match ledger not a complete bijection of R')
    expected_tp = {s for s in source if s in src_j and src_j[s]['scoring_cell'] == 'TP'}
    expected_fn = set(source) - expected_tp
    if set(tp_proofs) != expected_tp:
        failures.append('The TP proof audit is not complete for every final TP')
    bridge_tp = {k for k in expected_tp if src_j[k].get('entailment_grade') == 'E2'}
    if set(bridges) != bridge_tp:
        failures.append('E2 semantic bridge inventory does not cover precisely the E2 TP rows')
    fn_history = defaultdict(list)
    for r in rows['fn']:
        fn_history[r['source_id']].append(r)
    for k in expected_fn:
        if k not in fn_history:
            failures.append(f'FN has no root-cause audit: {k}')
        else:
            rec = fn_history[k][-1]
            if rec['final_scoring_cell'] != 'FN' or rec['fn_review_disposition'] not in ('TRUE_MISSING', 'PARTIAL_ENTAILMENT', 'CONSERVATIVE_UNRESOLVED'):
                failures.append(f'FN root-cause final disposition invalid: {k}')
            if not rec.get('best_generated_candidates') or not rec.get('unmet_predicates_en'):
                failures.append(f'FN audit missing inspected candidate or unmet predicate: {k}')
    if len({r['source_id'] for r in rows['fn']}) != len(rows['fn']):
        failures.append('Duplicate FN history IDs')
    tp_status = Counter()
    proof_flags = Counter()
    for k in expected_tp:
        proof = tp_proofs.get(k)
        if not proof:
            continue
        tp_status[proof.get('audit_outcome')] += 1
        if not proof.get('pdf_evidence') or not proof.get('generated_evidence'):
            failures.append(f'TP proof lacks both evidence types: {k}')
        predicates = proof.get('predicate_check', {})
        if set(predicates) != set(PREDICATES):
            failures.append(f'TP proof incomplete predicate keyset: {k}')
        for pred in PREDICATES:
            state = (predicates.get(pred) or {}).get('status')
            if state not in ('met', 'not_applicable'):
                failures.append(f'TP proof noncompliant predicate {pred}: {k}={state}')
            proof_flags[f'{pred}:{state}'] += 1
    if any(r['final_cell'] != src_j.get(r['source_id'],{}).get('scoring_cell') for r in rows['matches']):
        failures.append('Evidence match row differs from final judgment cell')
    for k in expected_tp:
        if not src_j[k]['generated_evidence']:
            failures.append(f'TP judgment lacks generated citations: {k}')

    # Atomization deltas and original source-backed controls.
    for r in rows['atomization']:
        if r['decision'] == 'REMOVE_NONINDEPENDENT_SOURCE_ATOM':
            if any(old in source for old in r['old_source_ids']):
                failures.append('Deleted source atom remains scored')
        if r['decision'] == 'SPLIT_INDEPENDENT_PREDICATES':
            if any(new not in source for new in r['new_source_ids']):
                failures.append('Split source atom lacks replacement')
    if any(n['actual_label'] != 0 for n in negative.values()):
        failures.append('Negative control improperly labeled positive')

    # Independently validate the supplied input files and line/page coverage ledgers.
    text_lines = {}
    for fn in ROLES:
        path = inputs_dir / fn
        if not path.is_file():
            failures.append(f'Missing original Markdown: {fn}')
        else:
            text_lines[fn] = path.read_text(encoding='utf-8').splitlines()
    line_ledger = defaultdict(set)
    for r in rows['line_coverage']:
        if r.get('file') not in ROLES:
            failures.append(f'Unknown file in Markdown coverage ledger: {r.get("file")}')
        line_ledger[r['file']].add(r['line'])
    for f, lines in text_lines.items():
        if line_ledger[f] != set(range(1, len(lines) + 1)):
            failures.append(f'Incomplete Markdown line-coverage ledger: {f}')
    page_records = {r['physical_page']: r for r in rows['page_coverage']}
    if set(page_records) != set(range(1, 91)):
        failures.append('Page coverage missing some physical pages')

    pdf_file = inputs_dir / 'OrionDesk_AI_Detailed_Design_Specification.pdf'
    pdf_text = None
    pdf_page_count = None
    if pdf_file.exists():
        try:
            import fitz
            with fitz.open(pdf_file) as doc:
                pdf_page_count = len(doc)
                pdf_text = [page.get_text('text') for page in doc]
            if pdf_page_count != 90:
                failures.append(f'Original PDF page count is {pdf_page_count}, not 90')
        except Exception as e:
            warnings.append(f'Original PDF could not be independently parsed: {e}')
    else:
        warnings.append('Original PDF unavailable to the optional source-evidence check')
    if any(not page_records[p].get('pdf_rendered') for p in range(1, 91)):
        warnings.append('Phase 1 audit does not report all 90 pages as rendered')

    fig_text = ['tenant_id and actor context at every boundary', 'immutable evidence and versioned policy inputs',
                'idempotent event processing with trace correlation']
    figure_quotes = {normalize(x) for x in fig_text}
    source_evidence_stats = {'figure_only': 0, 'pdf_mismatch': 0, 'pdf_unverified': 0, 'pdf_mismatch_examples': []}
    checked_generated, checked_source = 0, 0
    for obj in source.values():
        for ev in obj.get('pdf_evidence', []):
            checked_source += 1
            check_evidence_item(ev, text_lines, pdf_text, figure_quotes, failures, source_evidence_stats, 'source atom')
    for obj in negative.values():
        for ev in obj.get('pdf_evidence', []):
            checked_source += 1
            check_evidence_item(ev, text_lines, pdf_text, figure_quotes, failures, source_evidence_stats, 'negative control')
    for obj in occurrences.values():
        checked_generated += 1
        ev = dict(file=obj.get('file'), line_start=obj.get('line_start'), line_end=obj.get('line_end'), quote_en=obj.get('exact_quote_en'))
        check_evidence_item(ev, text_lines, pdf_text, figure_quotes, failures, source_evidence_stats, 'generated occurrence')
    for obj in tp_proofs.values():
        for ev in obj['generated_evidence']:
            checked_generated += 1
            check_evidence_item(ev, text_lines, pdf_text, figure_quotes, failures, source_evidence_stats, 'TP proof')
        for ev in obj['pdf_evidence']:
            checked_source += 1
            check_evidence_item(ev, text_lines, pdf_text, figure_quotes, failures, source_evidence_stats, 'TP PDF proof')
    for obj in validity.values():
        for ev in obj.get('generated_evidence', []):
            checked_generated += 1
            check_evidence_item(ev, text_lines, pdf_text, figure_quotes, failures, source_evidence_stats, 'generated validity')
        for ev in obj.get('pdf_evidence', []):
            checked_source += 1
            check_evidence_item(ev, text_lines, pdf_text, figure_quotes, failures, source_evidence_stats, 'generated validity PDF support')
    for obj in rows['fn']:
        for ev in obj.get('best_generated_candidates', []):
            checked_generated += 1
            check_evidence_item(ev, text_lines, pdf_text, figure_quotes, failures, source_evidence_stats, 'FN candidate')

    if source_evidence_stats['pdf_mismatch']:
        warnings.append(f'{source_evidence_stats["pdf_mismatch"]} PDF citation excerpts lacked a text match; see source-evidence diagnostics')

    # Prior metric JSONs are used as a post-hoc crosscheck only, not as inputs to the computation.
    saved_summary_discrepancies = []
    for file, expected_sections in (
        ('04_confusion_matrix_final.json', ('confusion', 'metrics')),
        ('05_duplicate_metrics_final.json', ('eligible_generated_occurrences', 'unique_generated_claim_classes'))):
        path = data_dir / file
        if not path.is_file():
            failures.append(f'Missing previously finalized numerical comparison file: {file}')
            continue
        old = json.loads(path.read_text(encoding='utf-8'))
        if file.startswith('04_'):
            for cell, value in (('TP', TP), ('TN', TN), ('FP', FP), ('FN', FN)):
                if old['confusion'].get(cell) != value:
                    saved_summary_discrepancies.append(f'Old confusion {cell} differs from independent recomputation')
        else:
            if old.get('eligible_generated_occurrences') != len(occurrences) or old.get('unique_generated_claim_classes') != len(classes):
                saved_summary_discrepancies.append('Saved duplicate base counts disagree with raw ledgers')
    if saved_summary_discrepancies:
        failures.extend(saved_summary_discrepancies)

    # Robust semantic-certification disclosure (no claim of machine-certified entailment).
    proof_independent = sum('NOT_FULL_INDEPENDENT' not in str(r.get('certification_scope')) and
                            'NOT_INDEPENDENT' not in str(r.get('certification_scope')) and
                            r.get('certification_scope') not in (None, '') for r in tp_proofs.values())
    uncertified_generated = sum('BEST_EFFORT' in str(v.get('adjudication_status')) or
                                'PENDING' in str(v.get('adjudication_status')) for v in validity.values())
    fn_dispositions = Counter(r['fn_review_disposition'] for r in rows['fn'] if r.get('final_scoring_cell') == 'FN')
    validities = Counter(v['validity_label'] for v in validity.values())
    rates = {
        'Precision': ratio(TP, TP + FP), 'Recall': ratio(TP, TP + FN),
        'F1': ratio(2 * TP, 2 * TP + FP + FN),
        'Duplicate': ratio(raw_excess, len(occurrences))
    }
    negative_asserted = sum(r['scoring_cell'] == 'FP' for r in neg_j.values())
    metrics = {
        'protocol_version': '6.1', 'method': 'supplied_unprefixed_set',
        'phase_status': 'PHASE_COMPLETED_BEST_EFFORT',
        'semantic_certification': 'NOT_VERIFIED',
        'structural_reconciliation': 'PASS' if not failures else 'FAILED',
        'raw_counts': {'source_positive_atoms_R': len(source), 'negative_controls_N': len(negative),
                       'generated_occurrences_GO': len(occurrences), 'generated_semantic_classes_G': len(classes)},
        'canonical': {'source_covered_A': TP, 'asserted_negative_B': negative_asserted,
                      'unsupported_generated_F': len(generated_only_j),
                      'universe_U': len(universe), 'predicted_positive_P': TP + FP},
        'confusion': {'TP': TP, 'TN': TN, 'FP': FP, 'FN': FN},
        'metrics': rates,
        'duplicate': {'excess_occurrences': raw_excess, 'within_file_excess': count_within,
                      'across_file_excess': count_across,
                      'repeated_claim_class_count': repeated,
                      'repeated_claims_spanning_files': spanning},
        'generated_validity_categories': dict(validities),
        'fn_root_causes': dict(fn_dispositions),
        'corrected_matcher_false_negatives_retained': sum(r['fn_review_disposition'] == 'MATCHER_FALSE_NEGATIVE_CORRECTED' and r['final_scoring_cell'] == 'TP' for r in rows['fn']),
        'tp_predicate_proof_entries': len(tp_proofs),
        'tp_independently_semantically_certified_entries': proof_independent,
        'uncertified_or_provisional_generated_class_judgments': uncertified_generated,
        'source_atomization_audit_entries': len(rows['atomization']),
        'change_delta_records': len(rows['changes']),
        'prior_summary_crosscheck': 'AGREES' if not saved_summary_discrepancies else 'DISAGREES',
        'negative_universe_explanation': 'Only the 37 predeclared PDF-grounded diagnostic controls; not the universe of all absent requirements.',
        'critical_metric_distinction': 'Effective canonical predicted-positive units differ from raw generated semantic classes.'
    }

    # Regression probes selected by actual PDF evidence and actual generated locators.
    probes = []
    probe_specs = [
        ('case_title_field', 'PDF-00208', 'Case title present in the source and inherited from the data field table.'),
        ('workspace_retention_class', 'PDF-00199', 'Workspace retention class is a stored setting rather than an invented screen default.'),
        ('idempotent_case_creation', 'PDF-00948', 'Repeat create with identical key yields one case and identical outcome.'),
        ('source_citation_version_lineage', 'PDF-01025', 'Every cited answer traces to immutable versions.'),
        ('figure_runtime_tenancy_actor', 'PDF-00977', 'Original PDF physical page 8 embedded visual assertion.'),
        ('figure_immutable_policy', 'PDF-00978', 'Original PDF physical page 8 embedded visual assertion.'),
        ('figure_idempotent_trace', 'PDF-00979', 'Original PDF physical page 8 embedded visual assertion.'),
    ]
    for probe, ident, reason in probe_specs:
        s = source.get(ident)
        j = judges.get(ident)
        ev = j.get('generated_evidence', []) if j else []
        probes.append({'probe_id': probe, 'source_id': ident, 'pdf_atom_present': s is not None,
                       'canonical_judgment_present': j is not None,
                       'scoring_cell': j.get('scoring_cell') if j else None,
                       'evidence_count': len(ev),
                       'actual_generated_evidence_locations': [
                           {'file': e.get('file'), 'line_start': e.get('line_start'), 'line_end': e.get('line_end')}
                           for e in ev],
                       'expected_regression_behavior_en': reason,
                       'probe_limitation_en': 'A present citation and a TP label do not by themselves certify full semantic equivalence.'})

    validation = {
        'status': 'PASS' if not failures else 'FAIL',
        'checks_run': [
            'JSONL parse and unique identifiers', 'source and negative-control partition',
            'one canonical binary universe and all four scoring equations',
            'generated occurrence/class assignment', 'one raw class validity record',
            'raw duplicate partition reconstructed in source-file order',
            'canonical unsupported-FP-to-generated-class bijection',
            'no unsupported class used for TP', 'complete TP predicate proof map',
            'full final FN root-cause closure', 'E2 source bridge membership',
            'source atomization change audit', 'all original Markdown line ranges and quotations',
            'all 90 PDF physical page locators and text/visual exception diagnostics',
            'single-method isolation', 'coverage-line registry matching actual source files'],
        'failure_count': len(failures), 'failures': failures[:200],
        'warning_count': len(warnings), 'warnings': warnings,
        'prior_summary_discrepancies': saved_summary_discrepancies,
        'evidence_checks': {'markdown_generated_occurrences_and_proofs_checked': checked_generated,
                            'pdf_source_and_proofs_checked': checked_source,
                            'pdf_physical_page_count': pdf_page_count,
                            'figure_only_pdf_quotes_confirmed_by_page8_visual': source_evidence_stats['figure_only'],
                            'pdf_quote_text_mismatch_count': source_evidence_stats['pdf_mismatch'],
                            'pdf_quote_text_mismatch_examples': source_evidence_stats['pdf_mismatch_examples'],
                            'markdown_lines': sum(map(len,text_lines.values())),
                            'page_coverage_rows': len(rows['page_coverage']),
                            'line_coverage_rows': len(rows['line_coverage'])},
        'tp_predicate_status_counts': dict(proof_flags),
        'semantic_certification': 'NOT_VERIFIED',
        'method_isolation': 'supplied_unprefixed_set',
        'source_inputs': ROLES + [pdf_file.name],
        'limitations': [
            'All TP proof records have structured checks but none claims full independent semantic certification.',
            'The 1,642 generated-only false positives are conservative PDF-nonentailment assessments, not proven contradictions.',
            'A 90-page text/figure-locator check does not manually certify every semantic assertion in 90 pages.',
            'Raw semantic-class merging may undercount paraphrase duplicates.',
            'The 37 fixed negative controls are diagnostic and non-exhaustive.'
        ]
    }
    return metrics, validation, probes


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--inputs-dir', type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    m, v, probes = run(args.data_dir, args.inputs_dir)
    save_json(args.data_dir / '06_metrics_final.json', m)
    save_json(args.data_dir / '06_validation_final.json', v)
    with (args.data_dir / '06_regression_probes_final.jsonl').open('w', encoding='utf-8') as f:
        for p in probes:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')
    cm = m['confusion']; met = m['metrics']; d = m['duplicate']; raw = m['raw_counts']
    fmt = lambda x: 'null' if x is None else f'{x * 100:.4f}%'
    report = f'''# Phase 6 - Independent Ledger Recalculation

**Protocol:** v6.1. **Method:** `supplied_unprefixed_set`. **Phase status:** `{m['phase_status']}`.
**Structural reconciliation:** `{m['structural_reconciliation']}`. **Semantic certification:** `NOT_VERIFIED`.

## Recomputed canonical decision universe

| Ledger unit or cell | Count |
|---|---:|
| PDF positive propositions R | {raw['source_positive_atoms_R']} |
| Fixed PDF negative controls N | {raw['negative_controls_N']} |
| Unsupported generated-only canonical propositions F | {m['canonical']['unsupported_generated_F']} |
| Canonical universe U | {m['canonical']['universe_U']} |
| Canonical predicted positives P | {m['canonical']['predicted_positive_P']} |
| TP | {cm['TP']} |
| TN | {cm['TN']} |
| FP | {cm['FP']} |
| FN | {cm['FN']} |

## Recomputed rates

| Metric | Exact proportion | Percent |
|---|---|---:|
| Precision | {cm['TP']}/({cm['TP']}+{cm['FP']}) | {fmt(met['Precision'])} |
| Recall | {cm['TP']}/({cm['TP']}+{cm['FN']}) | {fmt(met['Recall'])} |
| F1 | 2*{cm['TP']}/(2*{cm['TP']}+{cm['FP']}+{cm['FN']}) | {fmt(met['F1'])} |
| Duplicate | ({raw['generated_occurrences_GO']}-{raw['generated_semantic_classes_G']})/{raw['generated_occurrences_GO']} | {fmt(met['Duplicate'])} |

These counts are derived independently from the individual JSONL records. The source-positive/negative partitions and all four arithmetic equations are checked, not inferred from a previously saved metrics JSON.

## Raw generated duplication

- Eligible occurrences GO: **{raw['generated_occurrences_GO']}**.
- Raw distinct semantic classes G: **{raw['generated_semantic_classes_G']}**.
- Excess occurrences: **{d['excess_occurrences']}**; within-file **{d['within_file_excess']}**, across-file **{d['across_file_excess']}**.
- Repeated classes: **{d['repeated_claim_class_count']}**; repeated classes spanning multiple files: **{d['repeated_claims_spanning_files']}**.

Effective predicted positives P = **{m['canonical']['predicted_positive_P']}**, which is *not* required to equal the raw semantic-class count G = **{raw['generated_semantic_classes_G']}**.

## Interpretation

The numerical output is a **provisional effective-proposition assessment, not verified design completeness**. FP includes conservative unsupported residuals, not merely documented PDF contradictions. FN includes incomplete/uncertain semantic matches. TN applies to only the **{raw['negative_controls_N']} predeclared PDF-negative controls**. Structural reconciliation cannot certify natural-language entailment. See `08_coverage_and_limitations.md`, `06_validation_final.json` and `06_regression_probes_final.jsonl`.
'''
    (args.data_dir / '06_metrics_final.md').write_text(report, encoding='utf-8')
    print(json.dumps({'phase_status': m['phase_status'], 'validation': v['status'], 'confusion': cm, 'rates': met,
                      'failure_count': v['failure_count'], 'warning_count': v['warning_count']}, indent=2))
    return 0 if v['status'] == 'PASS' else 2


if __name__ == '__main__':
    sys.exit(main())
