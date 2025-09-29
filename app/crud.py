from sqlalchemy.orm import Session
from app import models, schemas

def create_document(db: Session, doc: schemas.DocumentCreate) -> models.Document:
    db_doc = models.Document(
        filename=doc.filename,
        file_type=doc.file_type
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def get_document(db: Session, doc_id: int) -> models.Document | None:
    return db.query(models.Document).filter(models.Document.id == doc_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 10) -> list[models.Document]:
    return db.query(models.Document).offset(skip).limit(limit).all()

def update_document(db: Session, doc_id: int, update_data: schemas.DocumentCreate) -> models.Document | None:
    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not doc:
        return None
    doc.filename = update_data.filename
    doc.file_type = update_data.file_type
    db.commit()
    db.refresh(doc)
    return doc

def delete_document(db: Session, doc_id: int) -> bool:
    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not doc:
        return False
    db.delete(doc)
    db.commit()
    return True
