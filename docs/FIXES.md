# FIXES

Documents the issues identified in the original frontend, API, and worker code, the fixes applied, and why they were necessary, as required by the [project requirements](REQUIREMENTS.md).

## The frontend code

### Line 6 `services/frontend/app.js` — Read the API URL from an environment variable

The original URL was hardcoded to `localhost:8000`. Inside the frontend container, `localhost` refers to the frontend container itself, not the API container.

Original code:
```javascript
6  | const API_URL = "http://localhost:8000";
```

Replaced with:
```javascript
6  | const API_URL = process.env.API_URL;
```

Set `API_URL=http://backend:8000`. Docker Compose provides DNS discovery between services on the same network, so `backend` resolves to the API service. Use the Compose **service name**, not `localhost` or the host machine's address.

### Lines 15–18 and 24–27 `services/frontend/app.js` — Log request errors

The frontend returned a generic error to the caller but did not log the underlying Axios error, making failed API requests harder to diagnose. Added `console.error(err)` in both `catch` blocks. The client still receives the generic message, while the server logs the actual error.

Original code (POST handler):
```javascript
15 |     res.status(500).json({ error: "something went wrong" });
16 |   }
17 | });
```

Replaced with (POST handler):
```javascript
15 |     res.status(500).json({ error: "something went wrong" });
16 |     console.error(err);
17 |   }
18 | });
```

Original code (status handler):
```javascript
23 |     res.status(500).json({ error: "something went wrong" });
24 |   }
25 | });
```

Replaced with (status handler):
```javascript
24 |     res.status(500).json({ error: "something went wrong" });
25 |     console.error(err);
26 |   }
27 | });
```

## The API code

### Lines 7–17 `services/api/main.py` — Configure the Redis connection through environment variables

The original connection used `localhost:6379` and did not provide a password. That points to the API container itself, and it cannot authenticate to the Compose Redis service when Redis is started with `--requirepass`.

Original code:
```python
8  | r = redis.Redis(host="localhost", port=6379)
```

Replaced with:
```python
7  | PORT = int(os.getenv('REDIS_PORT', '6379'))
9  | HOST = os.getenv('REDIS_HOST')
11 | PASSWORD = os.getenv('REDIS_PASSWORD')
16 | def get_redis():
17 |     return redis.Redis(host=HOST, port=PORT, password=PASSWORD)
```

Set `REDIS_HOST=redis` and provide `REDIS_PASSWORD` and `REDIS_PORT`. The `redis` hostname resolves to the Redis service through Compose DNS, and the password allows the client to authenticate.

### Lines 37–39 `services/api/main.py` — Add an API health endpoint

The original API had no `/health` endpoint, but `services/api/healthcheck.sh` checks that route. Added:

```python
37 | @app.get("/health")
38 | def get_health():
39 |     return {"status": "Healthy"}
```

The health-check script can now receive HTTP 200 when the API is responding.

## The worker code

### Lines 6–10 `services/worker/worker.py` — Configure the Redis connection through environment variables

The original worker also connected to `localhost:6379` without a password. From inside the worker container, `localhost` is the worker itself, and the Redis service requires authentication.

Original code:
```python
6  | r = redis.Redis(host="localhost", port=6379)
```

Replaced with:
```python
6  | PORT = int(os.getenv('REDIS_PORT', '6379'))
7  | HOST = os.getenv('REDIS_HOST')
8  | PASSWORD = os.getenv('REDIS_PASSWORD')
10 | r = redis.Redis(host=HOST, port=PORT, password=PASSWORD)
```

Set `REDIS_HOST=redis` and pass the Redis port and password through the environment. This lets the worker locate and authenticate with the Redis service over the Compose network.


