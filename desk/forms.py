from django import forms
from .models import Response, Post, Shot


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'category')
        widgets = {
                   'author': forms.HiddenInput(),
                   }


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ('author', 'text', 'post')
        widgets = {
                'post': forms.HiddenInput(),
                'author': forms.HiddenInput(),
                   }


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Shot
        fields = ('image', )
