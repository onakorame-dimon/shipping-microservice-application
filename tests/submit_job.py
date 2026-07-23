#! /bin/python3

import requests 
import time

# TODO: Handle all exceptions that may occur when making the request to the frontend. 

# submit the job through the frontend
res = requests.post('http://localhost:3000/submit', timeout=5)

# Get the job response which is the job id
job_res = res.json()
job_id = job_res['job_id']
print(f"Job submitted with ID: {job_id}")

# check the job status through the frontend
max_retries = 3
interval = 2  # seconds

#poll job status until it is completed or failed, with a maximum number of retries
for retries in range(max_retries):
    res = requests.get(f'http://localhost:3000/status/{job_id}', timeout=5)   
    job_status = res.json()

    if retries == (max_retries - 1):
        print("Max retries reached. Something went wrong with the job processing.")
        break

    if job_status['status'] == 'completed':
        print("Job completed successfully.")
        break

    elif job_status['status'] == 'queued':
        print("Job is still in progress. . .")
        time.sleep(interval)        

    else:
        print("Job failed.")
        break
        
