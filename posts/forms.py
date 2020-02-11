from django import forms
from ckeditor.widgets import CKEditorWidget
from main.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']