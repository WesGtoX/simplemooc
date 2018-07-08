from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement
from .forms import ContactCourse, CommentForm
from .decorators import enrollment_required

def index(request):
	courses = Course.objects.all()		# retorna todos o objetos cadastrados no bando de dados.
	template_name = 'courses/index.html'
	context = {		# dicionario passado no final.
		'courses': courses
	}
	return render(request, template_name, context)

#def details(request,pk):
#	course = get_object_or_404(Course, pk=pk)		# retorna a página do curso 'pk', é o númeroda página referente ao id do curso do banco de dados. Caso não for encontrada, retorna uma página 404
#	context = {
#		'course': course
#	}
#	template_name = 'courses/details.html'
#	return render(request, template_name, context)

def details(request,slug):
	course = get_object_or_404(Course, slug=slug)		# ao invés de passar o 'id', passa o 'slug'
	context = {}
	if request.method == 'POST':	# verifica se o metodo é um 'post' ou se é um metodo 'get'.
		form = ContactCourse(request.POST)		# se for 'post', ele recebe o dicionário com todos os campos submetido pelo usuário.
		if form.is_valid():
			context['is_valid'] = True 		# se enviaro formulário com sucesso...
			form.send_mail(course)
			form = ContactCourse()		# limpa o formulário
	else:	# caso contrário
		form = ContactCourse()		# Ok
	context['form'] = form		# variavel form		
	context['course'] = course
	template_name = 'courses/details.html'
	return render(request, template_name, context)

@login_required		# decorator, que o próprio Django já disponibiliza, para obrigar o usuário a estar logado. Olha o request, vê se o usuário está autenticado, se estiver, ele executa normalmente, se não ele redireciona o usuário para uma página de login.
def enrollment(request, slug):
	course = get_object_or_404(Course, slug=slug)	# pega o curso atual
	enrollment, created = Enrollment.objects.get_or_create(		# esse metodo vai ser passado um filtro, 'qual vai ser o user do request'. Ele retorna uma tupla, a inscrição se ouver, caso não, será criado, e um boleano dizendo se criou ou não.
		user=request.user, course=course 		# essa inscrição será do usuário atual, que está logado no sistema, e vai ter o curso em questão.
	)
	if created:
		#enrollment.active()
		messages.success(request, 'Você foi inscrito no curso com sucesso')	# função do modo messages que já está disponível
	else:
		messages.info(request, 'Você já está inscrito no curso')

	return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug):		# todas as páginas associadas ao curso está com slug, mas não necessariamente é preciso. Não tem a necessidade de ser uma url descriptiva, poderia ser coloca o ID da matricula diretamente. Porém estamos deixando padrão com o slug em todas.
	course = get_object_or_404(Course, slug=slug)
	enrollment = get_object_or_404(
		Enrollment, user=request.user, course=course
	)
	if request.method == 'POST':
		enrollment.delete()
		messages.success(request, 'Sua inscrição foi cancelada com sucesso')
		return redirect('accounts:dashboard')
	template = 'courses/undo_enrollment.html'
	context = {
		'enrollment':enrollment,
		'course':course,
	}
	return render(request, template, context)

@login_required
@enrollment_required
def announcements(request, slug):
	course = request.course 	# busca o 'curso' do 'request'.
	template = 'courses/announcements.html'
	context = {
		'course': course,
		'announcements':course.announcements.all()	# todos os anúncios do curso está nessa variável.
	}
	return render(request, template, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
	course = course = request.course 	# busca o 'curso' do 'request'.
	announcement = get_object_or_404(course.announcements.all(), pk=pk)
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False)	# cria e salva o comentário.
		comment.user = request.user 	# usuário logao.
		comment.announcement = announcement 	# o anúncio 'announcement = get_object_or_404(course.announcements.all(), pk=pk)'.
		comment.save()		# depois chama o 'comment.save()' para de fato salvar o comentário.
		form = CommentForm()	# apenas para zerar o formulário.
		messages.success(request, 'Seu comentário foi enviado com sucesso')
	template = 'courses/show_announcement.html'
	context = {
		'course': course,
		'announcement': announcement,
		'form': form,
	}
	return render(request, template, context)

