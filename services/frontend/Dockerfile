FROM jupyter/scipy-notebook:python-3.11

USER root

# Apenas dependências mínimas (sem GDAL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

USER jovyan

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt 

# Extensões para mapas interativos
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet --no-build && \
    jupyter lab build

RUN mkdir -p /home/jovyan/work /data/inputs /data/outputs /examples
COPY jupyter_config.py /etc/jupyter/

WORKDIR /home/jovyan/work

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8888/api || exit 1

CMD ["start-notebook.sh", "--NotebookApp.token=''"]