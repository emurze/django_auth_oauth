import enum
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import DetailView

from apps.image.forms import ImageCreateForm
from apps.image.models import Image
from apps.image.serializers import ImageUsersSerializer

lg = logging.getLogger(__name__)


class LikeAction(enum.StrEnum):
    LIKE = 'like'
    UNLIKE = 'unlike'


class ImageCreateView(LoginRequiredMixin, View):
    template_name = 'image/create.html'

    def get(self, request: WSGIRequest) -> HttpResponse:
        context = {
            'selected': 'images',
            'form': ImageCreateForm()
        }
        return render(request, self.template_name, context)

    def post(self, request: WSGIRequest) -> HttpResponse:
        if (form := ImageCreateForm(request.POST)).is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            messages.success(request, 'Image added successfully!')
            return redirect(image.get_absolute_url())
        else:
            context = {
                'selected': 'images',
                'form': form,
            }
            return render(request, self.template_name, context)


class ImageDetailView(LoginRequiredMixin, DetailView):
    model = Image
    template_name = 'image/detail.html'
    context_object_name = 'image'
    extra_context = {'selected': 'images'}

    def get_context_data(self, **kwargs):
        image = self.object

        if image.user_likes.contains(self.request.user):
            action = LikeAction.UNLIKE
        else:
            action = LikeAction.LIKE

        kwargs['action'] = action
        return super().get_context_data(**kwargs)


@login_required
@require_POST
def image_like(request: WSGIRequest) -> HttpResponse:
    image_id = request.POST.get('image_id')
    image = get_object_or_404(Image, id=image_id)

    action = request.POST.get('action')
    match action:
        case LikeAction.LIKE:
            image.user_likes.add(request.user)
            action = LikeAction.UNLIKE

        case LikeAction.UNLIKE:
            image.user_likes.remove(request.user)
            action = LikeAction.LIKE

    image_serializer = ImageUsersSerializer(image.user_likes.all(),
                                            many=True)
    return JsonResponse({
        'action': action,
        'counter': image.user_likes.count(),
        'user_likes': image_serializer.data,
    })


@login_required
@require_GET
def images_list(request: WSGIRequest) -> HttpResponse:
    images = Image.objects.all()
    paginator = Paginator(images, 8)

    page = request.GET.get('page')
    images_only = request.GET.get('images_only')

    if images_only and int(page) > paginator.num_pages:
        return HttpResponse('')

    try:
        images = paginator.get_page(page)
    except PageNotAnInteger:
        images = paginator.get_page(1)

    if images_only:
        context = {'images': images}
        return render(request, 'image/list_images.html', context)
    else:
        context = {
            'images': images,
            'selected': 'images',
        }
        return render(request, 'image/list.html', context)
