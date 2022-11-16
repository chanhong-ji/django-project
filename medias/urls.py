from django.urls import path
from medias.views import PhotoDetail


url_patterns = [
    path("photos/<int:pk>", PhotoDetail.as_view()),
]
