from rest_framework import serializers
from users.serializers import PublicUserSerializer
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = PublicUserSerializer(
        read_only=True,
    )
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = (
            "pk",
            "user",
            "payload",
            "rating",
            "created_at",
        )
