from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
	email = forms.EmailField(label='E-mail')

	def clean_email(self):		# serve tanto para uma verificação extra, quanto para fazer uma modificação no valor, se quisesse extrair alguma parte do e-mail, poderia ser adaptado.
		email = self.cleaned_data['email']		# clean_email()	- pega  um e-mail submetido pelo usuário, 
		if User.objects.filter(email=email).exists():	# vai fazer um filtro na queryset de usuário, e vai chamar a função 'exists()' que retorna um bolean.
			raise forms.ValidationError('Já existe usuário com este E-mail')	# se existe vai dar um 'ValidationError()'. Se não existe, vai retornar o valor e o procedimento continua normal.
		return email


	def save(self, commit=True):	# novo metodo 'save' que substitui o do 'UserCreationForm'. Ele recebe o commite igual a 'True', chama o save do meu 'super' que no caso é 'UserCreationForm'.
		user = super(RegisterForm, self).save(commit=False)		# No 'UserCreationForm' ele chama o 'save' do 'ModelForm' através do super. Chama o 'save' passa o 'commit=False' para não salvar, vai pegar usuário, vai setar a senha. Como também foi passado 'commit=False', ele não vai salvar o usuário, ele vai retornar o usuário.
		user.email = self.cleaned_data['email']		# coloca só o 'user.email' e dicionario que contem os valores do form validados e transformados em objetos python.
		if commit:		# da uma possibilidade de se quiser herdar e fazer outro registerForm, pode chamar parte desse commit e não salvar na hora, posso querer alterar alguma coisa do usuário antes de salvar.
			user.save()
		return user		# o padrão de 'ModelForm' é sempre o save retornar a instancia do objeto relacionado.





