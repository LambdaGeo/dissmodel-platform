# ═══════════════════════════════════════════════════════════════
# DISSMODEL PLATFORM - Frontend (JupyterLab)
# ═══════════════════════════════════════════════════════════════

FROM jupyter/scipy-notebook:python-3.11

LABEL maintainer="LambdaGeo / INPE"
LABEL description="DisSModel Platform - JupyterLab Frontend"

# Switch to root for system installations
USER root

# Install system dependencies for geospatial libraries
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libspatialindex-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Switch back to jovyan for Python installations
USER jovyan

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Install Jupyter extensions for maps
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet --no-build && \
    jupyter lab build

# Create directories
RUN mkdir -p /home/jovyan/work /data/inputs /data/outputs /examples

# Copy configuration
COPY jupyter_config.py /etc/jupyter/

# Set working directory
WORKDIR /home/jovyan/work

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8888/api || exit 1

# Default command
CMD ["start-notebook.sh", "--NotebookApp.token=''"]