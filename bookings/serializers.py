from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "experience_time",
        )


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
            check_in__lte=check_out,
            check_out__gt=check_in,
        ).exists():
            raise serializers.ValidationError(
                "Reservation for that day is already taken"
            )

        return data
