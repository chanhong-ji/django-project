from rest_framework import serializers
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from rooms.models import Amenity, Room
from users.serializers import PublicUserSerializer
from wishlists.models import Wishlist


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
    thumb_photo = serializers.SerializerMethodField(read_only=True)

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
            "thumb_photo",
        )

    def get_rating(self, room):
        rating = room.rating()
        return rating

    def get_is_owner(self, room):
        if "request" not in self.context:
            return False
        request = self.context["request"]
        return request.user == room.owner

    def get_is_liked(self, room):
        if (
            "request" not in self.context
            or not self.context["request"].user.is_authenticated
        ):
            return False
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()

    def get_thumb_photo(self, room):
        thumb_photos = room.photos.filter(thumb=True).values()
        if thumb_photos:
            return thumb_photos[0]["file"]
        return None


class RoomDetailSerializer(serializers.ModelSerializer):

    owner = PublicUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    thumb_photo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        rating = room.rating()
        return rating

    def get_is_owner(self, room):
        if "request" not in self.context:
            return False
        request = self.context["request"]
        return request.user == room.owner

    def get_thumb_photo(self, room):
        thumb_photos = room.photos.filter(thumb=True).values()
        if thumb_photos:
            return thumb_photos[0]["file"]
        return None
