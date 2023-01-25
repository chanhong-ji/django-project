from rest_framework import serializers
from users.models import User


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "avatar",
            "username",
        )


class PrivateUserSerializer(serializers.ModelSerializer):
    social = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "name",
            "avatar",
            "gender",
            "social",
            "language",
            "currency",
            "is_host",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=20,
        min_length=10,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "name",
            "avatar",
            "gender",
            "language",
            "currency",
            "first_name",
            "last_name",
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=20,
    )
    new_password = serializers.CharField(
        max_length=20,
        min_length=10,
    )


class LoginSerializer(serializers.Serializer):
    # email = serializers.EmailField(max_length=300)
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
