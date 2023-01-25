from django.urls import path
from medias.views import PhotoDetail, PhotoUrls, Photo


urlpatterns = [
    # medias/photos
    path("photos", Photo.as_view()),
    # media/photos/:int
    path("photos/<int:pk>", PhotoDetail.as_view()),
    # media/photos/get-urls
    path("photos/get-urls", PhotoUrls.as_view()),
]
