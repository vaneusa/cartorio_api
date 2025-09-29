import os
import shutil
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routes.documents import UPLOAD_DIR

client = TestClient(app)
DOCUMENTS_DIR = UPLOAD_DIR

@pytest.fixture(autouse=True)
def cleanup_docs():
    if os.path.exists(DOCUMENTS_DIR):
        # Remove apenas os arquivos dentro do diretório
        for filename in os.listdir(DOCUMENTS_DIR):
            file_path = os.path.join(DOCUMENTS_DIR, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    yield
    # Faz a mesma limpeza após o teste
    for filename in os.listdir(DOCUMENTS_DIR):
        file_path = os.path.join(DOCUMENTS_DIR, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


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
    # Cria documento inicial
    create_resp = client.post(
        "/documents/",
        files={"file": ("old.pdf", b"old content", "application/pdf")}
    )
    doc_id = create_resp.json()["id"]
    old_file_type = create_resp.json()["file_type"]  # pega o file_type atual

    # Atualiza apenas o nome do arquivo, mantendo file_type
    response = client.put(f"/documents/{doc_id}", json={
        "filename": "new.pdf",
        "file_type": old_file_type  # garante que não vai ser NULL
    })

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "new.pdf"
    assert data["file_type"] == old_file_type

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
