from django.contrib import messages as ms
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.account.forms import RegistrationForm, UserEditForm, AccountEditForm
from apps.account.models import Account


class RegistrationView(View):
    template_name = 'account/register.html'
    template_name_done = 'account/register_done.html'

    def get(self, request: WSGIRequest) -> HttpResponse:
        context = {'form': RegistrationForm()}
        return render(request, self.template_name, context)

    def post(self, request: WSGIRequest) -> HttpResponse:
        if (form := RegistrationForm(request.POST)).is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)
            user.set_password(cd['password1'])
            user.save()
            Account.objects.create(user=user)
            return render(request, self.template_name_done)
        else:
            return self.get(request)


class EditView(View):
    template_name = 'account/edit.html'
    template_name_done = 'account/edit_done.html'

    def get(self, request: WSGIRequest) -> HttpResponse:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account,)
        context = {
            'user_form': user_form,
            'account_form': account_form,
        }
        return render(request, self.template_name, context)

    def post(self, request: WSGIRequest) -> HttpResponse:
        user_form = UserEditForm(instance=request.user, data=request.POST)
        account_form = AccountEditForm(instance=request.user.account,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()

            message = 'Cool! You edited your account <strong>GAY</strong>'
            ms.success(request, message)
            return self.get(request)
        else:
            ms.error(request, 'Please enter the correct data.')

            context = {
                'user_form': user_form,
                'account_form': account_form,
            }
            return render(request, self.template_name, context)
