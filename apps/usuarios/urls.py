from django.urls import path
from .views import *


urlpatterns = [
    path('cadastro', cadastro, name='cadastro'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('lista_usuarios', lista_usuarios, name='lista_usuarios'),
    path('<id_n>/remover_usuario', remover_usuario, name='remover_usuario'),
    path('<id_n>/editar_usuario', editar_usuario, name='editar_usuario'),
]
