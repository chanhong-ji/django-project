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
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "name",
            "avatar",
            "gender",
            "language",
            "currency",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=20,
        min_length=10,
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        max_length=20,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password_confirm",
            "name",
            "avatar",
            "gender",
            "language",
            "currency",
            "first_name",
            "last_name",
        )

    def validate(self, data):
        password = data["password"]
        password_confirm = data["password_confirm"]
        if password != password_confirm:
            raise serializers.ValidationError("Password confirm Wrong")
        data.pop("password")
        data.pop("password_confirm")
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=20,
    )
    new_password = serializers.CharField(
        max_length=20,
        min_length=10,
    )
    new_password_confirm = serializers.CharField(
        max_length=20,
    )


class LoginSerializer(serializers.Serializer):
    # email = serializers.EmailField(max_length=300)
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
