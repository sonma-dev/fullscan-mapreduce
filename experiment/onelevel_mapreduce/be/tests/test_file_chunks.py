import base64
import re
import unittest
from io import BytesIO
from zipfile import ZipFile
from unittest.mock import patch

from fastapi import HTTPException
from pptx import Presentation
from pptx.util import Inches

from server.file_chunks import split_file


def make_deck(count=5):
    deck = Presentation()
    for number in range(1, count + 1):
        slide = deck.slides.add_slide(deck.slide_layouts[5])
        slide.shapes.title.text = f"Slide {number}"
        slide.notes_slide.notes_text_frame.text = f"Note {number}"
    output = BytesIO()
    deck.save(output)
    return output.getvalue()


class PowerPointChunkTests(unittest.TestCase):
    def test_native_sections_and_titles_define_chunk_boundaries(self):
        from lxml import etree
        deck = Presentation(BytesIO(make_deck(5)))
        ns = 'http://schemas.microsoft.com/office/powerpoint/2010/main'
        sections = etree.SubElement(deck.element, f'{{{ns}}}sectionLst')
        for name, slides in [('Access', list(deck.slides)[:2]), ('Billing', list(deck.slides)[2:])]:
            section = etree.SubElement(sections, f'{{{ns}}}section', name=name)
            members = etree.SubElement(section, f'{{{ns}}}sldIdLst')
            for slide in slides:
                etree.SubElement(members, f'{{{ns}}}sldId', id=str(slide.slide_id))
        output = BytesIO()
        deck.save(output)
        chunks = split_file(output.getvalue(), 'sections.pptx', max_slides=8)
        self.assertEqual([(c.start, c.end, c.section) for c in chunks], [(1, 2, 'Access'), (3, 5, 'Billing')])
        self.assertEqual(chunks[1].headings, ('Slide 3', 'Slide 4', 'Slide 5'))

    def test_duplicated_package_assets_are_bounded(self):
        with patch('server.file_chunks.MAX_BYTES', 1), self.assertRaises(HTTPException) as error:
            split_file(make_deck(2), 'sample.pptx', max_slides=1)
        self.assertEqual(error.exception.status_code, 413)

    def test_slide_order_ranges_and_notes_survive_splitting(self):
        chunks = split_file(make_deck(), "sample.PPTX", max_slides=2)
        self.assertEqual([(c.start, c.end) for c in chunks], [(1, 2), (3, 4), (5, 5)])
        self.assertEqual([c.index for c in chunks], [1, 2, 3])
        for chunk in chunks:
            deck = Presentation(BytesIO(chunk.data))
            self.assertEqual([s.shapes.title.text for s in deck.slides], [f"Slide {n}" for n in range(chunk.start, chunk.end + 1)])
            self.assertEqual([s.notes_slide.notes_text_frame.text for s in deck.slides], [f"Note {n}" for n in range(chunk.start, chunk.end + 1)])

    def test_images_survive_and_links_do_not_reintroduce_removed_slides(self):
        deck = Presentation(BytesIO(make_deck(3)))
        png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aE1sAAAAASUVORK5CYII=")
        deck.slides[0].shapes.add_picture(BytesIO(png), Inches(1), Inches(1))
        deck.slides[0].shapes.title.click_action.target_slide = deck.slides[2]
        data = BytesIO()
        deck.save(data)
        first = split_file(data.getvalue(), "linked.pptx", max_slides=1)[0]
        reopened = Presentation(BytesIO(first.data))
        self.assertEqual(reopened.slides[0].shapes[-1].image.blob, png)
        with ZipFile(BytesIO(first.data)) as archive:
            slides = [name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)]
            self.assertEqual(len(slides), 1)

    def test_invalid_and_empty_presentations_are_rejected(self):
        for data in (b"not a presentation", make_deck(0)):
            with self.assertRaises(HTTPException) as error:
                split_file(data, "bad.pptx")
            self.assertEqual(error.exception.status_code, 400)

    def test_chunk_boundaries(self):
        for count, size, expected in ((1, 8, 1), (8, 8, 1), (9, 8, 2)):
            with self.subTest(count=count):
                chunks = split_file(make_deck(count), "sample.pptx", max_slides=size)
                self.assertEqual(len(chunks), expected)
                self.assertEqual(sum(c.end - c.start + 1 for c in chunks), count)


class PDFChunkTests(unittest.TestCase):
    def test_nested_pdf_outline_preserves_native_semantic_boundaries(self):
        from pypdf import PdfWriter
        writer = PdfWriter()
        for _ in range(6):
            writer.add_blank_page(width=100, height=100)
        parent = writer.add_outline_item('Accounts', 0)
        writer.add_outline_item('Exceptions', 2, parent=parent)
        writer.add_outline_item('Billing', 4)
        output = BytesIO()
        writer.write(output)
        chunks = split_file(output.getvalue(), 'outlined.pdf', max_pages=8)
        self.assertEqual([(c.start, c.end, c.section) for c in chunks], [(1, 2, 'Accounts'), (3, 4, 'Accounts / Exceptions'), (5, 6, 'Billing')])

    def make_pdf(self, count=5, encrypt=False):
        from pypdf import PdfWriter
        writer = PdfWriter()
        for index in range(count):
            writer.add_blank_page(width=100 + index, height=200)
        if encrypt:
            writer.encrypt("password")
        output = BytesIO()
        writer.write(output)
        return output.getvalue()

    def test_pdf_page_order_and_ranges_survive_splitting(self):
        from pypdf import PdfReader
        chunks = split_file(self.make_pdf(), "sample.pdf", max_pages=2)
        self.assertEqual([(c.start, c.end) for c in chunks], [(1, 2), (3, 4), (5, 5)])
        widths = []
        for chunk in chunks:
            reader = PdfReader(BytesIO(chunk.data))
            self.assertEqual(len(reader.pages), chunk.end - chunk.start + 1)
            widths.extend(float(page.mediabox.width) for page in reader.pages)
        self.assertEqual(widths, [100, 101, 102, 103, 104])

    def test_invalid_empty_and_encrypted_pdfs_are_rejected(self):
        for data in (b"broken PDF", self.make_pdf(0), self.make_pdf(1, encrypt=True)):
            with self.assertRaises(HTTPException) as error:
                split_file(data, "bad.pdf")
            self.assertEqual(error.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
