import base64
from pathlib import PurePosixPath

from fastapi import HTTPException
from openai.types.responses import ResponseInputFileParam

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
