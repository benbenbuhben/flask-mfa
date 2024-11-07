# Stage 1: Build dependencies and install Python packages
FROM python:3.10-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1


# Copy requirements and install dependencies in builder stage
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*


# Stage 2: Copy only necessary files and dependencies to the final image
FROM python:3.10-slim

# WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


COPY Pipfile Pipfile.lock ./

# Copy only the installed packages from the builder image
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application files
COPY app .
COPY run.py .

# Expose port and run the application
EXPOSE 5000
CMD ["python", "run.py"]
