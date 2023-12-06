from django import forms
from .models import Article
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }
