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
