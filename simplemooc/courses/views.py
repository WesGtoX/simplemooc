from django.shortcuts import render

from .models import Course

def index(request):
	courses = Course.objects.all()		# retorna todos o objetos cadastrados no bando de dados.
	template_name = 'courses/index.html'
	context = {		# dicionario passado no final.
		'courses': courses
	}

	return render(request, template_name, context)

def details(request,pk):
	course = Course.objects.get(pk=pk)		# retorna a página do curso 'pk', é o númeroda página referente ao id do curso do banco de dados.
	context = {
		'course': course
	}
	template_name = 'courses/details.html'

	return render(request, template_name, context)