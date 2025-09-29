import pytest
from fastapi.testclient import TestClient
from app.main import app, DOCUMENTS_DIR
import os
import shutil

client = TestClient(app)

# Antes de cada teste, limpa o diretório de documentos
@pytest.fixture(autouse=True)
def cleanup_docs():
    if os.path.exists(DOCUMENTS_DIR):
        shutil.rmtree(DOCUMENTS_DIR)
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    yield
    shutil.rmtree(DOCUMENTS_DIR)

def test_create_document():
    response = client.post("/documents/", json={"title": "Test Doc", "content": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Doc"
    assert data["content"] == "Hello"
    assert "id" in data

def test_read_document_success():
    # Primeiro cria
    create_resp = client.post("/documents/", json={"title": "Read Doc", "content": "Read Content"})
    doc_id = create_resp.json()["id"]

    # Agora lê
    response = client.get(f"/documents/{doc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == doc_id
    assert data["title"] == "Read Doc"

def test_read_document_not_found():
    response = client.get("/documents/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"

def test_update_document_success():
    create_resp = client.post("/documents/", json={"title": "Old Title", "content": "Old Content"})
    doc_id = create_resp.json()["id"]

    response = client.put(f"/documents/{doc_id}", json={"title": "New Title", "content": "New Content"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["content"] == "New Content"

def test_update_document_not_found():
    response = client.put("/documents/999", json={"title": "Doesn't exist", "content": "No content"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"

def test_delete_document_success():
    create_resp = client.post("/documents/", json={"title": "To Delete", "content": "Delete Me"})
    doc_id = create_resp.json()["id"]

    response = client.delete(f"/documents/{doc_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Document deleted"

def test_delete_document_not_found():
    response = client.delete("/documents/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"
