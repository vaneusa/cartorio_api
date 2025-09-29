#!/bin/bash
set -e

host="$DB_HOST"
port=5432   # Porta do PostgreSQL

until pg_isready -h "$host" -p "$port"; do
  echo "Aguardando banco $host:$port..."
  sleep 2
done

echo "Banco pronto! Iniciando a API..."
exec "$@"

