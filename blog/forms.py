from django import forms
from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'tags']

    image = forms.ImageField(required=False)
    tags = forms.CharField(required=False)