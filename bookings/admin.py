from django.contrib import admin
from bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "__str__",
        "room",
        "experience",
        "check_in",
        "check_out",
        "experience_date",
        "guests",
    )
    list_filter = ("kind",)
