from django.urls import path
from . import views


urlpatterns = [
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('lista_usuarios', views.lista_usuarios, name='lista_usuarios'),
    path('<id_n>/remover_usuario', views.remover_usuario, name='remover_usuario'),
    path('<id_n>/editar_usuario', views.editar_usuario, name='editar_usuario'),
]