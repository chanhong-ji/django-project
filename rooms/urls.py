from django.urls import path
from rooms.views import Amenities, AmenityDetail

urlpatterns_amenities = [
    path("", Amenities.as_view()),
    path("<int:pk>/", AmenityDetail.as_view()),
]
