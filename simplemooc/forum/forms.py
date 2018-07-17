from django import forms

from .models import Reply


class ReplyForm(forms.ModelForm):

	class Meta:
		model = Reply
		fields = ['reply']
