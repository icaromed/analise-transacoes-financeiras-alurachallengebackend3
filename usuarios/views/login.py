from django.shortcuts import render, redirect
from usuarios.models import User
from django.contrib import messages
from django.contrib import auth


def login(request):
    if request.method == "GET":
        return render(request, 'usuarios/login.html')

    elif request.method == "POST":
        email = request.POST['email']
        senha = request.POST['senha']

        if not User.objects.filter(email=email).exists():
            messages.error(request, 'Email não cadastrado')
            return redirect('login')
        username = User.objects.filter(email=email).values_list('username', flat=True).get()
        user = auth.authenticate(request, username=username, password=senha)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Senha incorreta')
            return redirect('login')


def logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.deleted:
        return redirect('login')

    auth.logout(request)
    return redirect('login')
