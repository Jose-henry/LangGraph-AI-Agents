# C:\Users\cherub\OneDrive\Desktop\test\langchain\rag\src\tool.py
# Postgres (PGVector)

# import os
# from typing import Optional, Dict, Any
# from pydantic import BaseModel, Field
# from sqlalchemy import create_engine, text
# from langchain_postgres.vectorstores import PGVector
# from langchain_openai import OpenAIEmbeddings
# from dotenv import load_dotenv

# load_dotenv()

# # Retrieve the connection string from environment variables
# connection_string = os.getenv(
#     "POSTGRES_URI"
# )

# """ # Create engine
# engine = create_engine(connection_string)

# # Set the YugabyteDB flag before initializing PGVector
# with engine.connect() as connection:
#     connection.execute(text("SET yb_silence_advisory_locks_not_supported_error = on;"))
#     connection.commit()
#  """
# # Initialize the OpenAI embeddings model
# embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# # Initialize the PGVector store
# pgvector_store = PGVector(
#     embeddings=embedding_model,
#     collection_name="documents",
#     connection=connection_string,
#     use_jsonb=True,
# )

# def vector_search(query: str, filter_dict: Optional[Dict[str, Any]] = None, k: int = 10) -> str:
#     print(f"Running vector search for: {query}")
#     print(f"Filter: {filter_dict}")
#     print(f"Retrieving {k} results...")

#     # Generate the embedding for the query
#     query_embedding = embedding_model.embed_query(query)
#     print(f"Query Embedding: {query_embedding}")  # Debugging output

#     # Manually check results
#     try:
#         raw_results = pgvector_store.similarity_search_with_score(query, k=k, filter=filter_dict)
#         print(f"Raw Results: {raw_results}")  # Debugging output

#         if not raw_results:
#             print("No matching results found!")
#             return "No results found."

#         return "\n".join([
#             f"Content: {doc.page_content}\nScore: {score}\nMetadata: {doc.metadata}\n"
#             for doc, score in raw_results
#         ])
#     except Exception as e:
#         return f"Error performing vector search: {str(e)}"




# Pinecone

import os
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

# Retrieve the Pinecone API key from environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "document-embeddings"  # Change this as needed

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set in environment variables.")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if the index exists, create if not
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1536,  # Adjust this according to your embedding model
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(PINECONE_INDEX_NAME)

# Initialize the OpenAI embeddings model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Initialize the Pinecone vector store
vector_store = PineconeVectorStore(index=index, embedding=embedding_model)

def vector_search(query: str, filter_dict: Optional[Dict[str, Any]] = None, k: int = 5) -> str:
    print(f"Running vector search for: {query}")
    print(f"Filter: {filter_dict}")
    print(f"Retrieving {k} results...")

    try:
        results = vector_store.similarity_search_with_score(query, k=k, filter=filter_dict)
        print(f"Raw Results: {results}")  # Debugging output

        if not results:
            print("No matching results found!")
            return "No results found."

        return "\n".join([
            f"Content: {doc.page_content}\nScore: {score}\nMetadata: {doc.metadata}\n"
            for doc, score in results
        ])
    except Exception as e:
        return f"Error performing vector search: {str(e)}"
 


 # Yugabyte
"""  
import os
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, text
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Retrieve the connection string from environment variables
connection_string = os.getenv("YUGABYTE_DB_URL")

# Create engine
engine = create_engine(connection_string)

# Set the YugabyteDB flag before initializing PGVector
with engine.connect() as connection:
    connection.execute(text("SET yb_silence_advisory_locks_not_supported_error = on;"))
    connection.commit()

# Initialize the OpenAI embeddings model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Initialize the PGVector store
pgvector_store = PGVector(
    embeddings=embedding_model,
    collection_name="documents",  # This should match the value in the 'name' column of langchain_pg_collection
    connection=engine,
    use_jsonb=True,
)

def vector_search(query: str, filter_dict: Optional[Dict[str, Any]] = None, k: int = 10) -> str:
    print(f"Running vector search for: {query}")
    print(f"Filter: {filter_dict}")
    print(f"Retrieving {k} results...")

    try:
        # Perform the similarity search
        raw_results = pgvector_store.similarity_search_with_score(query, k=k, filter=filter_dict)
        
        if not raw_results:
            print("No matching results found!")
            return "No results found."

        # Format and return the results
        formatted_results = []
        for i, (doc, score) in enumerate(raw_results, 1):
            formatted_results.append(f"Result {i}:")
            formatted_results.append(f"Content: {doc.page_content}")
            formatted_results.append(f"Score: {score}")
            formatted_results.append(f"Metadata: {doc.metadata}")
            formatted_results.append("")  # Empty line for readability
        
        return "\n".join(formatted_results)
    except Exception as e:
        print(f"Error in vector search: {str(e)}")
        return f"Error performing vector search: {str(e)}" """