from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class Contract(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.PROTECT,
                                  related_name='rel_from_set')
    user_to = models.ForeignKey(User, on_delete=models.PROTECT,
                                related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=('created',))
        ]

    def __str__(self) -> str:
        return f'{self.user_from} follows {self.user_to} at {self.created}'


User.add_to_class('following',
                  models.ManyToManyField(
                      User,
                      through=Contract,
                      related_name='followers',
                      symmetrical=False,
                  ))


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='actions')
    verb = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = ('content_type', 'object_id')

    class Meta:
        ordering = ('-created',)
        indexes = (
            models.Index(fields=('-created',)),
        )
