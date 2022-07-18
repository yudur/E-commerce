from django import forms
from . import models
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput(), label='Senha')
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(), label='Confirmação da senha')

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        confirmetion_password_data = cleaned.get('password2')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_user_msg_exists = 'Usuário já existe!'
        error_user_email_exists = 'E-mail já existe!'
        error_user_password_match = 'As duas senhas não conferem.'
        error_user_password_short = 'Sua senha precisa ter pelo menos 8 caracteres'
        error_msg_required_fields = 'Este campo é obrigatorio.'

        # Usuários logados: atualização
        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_error_msgs['username'] = error_user_msg_exists
    
            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_user_email_exists
            
            if password_data:
                if password_data != confirmetion_password_data:
                    validation_error_msgs['password'] = error_user_password_match
                    validation_error_msgs['password2'] = error_user_password_match

                if len(password_data) < 8:
                    validation_error_msgs['password'] = error_user_password_short
                
        # Usuários não logados: Cadastro
        else:
            if usuario_db:
                validation_error_msgs['username'] = error_user_msg_exists
    
            if email_db:
                validation_error_msgs['email'] = error_user_email_exists
            
            if not password_data:
                validation_error_msgs['password'] = error_msg_required_fields
            
            if not confirmetion_password_data:
                validation_error_msgs['password2'] = error_msg_required_fields

            if password_data != confirmetion_password_data:
                validation_error_msgs['password'] = error_user_password_match
                validation_error_msgs['password2'] = error_user_password_match

            if len(password_data) < 8:
                validation_error_msgs['password'] = error_user_password_short

            if validation_error_msgs:
                raise(forms.ValidationError(validation_error_msgs))
