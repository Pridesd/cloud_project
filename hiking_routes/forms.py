from django.forms import TextInput

from .models import Comment
from django import forms

#view안에 집어 넣을 폼 하나를 만듦
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': TextInput(attrs={
                'class': "form-control",
                'style': 'height: 30px;',
                'placeholder': 'Name'
            })
        }