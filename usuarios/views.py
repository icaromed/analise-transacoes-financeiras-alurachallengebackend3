from django.shortcuts import render, redirect, get_object_or_404
import random
import smtplib
from django.contrib import messages, auth
from django.contrib.auth.models import User


def cadastro(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "GET":
        return render(request, 'usuarios/cadastro.html')

    elif request.method == "POST":
        email = request.POST['email']
        username = request.POST['usuario']
        senha = str(random.randint(100000, 999999))

        if not username.strip():
            messages.error(request, 'O usuário não pode ficar vazio')
            return redirect('cadastro')
        if not email.strip():
            messages.error(request, 'O Email não pode ficar vazio')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este Email já foi cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este Nome de Usuário já foi cadastrado')
            return redirect('cadastro')

        user = User.objects.create_user(username, email, senha)
        eviar_email(email, senha)
        user.save()
        return redirect('lista_usuarios')


def lista_usuarios(request):
    if not request.user.is_authenticated:
        return redirect('login')
    usuarios_validos = User.objects.exclude(username='Admin')
    if request.method == "GET":
        return render(request, 'usuarios/lista_usuarios.html', {"usuarios_validos": usuarios_validos})
    elif request.method == "POST":

        return render(request, 'usuarios/lista_usuarios.html', {"usuarios_validos": usuarios_validos})


def remover_usuario(request, id_n):
    if not request.user.is_authenticated:
        return redirect('login')

    user = get_object_or_404(User, id=id_n)

    if int(id_n) == request.user.id:
        messages.error(request, 'Não é possivel excluir o próprio usuário')
        return redirect('lista_usuarios')

    if int(id_n) == User.objects.filter(id=2).get().id:
        messages.error(request, 'Não é possivel excluir o usuário padrão')
        return redirect('lista_usuarios')

    if request.method == "POST":
        user.delete()
        return redirect('lista_usuarios')
    return redirect('lista_usuarios')


def editar_usuario(request, id_n):
    if not request.user.is_authenticated:
        return redirect('login')

    user = get_object_or_404(User, id=id_n)

    if request.method == "GET":
        return render(request, 'usuarios/editar_usuario.html', {"user": user})

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        senha = request.POST['senha']
        # Continue aqui
        return redirect('lista_usuarios')


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
            print('Você está logado')
            return redirect('index')
        else:
            messages.error(request, 'Senha incorreta')
            return redirect('login')

def logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    auth.logout(request)
    return redirect('login')


def eviar_email(endereco, senha):
    gmail_user = 'senha.aleatoria.python@gmail.com'
    gmail_password = '123QWER4'

    sent_from = gmail_user
    to = [f'{endereco}']
    subject = 'Envio da senha aleatoria'
    body = f'Aqui esta a sua senha: {senha}'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)

