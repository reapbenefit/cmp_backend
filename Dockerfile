# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create a script to generate .env file from environment variables
RUN echo '#!/bin/bash\n\
    echo "OPENAI_API_KEY=${OPENAI_API_KEY}" > /app/src/.env\n\
    echo "PHOENIX_API_KEY=${PHOENIX_API_KEY}" >> /app/src/.env\n\
    echo "PHOENIX_ENDPOINT=${PHOENIX_ENDPOINT}" >> /app/src/.env\n\
    echo "ENV=${ENV}" >> /app/src/.env\n\
    echo "DATABASE_URL=${DATABASE_URL}" >> /app/src/.env\n\
    exec "$@"' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8001

# Change to src directory 
WORKDIR /app/src

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["sh", "-c", "python init.py && uvicorn main:app --host 0.0.0.0 --port 8001"]