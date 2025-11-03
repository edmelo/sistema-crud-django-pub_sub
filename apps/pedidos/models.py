"""
Models do app Pedidos
Responsável: Carolline Dias Pena
"""

from django.db import models
from django.conf import settings
from apps.core.model_utils import BaseModelMixin, generate_order_number
from apps.produtos.models import Produto


class Pedido(BaseModelMixin, models.Model):
    """Modelo para pedidos"""

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processando', 'Processando'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    numero = models.CharField('Número', max_length=50, unique=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuário', null=True, blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')
    valor_total = models.DecimalField('Valor Total', max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    observacoes = models.TextField('Observações', blank=True)

    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-criado_em']

    def __str__(self):
        return f'Pedido {self.numero}'

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = generate_order_number()
        super().save(*args, **kwargs)


class ItemPedido(models.Model):
    """Itens do pedido"""

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField('Quantidade')
    preco_unitario = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario
