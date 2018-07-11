from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from model_mommy import mommy

from simplemooc.courses.models import Course


class CourseManagerTestCase(TestCase):

	def setUp(self):
		self.courses_django = mommy.make(		
			'courses.Course', 
			name='Python na Web com Django', 	# quando faz o 'make' ele pega os campos e coloca valores aleatórios. então pode setar o "name=''".
			_quantity=5	# '_quantity' é um parâmetro de quantidade, ao invés de repetir a mesma linha, para criar varios, é só usar o '_quantity=qtd'. Quando faz o '_quantity' desses, ele vai retornar não um 'model', e sim uma 'queryset', alista lá de 'models'.
		)
		self.courses_dev = mommy.make(		
			'courses.Course', 
			name='Python para Devs',
			_quantity=10
		)
		self.client = Client()

	def tearDown(self):
		Course.objects.all().delete()

	def test_course_search(self):
		search = Course.objects.search('django')
		self.assertEqual(len(search), 5)		# o 'len()' desse 'search' vai ter que ser a quantidade definida, porque todos vão ter o 'Django' de 'Python na Web com Django'.
		search = Course.objects.search('python')
		self.assertEqual(len(search), 15)
