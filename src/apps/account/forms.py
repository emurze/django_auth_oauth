from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.account.models import Account


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password1']:
            raise ValidationError('Password must be the same.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('birthday', 'photo')
