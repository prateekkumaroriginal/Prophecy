from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'caption']
        widgets = {
            "caption": forms.Textarea(attrs={"cols": 500, "rows": 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'posted_by']
        widgets = {
            "body": forms.Textarea(attrs={"cols": 50, "rows": 3}),
        }