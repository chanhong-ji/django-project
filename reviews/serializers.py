from rest_framework import serializers
from users.serializers import PublicUserSerializer
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = PublicUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            "pk",
            "user",
            "payload",
            "rating",
            "created_at",
        )
