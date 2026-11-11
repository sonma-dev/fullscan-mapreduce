"""Chapter/section PDF leaves with original page coordinates and bounded parts.

Only simple horizontal page content is cut within a page. Complex Form XObjects
and rotated text use whole-page boundaries so uncertain coordinates cannot erase
source material. No OCR or semantic heading inference is performed.
"""

import logging
import math
import re
from collections import Counter
from dataclasses import dataclass
from io import BytesIO

from fastapi import HTTPException
from pypdf import PdfWriter
from pypdf.generic import ArrayObject, ByteStringObject, ContentStream, NameObject, RectangleObject

logger = logging.getLogger(__name__)
SECTION = re.compile(r"^(\d{1,3}\.\d+)(?![\d.])\s+\S")
SUBSECTION = re.compile(r"^\d{1,3}\.\d+\.\d+(?:\.\d+)*\s+\S")
CHAPTER = re.compile(r"^(?:(?:Chapter\s+)?(\d{1,3})[.)]?\s+|第\s*(\d+)\s*章\s*)(\S.*)$", re.I)
SHOW = {b"Tj", b"TJ", b"'", b'"'}


def estimate_tokens(text):
    """Operational estimate, not a model tokenizer or an API token guarantee."""
    return math.ceil(len(text.encode("utf-8")) / 3)


@dataclass(frozen=True)
class Line:
    text: str
    y: float
    size: float
    font: str
    x: float


@dataclass
class PageLayout:
    page: object
    lines: list[Line]
    operations: list
    text_y: dict[int, float]
    image_ranges: list[tuple[float, float]]
    safe: bool

    @property
    def top(self):
        return float(self.page.cropbox.top)

    @property
    def bottom(self):
        return float(self.page.cropbox.bottom)

    def text(self, bottom, top):
        return "\n".join(line.text for line in self.lines if bottom <= line.y < top)


def _layout(page):
    lines, text_y, images = [], {}, []
    content = page.get_contents()
    operations = ContentStream(content, page.pdf, "bytes").operations if content is not None else []
    resource_value = page.get("/Resources")
    resources = resource_value.get_object() if resource_value is not None else {}
    object_value = resources.get("/XObject")
    objects = object_value.get_object() if object_value is not None else {}
    safe = not page.rotation
    index = 0

    def operands(op, args, cm, tm):
        nonlocal index, safe
        if op == b"BDC":
            # Tagged replacement text (ActualText) may survive a visual crop.
            safe = False
        if op in SHOW:
            text_y[index] = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            if abs(cm[1]) > 0.001 or abs(cm[2]) > 0.001 or abs(tm[1]) > 0.001 or abs(tm[2]) > 0.001 or op in {b"'", b'"'}:
                safe = False
        if op == b"Do":
            obj = objects.get(args[0])
            if obj is not None:
                subtype = obj.get_object().get("/Subtype")
                if subtype == "/Form":
                    safe = False
                elif subtype == "/Image":
                    ys = [cm[5], cm[1] + cm[5], cm[3] + cm[5], cm[1] + cm[3] + cm[5]]
                    images.append((min(ys), max(ys)))
        index += 1

    def text(value, cm, tm, font, size):
        y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
        x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
        scale = math.hypot(cm[2], cm[3])
        for offset, line in enumerate(value.splitlines()):
            if line.strip():
                lines.append(Line(line.strip(), y - offset * size * 1.2 * scale, size * scale,
                                  str(font.get("/BaseFont", "")) if font else "", x))

    page.extract_text(visitor_operand_before=operands, visitor_text=text)
    # Form recursion changes the operand sequence; never rewrite it speculatively.
    safe = safe and (index == len(operations) or not text_y)
    return PageLayout(page, lines, operations, text_y, images, safe)


def _body_size(layout):
    sizes = Counter()
    normal = [line for line in layout.lines if not any(style in line.font.lower() for style in ("bold", "heavy", "black"))]
    for line in normal or layout.lines:
        sizes[round(line.size, 1)] += len(line.text)
    return sizes.most_common(1)[0][0] if sizes else 10


def _heading(line, body, minimum=1.15):
    return line.size >= body * minimum and ("bold" in line.font.lower() or line.size >= body * 1.3)


def _outlines(reader, layouts):
    entries = []

    def walk(items, parent=None, path=()):
        last = parent
        for item in items:
            if isinstance(item, list):
                walk(item, last, last["path"] if last else path)
                continue
            page = reader.get_destination_page_number(item)
            if page is None or not 0 <= page < len(layouts):
                continue
            title = str(item.title)
            chapter_id = parent["chapter_id"] if parent else f"pdf-chapter-{len(entries) + 1}"
            last = {"page": page, "top": layouts[page].top, "path": (*path, title),
                    "chapter": parent["chapter"] if parent else title, "chapter_id": chapter_id,
                    "section": " / ".join((*path, title)), "section_id": f"pdf-outline-{len(entries) + 1}"}
            # Prefer the actual heading position over a bookmark's imprecise Fit destination.
            if parent and layouts[page].safe:
                match = next((line for line in layouts[page].lines if line.text == title), None)
                if match:
                    last["top"] = min(layouts[page].top, match.y + match.size + 3)
            entries.append(last)

    walk(reader.outline)
    return entries


