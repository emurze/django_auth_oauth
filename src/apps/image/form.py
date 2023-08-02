import requests
from django import forms
from django.conf import settings
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def save(self, commit=True):
        image = super().save(commit=False)
        url = self.cleaned_data['url']
        extension = url.rsplit('.')[1].lower()

        name = slugify(image.title)

        image_p = requests.get(url)

        image_name = f'{name}.{extension}'

        if commit:
            image.save()
        return image

    def clean_url(self):
        url = self.cleaned_data['url']
        extension = url.rsplit('.')[1].lower()

        if extension not in settings.ALLOWED_IMAGE_EXTENSIONS:
            raise forms.ValidationError('Url isn\'t match.')
        else:
            return url

