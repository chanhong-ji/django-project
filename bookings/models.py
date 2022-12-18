from django.db import models
from common.models import CommonModel


class Booking(CommonModel):

    """Booking Model Definition"""

    def __str__(self):
        return f"{self.kind.title()} for : {self.user}"

    class BookingKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")

    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="bookings",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="bookings",
    )
    check_in = models.DateField(
        blank=True,
        null=True,
    )
    check_out = models.DateField(
        blank=True,
        null=True,
    )
    experience_date = models.DateField(
        blank=True,
        null=True,
    )
    guests = models.PositiveIntegerField()
