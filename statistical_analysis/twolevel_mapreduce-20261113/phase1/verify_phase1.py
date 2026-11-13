#!/usr/bin/env python3
"""Verify the reusable source-only Phase 1 evidence ledgers against the PDF.

Usage: python verify_phase1.py --pdf PATH [--directory PATH]
Requires PyMuPDF (fitz). Visual figure review remains a human task.
"""
import argparse
import collections
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import fitz


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path):
    with path.open(encoding='utf-8') as stream:
        return [json.loads(line) for line in stream if line.strip()]


def normalize(text):
    text = unicodedata.normalize('NFKC', text).replace('\u00ad', '')
    text = text.replace('’', "'").replace('“', '"').replace('”', '"')
    text = text.replace('–', '-').replace('—', '-').replace('≤', '<=').replace('≥', '>=').lower()
    return ' '.join(re.findall(r'[a-z0-9]+', text))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, required=True)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    directory = args.directory
    summary = json.loads((directory / '01_input_manifest_final.json').read_text(encoding='utf-8'))
    records = read_jsonl(directory / '01_source_atoms_final.jsonl')
    controls = read_jsonl(directory / '01_source_negative_controls_final.jsonl')
    proofs = read_jsonl(directory / '01_pdf_quote_verification_final.jsonl')
    coverage = read_jsonl(directory / '01_pdf_page_coverage_final.jsonl')
    assert sha256(args.pdf) == summary['reference_pdf']['sha256'], 'PDF SHA mismatch'
    assert sha256(directory / '01_source_atoms_final.jsonl') == summary['source_ledgers']['positive_sha256']
    assert sha256(directory / '01_source_negative_controls_final.jsonl') == summary['source_ledgers']['negative_sha256']
    assert len(records) == summary['source_ledgers']['positive_count']
    assert len(controls) == summary['source_ledgers']['negative_count']
    assert len(set(x['source_id'] for x in records)) == len(records)
    assert len(set(x['negative_control_id'] for x in controls)) == len(controls)
    assert len(coverage) == 90 and [x['physical_page'] for x in coverage] == list(range(1, 91))
    pdf = fitz.open(args.pdf)
    assert len(pdf) == 90
    texts = {
        idx + 1: [normalize(page.get_text('text', sort=False)), normalize(page.get_text('text', sort=True))]
        for idx, page in enumerate(pdf)
    }
    pdf_text = [p for p in proofs if p['evidence_type'] == 'PDF_TEXT']
    raster = [p for p in proofs if p['evidence_type'] != 'PDF_TEXT']
    for evidence in pdf_text:
        query = normalize(evidence['original_pdf_quote_en'])
        assert any(query in text for text in texts[evidence['physical_page']]), (
            evidence['record_id'], evidence['physical_page'])
    assert len(raster) == 3
    assert all(p['physical_page'] == 8 and p['verified_against_current_pdf'] for p in raster)
    assert pdf[7].get_images(full=True), 'Raster image missing for manual visual proof'
    assert len(proofs) == sum(len(x['pdf_evidence']) for x in records + controls)
    assert set(x['source_id'] for x in records).isdisjoint(x['negative_control_id'] for x in controls)
    for filename in ['01_source_atomization_challenge_final.jsonl', '09_excluded_units.jsonl']:
        assert read_jsonl(directory / filename)
    print(json.dumps({
        'result': 'PASS_PDF_TEXT_AND_STRUCTURE',
        'semantic_atomization_certified': False,
        'raster_figure_proofs': '3 previously manually visually reviewed; not automatically re-certified',
        'pdf_pages': len(pdf),
        'positive_atoms': len(records),
        'negative_controls': len(controls),
        'exact_text_evidence': len(pdf_text),
        'figure_image_evidence': len(raster),
        'all_evidence': len(proofs),
    }, indent=2))


if __name__ == '__main__':
    main()
