from django.urls import path
from var_dump import var_dump
from produto.views import ListaProdutos, DetalheProduto, AdicionarAoCarrinho, RemoverDoCarrinho, Carrinho, ResumoDaCompra



app_name = 'produto'


urlpatterns = [
    path('', ListaProdutos.as_view(), name='lista'),
    path('<slug>', DetalheProduto.as_view(), name='detalhe'),
    path('adicionaraocarrinho/', AdicionarAoCarrinho.as_view(), name='adicionaraocarrinho'),
    path('removerdocarrinho/', RemoverDoCarrinho.as_view(), name='removerdocarrinho'),
    path('carrinho/', Carrinho.as_view(), name='carrinho'),
    path('resumodacompra/', ResumoDaCompra.as_view(), name='resumodacompra'),
]