from django import forms
from django.core.mail import send_mail
from django.conf import settings

from simplemooc.core.mail import send_mail_template

from .models import Comment


class ContactCourse(forms.Form):
	
	name = forms.CharField(label='Nome', max_length=100)
	email = forms.EmailField(label='E-mail')
	message = forms.CharField(
		label='Mensagem/Dúvida', widget=forms.Textarea
	)

	def send_mail(self, course):
		subject = '[%s] Contato' % course	# course que está enviando o contato.
		context = {		# forma nomeada, dicionário
			'name': self.cleaned_data['name'],
			'email': self.cleaned_data['email'],
			'message': self.cleaned_data['message'],
		}
		template_name = 'courses/contact_email.html'
		send_mail_template(	# chama função 'send_mail_template'
			subject, # passa o assunto
			template_name, # passa o nome do template
			context, 	# recebe o contexto como parâmetro, que tem o 'nome', 'e-mail' e a 'mensagem'
			[settings.CONTACT_EMAIL]	# lista com os e-mails que serão enviados
		)

    # Envio antigo, sem o uso de template
    # def send_mail(self, course):
    #     subject = '[%s] Contato' % course
    #     message = 'Nome: %(name)s;E-mail: %(email)s;%(message)s'
    #     context = {
    #         'name': self.cleaned_data['name'],
    #         'email': self.cleaned_data['email'],
    #         'message': self.cleaned_data['message'],
    #     }
    #     message = message % context
    #     send_mail(
    #         subject, message, settings.DEFAULT_FROM_EMAIL,
    #         [settings.CONTACT_EMAIL]
    #     )


class CommentForm(forms.ModelForm):		# formulário para meu model.

	class Meta:
		model = Comment
		fields = ['comment']