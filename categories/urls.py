from django.urls import path
from categories.views import CategoriesExperience, CategoriesRoom, CategoryDetail

urlpatterns = [
    # categories/room
    path("room", CategoriesRoom.as_view()),
    # categories/experience
    path("experience", CategoriesExperience.as_view()),
    # categories/:int
    path("<int:pk>", CategoryDetail.as_view()),
]
