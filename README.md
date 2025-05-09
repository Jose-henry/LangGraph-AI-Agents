
---

## Development Setup
Before running the services, set up your development environment:

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   .\venv\Scripts\activate  # Windows

   # OR
    use conda
   ```

2. **Install dependencies:**
   # For integration and unit testing with testing
   pip install -r requirements-dev.txt in .gitlab-ci.yml file
   
   ```bash
   # For production/development only
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file with required configurations:
   ```env
   OPENAI_API_KEY=your_key_here
   PINECONE_API_KEY=your_key_here
   RAG_AGENT_URL=http://localhost:8001
   ```

---

## Running Tests
The project uses pytest for testing. Run tests using:

```bash
# Run all tests
pytest

# Run specific service tests
cd rag && pytest
cd QnA && pytest

# Run with coverage
pytest --cov=src
```

---

## Deployment Methods

### Method 1: Local Development
Run services using uvicorn:

1. **Start RAG service:**
   ```bash
   cd rag
   uvicorn src.main:app --host 0.0.0.0 --port 8001
   ```

2. **Start QnA service:**
   ```bash
   cd QnA
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

### Method 2: Docker Deployment
Build and run using Docker:

1. **Build and run RAG service:**
   ```bash
   docker build -t rag:2.0 -f rag/Dockerfile .
   docker run -p 8001:8001 rag:2.0
   ```

2. **Build and run QnA service:**
   ```bash
   docker build -t qna:2.0 -f QnA/Dockerfile .
   docker run -p 8000:8000 qna:2.0
   ```

### Method 3: Kubernetes Deployment
Deploy to Kubernetes cluster:

1. **Apply ConfigMap and Secrets:**
   ```bash
   kubectl apply -f agents-configmap.yaml
   kubectl apply -f agents-secret.yaml
   ```

2. **Deploy services:**
   ```bash
   kubectl apply -f rag-deployment.yaml
   kubectl apply -f qna-deployment.yaml
   ```

3. **Configure ingress:**
   ```bash
   kubectl apply -f agents-ingress.yaml
   ```

---

## API Endpoints

### QnA Service (Port 8000)
- **Health Check:** `GET /`
- **Query Endpoint:** `POST /query`
  ```json
  {
    "query": "Your question here",
    "thread_id": "optional-thread-id"
  }
  ```

### RAG Service (Port 8001)
- **Health Check:** `GET /`
- **Query Endpoint:** `POST /query`
  ```json
  {
    "query": "Search query",
    "thread_id": "optional-thread-id"
  }
  ```

---

## CI/CD Pipeline
The project includes GitLab CI configuration with Argo CD(USED):
- Automated testing
- Test coverage reporting
- JUnit test results
- Docker image building

---

## Vector Store Configuration
The RAG service uses Pinecone as the vector store:
- Index Name: "document-embeddings"
- Embedding Model: OpenAI text-embedding-3-small
- Vector Dimension: 1536
- Similarity Metric: cosine

---

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request


## Link to Resource configuration
[Yaml Configs](https://github.com/Jose-henry/QnA-Config)

---
