from rest_framework import serializers
from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