def _boundaries(reader, layouts):
    outlines = _outlines(reader, layouts)
    chapter_entries = [entry for entry in outlines if len(entry["path"]) == 1]
    # Without bookmarks, large numbered headings can still establish chapters.
    if not chapter_entries:
        for page, layout in enumerate(layouts):
            body = _body_size(layout)
            for line in layout.lines:
                if CHAPTER.match(line.text) and _heading(line, body, 1.5):
                    entry = {"page": page, "top": min(layout.top, line.y + line.size + 3) if layout.safe else layout.top,
                             "path": (line.text,), "chapter": line.text, "chapter_id": f"pdf-chapter-{len(chapter_entries) + 1}",
                             "section": line.text, "section_id": f"pdf-intro-{len(chapter_entries) + 1}"}
                    chapter_entries.append(entry)
                    outlines.append(entry)
    chapters = sorted(chapter_entries, key=lambda item: (item["page"], -item["top"]))
    boundaries = {(entry["page"], entry["top"]): entry for entry in outlines}
    sections_found = 0
    for ci, chapter in enumerate(chapters):
        end = chapters[ci + 1]["page"] if ci + 1 < len(chapters) else len(layouts)
        last_page = end
        if ci + 1 < len(chapters) and chapters[ci + 1]["top"] < layouts[end].top:
            last_page += 1
        if any(not layout.safe for layout in layouts[chapter["page"]:last_page]):
            logger.info("PDF chapter uses outline/page fallback for complex layout: chapter=%s", chapter["chapter"])
            continue
        match = CHAPTER.match(chapter["chapter"])
        number = str(int(match[1] or match[2])) if match else None
        candidates = []
        for page in range(chapter["page"], min(end + 1, len(layouts))):
            layout = layouts[page]
            if not layout.safe:
                continue
            body = _body_size(layout)
            for line in layout.lines:
                section_match = SECTION.match(line.text)
                position = (page, -(line.y + line.size + 3))
                start_pos = (chapter["page"], -chapter["top"])
                end_pos = (chapters[ci + 1]["page"], -chapters[ci + 1]["top"]) if ci + 1 < len(chapters) else (len(layouts), 0)
                if (number and section_match and section_match[1].split(".")[0] == number
                        and _heading(line, body) and start_pos <= position < end_pos):
                    candidates.append((page, line, section_match[1]))
        # Numbered headings must be unique and increasing within the chapter.
        numbers = [tuple(map(int, item[2].split("."))) for item in candidates]
        aligned = not candidates or max(item[1].x for item in candidates) - min(item[1].x for item in candidates) <= 20
        if numbers != sorted(set(numbers)) or not aligned:
            logger.warning("Ambiguous PDF section headings; using outline boundaries: chapter=%s", chapter["chapter"])
            continue
        for page, line, number in candidates:
            top = min(layouts[page].top, line.y + line.size + 3)
            if any(low < top < high for low, high in layouts[page].image_ranges):
                continue
            boundaries[(page, top)] = {**chapter, "page": page, "top": top, "section": line.text,
                                       "section_id": f'{chapter["chapter_id"]}:section-{number}',
                                       "path": (chapter["chapter"], line.text)}
            sections_found += 1
        if candidates:
            chapter["section"] = f'{chapter["chapter"]} / Introduction'
            # Replace the initial chapter record, preserving any nested section boundary.
            boundaries[(chapter["page"], chapter["top"])] = chapter
    if (0, layouts[0].top) not in boundaries:
        boundaries[(0, layouts[0].top)] = {
            "page": 0, "top": layouts[0].top, "path": (), "chapter": "Front matter" if chapters else "",
            "chapter_id": "pdf-front-matter" if chapters else "", "section": "Front matter" if chapters else "",
            "section_id": "pdf-front-matter" if chapters else "",
        }
    logger.info("PDF structure detected: pages=%d chapters=%d numbered_sections=%d", len(layouts), len(chapters), sections_found)
    return sorted(boundaries.values(), key=lambda item: (item["page"], -item["top"]))


def _pieces(layout, bottom, top, budget, visual_tokens):
    """Split oversized regions at subheadings, paragraph gaps, then whole lines."""
    def cost(low, high):
        return estimate_tokens(layout.text(low, high)) + visual_tokens

    if cost(bottom, top) <= budget:
        return [(bottom, top, cost(bottom, top))]
    if not layout.safe:
        raise HTTPException(413, "A complex PDF page exceeds the chunk token estimate budget; increase FILE_CHUNK_MAX_ESTIMATED_TOKENS")
    lines = sorted((line for line in layout.lines if bottom <= line.y < top), key=lambda line: -line.y)
    candidates = []
    for previous, line in zip(lines, lines[1:]):
        cut = min(line.y + line.size + 2, (previous.y + line.y) / 2)
        if cut <= line.y or any(low < cut < high for low, high in layout.image_ranges):
            continue
        priority = 2 if SUBSECTION.match(line.text) else int(previous.y - line.y > max(previous.size, line.size) * 1.7)
        candidates.append((cut, priority))
    pieces = []
    while cost(bottom, top) > budget:
        fitting = [(cut, priority) for cut, priority in candidates if bottom < cut < top and cost(cut, top) <= budget]
        if not fitting:
            raise HTTPException(413, "An indivisible PDF line or figure exceeds FILE_CHUNK_MAX_ESTIMATED_TOKENS")
        preferred = [pair for pair in fitting if pair[1] == max(p[1] for p in fitting)]
        cut = min(pair[0] for pair in preferred)
        pieces.append((cut, top, cost(cut, top)))
        top = cut
    pieces.append((bottom, top, cost(bottom, top)))
    return pieces


