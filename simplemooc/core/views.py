from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return render(request, 'home.html')
	# 1º parâmetro é o 'request'
	# 2º parâmetro 'home.html', é o nome do template
	# 3º parâmetro passei um dicionário que são as variaveis que ficaram disponiveis no template.

def contact(request):
	return render(request, 'contact.html')