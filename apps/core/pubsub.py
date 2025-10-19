"""
Sistema Publish-Subscribe para eventos do sistema
Implementado para atender aos requisitos do projeto
"""

from typing import Dict, List, Callable, Any
import logging

logger = logging.getLogger(__name__)


class PubSubManager:
    """
    Gerenciador de eventos Publish-Subscribe
    """

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self._active = True

    def subscribe(self, event: str, callback: Callable) -> None:
        """Inscrever um callback para um evento"""
        if not self._active:
            return

        if event not in self.subscribers:
            self.subscribers[event] = []

        if callback not in self.subscribers[event]:
            self.subscribers[event].append(callback)
            logger.info(f"Subscribed to event '{event}': {callback.__name__}")

    def unsubscribe(self, event: str, callback: Callable) -> None:
        """Cancelar inscrição de um callback"""
        if event in self.subscribers:
            try:
                self.subscribers[event].remove(callback)
                logger.info(f"Unsubscribed from event '{event}': {callback.__name__}")
            except ValueError:
                logger.warning(f"Callback {callback.__name__} not found in event '{event}'")

    def publish(self, event: str, data: Any = None) -> None:
        """Publicar um evento para todos os subscribers"""
        if not self._active:
            return

        if event in self.subscribers:
            logger.info(f"Publishing event '{event}' to {len(self.subscribers[event])} subscribers")

            for callback in self.subscribers[event]:
                try:
                    if data is not None:
                        callback(data)
                    else:
                        callback()
                except Exception as e:
                    logger.error(f"Error executing callback {callback.__name__} for event '{event}': {e}")
        else:
            logger.debug(f"No subscribers for event '{event}'")


# Instância global do sistema
pubsub_manager = PubSubManager()


def event_handler(event_name: str):
    """
    Decorator para registrar automaticamente handlers de eventos
    """
    def decorator(func: Callable):
        pubsub_manager.subscribe(event_name, func)
        return func
    return decorator


# Eventos padrão do sistema
class SystemEvents:
    """Constantes para eventos do sistema"""

    # Eventos de usuário
    USUARIO_CRIADO = 'usuario_criado'
    USUARIO_ATUALIZADO = 'usuario_atualizado'
    USUARIO_DELETADO = 'usuario_deletado'
    USUARIO_LOGIN = 'usuario_login'
    USUARIO_LOGOUT = 'usuario_logout'

    # Eventos de produto
    PRODUTO_CRIADO = 'produto_criado'
    PRODUTO_ATUALIZADO = 'produto_atualizado'
    PRODUTO_DELETADO = 'produto_deletado'
    PRODUTO_ESTOQUE_BAIXO = 'produto_estoque_baixo'

    # Eventos de pedido
    PEDIDO_CRIADO = 'pedido_criado'
    PEDIDO_ATUALIZADO = 'pedido_atualizado'
    PEDIDO_CANCELADO = 'pedido_cancelado'
    PEDIDO_PROCESSADO = 'pedido_processado'
    PEDIDO_ENVIADO = 'pedido_enviado'
    PEDIDO_ENTREGUE = 'pedido_entregue'
