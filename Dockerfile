# Dockerfile
# Builds the Luminary container for deployment
# SECURITY: No secrets in Dockerfile — injected at runtime via env vars.

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create memory data directory
RUN mkdir -p memory/data

# Render uses port 8000
EXPOSE 8000

# Run FastAPI via uvicorn
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000"]
