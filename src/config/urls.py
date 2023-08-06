import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, reverse_lazy

urlpatterns = [
    path('registration/', include('apps.account.urls')),
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace='social')),

    path('', lambda request: redirect(reverse_lazy('dashboard'))),
    path('dashboard/', include('apps.base.urls')),
    path('images/', include('apps.image.urls', namespace='images')),
]

if settings.DEBUG:
    urlpatterns += [
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        path('__debug__/', include(debug_toolbar.urls))
    ]

