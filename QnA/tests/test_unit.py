# import pytest
# from unittest.mock import Mock, patch
# from src.agent import run_agent, process_query, generate_response
# from src.tool import query_rag_agent
# import requests

# def test_query_rag_agent_success():
#     """Test successful RAG agent query"""
#     with patch('requests.post') as mock_post:
#         # Mock successful response
#         mock_post.return_value.status_code = 200
#         mock_post.return_value.json.return_value = {
#             "bullet_points": ["Test point 1", "Test point 2"],
#             "thread_id": "test-thread-id"
#         }
        
#         result = query_rag_agent("test query", "test-thread-id")
        
#         assert "bullet_points" in result
#         assert "thread_id" in result
#         assert len(result["bullet_points"]) == 2

# def test_query_rag_agent_failure():
#     """Test RAG agent query failure handling"""
#     with patch('requests.post') as mock_post:
#         mock_post.return_value.status_code = 500
#         mock_post.return_value.text = "Internal Server Error"
        
#         result = query_rag_agent("test query")
        
#         assert "bullet_points" in result
#         assert len(result["bullet_points"]) == 1
#         assert "Failed to get information" in result["bullet_points"][0]

# def test_process_query():
#     """Test process_query function"""
#     state = {
#         "messages": [{"role": "user", "content": "test query"}],
#         "thread_id": "test-thread-id"
#     }
    
#     with patch('src.tool.query_rag_agent') as mock_rag:
#         mock_rag.invoke.return_value = {
#             "bullet_points": ["Test response"],
#             "thread_id": "test-thread-id"
#         }
        
#         result = process_query(state)
        
#         assert "rag_results" in result
#         assert result["rag_results"]["bullet_points"] == ["Test response"]

# def test_generate_response():
#     """Test generate_response function"""
#     state = {
#         "messages": [{"role": "user", "content": "test query"}],
#         "rag_results": {
#             "bullet_points": ["Test point 1", "Test point 2"],
#             "thread_id": "test-thread-id"
#         },
#         "thread_id": "test-thread-id"
#     }
    
#     with patch('langchain_openai.ChatOpenAI') as mock_llm:
#         mock_llm.return_value.invoke.return_value = {"content": "Refined response"}
        
#         result = generate_response(state)
        
#         assert "messages" in result
#         assert len(result["messages"]) == 1

# def test_query_rag_agent_network_error():
#     """Test handling of network connectivity issues"""
#     with patch('requests.post') as mock_post:
#         mock_post.side_effect = requests.exceptions.ConnectionError()
#         result = query_rag_agent("test query")
#         assert "technical issue" in result["bullet_points"][0]

# def test_process_query_empty_messages():
#     """Test process_query with empty messages list"""
#     state = {
#         "messages": [],
#         "thread_id": "test-thread-id"
#     }
#     result = process_query(state)
#     assert "No valid user query found" in result["rag_results"]["bullet_points"][0]

# def test_generate_response_empty_bullets():
#     """Test response generation with empty bullet points"""
#     state = {
#         "messages": [{"role": "user", "content": "test query"}],
#         "rag_results": {
#             "bullet_points": [],
#             "thread_id": "test-thread-id"
#         },
#         "thread_id": "test-thread-id"
#     }
#     with patch('langchain_openai.ChatOpenAI') as mock_llm:
#         result = generate_response(state)
#         assert "messages" in result

# def test_run_agent_invalid_input():
#     """Test run_agent with invalid input"""
#     with pytest.raises(ValueError):
#         run_agent("", None) 