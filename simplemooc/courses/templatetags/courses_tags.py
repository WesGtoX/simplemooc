from django.template import Library

register = Library()	# objeto chamado register que é uma biblioteca.

from simplemooc.courses.models import Enrollment

@register.inclusion_tag('courses/templatetags/my_courses.html')	# 'decorator', 'inclusion_tag' converte a função 'my_course' em uma tag de fato que pode ser usado com o Django.
def my_courses(user):	# função que dado um usuário, pega as inscrições desse usuário e coloca em um dicionário, depois retorna o dicionário.
	enrollments = Enrollment.objects.filter(user=user)	# retorna as inscrições do usúário.
	context = {
		'enrollments': enrollments
	}
	return context

@register.simple_tag	# No Django 2.0, 'assignment_tag' foi removido. Agora basta ser uma 'simple_tag' normal e o "as" funciona.
def load_my_courses(user):
	return Enrollment.objects.filter(user=user)