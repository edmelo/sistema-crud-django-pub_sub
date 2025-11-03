"""
URLs do app Usuários
"""

from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # CRUD Views
    path('', views.UsuarioListView.as_view(), name='list'),
    path('criar/', views.UsuarioCreateView.as_view(), name='create'),
    path('<int:pk>/', views.UsuarioDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.UsuarioDeleteView.as_view(), name='delete'),

    # Autenticação
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.RegisterView.as_view(), name='register'),

    # APIs (JSON)
    path('api/list/', views.usuarios_api_list, name='api_list'),
]
