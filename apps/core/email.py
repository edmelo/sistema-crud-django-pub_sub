"""
Utilitário centralizado para envio de e-mails do sistema
"""
from typing import Iterable, Optional
import logging

from django.conf import settings
from django.core.mail import send_mail, EmailMessage

logger = logging.getLogger(__name__)


def get_default_from_email() -> str:
    """Determina o remetente padrão.
    Prioriza DEFAULT_FROM_EMAIL; caso ausente, usa EMAIL_HOST_USER; como último recurso, um placeholder.
    """
    return getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", None) or "no-reply@example.com"


def send_system_email(
    subject: str,
    message: str,
    recipient_list: Iterable[str],
    *,
    html_message: Optional[str] = None,
    from_email: Optional[str] = None,
    fail_silently: bool = False,
) -> int:
    """Envia um e-mail simples usando a configuração do Django.

    Retorna a quantidade de mensagens enviadas (0 ou 1), como em django.core.mail.send_mail.
    """
    if not recipient_list:
        logger.warning("Nenhum destinatário informado para o e-mail: %s", subject)
        return 0

    sender = from_email or get_default_from_email()

    try:
        sent = send_mail(
            subject=subject,
            message=message,
            from_email=sender,
            recipient_list=list(recipient_list),
            fail_silently=fail_silently,
            html_message=html_message,
        )
        logger.info("E-mail enviado: subject='%s' para %s (from %s), backend=%s", subject, recipient_list, sender, getattr(settings, "EMAIL_BACKEND", ""))
        return sent
    except Exception:
        logger.exception("Falha ao enviar e-mail: subject='%s' para %s", subject, recipient_list)
        if fail_silently:
            return 0
        raise


def send_system_email_message(msg: EmailMessage, *, fail_silently: bool = False) -> int:
    """Envia um EmailMessage para casos mais avançados (anexos, headers, etc.)."""
    try:
        result = msg.send(fail_silently=fail_silently)
        logger.info("EmailMessage enviado: subject='%s' para %s", msg.subject, msg.to)
        return result
    except Exception:
        logger.exception("Falha ao enviar EmailMessage: subject='%s' para %s", msg.subject, msg.to)
        if fail_silently:
            return 0
        raise
