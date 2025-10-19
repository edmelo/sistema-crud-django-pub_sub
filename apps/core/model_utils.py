"""
Utilitários seguros para uso em models (sem dependências de views/mixins)
"""

import re
import uuid
from datetime import datetime
from django.core.exceptions import ValidationError


class BaseModelMixin:
    """Mixin com funcionalidades básicas para models"""

    def clean(self):
        """Validação básica para todos os models"""
        super().clean()


def validate_cpf(cpf: str) -> str:
    """Valida CPF brasileiro e normaliza apenas dígitos."""
    cpf = re.sub(r"[^0-9]", "", cpf or "")

    if len(cpf) != 11:
        raise ValidationError("CPF deve ter 11 dígitos")

    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido")

    return cpf


def validate_phone(phone: str) -> str:
    """Valida telefone brasileiro e normaliza apenas dígitos."""
    phone = re.sub(r"[^0-9]", "", phone or "")

    if len(phone) not in [10, 11]:
        raise ValidationError("Telefone deve ter 10 ou 11 dígitos")

    return phone


def generate_order_number() -> str:
    """Gera número único para pedidos (ex.: PED20250101123045ABCDEF12)."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"PED{timestamp}{unique_id}"
