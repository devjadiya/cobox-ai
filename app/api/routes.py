from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.core.job_manager import create_job, update_job, log, JOBS, cancel
from app.middleware.sanitization import sanitize_text
from app.core.intent_parser import parse_intent
from app.core.asset_resolver import resolve_assets
from app.core.scene_compiler import compile_scene

router = APIRouter(prefix="/ai")


class CommandRequest(BaseModel):
    text: str


@router.post("/command")
async def ai_command(req: CommandRequest, request: Request):
    job_id = create_job()

    try:
        update_job(job_id, status="running")

        text = sanitize_text(req.text)
        log(job_id, "Intent parsed")

        intent = parse_intent(text)

        assets = resolve_assets(intent, request.app.state.asset_index)
        log(job_id, f"Assets resolved: {len(assets)}")

        scene = compile_scene(intent, assets)
        log(job_id, "Scene compiled")

        update_job(job_id, status="done", result=scene)

    except Exception as e:
        update_job(job_id, status="error")
        log(job_id, str(e))

    return {"job_id": job_id}


@router.get("/status/{job_id}")
def status(job_id: str):
    return JOBS.get(job_id, {"error": "not found"})


@router.post("/cancel/{job_id}")
def cancel_job(job_id: str):
    cancel(job_id)
    return {"status": "cancelled"}


@router.get("/logs/{job_id}")
def logs(job_id: str):
    return JOBS[job_id]["logs"]
