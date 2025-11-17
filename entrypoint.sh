#!/bin/bash
set -e

# Esperar o PostgreSQL ficar pronto
echo "Aguardando PostgreSQL ficar disponível..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL está pronto!"

# Executar migrações e coletar static files
python manage.py migrate
python manage.py collectstatic --no-input

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000