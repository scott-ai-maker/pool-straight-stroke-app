# Optimized Dockerfile for Hugging Face Spaces and Production
# Multi-stage build for minimal image size and enhanced security

# ============================================================================
# BUILDER STAGE - Install dependencies
# ============================================================================
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies required for OpenCV
# These packages are needed to build and run OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install Python dependencies
# Copying requirements first enables Docker layer caching
# If requirements.txt doesn't change, this layer is reused
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================================
# FINAL STAGE - Production image
# ============================================================================
FROM python:3.10-slim

LABEL maintainer="Scott Gordon <scott.aiengineer@outlook.com>"
LABEL description="Pool Stroke Trainer - AI-powered pool stroke analysis"
LABEL version="1.0.0"

# Install only runtime dependencies (smaller image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY app.py .
COPY stroke_analyzer.py .
COPY templates/ templates/
COPY static/ static/

# Create non-root user for security (following best practices)
# Running as non-root prevents privilege escalation attacks
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app

# Switch to non-root user
USER appuser

# Expose application port (Hugging Face Spaces uses 7860)
EXPOSE 7860

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=7860 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Health check for container orchestration
# Allows Kubernetes/Docker to verify application is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/health').read()"

# Run application
CMD ["python", "-u", "app.py"]
