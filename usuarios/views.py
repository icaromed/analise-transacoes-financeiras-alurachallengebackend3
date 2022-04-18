from django.shortcuts import render, redirect
import random
import smtplib
from django.contrib import messages
from django.contrib.auth.models import User

def cadastro(request):
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
        return redirect('login')


def dashboard(request):
    pass


def login(request):
    return render(request, 'usuarios/login.html')


def logout(request):
    pass


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
