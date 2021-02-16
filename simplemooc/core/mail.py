from django.template.loader import render_to_string
from django.template.defaultfilters import striptags

from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_mail_template(subject, template_name, context, recipient_list,
                       from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
    """
    :param subject: A função vai receber um assunto.
    :param template_name: Um template.
    :param context: O contexto que vai servir para esse template.
    :param recipient_list: A lista de usuários que vão receber essa mensagem.
    :param from_email: Por padrão aquele default from e-mail.
    :param fail_silently: Falha silenciosa que é uma variável que precisa no 'email.send'
    para saber quando o envio de e-mail falhar, ele vai lançar ou não essa ação.
    """

    # Vai ser a renderizaçãodo do template no contexto que foi mandado.
    message_html = render_to_string(template_name, context)

    # A mensagem em texto, porque por padrão se envia um texto, e a forma alternativa
    # seria o 'html'. a função 'striptags', remove as tags, é um filtro do Django.
    message_txt = striptags(message_html)

    # 'EmailMultiAlternatives' é uma classe do pacote 'django.core.mail',
    # que é um e-mail que tem várias alternativas. tem um conteúdo
    # principal e cria vários alternativos.
    email = EmailMultiAlternatives(
        # Assundo.
        subject=subject,
        # A mensagem.
        body=message_txt,
        # De quem veio o email.
        from_email=from_email,
        # Para quem vai.
        to=recipient_list
    )

    # Adiciona uma alternativa, eu vou dizer qual o conteúdo alternativo, o texto 'html'.
    email.attach_alternative(message_html, 'text/html')
    # Por final eu dou um send.
    email.send(fail_silently=fail_silently)
