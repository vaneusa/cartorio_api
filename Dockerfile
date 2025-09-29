FROM python:3.13-slim

# Define diretório de trabalho
WORKDIR /usr/src/app

# Copia requirements
COPY requirements.txt .

# Instala dependências do sistema e Python em um único RUN para otimização
RUN apt-get update && apt-get install -y \
    bash \
    libmagic1 \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir -r requirements.txt

 # Define o PYTHONPATH para que o pacote "app" seja reconhecido
 ENV PYTHONPATH=/usr/src/app

# Copia o restante do código da aplicação
COPY . .

# Permite execução do script wait-for-db.sh
RUN chmod +x /usr/src/app/wait-for-db.sh

# Expõe a porta da API
EXPOSE 8080

# Comando de inicialização da aplicação
CMD ["sh", "-c", "/usr/src/app/wait-for-db.sh && PYTHONPATH=/usr/src/app uvicorn app.main:app --host 0.0.0.0 --port 8080"]
