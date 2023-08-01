from django.urls import path

from apps.base import views

urlpatterns = [
    path('', lambda request: views.dashboard(request, 'dashboard')),
    path('<slug:name>/', views.dashboard, name='dashboard'),
]
