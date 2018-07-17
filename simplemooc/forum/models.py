from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager


class Thread(models.Model):		# justamento o tópico do fórum.
	
	title = models.CharField('Título', max_length=100)		# título do tópico.
	slug = models.SlugField('Identificador', max_length=100, unique=True)		# 'SlugField' por padrão cria com um index no banco de dados para indexar. A tendência é que seja único, mas ele não especifíca que tem que ser.
	body = models.TextField('Mensagem')		# corpo da mensagem.
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL, 		# tem que ser colocado dessa forma para que o Django fique compátivel, caso eu altere um modelo que é o usuário.
		verbose_name='Autor', 
		related_name='threads',			# a partir do momento que o tópico tem uma referência para o 'autor', o 'related_name' vai ser uma referência no 'autor' para todos os tópicos que ele criou, ou seja o Django vai criar um atributo dinâmico do usuário, chamado 'threads', e quando acessado a partir de uma isntância de um usuário, ele vai referênciar todos os tópicos criados pelo 'usuário'.
		on_delete = models.CASCADE		# 'on_delete' é obrigatório no Django 2.0
	)
	views = models.IntegerField('Visualizações', blank=True, default=0)		# forma de contabilizar as visualizações.
	answers = models.IntegerField('Respostas', blank=True, default=0)		# facilita na hora de ordenar os tópicos.

	tags = TaggableManager()

	created = models.DateTimeField('Criado em', auto_now_add=True)		# 'auto_now_add' pega a data que criou.
	modified = models.DateTimeField('Modificado em', auto_now=True)		# 'auto_now' pega a data que alterou.

	def __str__(self):
		return self.title

	@models.permalink	# pega a tupla e usa uma função chamada reverse que está no pacote: "from django.core.urlresolvers import reverse", é uma forma de resgatar a url dado um nome. E com isso ele retonar a url.
	def get_absolute_url(self):		# metodo que retorna uma tupla
		return ('forum:thread',(), {'slug': self.slug})		# quando usa esse decorator, não precisa indicar o caminho da 'url'. Só precisa indicar uma tupla de três valores: 1º é o nome da 'url', 2º os parâmetros posicionais e o 3º é um dicionário com os parâmetros nomeados.


	class Meta:
		verbose_name = 'Tópico'
		verbose_name_plural = 'Tópicos'
		ordering = ['-modified']


class Reply(models.Model):

	thread = models.ForeignKey(
		Thread, verbose_name='Tópico', 
		related_name='replies',
		on_delete = models.CASCADE		# 'on_delete' é obrigatório no Django 2.0
	)
	reply = models.TextField('Resposta', max_length=500)		# título do tópico.
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL, 		# tem que ser colocado dessa forma para que o Django fique compátivel, caso eu altere um modelo que é o usuário.
		verbose_name='Autor', 
		related_name='replies',
		on_delete = models.CASCADE		# 'on_delete' é obrigatório no Django 2.0
	)
	correct = models.BooleanField('Correta?', blank=True, default=False)

	created = models.DateTimeField('Criado em', auto_now_add=True)		# 'auto_now_add' pega a data que criou.
	modified = models.DateTimeField('Modificado em', auto_now=True)		# 'auto_now' pega a data que alterou.

	def __str__(self):
		return self.reply[:100]		# retorna as 100 primeiras letras.


	class Meta:
		verbose_name = 'Resposta'
		verbose_name_plural = 'Respostas'
		ordering = ['-correct', 'created']		# o valor booleano 'True' é maior que o 'False', então tem que ser ordenado de forma decrescente. E os outos ordena pela data.
