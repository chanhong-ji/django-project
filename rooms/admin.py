from django.contrib import admin
from rooms.models import Amenity, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "pk",
        "price",
        "kind",
        "owner",
        "created_at",
        "total_amenities",
        "rating",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_friendly",
        "kind",
        "amenities",
        "category",
    )

    search_fields = (
        "name",
        "owner__username",
        "^price",
    )

    def total_amenities(self, room):
        return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    readonly_fields = (
        "updated_at",
        "created_at",
    )
