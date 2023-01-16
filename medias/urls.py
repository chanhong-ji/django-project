from django.urls import path
from medias.views import PhotoDetail, PhotoUrls, Photo


urlpatterns = [
    path("photos", Photo.as_view()),
    path("photos/<int:pk>", PhotoDetail.as_view()),
    path("photos/get-urls", PhotoUrls.as_view()),
]
