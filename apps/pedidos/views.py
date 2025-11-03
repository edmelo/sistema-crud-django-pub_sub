from django.urls import reverse_lazy
from apps.core.utils import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Pedido

class PedidoListView(BaseListView):
    model = Pedido
    template_name = 'pedidos/pedido_list.html'
    context_object_name = 'pedidos'


class PedidoDetailView(BaseDetailView):
    model = Pedido
    template_name = 'pedidos/pedido_detail.html'
    context_object_name = 'pedido'


class PedidoCreateView(BaseCreateView):
    model = Pedido
    fields = ['usuario', 'status', 'valor_total', 'observacoes']
    template_name = 'pedidos/pedido_form.html'
    success_url = reverse_lazy('pedidos:list')


class PedidoUpdateView(BaseUpdateView):
    model = Pedido
    fields = ['status', 'valor_total', 'observacoes']
    template_name = 'pedidos/pedido_form.html'
    success_url = reverse_lazy('pedidos:list')


class PedidoDeleteView(BaseDeleteView):
    model = Pedido
    template_name = 'pedidos/pedido_confirm_delete.html'
    success_url = reverse_lazy('pedidos:list')
