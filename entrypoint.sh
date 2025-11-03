#!/bin/sh
# Entrypoint para o container web
# - roda migrate
# - roda collectstatic
# - ajusta permissões dos volumes (static e media)
# - executa o comando passado (ex: gunicorn ...)

set -e

echo "Entrypoint: usando settings em $DJANGO_SETTINGS_MODULE"

# Se o banco estiver usando sqlite, garantir diretório existe (é só uma proteção)
mkdir -p /app/staticfiles /app/media

echo "Rodando migrações..."
python manage.py migrate --noinput || true

echo "Rodando collectstatic..."
python manage.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE:-core.settings.production}

echo "Ajustando permissões em /app/staticfiles e /app/media"
chown -R appuser:appuser /app/staticfiles /app/media || true

echo "Executando comando: $@"
exec "$@"
