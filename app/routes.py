from fastapi import APIRouter
from pydantic import BaseModel
import uuid
import redis
import os
import json

router = APIRouter()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

class TaskRequest(BaseModel):
    text: str


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/task")
def create_task(req: TaskRequest):
    job_id = str(uuid.uuid4())

    try:
        # Store job state
        r.hset(job_id, mapping={
            "status": "pending",
            "result": ""
        })

        # Push to queue
        r.lpush("task_queue", json.dumps({
            "job_id": job_id,
            "text": req.text
        }))

        print(f"[INFO] Job created: {job_id}")

        return {"job_id": job_id}

    except Exception as e:
        print(f"[ERROR] Failed to create job: {e}")
        return {"error": "internal error"}


@router.get("/status/{job_id}")
def get_status(job_id: str):
    if not r.exists(job_id):
        return {"error": "job not found"}

    status = r.hget(job_id, "status")
    return {"status": status}


@router.get("/result/{job_id}")
def get_result(job_id: str):
    if not r.exists(job_id):
        return {"error": "job not found"}

    status = r.hget(job_id, "status")

    if status != "done":
        return {"result": None}

    result = r.hget(job_id, "result")
    return {"result": result}