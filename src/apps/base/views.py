from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def dashboard(request: WSGIRequest) -> HttpResponse:
    template_name = 'base/dashboard.html'
    context = {'selected': 'dashboard'}
    return render(request, template_name, context)
