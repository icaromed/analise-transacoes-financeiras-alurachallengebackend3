from django.test import TestCase, RequestFactory


class TransacoesDeslogadoURLSTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
