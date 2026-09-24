from api import main
import pytest
from  unittest.mock import patch, Mock


@pytest.fixture
def mocked_redis():
    with patch('api.main.redis.Redis') as mocked_redis:
        yield mocked_redis

@pytest.fixture
def mocked_uuid4(job_id):
    with patch('api.main.uuid.uuid4') as mock_uuid4:
        mock_uuid4.return_value = job_id
        yield mock_uuid4

@pytest.fixture
def job_id():
    return "1234-5678-91011-1213"


def test_get_redis(mocked_redis):
   result = main.get_redis()
   mocked_redis.assert_called_once() 

   expected = mocked_redis.return_value 
   assert result == expected

def test_create_job(mocked_redis, mocked_uuid4, job_id):
    
    result = main.create_job()
    expected = {"job_id": job_id }

    assert result == expected

def test_get_job_found(mocked_redis, job_id):
      
    mocked_redis.return_value.hget.return_value = b"completed"
    status = mocked_redis.return_value.hget.return_value

    result = main.get_job(job_id)
    expected = {"job_id": job_id, "status": status.decode()}
    
    assert result == expected

def test_get_job_not_found(mocked_redis, job_id):
    
    mocked_redis.return_value.hget.return_value = False
    
    result = main.get_job(job_id)
    expected = {"error": "not found"}
  
    assert result == expected

def test_get_health():

    result = main.get_health()
    expected = {"status": "Healthy"}

    assert result == expected