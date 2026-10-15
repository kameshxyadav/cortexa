# backend/app/main.py

from fastapi import FastAPI
from .config import settings
from .routers import health

app = FastAPI(title="StudyMate Backend", version="0.1.0")

# Include routers
app.include_router(health.router)

@app.get("/health")
async def health_check():
    """Simple health endpoint (also available at /health via router)."""
    return {"status": "ok", "version": "0.1.0"}
