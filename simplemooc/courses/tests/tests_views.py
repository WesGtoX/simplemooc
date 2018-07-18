from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from simplemooc.courses.models import Course


class ContactCourseTestCase(TestCase):		# toda vez que inicializar a classe 'ContactCourseTestCase', eu executo o 'setUpClass', e para cada teste que vou executar, eu executo o 'setUp' e o 'tearDown'. depois que terminar todos os testes, eu vou executar o 'tearDownClass'.

	def setUp(self):	# método.
		self.course = Course.objects.create(name='Django', slug='django')		# toda vez que for executar um teste, vai criar um curso. 

	def tearDown(self):
		self.course.delete()		# depois o curso vai ser apagado.

	def test_contact_form_error(self):		# formulário de teste criado quando ouver erro. Vou submeter o formulário e quero que ele de erro. Para isso tem um atalho em Django que é o 'assertFormError'.
		data = {'name': 'Fulano de Tal', 'email': '', 'message': ''}	# dados que é um dicionário. Esses dados são o 'name', 'email' e 'message' da 'class ContactCourse()' do 'forms.py'.
		client = Client()	# criei um cliente.
		path = reverse('courses:details', args=[self.course.slug])		# path usa a função 'reverse' só que ele tem um argumento a mais que é o 'slug' do curso, porque a 'url' 'details' precisa do 'slug' do curso.
		response = client.post(path, data)
		self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')	# testa se deu erro, esse campo tem que dar erro.
		self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')	# em 'Este campo é obrigatório.' pode ser uma lista ou um erro específico. Porque o formulário pode ter uma lista de erros.

	def test_contact_form_success(self):	# a ideia é funcionar corretamente. e o 'post' vai ser enviado.
		data = {'name': 'Fulano de Tal', 'email': 'admin@admin.com', 'message': 'Oi'}
		client = Client()
		path = reverse('courses:details', args=[self.course.slug])
		response = client.post(path, data)		# Quando o 'post' é enviado, não criamos nada, apenas envia um e-mail pelo 'send_mail'.
		self.assertEqual(len(mail.outbox), 1)	# no Django tem como testar se o e-mail foi enviado. Com o 'assertEqual' que pega o 'mail.outbox', faz o 'len()' dele que tem que ser igual a um email. No ambiente de testes, os e-mail ficam no 'outbox'.
		self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])	# teste para quem foi o email. Se foi para 'settings.CONTACT_EMAIL' que é uma lista.
