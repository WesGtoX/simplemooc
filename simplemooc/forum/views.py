from django.shortcuts import render, redirect
from django.views.generic import (TemplateView, View, ListView, DetailView)
from django.contrib import messages

from .models import Thread
from .forms import ReplyForm

#class ForumView(View):

#	#template_name = 'forum/index.html'
#    def get(self, request, *args, **kwargs):
#        return render(request, 'forum/index.html')


#class ForumView(TemplateView):

#	#template_name = 'forum/index.html'
class ForumView(ListView):

	#model = Thread		# na listagem indicamos o model, mas podemos indicar a 'queryset'.
	paginate_by = 2
	template_name='forum/index.html'

	def get_queryset(self):		# uma das opções de customização do 'ListView'.
		queryset = Thread.objects.all()		# quando indica o 'model', ele faz isso 'Thread.objects.all()'.
		#if 'order' in self.request.GET:		# procura o parâmetro, . Quando faço uma view baseada em função, o objeto request sempre estará disponível na função, quando faço em classe, esse objeto estará disponível na instância.
		order = self.request.GET.get('order', '')		# pode ser que o parâmetro 'order' não exista, então pode dar erro, então a string vazia ('') é o valor default.
		if order == 'views':
			queryset = queryset.order_by('-views')
		elif order == 'answers':
			queryset =  queryset.order_by('-answers')
		tag = self.kwargs.get('tag', '')	# a 'url' que acessar a view 'ForumView' ela é a url que tem o parâmetro nomeado.
		if tag:
			queryset = queryset.filter(tags__slug__icontains=tag)		# filtra as tags que o slug contém.
		return queryset

	def get_context_data(self, **kwargs):
	    context = super(ForumView, self).get_context_data(**kwargs)		# 'super' pegar os '**kwargs' e joga no 'contexto', esse '**kwargs' são argumentos que passa na 'url'.
	    context['tags'] = Thread.tags.all()		# não estou chamando uma instancia, quando chamo uma instancia, o tags é filtrado pelos valores que aquela instancia tem, quando chamo pela classe, ele chama todos as tags associadas a alguma instancia dessa classe.
	    return context


class ThreadView(DetailView):

	model = Thread
	template_name = 'forum/thread.html'

	def get_context_data(self, **kwargs):
	    context = super(ThreadView, self).get_context_data(**kwargs)		# implementa o 'get_context_data()' associado ao 'DetailView'.
	    context['tags'] = Thread.tags.all()
	    context['form'] = ReplyForm(self.request.POST or None)		# quando chamar o 'form.is_valid', ele retorna 'valido' apenas se os dados do formulário foram preenchidos, e se preenchidos, são 'válidos'. Os dados do 'form.is_valid' vai retornar falso,
	    return context 												# quando os dados do formulário não foram preenchidos, ou foram, mas não são válidos. Essa diferença é importante, porque quando eu faço uma requisição 'GET' então o 'POST' ele é vazio,
	    															# mas ele ainda vai tentar validar esses dados, pois ele é um dicionário. Com essa lógica, eu indico, quando o 'POST' for vazio, eu não vou retornar o formulário 'POST' com um dicionário vazio,
	    															# ele vai retonar a palavra 'None', e a implementação desse 'is_valid', ele verifica, quando for 'None', ou seja, eu não sobmeti o formulário, que só vai ser submetido quando de fato o método for o 'request.POST'.	    																

	def post(self, request, *arg, **kwargs):		# cógdigo do 'get' que o 'DetailView' implementa. Esse método 'post', só é executado no método 'POST', ou seja, o método do 'POST' da função 'ThreadView' só vai ser ativado, quando eu acessar essa 'view' através do método 'POST'.
		if not self.request.user.is_authenticated:
			messages.error(self.request, 'Para responder ao tópico é necessário estar logado')
			return redirect(self.request.path)		# redireciona para a mesma url, objeto 'request' tem um atributo chamado 'path' que é justamanete a url atual.
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		form = context['form']
		if form.is_valid():
			reply = form.save(commit=False)		# o 'ModelForm' tem o metodo 'save', diferente do 'form' normal, porque esse método 'save' vai salvar o objeto. Quando coloco o 'commit=False', eu indico ao 'ModelForm', que o método 'save' não deve salvar o objeto de fato, só deve preencher os dados do formulário, no objeto.
			reply.thread = self.object
			reply.author = self.request.user
			reply.save()
			messages.success(self.request, 'A sua resposta foi enviada com sucesso')
			context['form'] = ReplyForm()
		return self.render_to_response(context)		# 'render_to_response' bem parecido com o render, a diferença é que só passa o contexto. O 'request' já está acessível através de 'self.request', e o template, é o 'template_name'.


index = ForumView.as_view()		# 'index' recebe o resultado de 'ForumView.as_view()' o 'as_view' retorna uma função.
thread = ThreadView.as_view()	# a variável 'thread' vai receber a 'ThreadView' que é uma classe, transformada em função. Uma função em 'view'.

#index = TemplateView.as_view(template_name='forum/index.html')		# também poderia ter sido declarada dessa forma.

