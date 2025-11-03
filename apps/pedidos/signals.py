from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.core.pubsub import pubsub_manager, SystemEvents
from .models import Pedido


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