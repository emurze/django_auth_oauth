import logging
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()
lg = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This command create superuser'

    def handle(self, *_, **__) -> None:
        if not User.objects.exists():
            user = User.objects.create_superuser(
                username=os.getenv('ADMIN_NAME', settings.DEFAULT_ADMIN_NAME),
                email=os.getenv('ADMIN_EMAIL', settings.DEFAULT_ADMIN_EMAIL),
                password=os.getenv('ADMIN_PASSWORD',
                                   settings.DEFAULT_ADMIN_PASSWORD),
            )
            lg.debug(f'Admin {user.username} was created.')
