from django.urls import path
from medias.views import PhotoDetail


urlpatterns = [
    path("photos/<int:pk>", PhotoDetail.as_view()),
]
