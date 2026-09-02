import redis
import os
import sys


PORT = int(os.getenv('REDIS_PORT', '6379'))
HOST = os.getenv('REDIS_HOST')
PASSWORD = os.getenv('REDIS_PASSWORD')

try:
    r = redis.Redis(host=HOST, port=PORT, password=PASSWORD)
    ping_res = r.ping()
except Exception as err:
    print("An Error occurred: " + str(err))
    sys.exit(1)
else:
    print(f"Connection to Redis successfull: {ping_res}")
