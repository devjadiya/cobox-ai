from fastapi import APIRouter
from app.models.request import AIRequest
from app.services.scene_factory import create_scene_from_text
from app.core.job_store import create_job, update_job, get_job, cancel_job
import threading

router = APIRouter()

def run_scene_job(job_id, text):
    update_job(job_id, log="Intent parsed")
    result = create_scene_from_text(text)
    update_job(job_id, status="done", result=result, log="Scene compiled")

@router.post("/ai/command")
def start_async(req: AIRequest):
    job_id = create_job()
    thread = threading.Thread(target=run_scene_job, args=(job_id, req.text))
    thread.start()
    return {"job_id": job_id}

@router.get("/ai/status/{job_id}")
def status(job_id: str):
    job = get_job(job_id)
    return job or {"status": "not_found"}

@router.get("/ai/result/{job_id}")
def result(job_id: str):
    job = get_job(job_id)
    if job and job["result"]:
        return job["result"]
    return {"status": "not_ready"}

@router.get("/ai/logs/{job_id}")
def logs(job_id: str):
    job = get_job(job_id)
    return job["logs"] if job else []

@router.post("/ai/cancel/{job_id}")
def cancel(job_id: str):
    cancel_job(job_id)
    return {"status": "cancelled"}
