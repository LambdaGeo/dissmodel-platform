# ═══════════════════════════════════════════════════════════════
# DISSMODEL PLATFORM - Worker (DisSModel Execution)
# ═══════════════════════════════════════════════════════════════

FROM python:3.11-slim

LABEL maintainer="LambdaGeo / INPE"
LABEL description="DisSModel Platform - Worker"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Create app directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Run worker
CMD ["python", "worker.py"]