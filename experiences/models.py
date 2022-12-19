from django.db import models
from common.models import CommonModel


class Experience(CommonModel):

    """Experience Model Definition"""

    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=250,
    )
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    description = models.TextField()
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=300,
    )
    # start = ArrayField(
    #     models.TimeField(
    #         blank=True,
    #         null=True,
    #     ),
    #     size=5,
    # )
    start = models.TimeField()
    duration = models.DurationField()
    perks = models.ManyToManyField(
        "experiences.Perk",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def rating(self):
        ratings = [review["rating"] for review in self.reviews.all().values("rating")]
        if not ratings:
            return 0, 0
        return round(sum(ratings) / len(ratings), 2), len(ratings)


class Perk(CommonModel):

    """What is included in an Experience"""

    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        null=True,
        blank=True,
    )
