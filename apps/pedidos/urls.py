from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.PedidoListView.as_view(), name='list'),
    path('novo/', views.PedidoCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PedidoDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.PedidoUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.PedidoDeleteView.as_view(), name='delete'),
]
