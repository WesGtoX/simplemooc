from django.db import models
from django.conf import settings
from django.utils import timezone

from simplemooc.core.mail import send_mail_template


class CourseManager(models.Manager):

    def search(self, query):
        """
        Para fazer filtro no banco de dados.

        Busca um objeto do tipo 'queryset' no banco de dados, que fornece os registros do banco de dados.

        Faz busca no nome e na descrição.
        """
        return self.get_queryset().filter(models.Q(name__icontains=query) | models.Q(description__icontains=query))


class Course(models.Model):
    # Campo do tipo texto precisa de um atributo para determinar tamanho de caracteres.
    name = models.CharField('Nome', max_length=100)
    # Valor único para este curso, único por tabela, para utilização de 'url'.
    slug = models.SlugField('Atalho')
    # Um campo de 'CharField' sem tamanho máximo, 'blank'... diz que o campo não é obrigatório.
    description = models.TextField('Descrição Simples', blank=True)
    about = models.TextField('Sobre o Curso', blank=True)
    # Nesse caso no 'blank' também não é obrigatório, mas o valor 'null'
    # define que a nível de banco de dados ele recebe valor nulo.
    start_date = models.DateField('Data de Início', null=True, blank=True)
    image = models.ImageField(
        upload_to='courses/images', verbose_name='Imagem',
        null=True, blank=True
    )

    # Data e hora. 'auto_now_add' significa que toda vez que
    # criar o curso, automaticamente será colocado essa variável.
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    # auto_now siginifica que toda vez que ele for salvo,
    # a variavel será alterada para a data atual.
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    # Reescreve o atributo 'objects', o '.objects' não é mais o manager padrão do Django agora.
    objects = CourseManager()

    def __str__(self):
        """
        Mostra os nomes dos cursos na página 'admin'.
        """
        return self.name

    # Pega a 'tupla' e usa uma função chamada 'reverse' que está no
    # pacote: "from django.core.urlresolvers import reverse", é uma forma
    # de resgatar a 'url' dado um nome. E com isso ele retonar a 'url'.
    @models.permalink
    def get_absolute_url(self):
        """
        Método que retorna uma tupla.

        - 1º parâmetro: url
        - 2º parâmetro: argumentos não nomeáveis (não estamos utilizando).
        - 3º parâmetro: argumentos nomeáveis que é um dicionário (estamos utilizando).
        """
        return 'courses:details', (), {'slug': self.slug}

    def release_lessons(self):
        """
        Método que retorna todas as aulas disponíveis desse curso.
        """
        today = timezone.now().date()
        # '__gte' slow caps da queryset, maior ou igual. '__lte' slow caps da queryset, menor ou igual.
        return self.lessons.filter(release_date__lte=today)

    class Meta:  # uma versão mais bonita de falar essa classe.
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']


class Lesson(models.Model):
    # Nome da aula.
    name = models.CharField('Nome', max_length=100)
    # Descrição não obrigatória.
    description = models.TextField('Descrição', blank=True)
    # Número apenas para ordenação das aulas.
    number = models.IntegerField('Número (ordem)', blank=True, default=0)
    # Data para liberação da aula. Padrão sem data, nulo.
    release_date = models.DateField('Data de Liberação', blank=True, null=True)

    # Ligação da aula com o curso. Lembrando que sempre que não se coloca
    # o 'related_name', o Django vai criar o nome do 'model_settings'.
    course = models.ForeignKey(
        Course, verbose_name='Curso',
        related_name='lessons',
        # 'on_delete' é obrigatório no Django 2.0.
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name

    def is_available(self):
        """
        Diz se a aula está disponível ou não.
        """
        if self.release_date:
            today = timezone.now().date()
            return self.release_date <= today

        return False

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class Material(models.Model):
    """
    Conteúdo da aula, vai ter uma relação com a aula e ela vai ter vários materiais.
    """

    # Nome do material.
    name = models.CharField('Nome', max_length=100)

    # Campo de texto para que seja adicionado vídeos do YouTube, Vimeo, etc. Será o principal material da aula.
    embedded = models.TextField('Vídeo embedded', blank=True)

    # Arquivo de materiais, pdf, documento, etc.
    file = models.FileField(upload_to='lessons/materials', blank=True, null=True)

    # Ligação dos materiais com as aulas.
    lesson = models.ForeignKey(
        Lesson, verbose_name='Aula',
        related_name='materials',
        # 'on_delete' é obrigatório no Django 2.0.
        on_delete=models.CASCADE
    )

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'


class Enrollment(models.Model):
    # Seria uma 'tupla' de 'tuplas', porque é a 'tupla' nº de opções e para
    # cada opção ele vai ter um valor que corresponde ao título. A outra será
    # um texto qualquer que será exibido no lugar do número.
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        # É um atributo que será criado no usuário, que é o 'model' que está
        # sendo realizado a 'ForeignKey' para fazer uma buscar no 'model' filho,
        # faz a relação com esse usuário.
        related_name='enrollments',
        # 'on_delete' é obrigatório no Django 2.0.
        on_delete=models.CASCADE
    )

    # Indica a situação do usuário no curso.
    course = models.ForeignKey(
        Course, verbose_name='Curso',
        related_name='enrollments',
        # 'on_delete' é obrigatório no Django 2.0.
        on_delete=models.CASCADE
    )
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=1, blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        """
        Conhecido como 'FatModel', deixa o model um pouco mais gordo,
        mas a informação do 'model' no 'model', ao invés de ficar fazendo
        lógica de negócio nas 'views', que tem que ser a mais enxuta possível.
        """
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        # Essa opção é uma 'tupla' de 'tupla' também, para cada 'tupla',
        # ele deve indicar dois ou mais campos. É para evitar repetição de inscrição.
        unique_together = (('user', 'course'),)


class Announcement(models.Model):
    course = models.ForeignKey(
        Course, verbose_name='Curso',
        # Dentro do curso vai ter um atributo chamado 'announcements'
        # que vai estar os anúncios relacionados a ele.
        related_name='announcements',
        on_delete=models.CASCADE
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
        # Ordena a listagem de curso decrescente, sempre o mais atual será exibido primeiro.
        ordering = ['-created_at']


class Comment(models.Model):
    # Uma determinada instância de anúncio vai ter uma ação
    # chamada 'comments' que irá trazer os seus comentários.
    announcement = models.ForeignKey(
        Announcement, verbose_name='Anúncio',
        related_name='comments',
        on_delete=models.CASCADE
    )

    # Usuário que comentou.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='usuário',
        on_delete=models.CASCADE
    )
    comment = models.TextField('Comentário')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        # Ordenado de forma crescente.
        ordering = ['created_at']


def post_save_announcement(instance, created, **kwargs):
    if created:
        # Vai ser o título.
        subject = instance.title
        context = {'announcement': instance}

        template_name = 'courses/announcement_mail.html'

        # Será enviado e-mail para todos que estiverem com inscrição, 'status == 1'.
        enrollments = Enrollment.objects.filter(course=instance.course, status=1)

        for enrollment in enrollments:
            # Para cada usuário inscrito no curso, será enviado um e-mail para ele.
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)


# Indica que a função deve ser executada naquele 'post_save',
# naquele 'signal' que o Django nos fornece para o model.
models.signals.post_save.connect(
    # Função que vai ser executada.
    post_save_announcement,
    # Quem é que vai enviar ele.
    sender=Announcement,
    # Verifica se a função já está cadastrada nesse sinal.
    dispatch_uid='post_save_announcement'
)
