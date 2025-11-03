"""
Signals do app Usuários
Handlers de eventos do sistema Publish-Subscribe
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.core.pubsub import event_handler, SystemEvents
from .models import Usuario, PerfilUsuario


@receiver(post_save, sender=Usuario)
def usuario_saved(sender, instance, created, **kwargs):
    """Signal para quando usuário é salvo"""
    if created:
        # Criar perfil automaticamente
        PerfilUsuario.objects.get_or_create(usuario=instance)


# Event handlers usando o sistema Pub/Sub
@event_handler(SystemEvents.USUARIO_CRIADO)
def handle_usuario_criado(data):
    """Handler para quando usuário é criado"""
    print(f"📧 Enviando email de boas-vindas para {data.get('email')}")


@event_handler(SystemEvents.USUARIO_LOGIN)
def handle_usuario_login(data):
    """Handler para login de usuário"""
    print(f"👤 Usuário {data.get('username')} fez login")


@event_handler(SystemEvents.USUARIO_LOGOUT)
def handle_usuario_logout(data):
    """Handler para logout de usuário"""
    print(f"👤 Usuário {data.get('username')} fez logout")


@event_handler(SystemEvents.USUARIO_DELETADO)
def handle_usuario_deletado(data):
    """Handler para usuário deletado"""
    print(f"🗑️ Usuário {data.get('username')} foi desativado")
