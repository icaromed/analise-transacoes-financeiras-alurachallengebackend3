from django import forms


class Login(forms.Form):
    email = forms.EmailField(label='Email')
    senha = forms.CharField(widget=forms.PasswordInput, max_length=100)


class EditarUsuario(forms.Form):
    username = forms.CharField(label='Nome de Usuário')
    email = forms.EmailField(label='Email')


class Cadastro(forms.Form):
    username = forms.CharField(label='Nome de Usuário')
    email = forms.EmailField(label='Email')