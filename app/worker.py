import redis
import json
import time
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def process(text):
    time.sleep(5)  # simulate work
    return text.upper()

print("Worker started...")

while True:
    try:
        print("Waiting for job...", flush=True)

        job = r.brpop("task_queue", timeout=5)

        if job:
            print(f"Job received: {job}", flush=True)

            _, data = job
            job_data = json.loads(data)

            job_id = job_data["job_id"]
            text = job_data["text"]

            print(f"Processing job {job_id}", flush=True)

            r.hset(job_id, "status", "processing")

            result = process(text)

            r.hset(job_id, mapping={
                "status": "done",
                "result": result
            })

            print(f"Job completed {job_id}", flush=True)

    except Exception as e:
        print(f"[ERROR] {e}", flush=True)