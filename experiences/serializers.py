from rest_framework import serializers
from categories.serializers import CategorySerializer
from experiences.models import Experience, Perk
from users.serializers import PublicUserSerializer


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        exclude = ("updated_at", "created_at")


class TinyExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        exclude = ("updated_at", "created_at")


class ExperienceSerializer(serializers.ModelSerializer):
    perks = TinyExperienceSerializer(many=True, read_only=True)
    host = PublicUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Experience
        exclude = ("updated_at", "created_at")
