from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cria engine sem retry manual, ativa o  wait-for-db.sh para garantir que o banco está pronto
engine = create_engine(SQLALCHEMY_DATABASE_URL) #engine = "motor" da conexão com banco de dados

try: #teste de conexão com banco de dados
    conexao_teste = engine.connect()
    print("Conexão bem-sucedida!")
    conexao_teste.close()
except Exception as e:
    print("Erro na conexão:", e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #sessionmaker cria uma fábrica de sessões para gerar session
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()