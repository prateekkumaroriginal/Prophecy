from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'caption']
        widgets = {
            "caption": forms.Textarea(attrs={"cols": 50, "rows": 10}),
        }