def _write_pdf(layouts, regions):
    writer = PdfWriter()
    for region in regions:
        layout = layouts[region["page"] - 1]
        bottom, top = region["bottom"], region["top"]
        page = writer.add_page(layout.page)
        if bottom == layout.bottom and top == layout.top:
            continue
        # Crop graphics and remove out-of-scope text, since cropbox alone leaves
        # invisible text extractable by PDF file-input parsers.
        stream = ContentStream(None, writer)
        stream.operations = []
        for index, (args, op) in enumerate(layout.operations):
            if index in layout.text_y and not bottom <= layout.text_y[index] < top:
                args = list(args)
                args[-1] = (ArrayObject([item if not isinstance(item, (str, bytes)) else ByteStringObject(b"") for item in args[-1]])
                            if op == b"TJ" else ByteStringObject(b""))
            stream.operations.append((args, op))
        page[NameObject("/Contents")] = writer._add_object(stream)
        rectangle = RectangleObject((float(page.cropbox.left), bottom, float(page.cropbox.right), top))
        page.cropbox = rectangle
        page.mediabox = RectangleObject(rectangle)
        # Keep annotations intersecting this region, including source comments.
        annotations = page.get("/Annots")
        if annotations is not None:
            kept = []
            for reference in annotations.get_object():
                rect = reference.get_object().get("/Rect")
                if rect is None or (float(rect[3]) >= bottom and float(rect[1]) <= top):
                    kept.append(reference)
            page[NameObject("/Annots")] = ArrayObject(kept)
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def _continuation_context(layouts, regions, start):
    """Carry opening text and recent bold headings/table labels as context only."""
    opening, labels = [], []
    for region in regions:
        for line in layouts[region["page"] - 1].lines:
            if not region["bottom"] <= line.y < region["top"]:
                continue
            if (region["page"], -line.y) >= (start["page"], -start["top"]):
                continue
            item = {"page": region["page"], "text": line.text}
            if len(opening) < 6:
                opening.append(item)
            if "bold" in line.font.lower() or SUBSECTION.match(line.text):
                labels.append(item)
    result, used = [], set()
    for item in [*labels[-8:], *opening]:
        key = (item["page"], item["text"])
        if key not in used and sum(len(entry["text"]) for entry in result) + len(item["text"]) <= 1200:
            result.append(item)
            used.add(key)
    return tuple(result)


def split_pdf_sections(reader, stem, max_pages, token_budget, visual_tokens):
    from server.file_chunks import FileChunk

    layouts = [_layout(page) for page in reader.pages]
    boundaries = _boundaries(reader, layouts)
    index = 0
    for offset, boundary in enumerate(boundaries):
        next_boundary = boundaries[offset + 1] if offset + 1 < len(boundaries) else {"page": len(layouts), "top": 0}
        regions = []
        for page in range(boundary["page"], min(next_boundary["page"] + 1, len(layouts))):
            layout = layouts[page]
            top = boundary["top"] if page == boundary["page"] else layout.top
            bottom = next_boundary["top"] if page == next_boundary["page"] else layout.bottom
            if top <= bottom:
                continue
            for low, high, estimate in _pieces(layout, bottom, top, token_budget, visual_tokens):
                regions.append({"page": page + 1, "bottom": low, "top": high, "estimated_tokens": estimate})
        part = 0
        all_regions = list(regions)
        while regions:
            part += 1
            selected, total = [], 0
            while regions and len(selected) < max_pages and total + regions[0]["estimated_tokens"] <= token_budget:
                # Keep disjoint pieces on the same source page in separate leaves.
                if selected and selected[-1]["page"] == regions[0]["page"]:
                    break
                region = regions.pop(0)
                total += region["estimated_tokens"]
                selected.append(region)
            if not selected:
                raise HTTPException(413, "PDF region exceeds the configured chunk budget")
            index += 1
            yield FileChunk(
                index, f"{stem}-section-{offset + 1:03d}-part-{part:02d}.pdf", _write_pdf(layouts, selected),
                "Pages", selected[0]["page"], selected[-1]["page"], boundary["section"], tuple(boundary["path"]),
                boundary["section_id"], boundary["chapter"], boundary["chapter_id"], part, tuple(selected), total,
                _continuation_context(layouts, all_regions, selected[0]) if part > 1 else (),
            )
