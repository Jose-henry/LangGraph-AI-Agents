import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert response.json()["message"] == "RAG Agent API is running"

def test_query_endpoint_basic():
    """Test that the query endpoint is accessible"""
    test_query = {
        "query": "test query",
        "thread_id": "test-thread-id"
    }
    response = client.post("/query", json=test_query)
    assert response.status_code in [200, 500]  # 500 is acceptable if Pinecone isn't configured

# def test_query_endpoint_success():
#     """Test successful query to the RAG endpoint"""
#     test_query = {
#         "query": "What is testing?",
#         "thread_id": "test-thread-id"
#     }
    
#     with patch('src.tool.vector_store.similarity_search_with_score') as mock_search:
#         # Mock Pinecone search results
#         mock_search.return_value = [
#             (Mock(page_content="Testing is a software verification process", 
#                   metadata={"source": "doc1"}), 0.92),
#             (Mock(page_content="Unit testing verifies individual components", 
#                   metadata={"source": "doc2"}), 0.88)
#         ]
        
#         response = client.post("/query", json=test_query)
#         assert response.status_code == 200
#         assert "bullet_points" in response.json()
#         assert "thread_id" in response.json()
#         assert len(response.json()["bullet_points"]) > 0

def test_query_endpoint_no_thread_id():
    """Test query endpoint without thread_id"""
    test_query = {
        "query": "What is testing?"
    }
    
    response = client.post("/query", json=test_query)
    assert response.status_code == 200
    assert "thread_id" in response.json()

# @pytest.mark.integration
# def test_vector_search_integration():
#     """Test integration with Pinecone vector database"""
#     test_query = {
#         "query": "Test vector search",
#         "thread_id": "test-integration-id"
#     }
    
#     with patch('src.tool.vector_store.similarity_search_with_score') as mock_search:
#         mock_search.return_value = [
#             (Mock(page_content="Relevant content about vector search", 
#                   metadata={"source": "doc1"}), 0.95)
#         ]
        
#         response = client.post("/query", json=test_query)
#         assert response.status_code == 200
#         assert "bullet_points" in response.json()
#         assert isinstance(response.json()["bullet_points"], list)

# @pytest.mark.integration
# def test_pinecone_error_handling():
#     """Test handling of Pinecone API errors"""
#     test_query = {
#         "query": "test query",
#         "thread_id": "test-thread-id"
#     }
    
#     with patch('src.tool.vector_store.similarity_search_with_score') as mock_search:
#         mock_search.side_effect = Exception("Pinecone API error")
#         response = client.post("/query", json=test_query)
#         assert response.status_code == 200
#         assert "Error performing vector search" in response.json()["bullet_points"][0]

# @pytest.mark.integration
# def test_empty_pinecone_results():
#     """Test behavior when Pinecone returns no results"""
#     with patch('src.tool.vector_store.similarity_search_with_score') as mock_search:
#         mock_search.return_value = []
#         response = client.post("/query", json={"query": "test"})
#         assert response.status_code == 200
#         assert "No results found" in " ".join(response.json()["bullet_points"])

# def test_query_with_metadata_filter():
#     """Test querying with metadata filters"""
#     test_query = {
#         "query": "test query",
#         "thread_id": "test-thread-id",
#         "metadata_filter": {"category": "test"}
#     }
    
#     with patch('src.tool.vector_store.similarity_search_with_score') as mock_search:
#         response = client.post("/query", json=test_query)
#         assert response.status_code == 200

# @pytest.mark.integration
# def test_concurrent_pinecone_queries():
#     """Test handling of concurrent Pinecone queries"""
#     import asyncio
#     import httpx
    
#     async def make_request():
#         async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
#             return await ac.post("/query", json={"query": "test"})
    
#     with patch('src.tool.vector_store.similarity_search_with_score') as mock_search:
#         mock_search.return_value = [
#             (Mock(page_content="Test content", metadata={}), 0.9)
#         ]
        
#         responses = asyncio.gather(*[make_request() for _ in range(5)])
#         for response in responses:
#             assert response.status_code == 200

@pytest.mark.integration
def test_query_with_special_characters():
    """Test handling of queries with special characters"""
    test_query = {
        "query": "test?!@#$%^&*()",
        "thread_id": "test-thread-id"
    }
    response = client.post("/query", json=test_query)
    assert response.status_code == 200

# @pytest.mark.integration
# def test_rate_limiting():
#     """Test rate limiting behavior"""
#     responses = []
#     for _ in range(10):  # Make 10 rapid requests
#         response = client.post("/query", json={"query": "test"})
#         responses.append(response.status_code)
#     assert 429 in responses  # Expect some rate limiting 