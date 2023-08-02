from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='images')
    url = models.URLField(max_length=2000, unique=True)
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='images/%Y/%d/%m')
    created = models.DateTimeField(auto_now_add=True)
    user_likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='liked_images')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=('-created',))
        ]

    def __str__(self) -> str:
        return self.title


@receiver(pre_save, sender=Image)
def set_slug_by_title(_, instance: Image, *__, **___) -> None:
    if instance.slug is None:
        instance.slug = slugify(instance.title)
