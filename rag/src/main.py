from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from src.agent import run_agent
import uuid

# Create FastAPI application
app = FastAPI(
    title="RAG Agent API",
    description="API for querying a RAG-enhanced AI assistant",
    version="1.0.0"
)

# Define request model
class QueryRequest(BaseModel):
    query: str
    thread_id: Optional[str] = None

# Define response model
class QueryResponse(BaseModel):
    bullet_points: List[str]
    thread_id: str

@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Query the RAG agent and get a response in bullet points
    
    The agent will:
    1. Search the vector database for relevant information
    2. Process the results into helpful context
    3. Generate a response with 5-10 bullet points
    4. Return "I don't have enough information" if no relevant context is found
    """
    try:
        # Use provided thread_id or generate a new one
        thread_id = request.thread_id if request.thread_id else str(uuid.uuid4())
        
        # Run the agent
        bullets = run_agent(request.query, thread_id)
        
        # Return the response
        return QueryResponse(
            bullet_points=bullets,
            thread_id=thread_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "online", "message": "RAG Agent API is running"}

# Run the application
if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8001, reload=True)