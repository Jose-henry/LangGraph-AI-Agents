FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY QnA/src/ ./src/
# Make sure __init__.py is in the src directory
RUN touch ./src/__init__.py

# Set Python path to recognize the package
ENV PYTHONPATH=/app

# Expose the port that the FastAPI app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]