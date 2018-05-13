from django.db import models

class Course(models.Model):

	name = models.CharField('Nome', max_length=100) # campo do tipo texto precisa de um atributo para determinar tamanho de caracteres
	slug = models.SlugField('Atalho')	# valor unico para este curso, para utilização de url
	description = models.TextField('Descrição', blank=True) # um campo de CharField sem tamanho máximo, blank... diz que o campo não é obrigatório
	start_date = models.DateField(
		'Data de Início', null=True, blank=True
	) # nesse caso no blan também não é obrigatório, mas o valor null define que a nivel de banco de dados ele recebe valor nulo
	image = models.ImageField(upload_to='course/images', verbose_name='Imagem')

	created_at = models.DateTimeField('Criado em', auto_now_add=True) # Data e hora. auto_now_add significa que toda vez que criar o curso, automaticamente será colocado essa variavel.
	update_at = models.DateTimeField('Atualizado em', auto_now=True) # auto_now siginifica que toda vez que ele for salvo, a variavel será alterada para a data atual
	