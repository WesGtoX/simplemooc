from django.test import TestCase
from django.test.client import Client

from model_mommy import mommy

from simplemooc.courses.models import Course


class CourseManagerTestCase(TestCase):

    def setUp(self):
        # Quando faz o 'make' ele pega os campos e coloca valores aleatórios.
        # Então pode setar o "name=''".
        # '_quantity' é um parâmetro de quantidade, ao invés de repetir a mesma linha,
        # para criar vários, é só usar o '_quantity=qtd'. Quando faz o '_quantity' desses,
        # ele vai retornar não um 'model', e sim uma 'queryset', a lista lá de 'models'.
        self.courses_django = mommy.make('courses.Course', name='Python na Web com Django', _quantity=5)
        self.courses_dev = mommy.make('courses.Course', name='Python para Devs', _quantity=10)
        self.client = Client()

    def tearDown(self):
        Course.objects.all().delete()

    def test_course_search(self):
        search = Course.objects.search('django')
        # O 'len()' desse 'search' vai ter que ser a quantidade definida,
        # porque todos vão ter o "Django" de "Python na Web com Django".
        self.assertEqual(len(search), 5)

        search = Course.objects.search('python')
        self.assertEqual(len(search), 15)
