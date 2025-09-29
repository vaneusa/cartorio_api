from fastapi import FastAPI
from app.database import engine, Base
from app.routes import documents

# Cria as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cartório API")

# Registra as rotas
app.include_router(documents.router)
