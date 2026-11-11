import copy
import unittest
from collections import Counter, defaultdict
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, DecodedStreamObject, NumberObject, RectangleObject, TextStringObject

from server.evidence import EvidenceError, plan_record
from server.file_chunks import split_file


def make_pdf(pages=None, bookmarks=True, image=False, rotated=False):
    if pages is None:
        pages = [
            [("01 Accounts", 20, 760), ("Original evidence: account introduction.", 10, 730),
             ("1.1 Identity", 14, 680), ("Original evidence: alpha authentication.", 10, 650),
             ("1.2 Roles", 14, 520), ("Original evidence: beta permissions.", 10, 490)],
            [("Original evidence: beta continuation.", 10, 760), ("1.3 Exceptions", 14, 680),
             ("Original evidence: gamma denied.", 10, 650)],
            [("02 Billing", 20, 760), ("Original evidence: billing introduction.", 10, 730),
             ("2.1 Invoices", 14, 680), ("Original evidence: delta invoices.", 10, 650)],
        ]
    writer = PdfWriter()
    for rows in pages:
        page = writer.add_blank_page(width=600, height=800)
        fonts = DictionaryObject()
        for name, base in (("F1", "Helvetica"), ("F2", "Helvetica-Bold")):
            fonts[NameObject("/" + name)] = writer._add_object(DictionaryObject({
                NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"),
                NameObject("/BaseFont"): NameObject("/" + base),
            }))
        resources = DictionaryObject({NameObject("/Font"): fonts})
        operations = []
        for text, size, y in rows:
            escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            operations.append(f"BT /{'F2' if size >= 12 else 'F1'} {size} Tf 50 {y} Td ({escaped}) Tj ET")
        if image:
            obj = DecodedStreamObject()
            obj.set_data(b"\xff\x00\x00")
            obj.update({NameObject("/Type"): NameObject("/XObject"), NameObject("/Subtype"): NameObject("/Image"),
                        NameObject("/Width"): NumberObject(1), NameObject("/Height"): NumberObject(1),
                        NameObject("/BitsPerComponent"): NumberObject(8), NameObject("/ColorSpace"): NameObject("/DeviceRGB")})
            resources[NameObject("/XObject")] = DictionaryObject({NameObject("/Im1"): writer._add_object(obj)})
            operations.append("q 60 0 0 60 50 570 cm /Im1 Do Q")
        page[NameObject("/Resources")] = resources
        stream = DecodedStreamObject()
        stream.set_data("\n".join(operations).encode("ascii"))
        page[NameObject("/Contents")] = writer._add_object(stream)
        if rotated:
            page.rotate(90)
    if bookmarks:
        writer.add_outline_item("01 Accounts", 0)
        if len(pages) > 2:
            writer.add_outline_item("02 Billing", 2)
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def text_of(chunk):
    return "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(chunk.data)).pages)


