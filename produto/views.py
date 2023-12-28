from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from var_dump import var_dump
from pprint import pprint
from django.contrib import messages
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views import View
from django.http import HttpResponse
from produto.models import Produto, Variacao



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
        # self.request --> pega a requisição HTTP atual: <WSGIRequest: GET '/adicionaraocarrinho/?vid=6'>
        # Exemplo de retorno da chave ['HTTP_REFERER'] --> 'http://127.0.0.1:8000/faca'
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))

        # self.request.GET # Retorna um dicionário de consulta --> <QueryDict: {'vid': ['6']}>
        # self.request.GET.get("vid")) # get() --> Faz buscas dentro da QueryDict retornada pelo GET
        variacao_id = self.request.GET.get("vid")

        # Messages -> Módulo do Django, configurado em settings.py do projeto(arquivo loja)
        # <module 'django.contrib.messages' from 'C:\\Users\\rafae\\Documents\\projeto-ecommerce-django-2023\\venv\\Lib\\site-packages\\django\\contrib\\messages\\__init__.py'>
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            # Pegando a URL anterior --> Redirecionando de volta à página anterior.
            return redirect(http_referer)
        
        # Obtenha algum objeto do modelo Variacao com base no id do get
        # Exemplo de <Modelo: Objeto> --> <Variacao: Faca>
        variacao = get_object_or_404(Variacao, id=variacao_id)

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            # De volta à página anterior
            return redirect(http_referer)

        # self.request.session) --> <django.contrib.sessions.backends.db.SessionStore object at 0x000001D6A5341FD0>
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}  # Cria um novo dict (vazio) na chave ['carrinho']
            self.request.session.save()

        # self.request.session.get('carrinho')) --> {} # Dict vazio criado no bloco if acima ^
        carrinho = self.request.session['carrinho']

        # Caso o id da variação exista no carrinho
        if variacao_id in carrinho:
            ...
        # Se não existir adiciona o id da variação na chave do ['carrinho']    
        else:
            dicionario = carrinho[variacao_id]
            print('carrinho[variacao_id]')
            pprint(dicionario)
            print()
            
            carrinho[variacao_id] = {

            }


        return HttpResponse(f'{variacao.produto} {variacao.nome}')



class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoverDoCarrinho')



class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')



class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
