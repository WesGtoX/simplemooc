from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


class HomeViweTest(TestCase):
    """
    Teste da app 'core'
    """

    def setUp(self):
        # Inicializa o cliente.
        self.client = Client()

    def test_home_status_code(self):
        # Pega a resposta dele para um 'GET' nessa página.
        response = self.client.get(reverse('core:home'))

        # 'assertEqual' assert's do 'TestCase'.
        self.assertEqual(response.status_code, 200)

    def test_home_template_used(self):
        response = self.client.get(reverse('core:home'))

        # 'assertTemplateUsed' mostra templates que são usados.
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')