class PDFSectionTests(unittest.TestCase):
    def test_indirect_resources_tj_arrays_and_in_scope_annotations_survive(self):
        reader = PdfReader(BytesIO(make_pdf()))
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_outline_item("01 Accounts", 0)
        writer.add_outline_item("02 Billing", 2)
        page = writer.pages[0]
        resource = page["/Resources"]
        page[NameObject("/Resources")] = writer._add_object(resource)
        stream = DecodedStreamObject()
        stream.set_data(page.get_contents().get_data().replace(
            b"(Original evidence: beta permissions.) Tj", b"[(Original evidence: beta ) 0 (permissions.)] TJ"))
        page[NameObject("/Contents")] = writer._add_object(stream)
        annotations = ArrayObject()
        for y, message in ((635, "Identity comment"), (475, "Role comment")):
            annotations.append(writer._add_object(DictionaryObject({
                NameObject("/Type"): NameObject("/Annot"), NameObject("/Subtype"): NameObject("/Text"),
                NameObject("/Rect"): RectangleObject((100, y, 120, y + 10)),
                NameObject("/Contents"): TextStringObject(message),
            })))
        page[NameObject("/Annots")] = annotations
        output = BytesIO()
        writer.write(output)
        chunks = split_file(output.getvalue(), "arrays.pdf")
        identity = next(c for c in chunks if c.section == "1.1 Identity")
        roles = next(c for c in chunks if c.section == "1.2 Roles")
        self.assertNotIn("beta permissions", text_of(identity))
        self.assertIn("beta permissions", text_of(roles))
        for chunk, expected in ((identity, "Identity comment"), (roles, "Role comment")):
            page = PdfReader(BytesIO(chunk.data)).pages[0]
            self.assertEqual([ref.get_object()["/Contents"] for ref in page["/Annots"]], [expected])

    def test_one_unsupported_page_disables_inferred_sections_for_its_chapter(self):
        reader = PdfReader(BytesIO(make_pdf()))
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.pages[1].rotate(90)
        writer.add_outline_item("01 Accounts", 0)
        writer.add_outline_item("02 Billing", 2)
        output = BytesIO()
        writer.write(output)
        chunks = split_file(output.getvalue(), "mixed-layout.pdf")
        self.assertFalse(any(":section-" in c.section_id for c in chunks if c.chapter == "01 Accounts"))
        self.assertTrue(any(c.section == "2.1 Invoices" for c in chunks))
        self.assertIn("beta continuation", "\n".join(text_of(c) for c in chunks))

    def test_sections_on_same_page_are_separate_pdfs_without_hidden_neighbor_text(self):
        chunks = split_file(make_pdf(image=True), "sections.pdf")
        identity = next(c for c in chunks if c.section == "1.1 Identity")
        roles = next(c for c in chunks if c.section == "1.2 Roles")
        self.assertEqual(identity.chapter, "01 Accounts")
        self.assertEqual(identity.chapter_id, roles.chapter_id)
        self.assertNotEqual(identity.section_id, roles.section_id)
        self.assertEqual((roles.start, roles.end), (1, 2))
        self.assertIn("alpha authentication", text_of(identity))
        self.assertNotIn("beta permissions", text_of(identity))
        self.assertIn("beta permissions", text_of(roles))
        self.assertIn("beta continuation", text_of(roles))
        self.assertNotIn("alpha authentication", text_of(roles))
        self.assertNotIn("gamma denied", text_of(roles))
        image = PdfReader(BytesIO(identity.data)).pages[0]["/Resources"]["/XObject"]["/Im1"].get_object()
        self.assertEqual(image.get_data(), b"\xff\x00\x00")
        region = identity.source_regions[0]
        self.assertLess(region["bottom"], 570)
        self.assertGreater(region["top"], 630)
        self.assertTrue(any("Introduction" in c.section and "account introduction" in text_of(c) for c in chunks))

    def test_numbered_headings_work_without_bookmarks(self):
        chunks = split_file(make_pdf(bookmarks=False), "no-bookmarks.pdf")
        self.assertEqual({c.section for c in chunks if ":section-" in c.section_id},
                         {"1.1 Identity", "1.2 Roles", "1.3 Exceptions", "2.1 Invoices"})
        self.assertEqual(len({c.chapter_id for c in chunks if c.chapter != "Front matter"}), 2)

    def test_big_sections_keep_parent_and_section_ids_and_carry_context(self):
        rows = [("01 Accounts", 20, 780), ("Introduction.", 10, 755), ("1.1 Rules", 14, 725)]
        rows += [(f"Row {i:02d} contains an independent account constraint with a unique value {i:02d}.", 10, 700 - i * 18) for i in range(30)]
        with patch.dict("os.environ", {"FILE_CHUNK_MAX_ESTIMATED_TOKENS": "150", "FILE_CHUNK_PAGE_TOKEN_ESTIMATE": "20"}):
            chunks = split_file(make_pdf([rows]), "large-section.pdf")
        parts = [c for c in chunks if c.section == "1.1 Rules"]
        self.assertGreater(len(parts), 1)
        self.assertEqual([c.part for c in parts], list(range(1, len(parts) + 1)))
        self.assertEqual(len({c.chapter_id for c in parts}), 1)
        self.assertEqual(len({c.section_id for c in parts}), 1)
        self.assertTrue(all(c.estimated_tokens <= 150 for c in parts))
        self.assertTrue(all(c.continuation_context for c in parts[1:]))
        content = "\n".join(text_of(c) for c in parts)
        for i in range(30):
            self.assertEqual(content.count(f"Row {i:02d} contains"), 1)

    def test_chapter_ownership_accepts_sibling_sections_and_rejects_split_chapters(self):
        chunks = split_file(make_pdf(), "chapters.pdf")
        groups = []
        for chapter in dict.fromkeys(c.chapter_id for c in chunks):
            groups.append({"title": "Context", "context": "Constraints", "basis": "Source headings",
                           "chunk_ids": [c.index for c in chunks if c.chapter_id == chapter]})
        plan = {"global_context": "Source document", "groups": groups}
        result = plan_record(copy.deepcopy(plan), chunks)
        self.assertEqual([g["title"] for g in result["groups"]], ["01 Accounts", "02 Billing"])
        invalid = copy.deepcopy(plan)
        members = invalid["groups"][0]["chunk_ids"]
        invalid["groups"][0]["chunk_ids"] = members[:1]
        invalid["groups"].insert(1, {**groups[0], "chunk_ids": members[1:]})
        with self.assertRaisesRegex(EvidenceError, "single adjudicator"):
            plan_record(invalid, chunks)
        invalid = copy.deepcopy(plan)
        invalid["groups"] = [{**groups[0], "chunk_ids": list(range(1, len(chunks) + 1))}]
        with self.assertRaisesRegex(EvidenceError, "boundary"):
            plan_record(invalid, chunks)

    def test_rotated_pages_use_conservative_page_boundaries(self):
        chunks = split_file(make_pdf(rotated=True), "rotated.pdf")
        self.assertFalse(any(":section-" in c.section_id for c in chunks))
        self.assertIn("alpha authentication", "\n".join(text_of(c) for c in chunks))
        self.assertIn("gamma denied", "\n".join(text_of(c) for c in chunks))

    def test_indivisible_line_reports_budget_failure(self):
        with patch.dict("os.environ", {"FILE_CHUNK_MAX_ESTIMATED_TOKENS": "20", "FILE_CHUNK_PAGE_TOKEN_ESTIMATE": "20"}):
            with self.assertRaises(HTTPException) as raised:
                split_file(make_pdf(), "too-small.pdf")
        self.assertEqual(raised.exception.status_code, 413)


