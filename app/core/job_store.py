import uuid
from datetime import datetime

JOBS = {}

def create_job():
    job_id = uuid.uuid4().hex
    JOBS[job_id] = {
        "status": "running",
        "logs": ["Job created"],
        "result": None,
        "created_at": datetime.utcnow().isoformat()
    }
    return job_id

def update_job(job_id, status=None, log=None, result=None):
    job = JOBS.get(job_id)
    if not job:
        return
    if status:
        job["status"] = status
    if log:
        job["logs"].append(log)
    if result:
        job["result"] = result

def get_job(job_id):
    return JOBS.get(job_id)

def cancel_job(job_id):
    job = JOBS.get(job_id)
    if job:
        job["status"] = "cancelled"
