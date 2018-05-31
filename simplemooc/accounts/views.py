from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import RegisterForm

@login_required		# essa função é chamada passando como primeiro parametro, a função que vai ser executada, virifica se o usuário está logado, se estiver ok, se não estiver ele faz um redirect para a página de login, colocando um parêmetro na url o 'next'.
def dashboard(request):
	template_name = 'accounts/dashboard.html'
	return render(request, template_name)

def register(request):
	template_name = 'accounts/register.html'
	if request.method == 'POST':	# verifica se o method é 'post'...
		form = RegisterForm(request.POST)	# ...se for 'psot', vou pegar o formulário...
		if form.is_valid():
			user = form.save()		# ...e salvar o usuário. # 'form.save()' vai retornar o usuário.
			user = authenticate(
				username=user.username,
				password=form.cleaned_data['password1']	# a senha não está em 'user.password', 'user.password' é uma senha criptografada, que é a senha que vai para o banco de dados.
			)
			login(request, user)	# é responsável por logar de fato o usuário, coloca o usuário na sessão.
			return redirect('core:home')	# depois faz o redirect para a 'home'.
	else:
		form = RegisterForm()
	context = {
		'form': form
	}
	return render(request, template_name, context)
