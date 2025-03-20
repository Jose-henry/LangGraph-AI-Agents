FROM python:3.10-slim

# Install required system dependencies including libpq-dev and build tools
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY rag/src/ ./src/
# Ensure __init__.py is present in the src directory
RUN touch ./src/__init__.py

# Set Python path to recognize the package
ENV PYTHONPATH=/app

# Expose the port that the FastAPI app runs on
EXPOSE 8001

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
