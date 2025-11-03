from django.urls import reverse_lazy
from apps.core.utils import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Produto

class ProdutoListView(BaseListView):
    model = Produto
    template_name = 'produtos/produto_list.html'
    context_object_name = 'produtos'


class ProdutoDetailView(BaseDetailView):
    model = Produto
    template_name = 'produtos/produto_detail.html'
    context_object_name = 'produto'


class ProdutoCreateView(BaseCreateView):
    model = Produto
    fields = ['nome', 'descricao', 'preco', 'categoria', 'estoque', 'ativo']
    template_name = 'produtos/produto_form.html'
    success_url = reverse_lazy('produtos:list')


class ProdutoUpdateView(BaseUpdateView):
    model = Produto
    fields = ['nome', 'descricao', 'preco', 'categoria', 'estoque', 'ativo']
    template_name = 'produtos/produto_form.html'
    success_url = reverse_lazy('produtos:list')


class ProdutoDeleteView(BaseDeleteView):
    model = Produto
    template_name = 'produtos/produto_confirm_delete.html'
    success_url = reverse_lazy('produtos:list')
