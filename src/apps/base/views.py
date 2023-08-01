from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def dashboard(request: WSGIRequest, name: str) -> HttpResponse:
    template_name = 'base/dashboard.html'
    context = {'selected': name}
    return render(request, template_name, context)
