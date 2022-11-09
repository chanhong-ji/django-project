from django.db import models
from common.models import CommonModel


class Category(CommonModel):
    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experieces"

    def __str__(self):
        return f"{self.kind.title()}: {self.name}"

    name = models.CharField(
        max_length=50,
    )
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
    )

    class Meta:
        verbose_name_plural = "Categories"
