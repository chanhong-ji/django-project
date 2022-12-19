from rest_framework import serializers
from categories.serializers import CategorySerializer
from experiences.models import Experience, Perk
from users.serializers import PublicUserSerializer
from wishlists.models import Wishlist


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        exclude = ("updated_at", "created_at")


class ExperienceListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        exclude = (
            "updated_at",
            "created_at",
            "perks",
            "host",
            "description",
        )

    def get_rating(self, experience):
        rating, count = experience.rating()
        return f"{rating}({count})"

    def get_is_liked(self, experience):
        user = self.context.get("user")
        if not user:
            return False
        return Wishlist.objects.filter(
            user=user, experiences__pk=experience.pk
        ).exists()


class ExperienceDetailSerializer(serializers.ModelSerializer):
    perks = PerkSerializer(many=True, read_only=True)
    host = PublicUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        exclude = ("created_at",)

    def get_rating(self, experience):
        rating, count = experience.rating()
        return f"{rating}({count})"

    def get_is_liked(self, experience):
        user = self.context.get("user")
        if not user:
            return False
        return Wishlist.objects.filter(
            user=user, experiences__pk=experience.pk
        ).exists()

    def get_is_owner(self, experience):
        user = self.context.get("user")
        if not user:
            return False
        return user == experience.host
