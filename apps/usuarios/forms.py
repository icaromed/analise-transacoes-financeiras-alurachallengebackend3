from django import forms


class Login(forms.Form):
    email = forms.EmailField(label='email')
    senha = forms.PasswordInput()

