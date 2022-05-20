from django.test import LiveServerTestCase
from selenium import webdriver
from decouple import config
import time
from apps.usuarios.models import User


class ServerTestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=config('selenium_browser'))
        self.user = User.objects.create_user('Admin', 'admin@email.com.br', '123999')

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        """acessa o endereço do site e faz o login, usando as credenciais
        padrão de Admin"""

        self.browser.get(url=self.live_server_url)
        titulo = self.browser.find_element(by='css selector', value='h2')
        self.assertEqual('Login', titulo.text)

        input_email = self.browser.find_element(value='id_email')
        input_senha = self.browser.find_element(value='id_senha')
        self.assertEqual(input_email.get_attribute('placeholder'), '')
        self.assertEqual(input_senha.get_attribute('placeholder'), '')

        input_email.send_keys('admin@email.com.br')
        input_senha.send_keys(123999)
        self.browser.find_element(value='submit_button').click()

        titulo = self.browser.find_element(by='css selector', value='h2')
        self.assertEqual('Importar Transações', titulo.text)