DATASET = Path(__file__).resolve().parents[4] / "dataset/OrionDesk_AI_Detailed_Design_Specification.pdf"


@unittest.skipUnless(DATASET.exists(), "Repository sample PDF is not available")
class OrionDocumentTests(unittest.TestCase):
    def test_actual_document_sections_cover_all_original_page_text_and_regions(self):
        original = PdfReader(DATASET)
        chunks = split_file(DATASET.read_bytes(), DATASET.name)
        self.assertEqual(len({c.section_id for c in chunks if ":section-" in c.section_id}), 110)
        sections = {c.section: c for c in chunks}
        self.assertNotIn("5.3 Tenant Isolation", text_of(sections["5.2 Authorization Model"]))
        regions, characters = defaultdict(list), defaultdict(Counter)
        for chunk in chunks:
            for page, region in zip(PdfReader(BytesIO(chunk.data)).pages, chunk.source_regions):
                regions[region["page"]].append((region["bottom"], region["top"]))
                characters[region["page"]].update(c for c in (page.extract_text() or "") if not c.isspace())
        for number, page in enumerate(original.pages, 1):
            spans = sorted(regions[number])
            self.assertAlmostEqual(spans[0][0], float(page.cropbox.bottom))
            self.assertAlmostEqual(spans[-1][1], float(page.cropbox.top))
            for left, right in zip(spans, spans[1:]):
                self.assertAlmostEqual(left[1], right[0])
            self.assertEqual(characters[number], Counter(c for c in (page.extract_text() or "") if not c.isspace()), f"Page {number}")


if __name__ == "__main__":
    unittest.main()
