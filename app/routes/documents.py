from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import aiofiles
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
import os

router = APIRouter(prefix="/documents", tags=["documents"])

DOC_NOT_FOUND = "Document not found"
ALLOWED_EXTENSIONS = {"pdf", "docx"}
UPLOAD_DIR = "app/documents"

# Garante que o diretório exista
os.makedirs(UPLOAD_DIR, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/", response_model=schemas.DocumentResponse)
async def create(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Arquivo deve ser PDF ou DOCX")
    
    file_type = file.filename.rsplit(".", 1)[1].lower()
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Salva arquivo no disco de forma assíncrona
    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao salvar arquivo no disco")

    # Cria registro no banco
    try:
        doc_in = schemas.DocumentCreate(filename=file.filename, file_type=file_type)
        db_doc = crud.create_document(db, doc_in)
        return db_doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {e}")

@router.get("/{doc_id}", response_model=schemas.DocumentResponse)
def read(doc_id: int, db: Session = Depends(get_db)):
    doc = crud.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail=DOC_NOT_FOUND)
    return doc

@router.get("/", response_model=list[schemas.DocumentResponse])
def list_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_documents(db, skip, limit)

@router.put("/{doc_id}", response_model=schemas.DocumentResponse)
def update(doc_id: int, update_data: schemas.DocumentUpdate, db: Session = Depends(get_db)):
    doc = crud.update_document(db, doc_id, update_data)
    if not doc:
        raise HTTPException(status_code=404, detail=DOC_NOT_FOUND)
    return doc

@router.delete("/{doc_id}")
def delete(doc_id: int, db: Session = Depends(get_db)):
    doc = crud.delete_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail=DOC_NOT_FOUND)
    return {"message": "Document deleted"}
