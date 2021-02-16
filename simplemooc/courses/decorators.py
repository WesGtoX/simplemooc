from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from simplemooc.courses.models import Course, Enrollment


def enrollment_required(view_func):
    """
    Recebe primeiro a função, que vai receber a 'view' que é a função
    que vai ser executada do Django, a 'view' normal do Django.
    """

    def _wrapper(request, *args, **kwargs):
        # Busca um 'slug' nos 'kwargs' da 'url', para usar esse 'decorator'
        # tem que necessariamente ter o 'slug' do curso na 'url'.
        # Porque vou pegar esse 'slug' e buscar o curso...
        slug = kwargs['slug']

        # Pega o curso atual...
        course = get_object_or_404(Course, slug=slug)

        # Inicialmente verifica se o usuário tem permissão ou não, se ele
        # for 'staff', porque se for, ele tem permissão automaticamente.
        has_permission = request.user.is_staff

        # Se ele não tiver permissão aqui é porque ele não é 'staff'.
        message = ''
        if not has_permission:
            try:
                # Busca a matrícula no curso, pelo usuário e curso.
                enrollment = Enrollment.objects.get(user=request.user, course=course)
            except Enrollment.DoesNotExist:
                # Se não existir permissão, manda a mensagem...
                message = 'Desculpe, mas você não tem permissão para acessar esta página'
            else:  # se existir...
                if enrollment.is_approved():
                    # Vai ser verificado se o 'status' está como aprovado.
                    # Caso estiver ai sim da permissão a ele.
                    has_permission = True
                else:
                    # Se não, mostra uma mensagem que o 'status' ainda está pendente...
                    message = 'A sua inscrição no curso ainda está pendente'

        # Por fim verifica se tem permissão de fato...
        if not has_permission:
            # Se não tiver, mostra uma mensagem de erro, uma das duas acima...
            messages.error(request, message)
            # E redireciona para o 'dashboard'.
            return redirect('accounts:dashboard')

        # Se passar, porque ele tem permissão... Para não fazer uma nova consulta desse
        # curso na 'view', vou jogar o 'objeto' 'curso' no 'request'. Então toda 'view'
        # que usar esse 'decorator', vai ter um 'objeto course' no 'request'.
        # Para que essa consulta não seja repetida na 'view'.
        request.course = course

        # Finalmente executa a 'view' de fato, a 'view' que deve ser executada para
        # aquela determinada 'url', passa no 'request', usa '*args' e o '**kwargs'.
        return view_func(request, *args, **kwargs)

    return _wrapper
