import os
from pathlib import Path

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['mysite.com', '0.0.0.0']


INSTALLED_APPS = [
    'apps.account.apps.AccountConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'debug_toolbar',
    'social_django',
    'django_extensions',
    'easy_thumbnails',
    'rest_framework',

    'apps.image.apps.ImageConfig',
    'apps.base.apps.BaseConfig',
    'apps.people.apps.PeopleConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

ALLOWED_IMAGE_EXTENSIONS = ('jpeg', 'jpg', 'png',)

CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True

LOGIN_REDIRECT_URL = reverse_lazy('dashboard')
LOGIN_URL = reverse_lazy('login')

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('people:detail', args=(u.username,)),
}

DEFAULT_ADMIN_NAME = 'adm1'
DEFAULT_ADMIN_PASSWORD = 'adm1'
DEFAULT_ADMIN_EMAIL = 'adm1@adm1.com'

if DEBUG:
    import socket  # only if you haven't already imported this
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + \
                   ["0.0.0.0", "127.0.0.1", "10.0.2.2"]
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
