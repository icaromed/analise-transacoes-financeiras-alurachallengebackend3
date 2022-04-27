from django.shortcuts import render, redirect
from django.contrib import messages
from .error import *


def login(request):
    """Login"""
    if request.method == "GET":
        return render(request, 'usuarios/login.html')

    elif request.method == "POST":
        email = request.POST['email']
        senha = request.POST['senha']

        if email_erro(email):
            messages.error(request, 'Email não cadastrado')
            return redirect('login')

        user = get_user(email, senha, request)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Senha incorreta')
            return redirect('login')


def logout(request):
    """Logout"""
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.deleted:
        return redirect('login')

    auth.logout(request)
    return redirect('login')
