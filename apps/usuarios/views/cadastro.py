from django.shortcuts import render, redirect
from django.contrib import messages
from apps.usuarios.models import User
import random
from..functions import *


def cadastro(request):
    """renders a user-register page"""
    if sem_permissao(request):
        return redirect('login')

    if request.method == "GET":
        return render(request, 'usuarios/cadastro.html')

    elif request.method == "POST":
        email = request.POST['email']
        username = request.POST['usuario']
        senha = str(random.random())[2:8]

        erro = erro_cadastro(username, email)
        if erro:
            messages.error(request, erro)
            return redirect('cadastro')

        user = User.objects.create_user(username, email, senha)
        if eviar_email(email, senha):
            user.save()
        else:
            messages.error(request, 'O Email contendo a senha não pôde ser enviado')
            return redirect('cadastro')
        return redirect('lista_usuarios')
