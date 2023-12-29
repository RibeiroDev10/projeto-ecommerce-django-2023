from django.shortcuts import render
from var_dump import var_dump
from pprint import pprint
from django.views.generic.list import ListView 
from django.views import View
from django.http import HttpResponse
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
                'perfilform': forms.PerfilForm(data=self.request.POST or None)
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

        # Renderiza o template usando o método render do Django
        # self.renderizar --> <HttpResponse status_code=200, "text/html; charset=utf-8">
        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar



class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('senha')
        email = self.userform.cleaned_data.get('email')

        # Usuário logado
        if self.request.user.is_authenticated:
            pass
        # Usuário não logado (novo)
        else:
            usuario = self.userform.save(commit=False)
            print(usuario)
            usuario.set_password(password)
            usuario.save()

            print(self.perfilform.cleaned_data)
            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        return self.renderizar



class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')



class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')



class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')