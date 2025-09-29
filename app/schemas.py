from pydantic import BaseModel

# Schema usado na criação do documento
class DocumentCreate(BaseModel):
    filename: str
    file_type: str  # "pdf" ou "docx"

# Schema usado para atualização (mesmo que create)
class DocumentUpdate(BaseModel):
    filename: str | None = None
    file_type: str | None = None

# Schema usado para resposta
class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str

    class Config:
        orm_mode = True
