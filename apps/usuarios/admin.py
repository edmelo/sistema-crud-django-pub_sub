"""
Configuração do Django Admin para Usuários
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Usuario, PerfilUsuario
from .forms import RegisterForm, UsuarioUpdateForm


class PerfilUsuarioInline(admin.StackedInline):
    """Inline para o perfil do usuário"""
    model = PerfilUsuario
    can_delete = False
    extra = 0
    verbose_name = 'Perfil'
    verbose_name_plural = 'Perfil'


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    """Configuração do admin para Usuario"""

    # Formularios customizados para criação e edição
    add_form = RegisterForm
    form = UsuarioUpdateForm

    list_display = [
        'username', 'get_full_name', 'email', 'telefone',
        'is_active', 'is_staff', 'criado_em'
    ]

    list_filter = ['is_active', 'is_staff', 'is_superuser', 'criado_em', 'estado']

    search_fields = ['username', 'first_name', 'last_name', 'email', 'cpf', 'telefone']

    fieldsets = (
        ('Informações de Login', {'fields': ('username', 'password')}),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'email', 'cpf', 'telefone', 'data_nascimento')
        }),
        ('Endereço', {
            'fields': ('endereco', 'cidade', 'estado', 'cep'),
            'classes': ('collapse',)
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )

    # Campos exibidos no formulário de criação no Admin (Add User)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)

    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [PerfilUsuarioInline]
    ordering = ['-criado_em']

    def get_inline_instances(self, request, obj=None):
        """Não exibe o inline de Perfil na tela de criação para evitar duplicidade com o signal."""
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)

    def get_full_name(self, obj):
        """Exibe nome completo"""
        return obj.get_full_name() or '-'
    get_full_name.short_description = 'Nome Completo'


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """Configuração do admin para PerfilUsuario"""

    list_display = ['usuario', 'receber_emails', 'receber_notificacoes', 'tema_preferido']
    list_filter = ['receber_emails', 'receber_notificacoes', 'tema_preferido']
    search_fields = ['usuario__username', 'usuario__email', 'bio']


# Configurações do site admin
admin.site.site_header = 'Sistema CRUD - Administração'
admin.site.site_title = 'Sistema CRUD Admin'
admin.site.index_title = 'Administração do Sistema'
