# C:\Users\cherub\OneDrive\Desktop\test\langchain\rag\agent.py

from typing import Annotated, List, Dict, Any, Optional
import uuid
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from src.tool import vector_search
from langchain_core.tools import tool

# Define our RAG search tool
@tool
def rag_search(query: str, k: int = 10) -> str:
    """
    Search the vector database for relevant information about the query.
    
    Args:
        query: The search query
        k: Number of results to return (default: 5)
        
    Returns:
        String containing the search results
    """
    results = vector_search(query, k=k)
    return results

# Define the state type for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]
    context: Optional[str]

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# Create tools list
tools = [rag_search]
llm_with_tools = llm.bind_tools(tools)

# Create state graph
graph_builder = StateGraph(State)

# Define the agent nodes
def chatbot(state: State):
    """Process user query and generate response using context if available"""
    messages = state["messages"]
    context = state.get("context")
    
    # Prepare system message with instructions
    system_message = {
        "role": "system", 
        "content": """You are a helpful assistant that provides information based on the available context.
        If context is provided, use it to formulate your response into 5-10 concise bullet points.
        If no relevant context is found, respond with 'I don't have enough information to answer that question.'
        Always be clear, concise, and helpful."""
    }
    
    # Add context if available
    if context:
        system_message["content"] += f"\n\nHere is the context to use for your response:\n{context}"
    
    # Create message list with system message
    all_messages = [system_message] + messages
    
    # Invoke the LLM
    response = llm_with_tools.invoke(all_messages)
    
    return {"messages": [response]}

def process_rag_results(state: State):
    """Process the results from the RAG tool and add it to the state"""
    messages = state["messages"]
    
    # Get the most recent user query
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage) or (hasattr(msg, "role") and msg.role == "user"):
            user_query = msg.content
            break
    else:
        return {"context": "No user query found"}
    
    # Search the vector database
    try:
        results = rag_search.invoke(user_query)
        
        # Debug print to see what's being returned
        print(f"RAG results: {results}")
        
        # If no results found
        if not results or "No results found" in results:
            print("No results found in RAG search")
            return {"context": None}
        
        # Add the entire results as context instead of parsing
        # The LLM is capable of processing this information
        return {"context": results}
        
    except Exception as e:
        print(f"Error in RAG search: {str(e)}")
        return {"context": None}

# Add nodes to the graph
graph_builder.add_node("rag_search", process_rag_results)
graph_builder.add_node("chatbot", chatbot)

# Define the edges
graph_builder.add_edge(START, "rag_search")
graph_builder.add_edge("rag_search", "chatbot")
graph_builder.add_edge("chatbot", END)

# Initialize memory saver for persistence
memory = MemorySaver()

# Compile the graph
# graph = graph_builder.compile(checkpointer=memory)
graph = graph_builder.compile()
# Function to invoke the agent with a query
def run_agent(query: str, thread_id: str = None) -> List[str]:
    """
    Run the agent with the given query and return the response as a list of bullet points.
    
    Args:
        query: The user's query
        thread_id: Thread ID for conversation persistence
        
    Returns:
        List of bullet points from the response
    """
    # Generate a random UUID if thread_id is not provided
    if thread_id is None:
        thread_id = str(uuid.uuid4())
    
    config = {"configurable": {"thread_id": thread_id}}
    
    # Create input state with user message
    input_state = {
        "messages": [{"role": "user", "content": query}],
        "context": None
    }
    
    # Run the graph
    result = graph.invoke(input_state, config)
    
    # Extract the assistant's response
    assistant_response = result["messages"][-1].content
    
    # Print the full response for debugging
    print(f"Full assistant response: {assistant_response}")
    
    # Convert response to bullet points if it's not already
    if "•" not in assistant_response and "\n- " not in assistant_response:
        # If the response is "I don't have enough information", return as is
        if "I don't have enough information" in assistant_response:
            return ["I don't have enough information to answer that question."]
        
        # Otherwise, format into bullet points
        sentences = [s.strip() for s in assistant_response.split(".") if s.strip()]
        bullets = [f"{s}." for s in sentences[:10] if len(s) > 5]
        
        # Limit to 5-10 bullet points
        if len(bullets) > 10:
            bullets = bullets[:10]
        elif len(bullets) < 5 and len(bullets) > 0:
            # If fewer than 5 bullets, make them more detailed if possible
            bullets = bullets[:5]
            
        return bullets
    else:
        # Already in bullet point format
        bullets = []
        for line in assistant_response.split("\n"):
            line = line.strip()
            if line.startswith("•") or line.startswith("-"):
                bullets.append(line)
        
        # Limit to 5-10 bullet points
        if len(bullets) > 10:
            return bullets[:10]
        elif len(bullets) < 5 and len(bullets) > 0:
            return bullets[:5]
        
        # If no bullets were found, just return the full response split into lines
        if not bullets:
            return [line.strip() for line in assistant_response.split("\n") if line.strip()][:10]
        
        return bullets