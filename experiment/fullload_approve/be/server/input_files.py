import base64
from io import BytesIO
from pathlib import PurePosixPath

from fastapi import HTTPException
from openai.types.responses import ResponseInputFileParam
from pypdf import PdfReader
from pptx import Presentation

from server.utils import MAX_BYTES


FILE_MEDIA_TYPES = {
    ".pdf": "application/pdf",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


def validate_file(file_bytes: bytes, file_name: str) -> str:
    if not file_bytes:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")
    if len(file_bytes) > MAX_BYTES:
        raise HTTPException(status_code=413, detail=f"File too large (max {MAX_BYTES} bytes)")
    suffix = PurePosixPath(file_name).suffix.lower()
    if suffix not in FILE_MEDIA_TYPES:
        raise HTTPException(status_code=415, detail="Supported file types: PDF, PPTX")
    return suffix


def create_input_file(file_bytes: bytes, file_name: str) -> ResponseInputFileParam:
    suffix = validate_file(file_bytes, file_name)
    encoded = base64.b64encode(file_bytes).decode("ascii")
    return {
        "type": "input_file",
        "filename": file_name,
        "file_data": f"data:{FILE_MEDIA_TYPES[suffix]};base64,{encoded}",
    }


def source_manifest(file_bytes: bytes, file_name: str) -> dict:
    """Count original pages/slides; keep the original attachment intact."""
    suffix = validate_file(file_bytes, file_name)
    try:
        if suffix == ".pdf":
            count = len(PdfReader(BytesIO(file_bytes)).pages)
            unit_kind = "page"
        else:
            count = len(Presentation(BytesIO(file_bytes)).slides)
            unit_kind = "slide"
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Unable to read source pages or slides") from exc
    if count == 0:
        raise HTTPException(status_code=400, detail="The source document has no pages or slides")
    return {"file_name": file_name, "unit_kind": unit_kind, "source_unit_ids": list(range(1, count + 1))}
