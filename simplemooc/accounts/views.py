from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm, SetPasswordForm)
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings

from simplemooc.core.utils import generate_hash_key

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset

User = get_user_model()

@login_required		# essa função é chamada passando como primeiro parametro, a função que vai ser executada, verifica se o usuário está logado, se estiver ok, se não estiver ele faz um redirect para a página de login, colocando um parêmetro na url o 'next'.
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
				username=user.username, password=form.cleaned_data['password1']	# a senha não está em 'user.password', 'user.password' é uma senha criptografada, que é a senha que vai para o banco de dados.
			)
			login(request, user)	# é responsável por logar de fato o usuário, coloca o usuário na sessão.
			return redirect('core:home')	# depois faz o redirect para a 'home'.
	else:
		form = RegisterForm()
	context = {
		'form': form
	}
	return render(request, template_name, context)

def password_reset(request):
	template_name = 'accounts/password_reset.html'
	context = {}
	form = PasswordResetForm(request.POST or None)		# forma mais pratica para que os dados não sejam validados, quando for 'POST' de fato ele vai validar os dados, e quando não for, não vai ser validado.
	print(request.POST)
	if form.is_valid():
		form.save()
		context['success'] = True	# exibe a mensagem de erro.
	context['form'] = form
	return render(request, template_name, context)

def password_reset_confirm(request, key):	# pega a chave que está na url, busca o model, deu tudo ok, passou, não deu erro 404...
	template_name = 'accounts/password_reset_confirm.html'
	context = {}
	reset = get_object_or_404(PasswordReset, key=key)
	form = SetPasswordForm(user=reset.user, data=request.POST or None)	# 
	if form.is_valid():
		form.save()
		context['success'] = True
	context['form'] = form
	return render(request, template_name, context)

@login_required
def edit(request):
	template_name = 'accounts/edit.html'
	context = {}	# dicionario
	if request.method == 'POST':	# verifica se o methodo é 'POST'
		form = EditAccountForm(request.POST, instance=request.user)		# se for 'POST' chama o 'EditAccountForm', passando o 'POST' que são os dados. 'instance' é a instancia que está sendo alterada, o model, que é o 'request.user', usuário atual da sessão.
		if form.is_valid():		# se o form estiver válido...
			form.save()		# ...ele salva.
			form = EditAccountForm(instance=request.user)	# cria novamente um usuário vazio.
			context['success'] = True	# e faz uma variável de 'sucesso', para apenas no template jogar um if e jogar uma mensagem lá.
	else:	# se não for 'POST'...
		form = EditAccountForm(instance=request.user)	# ...é apenas um formulário vazio.
	context['form'] = form 	# renderiza apenas o template com esse formulário
	return render(request, template_name, context)

@login_required
def edit_password(request):
	template_name = 'accounts/edit_password.html'
	context = {}
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)		# Foi passado parâmetros nomeados porque esse 'form' é um pouco customizado, 
		if form.is_valid():													# então além dos parâmetros normais de um form qualquer, ele recebe esse parêmetro 'user', e como não sei qual a ordem deles, então passa nomeado.
			form.save()
			context['success'] = True
	else:
		form = PasswordChangeForm(user=request.user)
	context['form'] = form
	return render(request, template_name, context)
