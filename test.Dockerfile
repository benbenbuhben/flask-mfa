# Base Image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

# Install necessary dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends build-essential && \
  pip install --upgrade pip && \
  apt-get autoremove -y && \
  rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy application and test files
COPY app ./app
COPY run.py ./run.py
COPY test_routes.py ./test_routes.py

# Expose port
EXPOSE 5000

# Default command for tests
CMD ["pytest", "-x", "test_routes.py"]
