"""
Views do app Usuários
Implementação das operações CRUD
Responsável: Ednaldo Batista de Melo
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView
from django.http import JsonResponse
from django.db.models import Q
from apps.core.utils import BaseCreateView, BaseUpdateView, BaseDeleteView, BaseListView, BaseDetailView
from apps.core.pubsub import pubsub_manager, SystemEvents
from .models import Usuario, PerfilUsuario
from .forms import UsuarioForm, UsuarioUpdateForm, LoginForm, RegisterForm


class UsuarioListView(BaseListView):
    """Lista todos os usuários"""
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )

        return queryset.filter(is_active=True)


class UsuarioDetailView(BaseDetailView):
    """Exibe detalhes de um usuário"""
    model = Usuario
    template_name = 'usuarios/usuario_detail.html'
    context_object_name = 'usuario'


class UsuarioCreateView(BaseCreateView):
    """Criar novo usuário"""
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Publicar evento de usuário criado
        pubsub_manager.publish(SystemEvents.USUARIO_CRIADO, {
            'usuario_id': self.object.id,
            'username': self.object.username,
            'email': self.object.email
        })

        messages.success(self.request, 'Usuário criado com sucesso!')
        return response


class UsuarioUpdateView(BaseUpdateView):
    """Atualizar usuário existente"""
    model = Usuario
    form_class = UsuarioUpdateForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Publicar evento de usuário atualizado
        pubsub_manager.publish(SystemEvents.USUARIO_ATUALIZADO, {
            'usuario_id': self.object.id,
            'username': self.object.username,
            'changes': form.changed_data
        })

        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return response


class UsuarioDeleteView(BaseDeleteView):
    """Desativar usuário (soft delete)"""
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuarios:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Soft delete - apenas desativar
        self.object.is_active = False
        self.object.save()

        # Publicar evento de usuário deletado
        pubsub_manager.publish(SystemEvents.USUARIO_DELETADO, {
            'usuario_id': self.object.id,
            'username': self.object.username
        })

        messages.success(request, 'Usuário desativado com sucesso!')
        return redirect(self.success_url)


# Views de autenticação
class LoginView(TemplateView):
    """View de login personalizada"""
    template_name = 'usuarios/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    # Publicar evento de login
                    pubsub_manager.publish(SystemEvents.USUARIO_LOGIN, {
                        'usuario_id': user.id,
                        'username': user.username
                    })

                    messages.success(request, f'Bem-vindo, {user.get_full_name()}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Conta desativada.')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')

        return render(request, self.template_name, {'form': form})


def logout_view(request):
    """View de logout"""
    if request.user.is_authenticated:
        # Publicar evento de logout
        pubsub_manager.publish(SystemEvents.USUARIO_LOGOUT, {
            'usuario_id': request.user.id,
            'username': request.user.username
        })

        messages.info(request, 'Logout realizado com sucesso!')

    logout(request)
    return redirect('home')


class RegisterView(TemplateView):
    """View de registro"""
    template_name = 'usuarios/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            # Publicar evento de usuário criado
            pubsub_manager.publish(SystemEvents.USUARIO_CRIADO, {
                'usuario_id': user.id,
                'username': user.username,
                'email': user.email
            })

            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')

        return render(request, self.template_name, {'form': form})


# API Views (JSON responses)
def usuarios_api_list(request):
    """API para listar usuários (JSON)"""
    usuarios = Usuario.objects.filter(is_active=True).values(
        'id', 'username', 'first_name', 'last_name', 'email'
    )

    return JsonResponse({'success': True, 'data': list(usuarios)})
