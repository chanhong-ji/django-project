from django.urls import path
from experiences.views import PerkDetail, Perks

urlpatterns_perk = [
    path("", Perks.as_view()),
    path("<int:pk>", PerkDetail.as_view()),
]
