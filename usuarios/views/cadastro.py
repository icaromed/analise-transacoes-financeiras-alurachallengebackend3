from django.shortcuts import render, redirect
from django.contrib import messages
from usuarios.models import User
import smtplib
import random
from decouple import config


def cadastro(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.deleted:
        return redirect('login')

    if request.method == "GET":
        return render(request, 'usuarios/cadastro.html')

    elif request.method == "POST":
        email = request.POST['email']
        username = request.POST['usuario']
        senha = str(random.random())[2:8]

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
        if eviar_email(email, senha):
            user.save()
        else:
            messages.error(request, 'O Email contendo a senha não pôde ser enviado')
            return redirect('cadastro')
        return redirect('lista_usuarios')


def eviar_email(endereco, senha):
    gmail_user = config('gmail_user')
    gmail_password = config('gmail_password')

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
        return True
    except Exception as ex:
        print("Something went wrong….", ex)
        return False