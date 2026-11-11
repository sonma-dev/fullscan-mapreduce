import base64
import json
import re
import unittest
from io import BytesIO
from types import SimpleNamespace

from pypdf import PdfReader

from server import chat
from server.models import AppServices
from test_chat import FakeResponses
from test_pdf_sections import make_pdf


class PDFResponses(FakeResponses):
    async def create_response(self, **kwargs):
        query = kwargs['query']
        phase = re.search(r'^Phase: (\w+)$', query, re.M)[1]
        if phase not in ('global_context', 'map'):
            return await super().create_response(**kwargs)
        payload = json.loads(query.split('<payload>\n', 1)[1].rsplit('\n</payload>', 1)[0])
        match = re.search(r'^Stage: (\d+)/8$', query, re.M)
        step = int(match[1]) if match else 0
        self.calls.append((phase, step, payload))
        self.output_limits.append((phase, kwargs['max_output_tokens']))
        if phase == 'global_context':
            groups = []
            for chunk in payload['chunks']:
                if not groups or groups[-1]['title'] != chunk['chapter']:
                    groups.append({'title': chunk['chapter'], 'context': 'Source chapter meaning',
                                   'basis': 'Chapter heading', 'chunk_ids': []})
                groups[-1]['chunk_ids'].append(chunk['index'])
            value = {'global_context': 'Global business constraints', 'groups': groups}
        else:
            self.test.assertEqual(step, len(self.approved) + 1)
            chunk = payload['chunk']
            self.test.assertEqual(chunk['chapter_id'], payload['jurisdiction']['chapter_id'])
            pages = PdfReader(BytesIO(base64.b64decode(kwargs['input_file']['file_data'].split(',', 1)[1]))).pages
            self.test.assertEqual(len(pages), len(chunk['source_regions']))
            sources = []
            for page, region in zip(pages, chunk['source_regions']):
                self.test.assertAlmostEqual(float(page.cropbox.top), region['top'])
                self.test.assertAlmostEqual(float(page.cropbox.bottom), region['bottom'])
                evidence = next(line for line in page.extract_text().splitlines() if 'Original evidence' in line)
                sources.append({'unit': region['page'], 'quote': evidence})
            value = {'covered_units': list(range(chunk['start'], chunk['end'] + 1)), 'findings': [{
                'statement': 'Scoped source rule', 'scope': chunk['section'], 'strength': 'explicit',
                'conditions': [], 'exceptions': [], 'sources': sources,
            }], 'gaps': []}
        return SimpleNamespace(output_text=json.dumps(value), usage=SimpleNamespace(input_tokens=10, output_tokens=2, total_tokens=12))


class PDFHierarchyTests(unittest.IsolatedAsyncioTestCase):
    async def test_eight_stages_use_chapter_forks_with_section_leaves_and_source_regions(self):
        fake = PDFResponses(self)
        with self.assertLogs('server', level='INFO'):
            result = await chat.generate_specifications(AppServices(responses=fake), make_pdf(), 'chapters.pdf')
        self.assertEqual(len(result['specifications']), 8)
        chunks = result['chunks']
        self.assertEqual(len(chunks), 6)
        self.assertEqual(len({chunk['chapter_id'] for chunk in chunks}), 2)
        self.assertEqual(len({chunk['section_id'] for chunk in chunks}), 6)
        for audit in result['hierarchy']['stages']:
            attempt = audit['attempts'][0]
            self.assertEqual(len(attempt['nodes']), 2)
            for node in attempt['nodes']:
                members = [chunks[index - 1] for index in node['jurisdiction']['chunk_ids']]
                self.assertEqual({chunk['chapter_id'] for chunk in members}, {node['node']})
            for scan in attempt['scans']:
                chunk = chunks[scan['chunk_id'] - 1]
                for finding in scan['findings']:
                    for source in finding['sources']:
                        region = next(r for r in chunk['source_regions'] if r['page'] == source['unit'])
                        self.assertEqual(source['region'], {'bottom': region['bottom'], 'top': region['top']})
        self.assertEqual(result['usage']['total_tokens'], len(fake.calls) * 12)


if __name__ == '__main__':
    unittest.main()
