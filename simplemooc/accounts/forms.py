from django import forms
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from simplemooc.core.mail import send_mail_template
from simplemooc.core.utils import generate_hash_key

from .models import PasswordReset

# Indica que estamos usando o 'user' que o Django reconhece
# como usuário do sistema que no nosso caso é o 'CustomUser'.
User = get_user_model()


# Não vai ser um 'ModelForm' porque ele não vai estar associado a
# nenhum model inicialmente. Porque só queremos um campo de e-mail.
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    # Para validar se o 'email' é de algum usuário do sistema.
    def clean_email(self):
        email = self.cleaned_data['email']

        # Detectar se existem algum usuário do sistema, retorna um boleano.
        if User.objects.filter(email=email).exists():
            # TODO: 'clean_...' retorna o valor que o formulátio vai pegar no final.
            return email

        raise forms.ValidationError('Nenhum usuário encontrado com este e-mail')

    def save(self, base_domain=None):
        # Quando for válido, eu busco o usuário com aquele e-mail.
        user = User.objects.get(email=self.cleaned_data['email'])

        # Gera a chave.
        key = generate_hash_key(user.username)

        # Cria o 'model' para resetar a senha.
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'

        # Assunto.
        subject = 'Criar nova senha no Simple MOOC'
        context = {
            'reset': reset,
            'base_domain': base_domain
        }

        # Função criada de envio de 'email' no 'core'.
        send_mail_template(subject, template_name, context, [user.email])


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        """
        Esse método vai ser para a senha 2.
        """
        # Pega a senha 1...
        password1 = self.cleaned_data.get("password1")

        # ...pega a senha 2...
        password2 = self.cleaned_data.get("password2")

        # ...verifica se foram enviadas, e depois se são iguais.
        if password1 and password2 and password1 != password2:
            # Se elas não forem iguais mostra uma mensagem de erro.
            raise forms.ValidationError('A confirmação não está correta')

        return password2

    def save(self, commit=True):
        """
        Novo método 'save' que substitui o do 'UserCreationForm'.
        Ele recebe o 'commit' igual a 'True', chama o 'save' do
        meu 'super' que no caso é 'UserCreationForm'.
        """
        # No 'UserCreationForm' ele chama o 'save' do 'ModelForm' através do 'super'.
        # Chama o 'save' passa o 'commit=False' para não salvar, vai pegar usuário,
        # vai setar a senha. Como também foi passado 'commit=False', ele não vai salvar
        # o usuário, ele vai retornar o usuário.
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # seta a senha...

        # Da uma possibilidade de se quiser herdar e fazer outro 'registerForm', pode chamar parte desse
        # 'commit' e não salvar na hora, posso querer alterar alguma coisa do usuário antes de salvar.
        if commit:
            user.save()

        # O padrão de 'ModelForm' é sempre o 'save' retornar a instância do objeto relacionado.
        return user

    class Meta:
        model = User
        # No formulário de registro vai precisar apenas do 'username' e 'email'.
        fields = ['username', 'email']


class EditAccountForm(forms.ModelForm):
    class Meta:
        # Para saber qual 'model' que o formulário vai precisar...
        model = User
        # Campos modificados para os que criamos.
        fields = ['username', 'email', 'name']
