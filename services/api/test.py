import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_redis

client = TestClient(app)

class TestJobs(unittest.TestCase):

    def test_create_job(self):
        mock_redis = MagicMock()
        app.dependency_overrides[get_redis] = lambda: mock_redis

        response = client.post("/jobs")
        job_id = response.json()["job_id"]

        self.assertEqual(response.status_code, 200)
        mock_redis.lpush.assert_called_once_with("job", job_id)
        mock_redis.hset.assert_called_once_with(f"job:{job_id}", "status", "queued")

        app.dependency_overrides.clear()

    def test_get_job_found(self):
        mock_redis = MagicMock()
        mock_redis.hget.return_value = b'queued'
        app.dependency_overrides[get_redis] = lambda: mock_redis

        response = client.get("/jobs/abc-123")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"job_id": "abc-123", "status": "queued"})
        mock_redis.hget.assert_called_once_with("job:abc-123", "status")

        app.dependency_overrides.clear()

    def test_get_job_not_found(self):
        mock_redis = MagicMock()
        mock_redis.hget.return_value = None
        app.dependency_overrides[get_redis] = lambda: mock_redis

        response = client.get("/jobs/abc-123")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"error": "not found"})

        app.dependency_overrides.clear()


if __name__ == "__main__":
    unittest.main()
