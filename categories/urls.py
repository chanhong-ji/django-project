from django.urls import path
from categories.views import CategoriesExperience, CategoriesRoom, CategoryDetail

urlpatterns = [
    path("room", CategoriesRoom.as_view()),
    path("experience", CategoriesExperience.as_view()),
    path("<int:pk>", CategoryDetail.as_view()),
]
