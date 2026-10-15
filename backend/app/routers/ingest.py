# backend/app/routers/ingest.py

from fastapi import APIRouter, UploadFile, File
from typing import List

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("/pdf")
async def ingest_pdf_endpoint(file: UploadFile = File(...)):
    """Placeholder PDF ingestion endpoint. Returns empty list of unit IDs."""
    # In real implementation, file would be saved and processed.
    return {"status": "queued", "units": []}

@router.post("/pptx")
async def ingest_pptx_endpoint(file: UploadFile = File(...)):
    """Placeholder PPTX ingestion endpoint. Returns empty list of unit IDs."""
    return {"status": "queued", "units": []}
