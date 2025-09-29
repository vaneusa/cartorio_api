from dotenv import load_dotenv #dotenv Biblioteca que lê variaveis de ambiente no .env / load_dotenv() carrega as variaveis de ambiente no sistema
import os # Modulo padrão do python para interagir com o sistema

load_dotenv()

# Após o load_dotenv() rodar, os arquivos para serem puxados do .env para ca sem colocar as infos de forma exposta no codigo, será transcrito pelo os.getenv

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 8080)) # Vai buscar a variavel PORT, mas caso não encontre tem a porta para puxar ao lado
