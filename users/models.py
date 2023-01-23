from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = ("won", "Korean won")
        USD = ("usd", "Dollar")

    class SocialChoices(models.TextChoices):
        KA = ("kakao", "Kakao")
        GH = ("github", "Github")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    email = models.EmailField(
        max_length=300,
        unique=True,
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    avatar = models.URLField(
        blank=True,
        null=True,
    )
    is_host = models.BooleanField(
        default=False,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        blank=True,
        null=True,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        default=LanguageChoices.KR,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.WON,
    )
    social = models.CharField(
        max_length=10,
        choices=SocialChoices.choices,
        blank=True,
        null=True,
    )
