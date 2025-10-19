"""
Utilitários compartilhados do sistema
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from rest_framework import status
from rest_framework.response import Response
import re


class BaseModelMixin:
    """Mixin com funcionalidades básicas para models"""

    def clean(self):
        """Validação básica para todos os models"""
        super().clean()


class LoginRequiredViewMixin(LoginRequiredMixin):
    """Mixin que requer login para acessar as views"""
    login_url = '/admin/login/'
    redirect_field_name = 'next'


class BaseCRUDView:
    """Classe base para views CRUD"""

    def get_success_message(self, action):
        """Retorna mensagem de sucesso baseada na ação"""
        model_name = self.model._meta.verbose_name
        messages = {
            'create': f'{model_name} criado com sucesso!',
            'update': f'{model_name} atualizado com sucesso!',
            'delete': f'{model_name} excluído com sucesso!'
        }
        return messages.get(action, 'Operação realizada com sucesso!')


class BaseCreateView(LoginRequiredViewMixin, CreateView, BaseCRUDView):
    """View base para criação"""
    pass


class BaseUpdateView(LoginRequiredViewMixin, UpdateView, BaseCRUDView):
    """View base para atualização"""
    pass


class BaseDeleteView(LoginRequiredViewMixin, DeleteView, BaseCRUDView):
    """View base para exclusão"""
    pass


class BaseListView(LoginRequiredViewMixin, ListView):
    """View base para listagem"""
    paginate_by = 20


class BaseDetailView(LoginRequiredViewMixin, DetailView):
    """View base para detalhes"""
    pass


def validate_cpf(cpf):
    """Valida CPF brasileiro"""
    cpf = re.sub(r'[^0-9]', '', cpf)

    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos')

    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')

    return cpf


def validate_phone(phone):
    """Valida telefone brasileiro"""
    phone = re.sub(r'[^0-9]', '', phone)

    if len(phone) not in [10, 11]:
        raise ValidationError('Telefone deve ter 10 ou 11 dígitos')

    return phone


def format_currency(value):
    """Formata valor monetário para exibição"""
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return "R$ 0,00"


class APIResponseMixin:
    """Mixin para padronizar respostas da API"""

    def success_response(self, data=None, message="Success", status_code=status.HTTP_200_OK):
        """Resposta de sucesso padronizada"""
        response_data = {
            'success': True,
            'message': message,
        }
        if data is not None:
            response_data['data'] = data

        return Response(response_data, status=status_code)

    def error_response(self, message="Error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Resposta de erro padronizada"""
        response_data = {
            'success': False,
            'message': message,
        }
        if errors:
            response_data['errors'] = errors

        return Response(response_data, status=status_code)


def generate_order_number():
    """Gera número único para pedidos"""
    import uuid
    from datetime import datetime

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:8].upper()

    return f"PED{timestamp}{unique_id}"
