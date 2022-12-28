from rest_framework import serializers
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from rooms.models import Amenity, Room
from users.serializers import PublicUserSerializer
from wishlists.models import Wishlist
from django.contrib.auth.models import AnonymousUser


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "pk",
            "name",
            "description",
        )


class RoomListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "is_liked",
        )

    def get_rating(self, room):
        raiting, count = room.rating()
        return f"{raiting}({count})"

    def get_is_owner(self, room):
        if "request" not in self.context:
            return False
        request = self.context["request"]
        return request.user == room.owner

    def get_is_liked(self, room):
        if (
            "request" not in self.context
            or self.context["request"].user == AnonymousUser()
        ):
            return False
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()


class RoomDetailSerializer(serializers.ModelSerializer):

    owner = PublicUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    photos = PhotoSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        raiting, count = room.rating()
        return f"{raiting}({count})"

    def get_is_owner(self, room):
        if "request" not in self.context:
            return False
        request = self.context["request"]
        return request.user == room.owner
