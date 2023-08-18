from django.contrib import admin

from apps.image.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created')
    list_filter = ('created',)
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ('user',)
