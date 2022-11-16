from django.urls import path
from rooms.views import (
    Amenities,
    AmenityDetail,
    RoomDetail,
    RoomReviews,
    Rooms,
)

urlpatterns_amenities = [
    path("", Amenities.as_view()),
    path("<int:pk>/", AmenityDetail.as_view()),
]

urlpatterns_rooms = [
    path("", Rooms.as_view()),
    path("<int:pk>", RoomDetail.as_view()),
    path("<int:pk>/reviews", RoomReviews.as_view()),
]
