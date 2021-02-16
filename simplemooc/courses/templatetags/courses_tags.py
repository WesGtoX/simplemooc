from django.template import Library
from simplemooc.courses.models import Enrollment

# Objeto chamado register que é uma biblioteca.
register = Library()


# 'decorator', 'inclusion_tag' converte a função 'my_course'
# em uma tag de fato que pode ser usado com o Django.
@register.inclusion_tag('courses/templatetags/my_courses.html')
def my_courses(user):
    """
    Função que dado um usuário, pega as inscrições desse usuário
    e coloca em um dicionário, depois retorna o dicionário.

    Retorna as inscrições do usúário.
    """
    enrollments = Enrollment.objects.filter(user=user)
    context = {'enrollments': enrollments}
    return context


# No Django 2.0, 'assignment_tag' foi removido.
# Agora basta ser uma 'simple_tag' normal e o "as" funciona.
@register.simple_tag
def load_my_courses(user):
    return Enrollment.objects.filter(user=user)
