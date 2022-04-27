from apps.usuarios.models import User
from django.contrib import auth


def email_erro(email,):
    if User.objects.filter(email=email).exists():
        return False
    return True


def get_user(email, senha, request):
    username = User.objects.filter(email=email).values_list('username', flat=True).get()
    return auth.authenticate(request, username=username, password=senha)