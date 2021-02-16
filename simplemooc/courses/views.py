from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from simplemooc.courses.models import Course, Enrollment, Lesson, Material
from simplemooc.courses.forms import ContactCourse, CommentForm
from simplemooc.courses.decorators import enrollment_required


def index(request):
    """
    Retorna os objetos cadastrados no banco de dados.
    """
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    # Dicionário passado no final.
    context = {'courses': courses}
    return render(request, template_name, context)


# def details(request, pk):
# 	"""
# 	Retorna a página do curso 'pk', caso não for encontrada, retorna uma página 404.
#
# 	:param pk: É o númeroda da página referente ao 'id' do curso do banco de dados.
# 	"""
# 	course = get_object_or_404(Course, pk=pk)
# 	context = {'course': course}
# 	template_name = 'courses/details.html'
# 	return render(request, template_name, context)


def details(request, slug):
    # Ao invés de passar o 'id', passa o 'slug'.
    course = get_object_or_404(Course, slug=slug)
    context = {}

    # Verifica se o método é um 'post' ou se é um método 'get'.
    if request.method == 'POST':
        # Se for 'post', ele recebe o dicionário com todos os campos submetido pelo usuário.
        form = ContactCourse(request.POST)

        if form.is_valid():
            # Se enviaro formulário com sucesso...
            context['is_valid'] = True
            form.send_mail(course)

            # Limpa o formulário.
            form = ContactCourse()
    else:
        # Caso contrário, ok.
        form = ContactCourse()

    # Variável form.
    context['form'] = form
    context['course'] = course
    template_name = 'courses/details.html'
    return render(request, template_name, context)


# 'decorator', que o próprio Django já disponibiliza, para obrigar o usuário
# a estar logado. Olha o 'request', vê se o usuário está autenticado, se estiver,
# ele executa normalmente, se não ele redireciona o usuário para uma página de 'login'.
@login_required
def enrollment(request, slug):
    # Pega o curso atual.
    course = get_object_or_404(Course, slug=slug)
    # Esse método vai ser passado um filtro, qual vai ser o 'user' do 'request.
    # Ele retorna uma 'tupla', a inscrição se ouver, caso não,
    # será criado, e um boleano dizendo se criou ou não.
    # Essa inscrição será do usuário atual, que está logado
    # no sistema, e vai ter o curso em questão.
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        # enrollment.active()
        # Função do modo 'messages' que já está disponível.
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')

    return redirect('accounts:dashboard')


@login_required
def undo_enrollment(request, slug):
    """
    Todas as páginas associadas ao curso está com 'slug', mas não necessariamente é preciso.
    Não tem a necessidade de ser uma 'url' descritiva, poderia ser coloca o 'id' da
    matrícula diretamente. Porém estamos deixando padrão com o 'slug' em todas.
    """
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')

    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }

    return render(request, template, context)


@login_required
@enrollment_required
def announcements(request, slug):
    # Busca o 'curso' do 'request'.
    course = request.course
    template = 'courses/announcements.html'
    context = {
        'course': course,
        # Todos os anúncios do curso estão nessa variável.
        'announcements': course.announcements.all()
    }
    return render(request, template, context)


@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course  # Busca o 'curso' do 'request'.
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        # Cria e salva o comentário.
        comment = form.save(commit=False)

        # Usuário logado.
        comment.user = request.user

        # O anúncio 'announcement = get_object_or_404(course.announcements.all(), pk=pk)'.
        comment.announcement = announcement

        # Depois chama o 'comment.save()' para de fato salvar o comentário.
        comment.save()

        # Apenas para zerar o formulário.
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso')

    template = 'courses/show_announcement.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form,
    }
    return render(request, template, context)


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template = 'courses/lessons.html'
    lessons = course.release_lessons()

    if request.user.is_staff:
        lessons = course.lessons.all()

    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, template, context)


@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    # 'course=course' garantia de que as aulas são mesmo desse curso.
    lesson = get_object_or_404(Lesson, pk=pk, course=course)

    # Verificação básica de segurança.
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)

    template = 'courses/lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }
    return render(request, template, context)


@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    # Não tem relacionamento com o curso, mas tem relacionamento com a aula
    # que tem relacionamento com o curso. Quando coloca dois underscore '__'
    # vou acessar uma propriedade já do outro objeto 'lesson__course'.
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson

    # Verificação básica de segurança.
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Este material não está disponível')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)

    # Verifica se o usuário é 'is_embedded', se não for ele redireciona
    # para 'material.file.url', se for ele exibe realmente o template.
    if not material.is_embedded():
        return redirect(material.file.url)

    template = 'courses/material.html'
    context = {
        'course': course,
        'lesson': lesson,
        'material': material
    }
    return render(request, template, context)
