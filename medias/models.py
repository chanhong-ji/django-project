from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    file = models.URLField()
    description = models.CharField(
        max_length=140,
        blank=True,
        null=True,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="photos",
    )
    thumb = models.BooleanField(
        default=False,
    )

    def __str__(self):

        if self.room:
            return f"Image for room: {self.room.pk}"
        elif self.experience:
            return f"Image for experience: {self.experience.pk}"
        else:
            return ""


class Video(CommonModel):
    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="videos",
    )

    def __str__(self):
        return "Video File"
