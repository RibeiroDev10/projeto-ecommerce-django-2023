from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from var_dump import var_dump
from pprint import pprint
from django.contrib.auth.models import User
from django.views.generic.list import ListView 
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import copy
from . import models
from . import forms  # forms.py da raiz do app pedido



# Classe de visualização (View) para a criação de perfis de usuário
class BasePerfil(View):
    # Define o nome do template a ser utilizado
    template_name = 'perfil/criar.html'

    # Método de configuração executado antes da execução de qualquer método de visualização
    def setup(self, *args, **kwargs):
        self.perfil = None

        # Chama o método setup da classe pai (superclasse)
        super().setup(*args, **kwargs)

        # Copia profundamente o carrinho de compras da sessão atual
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho'))

        # Dados da requisição POST e a requisição completa
        self.request.POST # <QueryDict: {'csrfmiddlewaretoken': ['7ihurNqWRI3WnTJWVT3amlzyq2lsMEo1QB5ABHun3Ql7iMF5Ulfs5RaxUz6NqEuq'], 'first_name': ['Rafael'], 'last_name': ['Ribeiro'], 'username': ['rafaelrib10'], 'password': ['1234'], 'email': ['rafaelTeste@gmail.com.br']}>
        self.request # <WSGIRequest: GET '/perfil/'>
        self.request.user # <SimpleLazyObject: <User: rafael>>

        # Verifica se o usuário está autenticado
        if self.request.user.is_authenticated:

            # Filtrando e pegando o usuario da base com base no usuário da requisição --> <Perfil: rafael> --> <Modelo: objeto>
            self.perfil = models.Perfil.objects.filter(usuario=self.request.user).first()

            # Se autenticado, cria um dicionário de contexto
            self.contexto = {
                # Instancia o formulário 'UserForm' associado aos dados da requisição POST, se disponíveis, ou None
                'userform': forms.UserForm(
                    data=self.request.POST or None, 
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                # Instancia o formulário 'PerfilForm' associado aos dados da requisição POST, se disponíveis, ou None
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                )
            }
        else:
            # Se não autenticado, cria um dicionário de contexto
            self.contexto = {
                # Instancia o formulário 'UserForm' associado aos dados da requisição POST, se disponíveis, ou None
                'userform': forms.UserForm(data=self.request.POST or None), 
                # Instancia o formulário 'PerfilForm' associado aos dados da requisição POST, se disponíveis, ou None
                'perfilform': forms.PerfilForm(data=self.request.POST or None)
            }

        self.contexto # {'perfilform': <PerfilForm bound=True, valid=Unknown, fields=(idade;data_nascimento;cpf;endereco;numero;complemento;bairro;cep;cidade;estado)>, 'userform': <UserForm bound=True, valid=Unknown, fields=(first_name;last_name;username;senha;email)>}
        
        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        # Renderiza o template usando o método render do Django
        # self.renderizar --> <HttpResponse status_code=200, "text/html; charset=utf-8">
        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar



class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        # Verifica se os formulários de usuário e perfil são válidos
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            # Se algum dos formulários não for válido, exibe uma mensagem de erro
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se todos '
                'os campos foram preenchidos corretamente.'
            )
            # Retorna uma função ou método chamado 'self.renderizar', possivelmente para renderizar uma resposta HTTP
            return self.renderizar
            
        # Obtém dados do formulário de usuário
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('senha')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        email = self.userform.cleaned_data.get('email')

        # Usuário logado
        if self.request.user.is_authenticated:
            # Obtém o usuário autenticado da base de dados usando o username
            usuario = get_object_or_404(User, username=self.request.user.username) # type: ignore
            usuario.username = username

            # Verifica se uma senha foi fornecida e a atualiza se necessário
            if password:
                usuario.set_password(password)

            usuario.email = email  # Atualiza o e-mail
            usuario.first_name = first_name  # Atualiza o primeiro nome
            usuario.last_name = last_name  # Atualiza o sobrenome
            usuario.save()

            # Se nao tiver perfil, criamos um
            if not self.perfil:
                self.perfilform.cleaned_data['usuario'] = usuario
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:  # Se já tiver perfil
                self.perfilform.save(commit=False)
                perfil.usuario = usuario  # type: ignore
                perfil.save()  # type: ignore

        # Usuário não logado (novo usuário)
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
            )

            if autentica:
                login(self.request, user=usuario)

        # Atualiza o carrinho de compras na sessão do usuário.
        # A sessão em Django é um mecanismo para armazenar dados temporários associados a um usuário específico.
        # Aqui, o carrinho de compras atual (self.carrinho) é atribuído à chave 'carrinho' na sessão do usuário.
        # Isso garante que as informações do carrinho sejam mantidas entre diferentes solicitações do mesmo usuário.
        # Em seguida, chamamos self.request.session.save() para persistir as alterações na sessão.
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Seu cadastro foi criado/atualizado com sucesso!'
        )

        messages.success(
            self.request,
            "Você fez login e pode concluir a sua compra."
        )

        return redirect('produto:carrinho')



class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')



class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        
        if not username or not password:
            messages.error(
                self.request,
                "Usuário ou senha inválidos"
            )
            return redirect('perfil:criar')
        
        usuario = authenticate(self.request, username=username, password=password)
        
        if not usuario:
            messages.error(
                self.request,
                "Usuário ou senha inválidos"
            )
            return redirect('perfil:criar')
        
        login(self.request, user=usuario)

        messages.success(
                self.request,
                "Login feito com sucesso! Pode concluir sua compra"
            )
        
        return redirect('produto:carrinho')


class Logout(BasePerfil):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))

        # Chama a função de logout, encerrando a sessão do usuário atual.
        # self.request é a instância da requisição atual associada a esta view. 
        # A função logout precisa dessa instância para saber qual usuário está sendo deslogado.
        logout(self.request)

        # Salvando a copia do carrinho da sessão anterior para a nova sessão após o logout
        self.request.session['carrinho'] = carrinho
        self.request.session.save()

        # Redireciona o usuário para a página de criação de perfil após o logout
        return redirect('produto:lista')