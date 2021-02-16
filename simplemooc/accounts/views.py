from django.shortcuts import render, redirect, get_object_or_404

# from django.conf import settings

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required

# from simplemooc.core.utils import generate_hash_key
# from simplemooc.courses.models import Enrollment

from simplemooc.accounts.forms import RegisterForm, EditAccountForm, PasswordResetForm
from simplemooc.accounts.models import PasswordReset

User = get_user_model()


# Essa função é chamada passando como primeiro parâmetro,
# a função que vai ser executada, verifica se o usuário está logado,
# se estiver ok, se não estiver ele faz um 'redirect' para a página de 'login',
# colocando um parêmetro na 'url' o 'next'.
@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    context = {}
    return render(request, template_name, context)


def register(request):
    template_name = 'accounts/register.html'
    # Verifica se o método é 'post'...
    if request.method == 'POST':
        # ...se for 'post', vou pegar o formulário...
        form = RegisterForm(request.POST)

        if form.is_valid():
            # ...e salvar o usuário. # 'form.save()' vai retornar o usuário.
            user = form.save()

            # A senha não está em 'user.password', 'user.password' é uma senha
            # 'criptografada', que é a senha que vai para o banco de dados.
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])

            # É responsável por logar de fato o usuário, coloca o usuário na sessão.
            login(request, user)

            # Depois faz o 'redirect' para a 'home'.
            return redirect('core:home')
    else:
        form = RegisterForm()

    context = {'form': form}

    return render(request, template_name, context)


def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context = {}

    # Forma mais prática para que os dados não sejam validados, quando for 'POST'
    # de fato ele vai validar os dados, e quando não for, não vai ser validado.
    form = PasswordResetForm(request.POST or None)

    base_domain = request.build_absolute_uri('/')[:-1]

    if form.is_valid():
        form.save(base_domain)
        # Exibe a mensagem de erro.
        context['success'] = True

    context['form'] = form
    return render(request, template_name, context)


def password_reset_confirm(request, key):
    """
    Pega a chave que está na 'url', busca o 'model', deu tudo ok, passou, não deu 'erro 404'...
    """
    template_name = 'accounts/password_reset_confirm.html'
    context = {}

    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)

    if form.is_valid():
        form.save()
        context['success'] = True

    context['form'] = form
    return render(request, template_name, context)


@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    # Dicionário.
    context = {}

    # Verifica se o método é 'POST'.
    if request.method == 'POST':
        # Se for 'POST' chama o 'EditAccountForm', passando o 'POST' que são os dados.
        # 'instance' é a instância que está sendo alterada, o 'model',
        # que é o 'request.user', usuário atual da sessão.
        form = EditAccountForm(request.POST, instance=request.user)
        # Se o 'form' estiver válido...
        if form.is_valid():
            # ...ele salva.
            form.save()
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso')
            return redirect('accounts:dashboard')
            # # Cria novamente um usuário vazio.
            # form = EditAccountForm(instance=request.user)
            # # E faz uma variável de 'sucesso', para apenas no template jogar um 'if' e jogar uma mensagem lá.
            # context['success'] = True
    else:
        # Se não for 'POST', é apenas um formulário vazio.
        form = EditAccountForm(instance=request.user)

    # Renderiza apenas o template com esse formulário
    context['form'] = form
    return render(request, template_name, context)


@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}

    if request.method == 'POST':
        # Foi passado parâmetros nomeados porque esse 'form' é um pouco customizado,
        form = PasswordChangeForm(data=request.POST, user=request.user)

        # Então além dos parâmetros normais de um 'form' qualquer, ele recebe esse
        # parêmetro 'user', e como não sei qual a ordem deles, então passa nomeado.
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)

    context['form'] = form
    return render(request, template_name, context)
