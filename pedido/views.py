from django.shortcuts import render, redirect, reverse # type: ignore
from pprint import pprint
from var_dump import var_dump
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao
from utils import utils
from .models import Pedido, ItemPedido



class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar ')

        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs
    



class Pagar(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

    # --------------------------------------------------- Função para debugar a variavel de contexto
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     itempedidos = self.object.itempedido_set.all()
    #     for linha in itempedidos:
    #         print()
    #         pprint(linha.pedido_id)
    #         print()
    #     return context
    # --------------------------------------------------- Função para debugar a variavel de contexto



class Lista(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 10
    ordering = ['-id']


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'
    
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                "Você precisa fazer login"
            )
            return redirect('perfil:criar')
        
        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                "Carriho vazio."
            )
            return redirect('produto:lista')
        
        # Pegando o carrinho e relacionando com o banco de dados
        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [ v for v in carrinho]
        bd_variacoes = list(Variacao.objects.select_related('produto').filter(id__in=carrinho_variacao_ids))
        
        # Criando variaveis de controle, com base no banco de dados
        for variacao in bd_variacoes:
            vid = str(variacao.id)
            
            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = ""
            
            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo

                error_msg_estoque = "Estoque insuficiente para alguns produtos do seu carrinho. " \
                                    "Reduzimos a quantidade desses produtos. Por favor, " \
                                    "verifique quais produtos foram afetados a seguir." 
                
                if error_msg_estoque:
                    messages.error(
                        self.request,
                        error_msg_estoque
                    )

                    self.request.session.save()
                    return redirect('produto:carrinho')

        qtd_total_carrinho = utils.utils_cart_total_qtd(carrinho=carrinho)
        valor_total_carrinho = utils.utils_cart_totals(carrinho)

        # Registrando o pedido
        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C'
        )
        pedido.save()

        # Criando varios objetos em massa
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v,
                    variacao_id=v['variacao_id'],
                    preco=v['preco_unitario'],
                    preco_promocional=v['preco_unitario_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )
        print('Pedido inteiro: ', pedido)
        print('Pedido ID: ', pedido.id)
        print('Pedido PK: ', pedido.pk)
        del self.request.session['carrinho']
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )



class Detalhe(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'