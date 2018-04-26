from django.db import models

class Course(models.Model):

	name = models.CharField('Nome', max_length=100)
	slug = models.SlugField('Atalho')
	descrição = models.TextField('Descrição', blank=True)
	start_date = models.DateField(
		'Data de Início', null=True, blank=True
	)
	image = models.ImageField(
		upload_to='courses/images', verbose_name='Imagem'
	)

	created_at = models.DateTimeField(
		'Criado em', auto_now_add=True
	)
	update_at = models.DateTimeField('Atualizado em', auto_now=True)