from django.shortcuts import render
from var_dump import var_dump
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views import View
from django.http import HttpResponse
from produto.models import Produto



class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'  # Ao acessar a URL raiz de produto.urls, vai chamar essa view(ListaProdutos) e renderizar este template.
    context_object_name = 'produtos'
    paginate_by = 10



class DetalheProduto(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'  # Busca o objeto Produto correspondente ao slug passado no endpoint




class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AdicionarAoCarrinho')



class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoverDoCarrinho')



class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')



class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
