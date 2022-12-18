from django.urls import path
from experiences.views import (
    ExperienceBookingDetail,
    ExperienceBookings,
    ExperienceDetail,
    PerkDetail,
    Perks,
    Experiences,
    ExperiencePerks,
)

urlpatterns = [
    # experiences/
    path("", Experiences.as_view()),
    # experiences/:pk
    path("<int:pk>", ExperienceDetail.as_view()),
    # experiences/:pk/perks
    path("<int:pk>/perks", ExperiencePerks.as_view()),
    # experiences/:pk/bookings
    path("<int:pk>/bookings", ExperienceBookings.as_view()),
    # experiences/:pk/bookings/:pk
    path("<int:pk>/bookings/<int:booking_pk>", ExperienceBookingDetail.as_view()),
    # experiences/perks
    path("perks/", Perks.as_view()),
    # experiences/:pk
    path("perks/<int:pk>", PerkDetail.as_view()),
]
