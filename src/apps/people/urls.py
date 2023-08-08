from django.urls import path

from apps.people.views import PeopleList, PeopleDetail

app_name = 'people'

urlpatterns = [
    path('', PeopleList.as_view(), name='list'),
    path('<slug:username>/', PeopleDetail.as_view(), name='detail'),
]
