from django.conf import settings
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.PROTECT)
    birthday = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='account_photo/%Y%m%d/', blank=True,
                              null=True)

    def __str__(self) -> str:
        return self.user.username
