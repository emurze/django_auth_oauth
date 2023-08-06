from django.urls import path

from apps.image.views import ImageCreateView, ImageDetailView, images_list

app_name = 'images'

urlpatterns = [
    path('', images_list, name='list'),
    path('create/', ImageCreateView.as_view(), name='create'),
    path('detail/<slug:slug>/', ImageDetailView.as_view(), name='detail'),
]
