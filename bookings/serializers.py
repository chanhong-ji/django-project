from django.utils import timezone
from rest_framework import serializers
from experiences.serializers import ExperienceListSerializer
from medias.models import Photo
from medias.serializers import PhotoSerializer
from rooms.serializers import RoomListSerializer

from users.serializers import PublicUserSerializer
from .models import Booking


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_date",
        )


class PrivateBookingSerializer(serializers.ModelSerializer):
    room = RoomListSerializer()
    experience = ExperienceListSerializer()

    class Meta:
        model = Booking
        exclude = ("created_at",)


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience_date = serializers.DateField(required=True)
    guests = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = Booking
        fields = (
            "experience_date",
            "guests",
        )

    def validate_experience_date(self, value):
        now = timezone.localdate(timezone.now())
        if value < now:
            raise serializers.ValidationError("Wrong input")
        experience = self.context.get("experience")
        if Booking.objects.filter(experience=experience, experience_date=value):
            raise serializers.ValidationError("This experience is already taken")
        return value


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localdate(timezone.now())
        if value < now:
            raise serializers.ValidationError("Wrong input")
        return value

    def validate_check_out(self, value):
        now = timezone.localdate(timezone.now())
        if value < now:
            raise serializers.ValidationError("Wrong input")
        return value

    def validate(self, data):
        check_in = data["check_in"]
        check_out = data["check_out"]
        if check_out <= check_in:
            raise serializers.ValidationError(
                "The check-in date must come before the check-out date"
            )

        if Booking.objects.filter(
            room=self.context["room"],
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists():
            raise serializers.ValidationError(
                "Reservation for that day is already taken"
            )

        return data
