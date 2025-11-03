from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.core.pubsub import pubsub_manager, SystemEvents
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