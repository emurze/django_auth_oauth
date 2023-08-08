import logging

import requests
from django import forms
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.text import slugify

from apps.image.models import Image

lg = logging.getLogger(__name__)


class ImageCreateForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'description',
            'cols': 40,
            'rows': 10,
        }),
        required=False,
    )
    image_response = None

    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'title'}),
            'url': forms.TextInput(attrs={'placeholder': 'URL'}),
        }

    def save(self, commit=True):
        """
        1. Set slug and get upload_name.
        2. Set the image.
        """
        instance = super().save(commit=False)

        url = self.cleaned_data['url']

        instance.slug = file_name = slugify(instance.title)
        extension = url.rsplit('.', 1)[1].lower()
        upload_name = f'{file_name}.{extension}'

        instance.image.save(
            upload_name,
            ContentFile(self.image_response.content),
            save=False
        )

        if commit:
            instance.save()
        return instance

    def clean_url(self):
        """Check the url and request an image."""
        url = self.cleaned_data['url']
        extension = url.rsplit('.', 1)[1].lower()

        try:
            self.image_response = requests.get(url)
            if self.image_response.status_code != 200:
                raise requests.exceptions.ConnectionError
        except requests.exceptions.ConnectionError:
            raise forms.ValidationError('Enter a valid url')

        if extension not in settings.ALLOWED_IMAGE_EXTENSIONS:
            raise forms.ValidationError('Url isn\'t match.')
        else:
            return url
