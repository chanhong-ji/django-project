from django.urls import path
from rooms.views import (
    Amenities,
    AmenityDetail,
    RoomBookings,
    RoomBookingCheck,
    RoomDetail,
    RoomPhotos,
    RoomReviews,
    Rooms,
)

urlpatterns = [
    # rooms/
    path("", Rooms.as_view()),
    # rooms/:pk
    path("<int:pk>", RoomDetail.as_view()),
    # rooms/:pk/reviews
    path("<int:pk>/reviews", RoomReviews.as_view()),
    # rooms/:pk/photos
    path("<int:pk>/photos", RoomPhotos.as_view()),
    # rooms/:pk/bookings
    path("<int:pk>/bookings", RoomBookings.as_view()),
    # rooms/:pk/bookings/check?check_in={}&check_out={}
    path("<int:pk>/bookings/check", RoomBookingCheck.as_view()),
    # rooms/amenities/
    path("amenities/", Amenities.as_view()),
    # rooms/amenities/:pk
    path("amenities/<int:pk>", AmenityDetail.as_view()),
]
