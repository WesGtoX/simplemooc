from django.db import models
from django.conf import settings


class CourseManager(models.Manager):
	def search(self, query):	# para fazer filtro no banco de dados.
		return self.get_queryset().filter(		# busca um objeto do tipo 'queryset' no banco de dados, que fornece os registros do banco de dados.
			models.Q(name__icontains=query) | \
			models.Q(description__icontains=query)	# faz busca no nome e na descrição.
		)


class Course(models.Model):

	name = models.CharField('Nome', max_length=100)		# campo do tipo texto precisa de um atributo para determinar tamanho de caracteres.
	slug = models.SlugField('Atalho')		# valor unico para este curso, unico por tabela, para utilização de url.
	description = models.TextField('Descrição Simples', blank=True)		# um campo de CharField sem tamanho máximo, blank... diz que o campo não é obrigatório.
	about = models.TextField('Sobre o Curso', blank=True)
	start_date = models.DateField(
		'Data de Início', null=True, blank=True		# nesse caso no blank também não é obrigatório, mas o valor null define que a nivel de banco de dados ele recebe valor nulo.
	)
	image = models.ImageField(
		upload_to='course/images', verbose_name='Imagem', 
		null=True, blank=True
	)

	created_at = models.DateTimeField('Criado em', auto_now_add=True) 		# Data e hora. auto_now_add significa que toda vez que criar o curso, automaticamente será colocado essa variavel.
	update_at = models.DateTimeField('Atualizado em', auto_now=True)		# auto_now siginifica que toda vez que ele for salvo, a variavel será alterada para a data atual.

	objects = CourseManager()	# reescreve o atributo 'objects', o .objects não é mais o manager padrão do Django agora.

	def __str__(self):		# mostra os nomes dos cursos na página 'admin'.
		return self.name

	@models.permalink	# pega a tupla e usa uma função chamada reverse que está no pacote: "from django.core.urlresolvers import reverse", é uma forma de resgatar a url dado um nome. E com isso ele retonar a url.
	def get_absolute_url(self):		# metodo que retorna uma tupla
		return ('courses:details',(), {'slug': self.slug})
				# 1º parâmetro: url
				# 2º parâmetro: argumentos não nomeaveis (não estamos utilizando)
				# 3º parâmetro: argumentos nomeaveis que é um dicionário (estamos utilizando)

	class Meta:		# uma versão mais bonita de falar essa classe.
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['name']

class Enrollment(models.Model):

	STATUS_CHOICES = (	# seria uma tupla de tuplas, porque é a tupla nº de opções e para cada opção ele vai ter um valor que corresponde ao título. A outra será um texto qualquer que será exibido no lugar do número.
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	)

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, verbose_name='Usuário',
		on_delete = models.CASCADE,		# 'on_delete' é obrigatório no Django 2.0
		related_name='enrollments'		# é um atributo que será criado no usuário, que é o model que está sendo realizado a ForeignKey para fazer uma buscar no model filho, faz a relação com esse usuário.
	)
	course = models.ForeignKey(		# indica a situação do usuário no curso.
		Course, verbose_name='Curso', 
		on_delete = models.CASCADE,		# 'on_delete' é obrigatório no Django 2.0
		related_name='enrollments'
	)
	status = models.IntegerField(
		'Situação', choices=STATUS_CHOICES, default='1', blank=True
	)

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	update_at = models.DateTimeField('Atualizado em', auto_now=True)

	def active(self):	# conhecido como 'FatModel', deixa o model um pouco mais gordo, mas a informação do model no model, ao invés de ficar fazendo lógica de negócio nas views, que tem que ser o mais enxuta possível.
		self.status = 1
		self.save()

	def is_approved(self):
		return self.satus == 1

	class Meta:
		verbose_name='Inscrição'
		verbose_name_plural='Inscrições'
		unique_together = (('user', 'course'),)	# essa opão é uma tupla de tupla também, para cada tupla, ele deve indicar dois ou mais campos. É para evitar repetição de inscrição.