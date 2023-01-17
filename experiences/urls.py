from django.urls import path
from experiences.views import (
    ExperienceBookings,
    ExperienceDetail,
    ExperiencePhotos,
    ExperienceReviews,
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
    # experiences/:pk/photos
    path("<int:pk>/photos", ExperiencePhotos.as_view()),
    # experiences/:pk/video
    path("<int:pk>/photos", ExperiencePhotos.as_view()),
    # experiences/:pk/perks
    path("<int:pk>/perks", ExperiencePerks.as_view()),
    # experiences/:pk/bookings
    path("<int:pk>/bookings", ExperienceBookings.as_view()),
    # experiences/:pk/reviews
    path("<int:pk>/reviews", ExperienceReviews.as_view()),
    # experiences/perks
    path("perks/", Perks.as_view()),
    # experiences/perks/:pk
    path("perks/<int:pk>", PerkDetail.as_view()),
]
