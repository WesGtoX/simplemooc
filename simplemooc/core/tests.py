from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

class HomeViweTest(TestCase):		# teste da app 'core'.
	
	def test_home_status_code(self):
		client = Client()		# inicializa o cliente.
		response = client.get(reverse('core:home'))		# pega a resposta dele para um 'GET' nessa página.
		self.assertEqual(response.status_code, 200)		# 'assertEqual' assert's do 'TestCase'.

	def test_home_template_used(self):
		client = Client()
		response = client.get(reverse('core:home'))
		self.assertTemplateUsed(response, 'home.html')	# 'assertTemplateUsed' mostra templates que são usados.
		self.assertTemplateUsed(response, 'base.html')