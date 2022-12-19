from django.db import models
from common.models import CommonModel


class Room(CommonModel):

    """Room Model Description"""

    def __str__(self):
        return self.name

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(
        max_length=50,
    )
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    descriptions = models.TextField(
        max_length=250,
    )
    address = models.TextField(
        max_length=250,
    )
    pet_friendly = models.BooleanField(
        default=False,
    )
    kind = models.CharField(
        max_length=50,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        blank=True,
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()

    def rating(self):
        ratings = [review["rating"] for review in self.reviews.all().values("rating")]
        if not ratings:
            return 0, 0
        return round(sum(ratings) / len(ratings), 2), len(ratings)


class Amenity(CommonModel):

    """Amenity Model Definition"""

    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Amenities"
