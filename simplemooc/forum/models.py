from django.db import models
from django.conf import settings
from django.urls import reverse

from taggit.managers import TaggableManager


# Justamente o tópico do fórum.
class Thread(models.Model):
    # Título do tópico.
    title = models.CharField('Título', max_length=100)

    # 'SlugField' por padrão cria com um 'index' no banco de dados para indexar.
    # A tendência é que seja único, mas ele não especifica que tem que ser.
    slug = models.SlugField('Identificador', max_length=100, unique=True)

    # Corpo da mensagem.
    body = models.TextField('Mensagem')
    author = models.ForeignKey(
        # Tem que ser colocado dessa forma para que o Django fique
        # compátivel, caso eu altere um modelo que é o usuário.
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        # A partir do momento que o tópico tem uma referência para o 'autor', o 'related_name'
        # vai ser uma referência no 'autor' para todos os tópicos que ele criou, ou seja o
        # Django vai criar um atributo dinâmico do usuário, chamado 'threads', e quando
        # acessado a partir de uma instância de um usuário, ele vai referênciar todos
        # os tópicos criados pelo 'usuário'.
        related_name='threads',
        # 'on_delete' é obrigatório no Django 2.0.
        on_delete=models.CASCADE
    )
    # Forma de contabilizar as visualizações.
    views = models.IntegerField('Visualizações', blank=True, default=0)
    # Facilita na hora de ordenar os tópicos.
    answers = models.IntegerField('Respostas', blank=True, default=0)

    tags = TaggableManager()

    # 'auto_now_add' pega a data que criou.
    created = models.DateTimeField('Criado em', auto_now_add=True)
    # 'auto_now' pega a data que alterou.
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.title

    # Pega a 'tupla' e usa uma função chamada 'reverse' que está no
    # pacote: "from django.core.urlresolvers import reverse",
    # é uma forma de resgatar a 'url' dado um nome. E com isso ele retonar a 'url'.
    # @models.permalink  # deprecated
    def get_absolute_url(self):
        """
        'método' que retorna uma 'tupla'

        # Quando usa esse 'decorator', não precisa indicar o caminho da 'url'.
        Só precisa indicar uma 'tupla' de três valores:
            - 1º é o nome da 'url',
            - 2º os parâmetros posicionais e o
            - 3º é um dicionário com os parâmetros nomeados.
        """
        # return 'forum:thread', (), {'slug': self.slug}  # deprecated
        return reverse('forum:thread', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']


class Reply(models.Model):
    thread = models.ForeignKey(
        Thread, verbose_name='Tópico',
        related_name='replies',
        # 'on_delete' é obrigatório no Django 2.0.
        on_delete=models.CASCADE
    )
    # Título do tópico.
    reply = models.TextField('Resposta', max_length=500)
    author = models.ForeignKey(
        # Tem que ser colocado dessa forma para que o Django fique
        # compátivel, caso eu altere um modelo que é o usuário.
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='replies',
        # 'on_delete' é obrigatório no Django 2.0.
        on_delete=models.CASCADE
    )
    correct = models.BooleanField('Correta?', blank=True, default=False)

    # 'auto_now_add' pega a data que criou.
    created = models.DateTimeField('Criado em', auto_now_add=True)
    # 'auto_now' pega a data que alterou.
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        # Retorna as 100 primeiras letras.
        return self.reply[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        # O valor booleano 'True' é maior que o 'False', então tem que ser
        # ordenado de forma 'decrescente'. E os outos ordenam pela data.
        ordering = ['-correct', 'created']


def post_save_reply(created, instance, **kwargs):
    # Carrega a quantidade de resposta no tópico.
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()

    # toda vez que salvo a resposta, ele verifica se a resposta é uma resposta correta.
    if instance.correct:
        # Ele pega a instância, que é a resposta, pega a 'thread' em questão, busca todas as resposta...
        # ...e faz um filtro excluindo ela própria. Isso funciona porque o 'update' não chama o 'signal'
        # tanto do 'post_save', quanto do 'pre_save'. O 'pre_save' e o 'post_save', são executados apenas
        # no método '.save()', quando você executa de fato uma instância '.save()', o 'update'
        # não dispara esse gatilho.
        instance.thread.replies.exclude(pk=instance.pk).update(correct=False)


def post_deleate_reply(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()


# É importante colocar o 'sender', porque só vai disparar quando for o 'model' 'Reply',
# se não colocar o 'sender', ele vai disprar para qualquer 'model'. Por causa que as
# vezes o 'signal' pode ser carregado duas vezes caso esse arquivo seja importado mais
# de uma vez. E o 'dispatch_uid' é um verificador único.
models.signals.post_save.connect(post_save_reply, sender=Reply, dispatch_uid='post_save_reply')
models.signals.post_delete.connect(post_deleate_reply, sender=Reply, dispatch_uid='post_deleate_reply')

# # Sistema de 'sinais' que o Django criou e já implementou para os modelos,
# # sempre que um modelo for atualizado, ele dispara um 'sinal', e você pode
# # criar uma função e associar a esse 'sinal'. Sempre colocar o '**kwargs'
# # nessa função, porque esse 'post_save' recebe muitos parâmetros.
# def post_save_reply(created, instance, **kwargs):
# 	# todas as vezes que eu criar uma resposta, eu aumento o número do atributo resposta da 'thread'.
# 	if created:
# 		instance.thread.answers = instance.thread.answers + 1
# 		instance.thread.save()
#
# # Porque, toda vez que uma instância for removida, uma reposta for removida,
# # a ideia é que faça essa mesma lógica, só que ao contrário.
# def post_deleate_reply(instance, **kwargs):
# 	instance.thread.answers = instance.thread.answers - 1
# 	instance.thread.save()
