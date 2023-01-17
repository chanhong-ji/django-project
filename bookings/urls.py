from django.urls import path, include

from bookings.views import BookingDetail, BookingList

urlpatterns = [
    path("", BookingList.as_view()),
    path("<int:pk>", BookingDetail.as_view()),
]
