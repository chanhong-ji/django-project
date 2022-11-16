from rest_framework import serializers
from categories.serializers import CategorySerializer
from rooms.serializers import RoomListSerializer
from users.serializers import TinyUserSerializer
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )
