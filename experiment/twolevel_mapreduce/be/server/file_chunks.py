from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePosixPath
from zipfile import BadZipFile

from fastapi import HTTPException
from lxml.etree import XMLSyntaxError
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn

from server.input_files import validate_file
from server.utils import MAX_BYTES, env_int


@dataclass(frozen=True)
class FileChunk:
    index: int
    file_name: str
    data: bytes
    unit: str
    start: int
    end: int
    section: str = ""
    headings: tuple[str, ...] = ()
    section_id: str = ""
    chapter: str = ""
    chapter_id: str = ""
    part: int = 1
    source_regions: tuple[dict, ...] = ()
    estimated_tokens: int = 0
    continuation_context: tuple[dict, ...] = ()

    @property
    def title(self) -> str:
        return f"{self.unit} {self.start}-{self.end}"


def _ranges(count: int, size: int, sections: dict[int, str]):
    """Preserve native section boundaries, then cap the size of each leaf."""
    boundaries = sorted({0, count, *sections})
    for left, right in zip(boundaries, boundaries[1:]):
        for start in range(left, right, size):
            section = sections.get(left, "")
            yield start, min(start + size, right), section, f"native-{left + 1}" if section else ""


def _append_chunk(chunks: list[FileChunk], chunk: FileChunk):
    # PPTX chunks duplicate layouts/assets. Bound their cumulative memory too.
    if len(chunks) >= 256 or sum(len(item.data) for item in chunks) + len(chunk.data) > 3 * MAX_BYTES:
        raise HTTPException(status_code=413, detail="Split document exceeds the chunk count or memory budget")
    chunks.append(chunk)


def split_file(
    file_bytes: bytes,
    file_name: str,
    max_pages: int = 8,
    max_slides: int = 8,
) -> list[FileChunk]:
    suffix = validate_file(file_bytes, file_name)
    if max_pages < 1 or max_slides < 1:
        raise ValueError("Chunk size must be positive")
    stem = PurePosixPath(file_name).stem
    if suffix == ".pdf":
        return _split_pdf(file_bytes, stem, max_pages)
    return _split_pptx(file_bytes, stem, max_slides)


def _split_pdf(data: bytes, stem: str, size: int) -> list[FileChunk]:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError
    from server.pdf_sections import split_pdf_sections

    try:
        reader = PdfReader(BytesIO(data))
        if reader.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported")
        count = len(reader.pages)
        if not count:
            raise ValueError("The PDF has no pages")
        chunks = []
        for chunk in split_pdf_sections(
            reader, stem, size,
            env_int("FILE_CHUNK_MAX_ESTIMATED_TOKENS", 12000, 100000),
            env_int("FILE_CHUNK_PAGE_TOKEN_ESTIMATE", 2000, 10000),
        ):
            _append_chunk(chunks, chunk)
        return chunks
    except (PdfReadError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="Invalid, empty, or encrypted PDF") from exc


def _split_pptx(data: bytes, stem: str, size: int) -> list[FileChunk]:
    try:
        original = Presentation(BytesIO(data))
        count = len(original.slides)
        if not count:
            raise ValueError("The presentation has no slides")
        titles = tuple(slide.shapes.title.text if slide.shapes.title is not None else "" for slide in original.slides)
        positions = {slide.slide_id: index for index, slide in enumerate(original.slides)}
        sections = {}
        # Office sections are extension elements, outside python-pptx's API.
        for section in original.element.iter("{http://schemas.microsoft.com/office/powerpoint/2010/main}section"):
            ids = [int(item.get("id")) for item in section.iter("{http://schemas.microsoft.com/office/powerpoint/2010/main}sldId")]
            members = sorted(positions[slide_id] for slide_id in ids if slide_id in positions)
            if members:
                sections[members[0]] = section.get("name", "")
        del original
        chunks = []
        for start, end, section, section_id in _ranges(count, size, sections):
            deck = Presentation(BytesIO(data))
            # python-pptx has no public slide-deletion API. Retain each slide's
            # relationships so that images, charts, layouts, and notes survive.
            slide_ids = deck.slides._sldIdLst
            for position, slide_id in enumerate(list(slide_ids)):
                if not start <= position < end:
                    deck.part.drop_rel(slide_id.rId)
                    slide_ids.remove(slide_id)
            kept_parts = {slide.part for slide in deck.slides}
            for slide in deck.slides:
                for rel in list(slide.part.rels.values()):
                    if not rel.is_external and rel.reltype == RT.SLIDE and rel.target_part not in kept_parts:
                        # A link to a removed slide would otherwise serialize that
                        # slide (and its assets) back into the chunk's package.
                        for element in list(slide.element.iter()):
                            if element.get(qn("r:id")) == rel.rId:
                                element.getparent().remove(element)
                        slide.part.drop_rel(rel.rId)
            output = BytesIO()
            deck.save(output)
            _append_chunk(chunks, FileChunk(
                len(chunks) + 1, f"{stem}-slides-{start + 1}-{end}.pptx",
                output.getvalue(), "Slides", start + 1, end, section, titles[start:end], section_id,
            ))
        return chunks
    except (BadZipFile, KeyError, ValueError, XMLSyntaxError) as exc:
        raise HTTPException(status_code=400, detail="Invalid or empty PPTX") from exc
