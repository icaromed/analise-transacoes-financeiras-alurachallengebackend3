from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.usuarios.models import User
from..functions import *
from ..forms import EditarUsuario


def lista_usuarios(request):
    """renders a page containing all the registred users (but Admin and deleted users)"""
    if sem_permissao(request):
        return redirect('login')

    usuarios_validos = User.objects.exclude(username='Admin').exclude(deleted=True)
    if request.method == "GET":
        return render(request, 'usuarios/lista_usuarios.html', {"usuarios_validos": usuarios_validos})
    elif request.method == "POST":

        return render(request, 'usuarios/lista_usuarios.html', {"usuarios_validos": usuarios_validos})


def remover_usuario(request, id_n):
    """deletes a user"""
    if sem_permissao(request):
        return redirect('login')

    user = get_object_or_404(User, id=id_n)

    erro = erro_remover(id_n, request)
    if erro:
        messages.error(request, erro)
        return redirect('lista_usuarios')

    if request.method == "POST":
        user.deleted = True
        user.save()
        messages.success(request, 'Usuário removido com sucesso')
        return redirect('lista_usuarios')
    return redirect('lista_usuarios')


def editar_usuario(request, id_n):
    """renders a page for editing a given user"""
    if sem_permissao(request):
        return redirect('login')

    user = get_object_or_404(User, id=id_n)
    context = {
        "user": user,
        "form": EditarUsuario(initial={"email": user.email, "username": user.username}),
    }

    if request.method == "GET":
        return render(request, 'usuarios/editar_usuario.html', context)

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']

        erro = erro_editar(username, email, user, id_n)
        if erro:
            messages.error(request, erro)
            return redirect('lista_usuarios')
        else:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, 'Os dados do usuário foram atualizados')
            return redirect('lista_usuarios')
    return redirect('lista_usuarios')
