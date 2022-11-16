from rest_framework import serializers
from rooms.serializers import RoomListSerializer
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    rooms = RoomListSerializer(
        many=True,
        read_only=True,
    )
    # experiences

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
            # "experiences",
        )
