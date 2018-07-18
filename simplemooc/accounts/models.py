import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):

	username = models.CharField(		# nome de usuário padrão, que também é único.
		'Nome de Usuário', max_length=30, unique=True,
		validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),	# valida se o nome de usuário recebeu os caracteres permitidos.
			'O nome de usuário só pode conter letras, dígitos ou os '
			'seguintes caracteres: @/./+/-/_', 'invalid')]
	)	
	email = models.EmailField('E-mail', unique=True)	# e-mail que nesse caso é único, é a grande diferença para o do Django.
	name = models.CharField('Nome', max_length=100, blank=True)		# campo do nome completo que vai ser opcional, ao invés de 'first_name' e 'last_name'.
	is_active = models.BooleanField('Está ativo?', blank=True, default=True)	# vai verificar se o usuário está ativo e para logar, por padrão é 'True'.
	is_staff = models.BooleanField('É da equipe?', blank=True, default=False)	# para o Django 'admin' saber se ele pode acessar a área administrativa, se é da equipe administrativa, por padrão é 'False'.
	date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)	# essa data é importante na criação do 'superuser', é uma recomendação para ser compatível com a 'app' Django.

	objects = UserManager()		# o 'manager' que tem algumas coisas úteis para nós.

	USERNAME_FIELD = 'username'		# para ser compátivel com alguns comandos e algumas outras coisas do Django, 'app' de usuário. Indica o campo que é único e vai ser a referência na hora do 'login'. Por padrão é 'login', poderia ser o 'email'.
	REQUIRED_FIELDS = ['email']		# utilizado no comando de criação 'superusuario', vai utilizar esse comando porque vai precisar apagar o banco de dados, e vamos criar outro usuário atráves desse comando.

	def __str__(self):		# esse método é a representação do 'skin' do usuário.
		return self.name or self.username		# se tiver 'name', retorna o nome, caso contrário retorna o 'username'.

	def get_short_name(self):	# a 'app' de usuário de Django também pega as implementações de alguns métodos, não é obrigatório, mas é interessante para funcionamento do 'admin'.
		return self.username 	# descrição curta do nome.

	def get_full_name(self):	# 'fullname'.
		return str(self)	# o 'fullname' é a representação 'string' do próprio objeto.

	class Meta:
		verbose_name = 'Usuário'
		verbose_name_plural = 'Usuários'


class PasswordReset(models.Model):		# esse 'model' tem um relacionamento de 'n' para '1' com o usuário, o usuário pode ter um ou mais 'PasswordReset'.

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, verbose_name='Usuário',
		related_name='resets',
		on_delete = models.CASCADE		# 'on_delete' é obrigatório no Django 2.0.
	)
	key = models.CharField('Chave', max_length=100, unique=True)
	created_at = models.DateTimeField('Criado em', auto_now_add=True)	# vou permitir que esse usuário clique nesse 'link' randômico, em no máximo 2 horas.
	confirmed = models.BooleanField('Confirmado?', default=False, blank=True)	# vai indicar se o 'link' foi usado.
	
	def __str__(self):
		return '{0} em {1}'.format(self.user, self.created_at)

	class Meta:
		verbose_name = 'Nova Senha'
		verbose_name_plural = 'Novas Senhas'
		ordering = ['-created_at']		# parâmetro da classe 'Meta' do 'model' que pode indicar qual o ordenamento, uma lista de atributos do 'model', que servirão para ordenamento padrão, default.
