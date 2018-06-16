from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_mail_template(
	subject,	# a função vai receber um assunto.
	template_name,		# um template.
	context,	# o contexto que vai server para esse template.
	recipient_list,		# a lista de usuários que vão receber essa mensagem.
	from_email=settings.DEFAULT_FROM_EMAIL,		# por padrão aquele default from e-mail.
	fail_silently=False		# falha silenciosa que é uma variável qeu precisa no email.send para saber quando o envio de e-mail falhar, ele vai lançar ou não essa ação.
):

	message_html = render_to_string(template_name, context)		# vai ser a renderizaçãodo template no contexto que foi mandado.

	message_txt = striptags(message_html)	# a mensagem em texto, porque por padrão se envia um texto, e a forma alternativa seria o html. a função striptags, remove as tags, é um filtro do Django.

	email = EmailMultiAlternatives(		# EmailMultiAlternatives é uma classe do pacote django.core.mail, que é um e-mail que tem várias alternativas. tem um conteúdo principal e cria vários alternativos.
		subject=subject,	# assundo.
		body=message_txt, 	# a mensagem.
		from_email=from_email,	# de quem veio o email.
		to=recipient_list	# pra quem vai.
	)
	email.attach_alternative(message_html, "text/html")	# adiciona uma alternativa, eu vou dize qual o conteúdo alternativo, o texto html.
	email.send(fail_silently=fail_silently)		# por final eu dou um send