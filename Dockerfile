FROM python:3.11-slim

LABEL maintainer="Ednaldo Batista de Melo & Carolline Dias Pena"

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings.production

# Instalar dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements/ requirements/
RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r requirements/production.txt --no-cache-dir

# Copiar código da aplicação
COPY . /app/

# Criar usuário não-root
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput --settings=core.settings.production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

EXPOSE 8000

# Comando para produção
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "core.wsgi:application"]
