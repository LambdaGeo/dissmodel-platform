# ═══════════════════════════════════════════════════════════════
# DISSMODEL PLATFORM - API Gateway (FastAPI)
# ═══════════════════════════════════════════════════════════════

import os
import json
import uuid
import logging
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import redis
from minio import Minio

# ───────────────────────────────────────────────────────────────
# Configuration
# ───────────────────────────────────────────────────────────────

logging.basicConfig(level=os.getenv('DISSMODEL_LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DisSModel Platform API",
    description="API para submissão e gerenciamento de jobs do DisSModel",
    version="1.0.0"
)

# Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

# MinIO connection
minio_client = Minio(
    os.getenv('MINIO_ENDPOINT', 'minio:9000'),
    access_key=os.getenv('MINIO_ACCESS_KEY', 'inpe_admin'),
    secret_key=os.getenv('MINIO_SECRET_KEY', 'inpe_secret_2024'),
    secure=False
)

# ───────────────────────────────────────────────────────────────
# Models
# ───────────────────────────────────────────────────────────────

class JobSubmit(BaseModel):
    model_name: str = Field(..., description="Nome do modelo DisSModel")
    input_dataset: str = Field(..., description="Arquivo de entrada")
    parameters: dict = Field(default_factory=dict, description="Parâmetros do modelo")
    priority: str = Field(default="normal", description="prioridade: low, normal, high")

class JobStatus(BaseModel):
    job_id: str
    status: str
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    result_path: Optional[str] = None
    error: Optional[str] = None

# ───────────────────────────────────────────────────────────────
# Endpoints
# ───────────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        redis_client.ping()
        minio_client.bucket_exists("dissmodel-outputs")
        return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "DisSModel Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/submit_job", response_model=dict)
async def submit_job(job: JobSubmit):
    """
    Submete um novo job para processamento
    """
    job_id = str(uuid.uuid4())
    
    job_data = {
        "job_id": job_id,
        "model_name": job.model_name,
        "input_dataset": job.input_dataset,
        "parameters": job.parameters,
        "priority": job.priority,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Store job metadata in Redis
    redis_client.set(f"job:{job_id}", json.dumps(job_data))
    
    # Add to queue (priority-based)
    queue_key = f"queue:{job.priority}"
    redis_client.lpush(queue_key, job_id)
    
    logger.info(f"Job {job_id} submitted: {job.model_name}")
    
    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Job submitted successfully"
    }

@app.get("/job/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """
    Retorna o status de um job
    """
    job_data = redis_client.get(f"job:{job_id}")
    
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return json.loads(job_data)

@app.delete("/job/{job_id}")
async def cancel_job(job_id: str):
    """
    Cancela um job em fila
    """
    job_data = redis_client.get(f"job:{job_id}")
    
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = json.loads(job_data)
    
    if job["status"] in ["completed", "failed"]:
        raise HTTPException(status_code=400, detail="Cannot cancel completed/failed job")
    
    # Update status
    job["status"] = "cancelled"
    redis_client.set(f"job:{job_id}", json.dumps(job))
    
    logger.info(f"Job {job_id} cancelled")
    
    return {"message": "Job cancelled successfully"}

@app.get("/jobs")
async def list_jobs(limit: int = 100, status: Optional[str] = None):
    """
    Lista jobs (opcionalmente filtrado por status)
    """
    # Em produção, use um banco de dados real
    jobs = []
    for key in redis_client.scan_iter("job:*"):
        job_data = redis_client.get(key)
        if job_data:
            job = json.loads(job_data)
            if status is None or job.get("status") == status:
                jobs.append(job)
    
    return {"jobs": jobs[:limit], "total": len(jobs)}

# ───────────────────────────────────────────────────────────────
# Error Handlers
# ───────────────────────────────────────────────────────────────

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# ───────────────────────────────────────────────────────────────
# Main
# ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)