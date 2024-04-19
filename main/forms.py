from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    post_headline = forms.CharField(min_length=10)
    post_text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'author',
            'is_news',
            'categories',
            'post_headline',
            'post_text',
            'post_rating',
        ]

    def clean(self):
        cleaned_data = super().clean()
        post_headline = cleaned_data.get("post_headline")
        post_text = cleaned_data.get("post_text")

        if post_headline == post_text:
            raise ValidationError(
                "Текст поста не должен быть идентичным заголовку поста."
            )

        return cleaned_data
