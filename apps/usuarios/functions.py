from decouple import config
import smtplib
from apps.usuarios.models import User
from django.contrib import auth


def erro_email(email):
    """checks for error on a given email"""
    if User.objects.filter(email=email).exists():
        return False
    return True


def get_user(email, senha, request):
    """gets necessary login information and return a user"""
    username = User.objects.filter(email=email).values_list('username', flat=True).get()
    return auth.authenticate(request, username=username, password=senha)


def eviar_email(endereco, senha):
    """sends email to the new user containing the auto-generated password"""
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


def sem_permissao(request):
    """checks for user's permision to access the page"""
    if not request.user.is_authenticated:
        return True
    if request.user.deleted:
        return True


def erro_cadastro(username, email):
    """checks for error on register"""
    if not username.strip():
        return 'O usuário não pode ficar vazio'

    if not email.strip():
        return 'O Email não pode ficar vazio'

    if User.objects.filter(email=email).exists():
        return 'Este Email já foi cadastrado'

    if User.objects.filter(username=username).exists():
        return 'Este Nome de Usuário já foi cadastrado'
    else:
        return False


def erro_remover(id_n, request):
    """checks for error on delete"""
    if int(id_n) == request.user.id:
        return 'Não é possivel excluir o próprio usuário'

    if int(id_n) == User.objects.filter(username="Admin").get().id:
        return 'Não é possivel excluir o usuário padrão'

    else:
        return False


def erro_editar(username, email, user, id_n):
    """checks for error on edit"""
    if not username.strip():
        return 'O usuário não pode ficar vazio'

    if not email.strip():
        return'O Email não pode ficar vazio'

    if username == user.username and email == user.email:
        return 'Os dados do usuário não foram alterados '

    if User.objects.filter(username=username).exclude(id=id_n).exists():
        return 'Este Nome de Usuário já foi cadastrado'

    if User.objects.filter(email=email).exclude(id=id_n).exists():
        return 'Este Email já foi cadastrado'
    else:
        return False
