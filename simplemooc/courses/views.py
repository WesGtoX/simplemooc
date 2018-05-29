from django.shortcuts import render, get_object_or_404

from .models import Course
from .forms import ContactCourse

def index(request):
	courses = Course.objects.all()		# retorna todos o objetos cadastrados no bando de dados.
	template_name = 'courses/index.html'
	context = {		# dicionario passado no final.
		'courses': courses
	}

	return render(request, template_name, context)

#def details(request,pk):
#	course = get_object_or_404(Course, pk=pk)		# retorna a página do curso 'pk', é o númeroda página referente ao id do curso do banco de dados. Caso não for encontrada, retorna uma página 404
#	context = {
#		'course': course
#	}
#	template_name = 'courses/details.html'
#	return render(request, template_name, context)

def details(request,slug):
	course = get_object_or_404(Course, slug=slug)		# ao invés de passar o 'id', passa o 'slug'
	context = {}
	if request.method == 'POST':	# verifica se o metodo é um 'post' ou se é um metodo 'get'.
		form = ContactCourse(request.POST)		# se for 'post', ele recebe o dicionário com todos os campos submetido pelo usuário.
		if form.is_valid():
			context['is_valid'] = True 		# se enviaro formulário com sucesso...
			form.send_mail(course)
			form = ContactCourse()		# limpa o formulário
	else:	# caso contrário
		form = ContactCourse()		# Ok
	context['form'] = form		# variavel form		
	context['course'] = course
	template_name = 'courses/details.html'
	return render(request, template_name, context)