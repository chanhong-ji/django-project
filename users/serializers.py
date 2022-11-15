from rest_framework import serializers

from users.models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "avatar",
            "username",
        )
