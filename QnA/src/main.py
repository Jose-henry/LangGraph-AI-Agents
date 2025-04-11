from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from src.agent import run_agent
import uuid
from prometheus_fastapi_instrumentator import Instrumentator

# Create FastAPI application
app = FastAPI(
    title="QnA Agent API",
    description="API for querying a QnA agent that refines RAG-based responses",
    version="1.0.0"
)

instrumentator = Instrumentator(
    should_respect_env_var=True,
    env_var_name="ENABLE_METRICS",
)
instrumentator.instrument(app).expose(app)

# Define request model
class QueryRequest(BaseModel):
    query: str
    thread_id: Optional[str] = None

# Define response model
class QueryResponse(BaseModel):
    response: str
    thread_id: str

@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Query the QnA agent and get a refined response
    
    The agent will:
    1. Send the query to the RAG agent API (port 8001)
    2. Receive bullet-point information from the RAG agent
    3. Process and refine the information into a more natural, readable format
    4. Return a comprehensive and well-structured response
    """
    try:
        # Use provided thread_id or generate a new one
        thread_id = request.thread_id if request.thread_id else str(uuid.uuid4())
        
        # Run the agent
        refined_response = run_agent(request.query, thread_id)
        
        # Return the response
        return QueryResponse(
            response=refined_response,
            thread_id=thread_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "online", "message": "QnA Agent API is running"}

# Run the application
if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8000, reload=True)