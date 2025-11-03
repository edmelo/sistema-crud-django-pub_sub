from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.core.pubsub import pubsub_manager, SystemEvents, event_handler
from apps.core.email import send_system_email
from .models import Pedido
from django.contrib.auth import get_user_model


@receiver(post_save, sender=Pedido)
def pedido_saved(sender, instance: Pedido, created, **kwargs):
    if created:
        pubsub_manager.publish(SystemEvents.PEDIDO_CRIADO, {
            'id': instance.id,
            'numero': instance.numero,
            'usuario_id': instance.usuario_id,
            'status': instance.status,
        })
    else:
        pubsub_manager.publish(SystemEvents.PEDIDO_ATUALIZADO, {
            'id': instance.id,
            'status': instance.status,
        })

    if instance.status == 'enviado':
        pubsub_manager.publish(SystemEvents.PEDIDO_ENVIADO, {'id': instance.id, 'numero': instance.numero})
    if instance.status == 'entregue':
        pubsub_manager.publish(SystemEvents.PEDIDO_ENTREGUE, {'id': instance.id, 'numero': instance.numero})


@receiver(post_delete, sender=Pedido)
def pedido_deleted(sender, instance: Pedido, **kwargs):
    pubsub_manager.publish(SystemEvents.PEDIDO_CANCELADO, {'id': instance.id, 'numero': instance.numero})


# ==========================
# Handlers de e-mail (Pub/Sub)
# ==========================

User = get_user_model()


@event_handler(SystemEvents.PEDIDO_CRIADO)
def handle_pedido_criado(data):
    """Envia e-mail de confirmação de pedido ao usuário"""
    usuario_id = data.get('usuario_id')
    numero = data.get('numero')
    if not usuario_id:
        return

    email = User.objects.filter(id=usuario_id).values_list('email', flat=True).first()
    if not email:
        return

    subject = f"Seu pedido {numero} foi recebido"
    message = (
        f"Olá,\n\nRecebemos o seu pedido {numero}.\n"
        "Você receberá atualizações por e-mail a cada mudança de status.\n\n"
        "Obrigado pela preferência."
    )
    send_system_email(subject, message, [email])


@event_handler(SystemEvents.PEDIDO_ENVIADO)
def handle_pedido_enviado(data):
    """Notifica o usuário quando o pedido foi enviado"""
    pedido_id = data.get('id')
    if not pedido_id:
        return

    try:
        pedido = Pedido.objects.select_related('usuario').get(id=pedido_id)
    except Pedido.DoesNotExist:
        return

    email = getattr(pedido.usuario, 'email', None)
    if not email:
        return

    subject = f"Seu pedido {pedido.numero} foi enviado"
    message = (
        f"Olá,\n\nSeu pedido {pedido.numero} já está a caminho!\n"
        "Em breve você receberá mais detalhes da entrega.\n\n"
        "Agradecemos a compra."
    )
    send_system_email(subject, message, [email])


@event_handler(SystemEvents.PEDIDO_ENTREGUE)
def handle_pedido_entregue(data):
    """Notifica o usuário quando o pedido foi entregue"""
    pedido_id = data.get('id')
    if not pedido_id:
        return

    try:
        pedido = Pedido.objects.select_related('usuario').get(id=pedido_id)
    except Pedido.DoesNotExist:
        return

    email = getattr(pedido.usuario, 'email', None)
    if not email:
        return

    subject = f"Seu pedido {pedido.numero} foi entregue"
    message = (
        f"Olá,\n\nSeu pedido {pedido.numero} foi entregue com sucesso.\n"
        "Esperamos que você aproveite!\n\n"
        "Se puder, avalie sua experiência conosco."
    )
    send_system_email(subject, message, [email])