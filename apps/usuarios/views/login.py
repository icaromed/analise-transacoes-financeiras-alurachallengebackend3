from django.shortcuts import render, redirect
from django.contrib import messages
from ..functions import *
from ..forms import *


def login(request):
    """renders a login page"""
    if request.method == "GET":
        form = Login()
        context = {
            'form': form
        }
        return render(request, 'usuarios/login.html', context)

    elif request.method == "POST":
        email = request.POST['email']
        senha = request.POST['senha']

        if erro_email(email):
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
    """renders a logout page"""
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.deleted:
        return redirect('login')

    auth.logout(request)
    return redirect('login')
