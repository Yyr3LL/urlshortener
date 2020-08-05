from django import forms
from .models import ShortenedUrl


class CreateShortUrl(forms.ModelForm):
    class Meta:
        model = ShortenedUrl
        fields = ('long_url',)
