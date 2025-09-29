import os
import shutil
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routes.documents import UPLOAD_DIR  # CORRETO

client = TestClient(app)
DOCUMENTS_DIR = UPLOAD_DIR  # Definido localmente

# 🔹 Limpa o diretório antes e depois de cada teste
@pytest.fixture(autouse=True)
def cleanup_docs():
    if os.path.exists(DOCUMENTS_DIR):
        shutil.rmtree(DOCUMENTS_DIR)
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    yield
    shutil.rmtree(DOCUMENTS_DIR)


def test_create_document():
    file_content = b"%PDF-1.4 fake content"
    response = client.post(
        "/documents/",
        files={"file": ("test.pdf", file_content, "application/pdf")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.pdf"
    assert data["file_type"] == "pdf"
    assert "id" in data


def test_read_document_success():
    create_resp = client.post(
        "/documents/",
        files={"file": ("readme.pdf", b"read content", "application/pdf")}
    )
    doc_id = create_resp.json()["id"]

    response = client.get(f"/documents/{doc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == doc_id
    assert data["filename"] == "readme.pdf"


def test_read_document_not_found():
    response = client.get("/documents/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_update_document_success():
    create_resp = client.post(
        "/documents/",
        files={"file": ("old.pdf", b"old content", "application/pdf")}
    )
    doc_id = create_resp.json()["id"]

    response = client.put(f"/documents/{doc_id}", json={"filename": "new.pdf"})
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "new.pdf"


def test_update_document_not_found():
    response = client.put("/documents/999", json={"filename": "ghost.pdf"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_delete_document_success():
    create_resp = client.post(
        "/documents/",
        files={"file": ("todelete.pdf", b"delete me", "application/pdf")}
    )
    doc_id = create_resp.json()["id"]

    response = client.delete(f"/documents/{doc_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Document deleted"


def test_delete_document_not_found():
    response = client.delete("/documents/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"
