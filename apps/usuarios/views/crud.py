from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.usuarios.models import User


def lista_usuarios(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.deleted:
        return redirect('login')

    usuarios_validos = User.objects.exclude(username='Admin').exclude(deleted=True)
    if request.method == "GET":
        return render(request, 'usuarios/lista_usuarios.html', {"usuarios_validos": usuarios_validos})
    elif request.method == "POST":

        return render(request, 'usuarios/lista_usuarios.html', {"usuarios_validos": usuarios_validos})


def remover_usuario(request, id_n):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.deleted:
        return redirect('login')

    user = get_object_or_404(User, id=id_n)

    if int(id_n) == request.user.id:
        messages.error(request, 'Não é possivel excluir o próprio usuário')
        return redirect('lista_usuarios')

    if int(id_n) == User.objects.filter(username="Admin").get().id:
        messages.error(request, 'Não é possivel excluir o usuário padrão')
        return redirect('lista_usuarios')

    if request.method == "POST":
        user.deleted = True
        user.save()
        messages.success(request, 'Usuário removido com sucesso')
        return redirect('lista_usuarios')
    return redirect('lista_usuarios')


def editar_usuario(request, id_n):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.deleted:
        return redirect('login')

    user = get_object_or_404(User, id=id_n)

    if request.method == "GET":
        return render(request, 'usuarios/editar_usuario.html', {"user": user})

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']

        if not username.strip():
            messages.error(request, 'O usuário não pode ficar vazio')
            return redirect('lista_usuarios')

        if not email.strip():
            messages.error(request, 'O Email não pode ficar vazio')
            return redirect('lista_usuarios')

        if username == user.username and email == user.email:
            messages.success(request, 'Os dados do usuário foram atualizados')
            return redirect('lista_usuarios')

        if User.objects.filter(username=username).exclude(id=id_n).exists():
            messages.error(request, 'Este Nome de Usuário já foi cadastrado')
            return redirect('lista_usuarios')

        if User.objects.filter(email=email).exclude(id=id_n).exists():
            messages.error(request, 'Este Email já foi cadastrado')
            return redirect('lista_usuarios')
        else:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, 'Os dados do usuário foram atualizados')
            return redirect('lista_usuarios')
    return redirect('lista_usuarios')
