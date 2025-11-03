"""
Models do app Produtos
Responsável: Carolline Dias Pena
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.core.model_utils import BaseModelMixin


class Produto(BaseModelMixin, models.Model):
    """Modelo para produtos"""

    nome = models.CharField('Nome', max_length=200, blank=True)
    descricao = models.TextField('Descrição', blank=True)
    preco = models.DecimalField(
        'Preço', max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)], blank=True, null=True
    )
    categoria = models.CharField('Categoria', max_length=100, blank=True)
    estoque = models.PositiveIntegerField('Estoque', default=0)
    ativo = models.BooleanField('Ativo', default=True)

    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome
