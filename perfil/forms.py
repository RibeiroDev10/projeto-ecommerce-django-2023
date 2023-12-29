from django import forms
from var_dump import var_dump
from pprint import pprint
from . import models
from django.contrib.auth.models import User



class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)



# Definição de um formulário usando ModelForm do Django
class UserForm(forms.ModelForm):
    # Define um campo 'senha' para o formulário
    senha = forms.CharField(
        required=False,                  # Não é obrigatório preencher este campo
        widget=forms.PasswordInput(),   # Usa um widget de senha para a entrada do campo
        label='Senha'                    # Rótulo associado ao campo, exibido no formulário
    )

    # Define um campo 'senha2' para o formulário, utilizado para confirmar a senha
    senha2 = forms.CharField(
        required=False,                  # Não é obrigatório preencher este campo
        widget=forms.PasswordInput(),   # Usa um widget de senha para a entrada do campo
        label='Confirmação senha'        # Rótulo associado ao campo, exibido no formulário
    )


    # Define o inicializador (__init__) da classe
    def __init__(self, usuario=None, *args, **kwargs):
        # Chama o inicializador da classe pai (superclasse)
        super().__init__(*args, **kwargs)

        # Atribui o valor do parâmetro 'usuario' ao atributo 'usuario' da instância
        self.usuario = usuario


    # Meta classe que define o modelo associado e os campos a serem incluídos no formulário
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'senha', 'senha2', 'email', )

    # Método clean personalizado para validações adicionais no formulário
    def clean(self, *args, **kwargs):
        # Acessa os dados brutos do formulário
        data = self.data
        # Acessa os dados limpos e validados do formulário
        cleaned = self.cleaned_data

        # Dicionário para armazenar mensagens de erro de validação
        validation_error_messages = {}

        # Obtém dados do formulário limpo
        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        senha_data = cleaned.get('senha')
        senha2_data = cleaned.get('senha2')

        # Consulta ao banco de dados para obter dados se usuário e e-mail já existem
        # Retorna o nome do objeto que está no banco de dados
        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        # Mensagens de erro pré-definidas
        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As duas senhas não conferem'
        error_msg_password_short = 'Sua senha precisa ter pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório'
        
        # Usuários logados: atualização
        if self.usuario:

            # Verifica se o nome de usuário existe no banco de dados e não é o mesmo do usuário atual
            if usuario_db:
                if usuario_data != usuario_db.username:  # type:ignore
                    validation_error_messages['username'] = error_msg_user_exists
            
            # Verifica se o endereço de e-mail existe no banco de dados e não é o mesmo do usuário atual
            if email_db:
                if email_data != email_db.email:  # type:ignore
                    validation_error_messages['email'] = error_msg_email_exists
            
            # Verifica correspondência e comprimento da senha se uma senha estiver sendo fornecida
            if senha_data:
                if senha_data != senha2_data:
                    validation_error_messages['senha'] = error_msg_password_match
                    validation_error_messages['senha2'] = error_msg_password_match
                if len(senha_data) < 6:
                    validation_error_messages['senha'] = error_msg_password_short
        
        # Usuários não logados: cadastro
        else:
            # Verifica se o nome de usuário já existe no banco de dados
            if usuario_db:  # type: ignore
                validation_error_messages['username'] = error_msg_user_exists
            
            # Verifica se o endereço de e-mail já existe no banco de dados
            if email_db:  # type: ignore
                validation_error_messages['email'] = error_msg_email_exists

            # Verifica se a senha foi fornecida
            if not senha_data:
                validation_error_messages['senha'] = error_msg_required_field
                validation_error_messages['senha2'] = error_msg_required_field

            # Verifica se as senhas coincidem
            if senha_data != senha2_data:
                validation_error_messages['senha'] = error_msg_password_match
                validation_error_messages['senha2'] = error_msg_password_match

                # Verifica se a senha atende ao comprimento mínimo
                if len(senha_data) < 6:
                    validation_error_messages['senha'] = error_msg_password_short

        # Se houver mensagens de erro, lança uma exceção de validação do formulário
        if validation_error_messages:
            raise(forms.ValidationError(validation_error_messages))
