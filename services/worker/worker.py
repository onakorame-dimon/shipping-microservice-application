import redis
import time
import os


PORT = int(os.getenv('REDIS_PORT', '6379'))
HOST = os.getenv('REDIS_HOST')
PASSWORD = os.getenv('REDIS_PASSWORD')

r = redis.Redis(host=HOST, port=PORT, password=PASSWORD)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


while True:
    job = r.brpop("job", timeout=1)
    if job:
        _, job_id = job
        process_job(job_id.decode())
