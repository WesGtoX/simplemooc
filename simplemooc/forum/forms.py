from django import forms
from simplemooc.forum.models import Reply


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['reply']
