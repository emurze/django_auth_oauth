import enum
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

lg = logging.getLogger(__name__)


class FollowAction(enum.StrEnum):
    FOLLOW = 'follow'
    UNFOLLOW = 'unfollow'


class PeopleList(ListView, LoginRequiredMixin):
    queryset = User.objects.filter(is_active=True).exclude()
    template_name = 'people/list.html'
    context_object_name = 'people'
    extra_context = {'selected': 'people'}

    def get_queryset(self):
        self_user_id = self.request.user.id
        return User.objects.filter(is_active=True).exclude(id=self_user_id)


class PeopleDetail(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'people/detail.html'
    context_object_name = 'user'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    extra_context = {'selected': 'people'}

    @staticmethod
    def post(request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)

        action = request.POST.get('action')
        match action:
            case FollowAction.FOLLOW:
                user.followers.add(request.user)
                action = FollowAction.UNFOLLOW

            case FollowAction.UNFOLLOW:
                user.followers.remove(request.user)
                action = FollowAction.FOLLOW

        lg.info(action)

        return JsonResponse({
            'action': action,
            'followers_count': user.followers.count(),
        })

    def get_context_data(self, **kwargs):
        user = self.object

        lg.debug(self.request.user.followers.all())

        if user.followers.contains(self.request.user):
            action = FollowAction.UNFOLLOW
        else:
            action = FollowAction.FOLLOW

        kwargs['action'] = action
        return super().get_context_data(**kwargs)
