from django.db import models


class CourseManager(models.Manager):
	def search(self, query):	# para fazer filtro no banco de dados
		return self.get_queryset().filter(		# busca um objeto do tipo 'queryset' no banco de dados, que fornece os registros do banco de dados
			models.Q(name__icontains=query) | \
			models.Q(description__icontains=query)	# faz busca no nome e na descrição
		)


class Course(models.Model):

	name = models.CharField('Nome', max_length=100)		# campo do tipo texto precisa de um atributo para determinar tamanho de caracteres
	slug = models.SlugField('Atalho')		# valor unico para este curso, unico por tabela, para utilização de url
	description = models.TextField('Descrição', blank=True)		# um campo de CharField sem tamanho máximo, blank... diz que o campo não é obrigatório
	start_date = models.DateField(
		'Data de Início', null=True, blank=True
	)		# nesse caso no blan também não é obrigatório, mas o valor null define que a nivel de banco de dados ele recebe valor nulo
	image = models.ImageField(
		upload_to='course/images', verbose_name='Imagem', 
		null=True, blank=True
	)

	created_at = models.DateTimeField(
		'Criado em', auto_now_add=True
	)		# Data e hora. auto_now_add significa que toda vez que criar o curso, automaticamente será colocado essa variavel.
	update_at = models.DateTimeField('Atualizado em', auto_now=True)		# auto_now siginifica que toda vez que ele for salvo, a variavel será alterada para a data atual

	objects = CourseManager()	# reescreve o atributo 'objects', o .objects não é mais o manager padrão do Django agora

	def __str__(self):		# mostra os nomes dos cursos na página 'admin'
		return self.name

	class Meta:		# uma versão mais bonita de falar essa classe
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['name']