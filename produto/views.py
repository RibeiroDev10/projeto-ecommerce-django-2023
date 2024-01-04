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
from perfil.models import Perfil
from django.db.models import Q



class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'  # Ao acessar a URL raiz de produto.urls, vai chamar essa view(ListaProdutos) e renderizar este template.
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-id']



class DetalheProduto(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'  # Busca o objeto Produto correspondente ao slug passado no endpoint



class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        # if self.request.session.get('carrinho'):
        #     del self.request.session['carrinho']
        #     self.request.session.save()

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
        variacao_estoque = variacao.estoque
        produto = variacao.produto
        produto_id = produto.id  # type: ignore
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        # Se existir imagem
        if imagem:
            imagem = imagem.name  # Atribuindo o nome da imagem para a variavel imagem
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            # De volta à página anterior
            return redirect(http_referer)

        # self.request.session --> <django.contrib.sessions.backends.db.SessionStore object at 0x000001D6A5341FD0>
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}  # Cria um novo dict (vazio) na chave ['carrinho']
            self.request.session.save()

        # self.request.session.get('carrinho')) --> {} # Dict vazio criado no bloco if acima ^
        carrinho = self.request.session['carrinho']

        # Se já existir uma Variação no Carrinho, vamos acrescentar mais um, no índice 'quantidade'
        if variacao_id in carrinho:
            # Variaveis para controle interno da quantidade da variação de um produto dentro de um carrinho
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho = quantidade_carrinho + 1

            # Se não houver estoque para aquela quantidade da Variação no carrinho
            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                    f'no seu carrinho'
                )
                quantidade_carrinho = variacao_estoque
            
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho

        # Se não existir adiciona o id da variação na chave do ['carrinho']
        else:
            # chave 'carrinho' vai ter outros indices dentro dela 
            # por que que estamos associando [variavel_id] como indices da chave 'carrinho'
            # Entao a lógica é: Acessarmos o carrinho, e dentro do carrinho temos o id da variação, 
            # Dentro desse id da variação temos acesso aos atributos desejados do produto
            # A lógica da estrutura neste caso é: CHAVE-ÍNDICE-VALORES
            carrinho[variacao_id] = {
                "produto_id": produto_id,
                "produto_nome" : produto_nome,
                "variacao_nome" : variacao_nome,
                "variacao_id" : variacao_id,
                "preco_unitario" : preco_unitario,
                "preco_unitario_promocional" : preco_unitario_promocional,
                "preco_quantitativo": preco_unitario,
                "preco_quantitativo_promocional": preco_unitario_promocional,
                "quantidade" : 1,
                "slug" : slug,
                "imagem" : imagem,
            }
        
        # Salvando a sessão após incluir o produto no carrinho
        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu carrinho.'
            f'{carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)



class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get("vid")
        carrinho = self.request.session['carrinho']

        if not variacao_id:
            return redirect(http_referer)

        if not carrinho:
            return redirect(http_referer)
        
        if variacao_id not in carrinho:
            return redirect(http_referer)

        produto_nome = carrinho[variacao_id]['produto_nome']
        variacao_produto = carrinho[variacao_id]['variacao_nome']
        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_produto} removido do carrinho'
        )

        del carrinho[variacao_id]
        self.request.session.save()

        return redirect(http_referer)
        


class Carrinho(View):
    def get(self, *args, **kwargs):
        return render(
            self.request, 
            'produto/carrinho.html',
        )



class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        
        # Checar se usuário tem perfil
        perfil = Perfil.objects.filter(usuario=self.request.user).exists()
        
        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil'
            )
            redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio'
            )
            redirect('produto:lista')
        
        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho']
        }

        return render(self.request, 'produto/resumodacompra.html', contexto)



class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs
        
        pprint(self.request.session)
        self.request.session['termo'] = termo
        pprint(self.request.session)

        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )

        self.request.session.save()
        return qs