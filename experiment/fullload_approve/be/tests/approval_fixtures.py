import json
from io import BytesIO
from types import SimpleNamespace

from pypdf import PdfWriter
from pptx import Presentation


def pdf_bytes(pages=2):
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=612, height=792)
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def pptx_bytes(slides=2):
    presentation = Presentation()
    for _ in range(slides):
        presentation.slides.add_slide(presentation.slide_layouts[6])
    output = BytesIO()
    presentation.save(output)
    return output.getvalue()


def payload(query):
    return json.loads(query.rsplit("<payload>\n", 1)[1].rsplit("\n</payload>", 1)[0])


def revision_feedback(query):
    if "<revision_feedback>\n" not in query:
        return []
    return json.loads(query.rsplit("<revision_feedback>\n", 1)[1].rsplit("\n</revision_feedback>", 1)[0])


def review_response(request, body="## Content\nNeeds confirmation", usage=None):
    if request.get("json_output"):
        value = {"approved": True,
                 "reviewed_source_unit_ids": payload(request["query"])["required_review"]["source_unit_ids"],
                 "rationale": "All original source units checked against the candidate.", "feedback": []}
        body = json.dumps(value)
    return SimpleNamespace(output_text=body, usage=usage)
