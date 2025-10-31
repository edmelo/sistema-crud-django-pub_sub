"""
Models do app Usuários
Responsável: Ednaldo Batista de Melo
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from apps.core.model_utils import validate_cpf, validate_phone, BaseModelMixin


class Usuario(AbstractUser, BaseModelMixin):
    """Modelo customizado de usuário"""

    # Campos obrigatórios
    email = models.EmailField('E-mail', unique=True, blank=True, null=True, help_text='E-mail único no sistema')

    # Campos pessoais
    cpf = models.CharField('CPF', max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField('Telefone', max_length=15, blank=True, null=True)
    data_nascimento = models.DateField('Data de Nascimento', blank=True, null=True)

    # Campos de endereço
    endereco = models.CharField('Endereço', max_length=255, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True, null=True)
    estado = models.CharField('Estado', max_length=2, blank=True, null=True)
    cep = models.CharField('CEP', max_length=10, blank=True, null=True)

    # Campos de controle
    ativo = models.BooleanField('Ativo', default=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-criado_em']
        db_table = 'usuarios'

    def __str__(self):
        return self.get_full_name() or self.username

    def clean(self):
        """Validações customizadas"""
        super().clean()

        if self.cpf:
            try:
                self.cpf = validate_cpf(self.cpf)
            except ValidationError as e:
                raise ValidationError({'cpf': e.message})

        if self.telefone:
            try:
                self.telefone = validate_phone(self.telefone)
            except ValidationError as e:
                raise ValidationError({'telefone': e.message})

    def save(self, *args, **kwargs):
        """Sobrescrever save para executar clean"""
        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Retorna nome completo"""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def nome_completo(self):
        """Property para template"""
        return self.get_full_name()

    @property
    def endereco_completo(self):
        """Retorna endereço completo formatado"""
        partes = [self.endereco, self.cidade, self.estado, self.cep]
        return ', '.join([p for p in partes if p])

    def is_profile_complete(self):
        """Verifica se o perfil está completo"""
        required_fields = [self.first_name, self.last_name, self.email, self.telefone]
        return all(required_fields)


class PerfilUsuario(models.Model):
    """Informações adicionais do perfil do usuário"""

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name='perfil', verbose_name='Usuário'
    )

    bio = models.TextField('Biografia', max_length=500, blank=True, null=True)
    avatar = models.ImageField('Avatar', upload_to='avatars/', blank=True, null=True)
    receber_emails = models.BooleanField('Receber e-mails promocionais', default=True)
    receber_notificacoes = models.BooleanField('Receber notificações', default=True)
    tema_preferido = models.CharField(
        'Tema Preferido', max_length=20,
        choices=[('light', 'Claro'), ('dark', 'Escuro'), ('auto', 'Automático')],
        default='light'
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos Usuários'
        db_table = 'usuarios_perfil'

    def __str__(self):
        return f'Perfil de {self.usuario.get_full_name()}'
