"""
Configurações de desenvolvimento
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Email backend para desenvolvimento
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configurações de logging mais detalhadas
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Trusted origins for CSRF (development)
# Add the host(s) you access the dev server from (http and/or https).
CSRF_TRUSTED_ORIGINS = [
    "https://localhost:8000",
    "http://localhost:8000",
    "https://127.0.0.1:8000",
    "http://127.0.0.1:8000",
]
