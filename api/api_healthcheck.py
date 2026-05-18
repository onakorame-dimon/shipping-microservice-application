import redis
import os

#Connect to the redis instance
PORT = int(os.getenv('PORT'))
HOST = os.getenv('HOST')
PASSWORD = os.getenv('REDIS_PASSWORD')

r = redis.Redis(host=HOST, port=PORT, password=PASSWORD)
# Get a value by its key
value = r.get("job")

if value:
    print(f"Value: {value}")
else:
    print("Key does not exist.")