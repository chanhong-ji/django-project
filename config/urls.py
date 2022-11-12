from django.contrib import admin
from django.urls import path, include
from experiences.urls import urlpatterns_perk

urlpatterns = [
    path("admin/", admin.site.urls),
    path("perks/", include(urlpatterns_perk)),
]
