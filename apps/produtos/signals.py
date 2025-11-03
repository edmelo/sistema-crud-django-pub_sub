from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from apps.core.pubsub import pubsub_manager, SystemEvents, event_handler
from apps.core.email import send_system_email
from .models import Produto


@receiver(post_save, sender=Produto)
def produto_saved(sender, instance: Produto, created, **kwargs):
    if created:
        pubsub_manager.publish(SystemEvents.PRODUTO_CRIADO, {
            'id': instance.id,
            'nome': instance.nome,
            'categoria': instance.categoria,
            'estoque': instance.estoque,
        })
    else:
        pubsub_manager.publish(SystemEvents.PRODUTO_ATUALIZADO, {
            'id': instance.id,
            'changes': 'updated',  # simplificado
        })

    # Evento de estoque baixo
    try:
        if instance.estoque is not None and instance.estoque < 5:
            pubsub_manager.publish(SystemEvents.PRODUTO_ESTOQUE_BAIXO, {
                'id': instance.id,
                'nome': instance.nome,
                'estoque': instance.estoque,
            })
    except Exception:
        pass


@receiver(post_delete, sender=Produto)
def produto_deleted(sender, instance: Produto, **kwargs):
    pubsub_manager.publish(SystemEvents.PRODUTO_DELETADO, {
        'id': instance.id,
        'nome': instance.nome,
    })


# ==========================
# Handlers de e-mail (Pub/Sub)
# ==========================

def _admin_emails():
    # Usa ADMINS se configurado; fallback para EMAIL_HOST_USER
    admins = getattr(settings, 'ADMINS', None)
    if admins:
        return [email for _, email in admins if email]
    default = getattr(settings, 'EMAIL_HOST_USER', None)
    return [default] if default else []


@event_handler(SystemEvents.PRODUTO_ESTOQUE_BAIXO)
def handle_produto_estoque_baixo(data):
    """Notifica administradores quando estoque está baixo"""
    nome = data.get('nome')
    estoque = data.get('estoque')
    destinatarios = _admin_emails()
    if not destinatarios:
        return

    subject = f"Estoque baixo: {nome}"
    message = (
        f"Atenção,\n\nO produto '{nome}' está com estoque baixo (quantidade atual: {estoque}).\n"
        "Considere realizar reposição."
    )
    send_system_email(subject, message, destinatarios)