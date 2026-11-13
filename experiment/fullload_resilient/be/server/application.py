import asyncio
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from server.chat import generate_specifications
from server.input_files import validate_file
from server.models import AppServices
from server import output_files as output_storage
from server.output_files import OutputFiles
from server.resume import load_resume, run_identity
from server.specifications import SPECIFICATION_STAGES, specification_result
from server.security import verify_api_key
from server.services import get_services, lifespan
from server.utils import MAX_BYTES, raise_internal_error, safe_basename


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def _elapsed_ms(start: float) -> int:
    return max(0, int((time.perf_counter() - start) * 1000))


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        dependencies=[Depends(verify_api_key)],
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    @app.get("/")
    def read_root():
        return {"status": "ok"}

    @app.post("/upload")
    async def upload_endpoint(
        file: UploadFile = File(...),
        resume_from: str | None = Form(None),
        allow_legacy_resume: bool = Form(False),
        services: AppServices = Depends(get_services),
    ):
        total_started_at = time.perf_counter()
        original_filename = file.filename or ""
        try:
            file_bytes = await file.read(MAX_BYTES + 1)
            prefix = int(datetime.now(timezone.utc).timestamp())
            file_name = f"{prefix}-{safe_basename(original_filename)}"
            validate_file(file_bytes, file_name)
            if allow_legacy_resume and not resume_from:
                raise HTTPException(status_code=400, detail="allow_legacy_resume requires resume_from")
            identity = await asyncio.to_thread(run_identity, file_bytes, file_name)
            resume_state = None
            if resume_from is not None:
                resume_state = await asyncio.to_thread(
                    load_resume, output_storage.OUTPUT_DIR, resume_from, identity, allow_legacy=allow_legacy_resume,
                )
                file_name = resume_state["file_name"] or file_name
                logger.info(
                    "Resume accepted: source_run=%s reused_stages=%d unverified_stages=%s",
                    resume_from, len(resume_state["specifications"]), resume_state["resume"]["unverified_stages"],
                )
            resume_metadata = {"resume": resume_state["resume"]} if resume_state else {}
            logger.info(
                "Upload accepted: file_name=%s original_filename=%s bytes=%d",
                file_name,
                original_filename,
                len(file_bytes),
            )

            output_files = OutputFiles(identity=identity)
            llm_started_at = time.perf_counter()

            async def save_stage(result):
                snapshot = {
                    "file_name": file_name,
                    "request": "generate_specifications",
                    **result,
                    **resume_metadata,
                    "timing_ms": {"llm": _elapsed_ms(llm_started_at)},
                }
                saved = await asyncio.to_thread(
                    output_files.save, snapshot, complete=False, total_started_at=total_started_at,
                )
                logger.info(
                    "Stage output saved: file_name=%s completed=%d/%d markdown_files=%d directory=%s",
                    file_name, len(saved["specifications"]), len(SPECIFICATION_STAGES),
                    len(saved["output_files"]["markdown"]), output_files.directory,
                )

            if resume_state:
                # Preserve the completed prefix in a new run before any model calls.
                await save_stage(specification_result(resume_state["specifications"]))
            logger.info("Specification generation started: file_name=%s", file_name)
            result = await generate_specifications(
                services=services,
                file_bytes=file_bytes,
                file_name=file_name,
                on_stage_completed=save_stage,
                resume_state=resume_state,
            )
            llm_ms = _elapsed_ms(llm_started_at)
            total_ms = _elapsed_ms(total_started_at)
            payload = {
                "file_name": file_name,
                "request": "generate_specifications",
                "reply": result["reply"],
                "specifications": result["specifications"],
                "usage": result["usage"],
                **resume_metadata,
                "usage_scope": "completed_stages",
                "timing_ms": {
                    "llm": llm_ms,
                    "total": total_ms,
                },
            }
            payload = await asyncio.to_thread(output_files.save, payload, total_started_at=total_started_at)
            logger.info(
                "Output files saved: file_name=%s markdown_files=%d directory=%s",
                file_name, len(payload["output_files"]["markdown"]), output_files.directory,
            )
            logger.info(
                "Upload completed: file_name=%s llm_elapsed_ms=%d total_elapsed_ms=%d "
                "input_tokens=%s output_tokens=%s total_tokens=%s",
                file_name,
                llm_ms,
                payload["timing_ms"]["total"],
                result["usage"]["input_tokens"],
                result["usage"]["output_tokens"],
                result["usage"]["total_tokens"],
            )
            return JSONResponse(payload)
        except HTTPException:
            raise
        except Exception:
            raise_internal_error()
        finally:
            await file.close()

    return app
