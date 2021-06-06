# forms.py
from django import forms
from .models import Post

from .models import Comment

# 입력을 받기 위한 Form

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'content', 'image',]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
