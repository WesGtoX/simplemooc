import json

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.http import HttpResponse

from .models import Thread, Reply
from .forms import ReplyForm


# class ForumView(View):
#
# 	# template_name = 'forum/index.html'
#    	def get(self, request, *args, **kwargs):
# 		return render(request, 'forum/index.html')
#
#
# class ForumView(TemplateView):
#
# 	# template_name = 'forum/index.html'


class ForumView(ListView):
    # Na listagem indicamos o 'model', mas podemos indicar a 'queryset'.
    # model = Thread
    paginate_by = 10
    template_name = 'forum/index.html'

    # Uma das opções de customização do 'ListView'.
    def get_queryset(self):
        # Quando indica o 'model', ele faz isso 'Thread.objects.all()'.
        queryset = Thread.objects.all()

        # Procura o parâmetro. Quando faço uma 'view' baseada em função,
        # o objeto 'request' sempre estará disponível na função, quando faço
        # em 'classe', esse objeto estará disponível na instância.
        # if 'order' in self.request.GET:

        # Pode ser que o parâmetro 'order' não exista, então pode dar erro,
        # então a 'string' vazia ('') é o valor default.
        order = self.request.GET.get('order', '')

        if order == 'views':
            queryset = queryset.order_by('-views')
        elif order == 'answers':
            queryset = queryset.order_by('-answers')

        # A 'url' que acessar a 'view' 'ForumView' ela é a 'url' que tem o parâmetro nomeado.
        tag = self.kwargs.get('tag', '')

        if tag:
            queryset = queryset.filter(tags__slug__icontains=tag)  # filtra as 'tags' que o 'slug' contém.

        return queryset


def get_context_data(self, **kwargs):
    # 'super' pegar os '**kwargs' e joga no 'contexto', esse '**kwargs' são argumentos que passa na 'url'.
    context = super(ForumView, self).get_context_data(**kwargs)

    # Não estou chamando uma instância, quando chamo uma instância, o 'tags' é
    # filtrado pelos valores que aquela instância tem, quando chamo pela classe,
    # ele chama todos as 'tags' associadas a alguma instância dessa classe.
    context['tags'] = Thread.tags.all()
    return context


class ThreadView(DetailView):
    model = Thread
    template_name = 'forum/thread.html'

    def get(self, request, *args, **kwargs):
        # Quando chama o 'get' ele vai criar o 'self.object', que é justamente a 'thread' em questão.
        response = super(ThreadView, self).get(request, *args, **kwargs)

        # Se o usuário não estiver autenticado, ou ele estiver,
        # Mas não é o 'autor' do tópico, então vai contar uma visualização.
        if not self.request.user.is_authenticated or (self.object.author != self.request.user):
            self.object.views = self.object.views + 1
            self.object.save()

        return response

    def get_context_data(self, **kwargs):
        # Implementa o 'get_context_data()' associado ao 'DetailView'.
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()

        # Quando chamar o 'form.is_valid', ele retorna 'valido' apenas se os dados
        # do formulário foram preenchidos, e se preenchidos, são 'válidos'.
        # Os dados do 'form.is_valid' vai retornar 'False',
        context['form'] = ReplyForm(self.request.POST or None)

        # Quando os dados do formulário não foram preenchidos, ou foram,
        # mas não são válidos. Essa diferença é importante, porque quando
        # eu faço uma requisição 'GET' então o 'POST' ele é vazio, mas ele
        # ainda vai tentar validar esses dados, pois ele é um dicionário.
        # Com essa lógica, eu indico, quando o 'POST' for vazio, eu não vou
        # retornar o formulário 'POST' com um dicionário vazio, ele vai retonar
        # a palavra 'None', e a implementação desse 'is_valid', ele verifica,
        # quando for 'None', ou seja, eu não submeti o formulário, que só vai
        # ser submetido quando de fato o método for o 'request.POST'.
        return context

    # Cógdigo do 'get' que o 'DetailView' implementa. Esse método 'post',
    # só é executado no método 'POST', ou seja, o método do 'POST' da
    # função 'ThreadView' só vai ser ativado, quando eu acessar
    # essa 'view' através do método 'POST'.
    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Para responder ao tópico é necessário estar logado')
            # Redireciona para a mesma 'url', objeto 'request' tem um
            # atributo chamado 'path' que é justamanete a 'url' atual.
            return redirect(self.request.path)

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form']

        if form.is_valid():
            # O 'ModelForm' tem o método 'save', diferente do 'form' normal,
            # porque esse método 'save' vai salvar o objeto. Quando coloco
            # o 'commit=False', eu indico ao 'ModelForm', que o método 'save'
            # não deve salvar o objeto de fato, só deve preencher os dados
            # do formulário no objeto.
            reply = form.save(commit=False)
            reply.thread = self.object
            reply.author = self.request.user
            reply.save()
            messages.success(self.request, 'A sua resposta foi enviada com sucesso')
            context['form'] = ReplyForm()

        # 'render_to_response' bem parecido com o 'render', a diferença é que só passa o contexto.
        # O 'request' já está acessível através de 'self.request', e o template, é o 'template_name'.
        return self.render_to_response(context)


class ReplyCorrectView(View):
    correct = True

    def get(self, request, pk):
        # Tenta pegar a resposta que tem a chave, questão de segurança, pega apenas se for
        # o autor da 'thread'. os dois undescore '__', vai tentar buscar um atributo do
        # campo que é chave estrangeira do modelo atual.
        reply = get_object_or_404(Reply, pk=pk, thread__author=request.user)
        reply.correct = self.correct
        reply.save()
        message = 'Resposta atualizada com sucesso'

        # Essa 'request' tem esse método, que pode verificar se a requisição é 'ajax'.
        if request.is_ajax():
            data = {'success': True, 'message': message}

            # Não vai ser mais aquele 'html/plantext', ou algo desse tipo, vai ser 'application/json'.
            # 'content_type' é importante para o 'browser' saber que tipo está retornando.
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            messages.success(request, message)

            # definimos no model de 'forum', o 'get_absolute_url' para a 'thread' em específico.
            return redirect(reply.thread.get_absolute_url())


# 'index' recebe o resultado de 'ForumView.as_view()' o 'as_view' retorna uma função.
index = ForumView.as_view()

# A variável 'thread' vai receber a 'ThreadView' que é uma classe, transformada em função. Uma função em 'view'.
thread = ThreadView.as_view()
reply_correct = ReplyCorrectView.as_view()

# Quando eu uso o 'as_view', eu posso passar parâmetros nomeados,
# eles vão virar os atributos dessa classe, vão substitruir valores.
reply_incorrect = ReplyCorrectView.as_view(correct=False)

# também poderia ter sido declarada dessa forma.
# index = TemplateView.as_view(template_name='forum/index.html')
