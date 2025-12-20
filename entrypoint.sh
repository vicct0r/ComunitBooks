#!/bin/bash
set -e

# Esperar o PostgreSQL ficar pronto
echo "Aguardando PostgreSQL ficar disponível..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL está pronto!"

python manage.py migrate --no-input
python manage.py collectstatic --no-input

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000 