from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o settings do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

# Cria a instância do Celery
app = Celery('core')

# Carrega configuração do Django com prefixo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descobrir tasks de todos os apps instalados
app.autodiscover_tasks()
