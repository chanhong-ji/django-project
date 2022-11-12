from django.urls import path
from categories.views import Categories, CategoryDetail

urlpatterns__categories = [
    path("", Categories.as_view()),
    path("<int:pk>", CategoryDetail.as_view()),
]
