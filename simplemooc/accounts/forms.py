from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from simplemooc.core.mail import send_mail_template
from simplemooc.core.utils import generate_hash_key

from .models import PasswordReset

User = get_user_model()		# indica que estamos usando o 'user' que o Django reconhece como usuário do sistema que no nosso caso é o 'CustomUser'.


class PasswordResetForm(forms.Form):		# não vai ser um 'ModelForm' porque ele não vai estar associado a nenhum model inicialmente. Porque só queremos um campo de e-mail.

	email = forms.EmailField(label='E-mail')

	def clean_email(self):		# para validar se o 'email' é de algum usuário do sistema.
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():		# detectar se existem algum usuário do sistema, retorna um boleano.
			return email	# todo 'clean_...' retorna o valor que o formulátio vai pegar no final.
		raise forms.ValidationError(
			'Nenhum usuário encontrado com este e-mail'
		)

	def save(self):
		user = User.objects.get(email=self.cleaned_data['email'])		# quando for válido, eu busco o usuário com aquele e-mail.
		key = generate_hash_key(user.username)		# gera a chave.
		reset = PasswordReset(key=key, user=user)	# cria o 'model' para resetar a senha.
		reset.save()
		template_name = 'accounts/password_reset_mail.html'
		subject = 'Criar nova senha no Simple MOOC'		# assunto.
		context = {
			'reset': reset,
		}
		send_mail_template(subject, template_name, context, [user.email])		# função criada de envio de 'email' no 'core'.


class RegisterForm(forms.ModelForm):
	
	password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
	password2 = forms.CharField(
		label='Confirmação de Senha', widget=forms.PasswordInput
	)

	def clean_password2(self):		# esse método vai ser para a senha 2.
		password1 = self.cleaned_data.get("password1")		# pega a senha 1...
		password2 = self.cleaned_data.get("password2")		# ...pega a senha 2...
		if password1 and password2 and password1 != password2:		# ...verifica se foram enviadas, e depois se são iguais.
			raise forms.ValidationError('A confirmação não está correta')		# se elas não forem iguais mostra uma mensagem de erro.
		return password2

	def save(self, commit=True):	# novo método 'save' que substitui o do 'UserCreationForm'. Ele recebe o 'commit' igual a 'True', chama o 'save' do meu 'super' que no caso é 'UserCreationForm'.
		user = super(RegisterForm, self).save(commit=False)		# No 'UserCreationForm' ele chama o 'save' do 'ModelForm' através do 'super'. Chama o 'save' passa o 'commit=False' para não salvar, vai pegar usuário, vai setar a senha. Como também foi passado 'commit=False', ele não vai salvar o usuário, ele vai retornar o usuário.
		user.set_password(self.cleaned_data['password1'])		# seta a senha...
		if commit:		# da uma possibilidade de se quiser herdar e fazer outro 'registerForm', pode chamar parte desse 'commit' e não salvar na hora, posso querer alterar alguma coisa do usuário antes de salvar.
			user.save()
		return user		# o padrão de 'ModelForm' é sempre o 'save' retornar a instância do objeto relacionado.

	class Meta:
		model = User
		fields = ['username', 'email']		# no formulário de registro vai precisar apenas do 'username' e 'email'.


class EditAccountForm(forms.ModelForm):
	
	class Meta:
		model = User 	# para saber qual 'model' que o formulário vai precisar...
		fields = ['username', 'email', 'name']	# campos modificados para os que criamos.
