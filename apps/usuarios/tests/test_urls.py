from django.test import TestCase, RequestFactory
from ..views import *
from django.test.client import Client
from apps.usuarios.models import User


class UsuariosDeslogadosURLSTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('Admin', 'admin@email.com.br', '123999')

    def test_rota_url_redireciona_para_login(self):
        """teste se o usuario deslogado é redirecionado à página de login"""
        paths = ['/usuarios/login', '/usuarios/cadastro', '/usuarios/logout',
                 '/usuarios/lista_usuarios', '/usuarios/01/remover_usuario',
                 '/usuarios/01/editar_usuario', '/', '/detalhar/01', '/suspeitas/']
        for path in paths:
            request = self.factory.get(path)
            with self.assertTemplateUsed('usuarios/login.html'):
                response = login(request)
                self.assertEqual(response.status_code, 200)

    def test_rota_url_cadastro(self):
        admin = Client()
        admin.login(email='admin@email.com.br', password='123999', username='Admin')
        request = admin.get('/usuarios/cadastro')
        self.assertEqual(request.status_code, 200)

