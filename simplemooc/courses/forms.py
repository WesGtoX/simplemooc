from django import forms
# from django.core.mail import send_mail
from django.conf import settings

from simplemooc.core.mail import send_mail_template
from simplemooc.courses.models import Comment


class ContactCourse(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea)

    def send_mail(self, course):
        # 'course' que está enviando o contato.
        subject = f'[{course}] Contato'
        context = {
            # Forma nomeada, dicionário.
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }
        template_name = 'courses/contact_email.html'

        # Chama função 'send_mail_template'.
        send_mail_template(
            # Passa o assunto.
            subject,
            # Passa o nome do 'template'.
            template_name,
            # Recebe o contexto como parâmetro, que tem o 'nome', 'e-mail' e a 'mensagem'.
            context,
            # Lista com os e-mails que serão enviados.
            [settings.CONTACT_EMAIL]
        )

    # # Envio antigo, sem o uso de 'template'.
    # def send_mail(self, course):
    #     subject = f'[{course}}] Contato'
    #     message = 'Nome: %(name)s;E-mail: %(email)s;%(message)s'
    #     context = {
    #        'name': self.cleaned_data['name'],
    #        'email': self.cleaned_data['email'],
    #        'message': self.cleaned_data['message'],
    #     }
    #     message = message % context
    #     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])


class CommentForm(forms.ModelForm):
    """
    Formulário para meu model.
    """

    class Meta:
        model = Comment
        fields = ['comment']
