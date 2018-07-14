from django.shortcuts import render
from django.views.generic import TemplateView


class ForumView(TemplateView):

	template_name = 'forum/index.html'

index = ForumView.as_view()		# 'index' recebe o resultado de 'ForumView.as_view()' o 'as_view' retorna uma função.

#index = TemplateView.as_view(template_name='forum/index.html')		# também poderia ter sido declarada dessa forma.

