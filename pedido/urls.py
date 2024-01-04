from django.urls import path
from pedido.views import Pagar, SalvarPedido, Detalhe, Lista

app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', Pagar.as_view(), name='pagar'),
    path('salvarpedido/', SalvarPedido.as_view(), name='salvarpedido'),
    path('lista/', Lista.as_view(), name='lista'),
    path('detalhe/<int:pk>', Detalhe.as_view(), name='detalhe'),
]