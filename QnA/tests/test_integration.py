import pytest
from fastapi.testclient import TestClient
from src.main import app
import requests
from unittest.mock import patch


client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert response.json()["message"] == "QnA Agent API is running"
def test_rag_connection():
    """Test connection to RAG service"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "bullet_points": ["Test response"],
            "thread_id": "test-thread-id"
        }
        
        test_query = {
            "query": "test query",
            "thread_id": "test-thread-id"
        }
        response = client.post("/query", json=test_query)
        assert response.status_code == 200

def test_query_endpoint_success():
    """Test successful query to the QnA endpoint"""
    test_query = {
        "query": "What is the meaning of life?",
        "thread_id": "test-thread-id"

    }
    
    response = client.post("/query", json=test_query)
    assert response.status_code == 200
    assert "response" in response.json()
    assert "thread_id" in response.json()

def test_query_endpoint_no_thread_id():
    """Test query endpoint without thread_id"""
    test_query = {
        "query": "What is the meaning of life?"
    }
    
    response = client.post("/query", json=test_query)
    assert response.status_code == 200
    assert "thread_id" in response.json()

@pytest.mark.integration
def test_full_pipeline():
    """Test the full QnA pipeline with RAG integration"""
    test_query = {
        "query": "Tell me about testing",
        "thread_id": "test-integration-id"
    }
    
    response = client.post("/query", json=test_query)
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)

def test_query_endpoint_invalid_request():
    """Test handling of invalid request data"""
    test_query = {
        "invalid_field": "test"
    }
    response = client.post("/query", json=test_query)
    assert response.status_code == 422

@pytest.mark.integration
def test_long_query_handling():
    """Test handling of long queries"""
    test_query = {
        "query": "a" * 1000,  # Very long query
        "thread_id": "test-thread-id"
    }
    response = client.post("/query", json=test_query)
    assert response.status_code == 200

# @pytest.mark.integration
# def test_concurrent_requests():
#     """Test handling of concurrent requests"""
#     import asyncio
#     import httpx
    
#     async def make_request():
#         async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
#             return await ac.post("/query", json={"query": "test"})
    
#     responses = asyncio.gather(*[make_request() for _ in range(5)])
#     for response in responses:
#         assert response.status_code == 200 

# @pytest.mark.integration
# def test_concurrent_requests():
#     """Test handling of concurrent requests"""
#     import asyncio
#     import httpx

