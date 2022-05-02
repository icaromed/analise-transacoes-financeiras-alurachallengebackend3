from apps.usuarios.models import User
from .functions import get_user


def email_existe(email, error_list):
    """checks for the existence of email in database"""
    if not User.objects.filter(email=email).exists():
        error_list['email'] = 'Email não cadastrado'
    return error_list


def usuario_invalido(email, senha, request):
    """checks for the validation of user"""
    return get_user(email, senha, request)

