from django.db import models
from django.conf import settings
from django.utils import timezone

from simplemooc.core.mail import send_mail_template


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
		upload_to='courses/images', verbose_name='Imagem', 
		null=True, blank=True
	)

	created_at = models.DateTimeField('Criado em', auto_now_add=True) 		# Data e hora. auto_now_add significa que toda vez que criar o curso, automaticamente será colocado essa variavel.
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)		# auto_now siginifica que toda vez que ele for salvo, a variavel será alterada para a data atual.

	objects = CourseManager()	# reescreve o atributo 'objects', o .objects não é mais o manager padrão do Django agora.

	def __str__(self):		# mostra os nomes dos cursos na página 'admin'.
		return self.name

	@models.permalink	# pega a tupla e usa uma função chamada reverse que está no pacote: "from django.core.urlresolvers import reverse", é uma forma de resgatar a url dado um nome. E com isso ele retonar a url.
	def get_absolute_url(self):		# metodo que retorna uma tupla
		return ('courses:details', (), {'slug': self.slug})
				# 1º parâmetro: url
				# 2º parâmetro: argumentos não nomeaveis (não estamos utilizando)
				# 3º parâmetro: argumentos nomeaveis que é um dicionário (estamos utilizando)

	def release_lessons(self):		# método que retorna todas as aulas disponíveis desse curso.
		today = timezone.now().date()
		return self.lessons.filter(release_date__lte=today)		# '__gte' slow caps da queryset, maior ou igual. '__lte' slow caps da queryset, menor ou igual.

	class Meta:		# uma versão mais bonita de falar essa classe.
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['name']


class Lesson(models.Model):

	name = models.CharField('Nome', max_length=100)		# nome da aula.
	description = models.TextField('Descrição', blank=True)		# descrição não obrigatória.
	number = models.IntegerField('Número (ordem)', blank=True, default=0)		# número apenas para ordenação das aulas.
	release_date = models.DateField('Data de Liberação', blank=True, null=True)		# data para liberação da aula. Padrão sem data, nulo.

	course = models.ForeignKey(		# ligação da aula com o curso. Lembrando que sempre que não se coloca o 'related_name', o Django vai criar o nome do 'model_setting'.
		Course, verbose_name='Curso', 
		related_name='lessons',
		on_delete = models.CASCADE		# 'on_delete' é obrigatório no Django 2.0
	)

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	def __str__(self):
		return self.name

	def is_available(self):		# diz se a aula está disponível ou não.
		if self.release_date:
			today = timezone.now().date()
			return self.release_date >= today
		return False

	class Meta:
		verbose_name = 'Aula'
		verbose_name_plural = 'Aulas'
		ordering = ['number']


class Material(models.Model):	# conteúdo da aula, vai ter uma relação com a aula e ela vai ter vários materiais.

	name = models.CharField('Nome', max_length=100)		# nome do material.
	embedded = models.TextField('Vídeo embedded', blank=True)		# campo de texto para que seja adicionado vídos do YouTube, Vimeo, etc. Será o principal material da aula.
	file = models.FileField(upload_to='lessons/materials', blank=True, null=True)		# arquivo de materiais, pdf, documento, etc.

	lesson = models.ForeignKey(		# ligação dos materiais com as aulas.
		Lesson, verbose_name='Aula', 
		related_name='materials',
		on_delete = models.CASCADE		# 'on_delete' é obrigatório no Django 2.0
	)

	def is_embedded(self):
		return bool(self.embedded)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Material'
		verbose_name_plural = 'Materiais'


class Enrollment(models.Model):

	STATUS_CHOICES = (	# seria uma tupla de tuplas, porque é a tupla nº de opções e para cada opção ele vai ter um valor que corresponde ao título. A outra será um texto qualquer que será exibido no lugar do número.
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	)

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, verbose_name='Usuário',
		related_name='enrollments',		# é um atributo que será criado no usuário, que é o model que está sendo realizado a ForeignKey para fazer uma buscar no model filho, faz a relação com esse usuário.
		on_delete = models.CASCADE		# 'on_delete' é obrigatório no Django 2.0
	)
	course = models.ForeignKey(		# indica a situação do usuário no curso.
		Course, verbose_name='Curso', 
		related_name='enrollments',
		on_delete = models.CASCADE		# 'on_delete' é obrigatório no Django 2.0
	)
	status = models.IntegerField(
		'Situação', choices=STATUS_CHOICES, default=1, blank=True
	)

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	def active(self):	# conhecido como 'FatModel', deixa o model um pouco mais gordo, mas a informação do model no model, ao invés de ficar fazendo lógica de negócio nas views, que tem que ser o mais enxuta possível.
		self.status = 1
		self.save()

	def is_approved(self):
		return self.status == 1

	class Meta:
		verbose_name = 'Inscrição'
		verbose_name_plural = 'Inscrições'
		unique_together = (('user', 'course'),)	# essa opão é uma tupla de tupla também, para cada tupla, ele deve indicar dois ou mais campos. É para evitar repetição de inscrição.


class Announcement(models.Model):

	course = models.ForeignKey(
		Course, verbose_name='Curso',
		related_name='announcements',		# dentro do curso vai ter um atributo chamado 'announcements' que vai estar os anúncios relacionados a ele.
		on_delete = models.CASCADE
	)
	title = models.CharField('Título', max_length=100)
	content = models.TextField('Conteúdo')

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Anúncio'
		verbose_name_plural = 'Anúncios'
		ordering = ['-created_at']	# ordena a listagem de curso decrescente, sempre o mais atual sera exibido primeiro.


class Comment(models.Model):

	announcement = models.ForeignKey(		# uma determinada instancia de anúncio vai ter uma ação chamada 'comments' que irá trazer os seus comentários.
		Announcement, verbose_name='Anúncio', 
		related_name='comments', 
		on_delete = models.CASCADE
	)
	user = models.ForeignKey(		# usuário que comentou.
		settings.AUTH_USER_MODEL, 
		verbose_name='usuário', 
		on_delete = models.CASCADE
	)	
	comment = models.TextField('Comentário')

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	class Meta:
		verbose_name = 'Comentário'
		verbose_name_plural = 'Comentários'
		ordering = ['created_at']	# ordenado de forma crescente.


def post_save_announcement(instance, created, **kwargs):
	if created:
		subject = instance.title	# vai ser o título.
		context = {
			'announcement': instance
		}
		template_name = 'courses/announcement_mail.html'
		enrollments = Enrollment.objects.filter(		# será enviado e-mail para todos que estiverem com inscrição, 'status' = 1.
			course=instance.course, status=1
		)
		for enrollment in enrollments:		# para cada usuário inscrito no curso, será enviado um e-mail para ele.
			recipient_list = [enrollment.user.email]
			send_mail_template(subject, template_name, context, recipient_list)

models.signals.post_save.connect(		# indica que a função deve ser executada naquele 'post_save', naquele signal que o Django nos fornece para o model.
	post_save_announcement, 	# função que vai ser executada.
	sender=Announcement, 		# quem é que vai enviar ele.
	dispatch_uid='post_save_announcement'	# verifica se a função já está cadastrada nesse sinal.
)