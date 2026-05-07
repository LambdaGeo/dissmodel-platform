FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgdal-dev gcc git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/DisSModel/dissmodel-ca.git /tmp/repo \
    && pip install --no-cache-dir dissmodel /tmp/repo streamlit matplotlib \
    && cp /tmp/repo/src/dissmodel_ca/streamlit/ca_all.py /app/app.py \
    && rm -rf /tmp/repo

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.address", "0.0.0.0", \
     "--server.port", "8501", \
     "--server.headless", "true", \
     "--server.baseUrlPath", "/dissmodel/ca", \
     "--browser.gatherUsageStats", "false"]