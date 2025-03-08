import os
import requests
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from langchain_core.tools import tool


# Load environment variables
load_dotenv()




# Get API keys from environment
RAG_AGENT_URL = os.getenv("RAG_AGENT_URL") + "/query"


@tool
def query_rag_agent(query: str, thread_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Sends a query to the RAG agent API running on port 8001 and returns the response.
    
    Args:
        query: The user's query to send to the RAG agent
        thread_id: Optional thread ID for maintaining conversation context
        
    Returns:
        Dictionary containing the RAG agent's response with bullet points and thread_id
    """
    try:
        # Prepare request payload
        payload = {
            "query": query
        }
        
        # Add thread_id if provided
        if thread_id:
            payload["thread_id"] = thread_id
            
        # Send POST request to RAG agent API
        response = requests.post(
            RAG_AGENT_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            error_message = f"Error from RAG agent: {response.status_code} - {response.text}"
            print(error_message)
            return {
                "bullet_points": ["Failed to get information from the knowledge base."],
                "thread_id": thread_id or "error"
            }
            
    except Exception as e:
        error_message = f"Exception while querying RAG agent: {str(e)}"
        print(error_message)
        return {
            "bullet_points": ["I encountered a technical issue while retrieving information."],
            "thread_id": thread_id or "error"
        }