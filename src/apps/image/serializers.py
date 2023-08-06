from django.contrib.auth.models import User
from rest_framework import serializers


class ImageUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
