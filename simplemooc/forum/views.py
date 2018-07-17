from django.shortcuts import render
from django.views.generic import (TemplateView, View, ListView, DetailView)

from .models import Thread

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
	    context = super(ThreadView, self).get_context_data(**kwargs)
	    context['tags'] = Thread.tags.all()
	    return context


index = ForumView.as_view()		# 'index' recebe o resultado de 'ForumView.as_view()' o 'as_view' retorna uma função.
thread = ThreadView.as_view()	# a variável 'thread' vai receber a 'ThreadView' que é uma classe, transformada em função. Uma função em 'view'.

#index = TemplateView.as_view(template_name='forum/index.html')		# também poderia ter sido declarada dessa forma.

