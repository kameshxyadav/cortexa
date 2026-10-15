import sys
sys.path.append("../..")  # ensure app import works

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "ok"
    assert "version" in json


def test_ingest_pdf_endpoint():
    response = client.post("/ingest/pdf", files={"file": ("test.pdf", b"%PDF-1.4 dummy", "application/pdf")})
    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "queued"
    assert isinstance(json["units"], list)


def test_ingest_pptx_endpoint():
    response = client.post("/ingest/pptx", files={"file": ("test.pptx", b"PK\x03\x04 dummy", "application/vnd.openxmlformats-officedocument.presentationml.presentation")})
    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "queued"
    assert isinstance(json["units"], list)
