from rest_framework import serializers
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.models import Photo
from users.serializers import TinyUserSerializer


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )
