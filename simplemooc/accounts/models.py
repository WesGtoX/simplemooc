import re

from django.db import models
from django.core import validators

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)


class User(AbstractBaseUser, PermissionsMixin):
    # Nome de usuário padrão, que também é único.
    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True,
        # Valida se o nome de usuário recebeu os caracteres permitidos.
        validators=[validators.RegexValidator(
            re.compile('^[\w.@+-]+$'),
            'O nome de usuário só pode conter letras, dígitos ou os seguintes caracteres: @/./+/-/_', 'invalid'
        )]
    )
    # E-mail que nesse caso é único, é a grande diferença para o do Django.
    email = models.EmailField('E-mail', unique=True)
    # Campo do nome completo que vai ser opcional, ao invés de 'first_name' e 'last_name'.
    name = models.CharField('Nome', max_length=100, blank=True)
    # Vai verificar se o usuário está ativo e para logar, por padrão é 'True'.
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    # Para o Django 'admin' saber se ele pode acessar a área administrativa,
    # se é da equipe administrativa, por padrão é 'False'.
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    # Essa data é importante na criação do 'superuser', é uma recomendação para ser compatível com a 'app' Django.
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    # O 'manager' que tem algumas coisas úteis para nós.
    objects = UserManager()

    # Para ser compátivel com alguns comandos e algumas outras coisas do Django, 'app' de usuário.
    # Indica o campo que é único e vai ser a referência na hora do 'login'.
    # Por padrão é 'login', poderia ser o 'email'.
    USERNAME_FIELD = 'username'

    # Utilizado no comando de criação 'superusuario', vai utilizar esse comando porque vai precisar
    # apagar o banco de dados, e vamos criar outro usuário atráves desse comando.
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """
        Esse método é a representação do 'skin' do usuário.

        Se tiver 'name', retorna o nome, caso contrário retorna o 'username'.
        """
        return self.name or self.username

    def get_short_name(self):
        """
        A 'app' de usuário de Django também pega as implementações de alguns métodos,
        não é obrigatório, mas é interessante para funcionamento do 'admin'.

        :self.username: descrição curta do nome.
        """
        return self.username

    def get_full_name(self):
        """
        O 'fullname' é a representação 'string' do próprio objeto.
        """
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PasswordReset(models.Model):
    """
    Esse 'model' tem um relacionamento de 'n' para '1' com o usuário,
    o usuário pode ter um ou mais 'PasswordReset'.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        # 'on_delete' é obrigatório no Django 2.0.
        related_name='resets', on_delete=models.CASCADE
    )
    key = models.CharField('Chave', max_length=100, unique=True)

    # Vou permitir que esse usuário clique nesse 'link' randômico, em no máximo 2 horas.
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    # Vai indicar se o 'link' foi usado.
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        # Parâmetro da classe 'Meta' do 'model' que pode indicar qual o ordenamento,
        # uma lista de atributos do 'model', que servirão para ordenamento padrão, default.
        ordering = ['-created_at']
