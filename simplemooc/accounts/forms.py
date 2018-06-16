from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()		# indica que estamos usando o user que o Django reconhece como usuário do sistema que no nosso caso é o 'CustomUser'

class PasswordResetForm(forms.Form):		# não vai ser um 'ModelForm' porque ele vai estar associado a nenhum model, inicialmente. Porque só queremos um campo de e-mail.

	email = forms.EmailField(label='E-mail')

	def clean_email(self):		# para validar se o email é de algum usuário do sistema.
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():		# retorna um boleano.
			return email	# todo 'clean_...' retorna o valor que o formulátio vai pegar no final.
		raise forms.ValidationError(
			'Nenhum usuário encontrado com este e-mail'
		)

class RegisterForm(forms.ModelForm):
	
	password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
	password2 = forms.CharField(
		label='Confirmação de Senha', widget=forms.PasswordInput
	)

	def clean_password2(self):		# esse método vai ser para a senha 2.
		password1 = self.cleaned_data.get("password1")		# pega a senha 1...
		password2 = self.cleaned_data.get("password2")		# ...pega a senha 2...
		if password1 and password2 and password1 != password2:		# ...verifica se foram enviadas, e depois se são iguais.
			raise forms.ValidationError('A confirmação de senha não está correta')		# se elas não forem iguais mostra uma mensagem de erro.
		return password2

	def save(self, commit=True):	# novo metodo 'save' que substitui o do 'UserCreationForm'. Ele recebe o commite igual a 'True', chama o save do meu 'super' que no caso é 'UserCreationForm'.
		user = super(RegisterForm, self).save(commit=False)		# No 'UserCreationForm' ele chama o 'save' do 'ModelForm' através do super. Chama o 'save' passa o 'commit=False' para não salvar, vai pegar usuário, vai setar a senha. Como também foi passado 'commit=False', ele não vai salvar o usuário, ele vai retornar o usuário.
		user.set_password(self.cleaned_data['password1'])		# seta a senha...
		if commit:		# da uma possibilidade de se quiser herdar e fazer outro registerForm, pode chamar parte desse commit e não salvar na hora, posso querer alterar alguma coisa do usuário antes de salvar.
			user.save()
		return user		# o padrão de 'ModelForm' é sempre o save retornar a instancia do objeto relacionado.

	class Meta:
		model = User
		fields = ['username', 'email']		# no formulário de registro vai precisar apenas do 'username' e 'email'.

class EditAccountForm(forms.ModelForm):
	
	class Meta:
		model = User 	# para saber qual model que o formulário vai precisar...
		fields = ['username', 'email', 'name']	# campos modificados para os que criamos.
