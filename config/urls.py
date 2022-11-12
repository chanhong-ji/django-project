from django.contrib import admin
from django.urls import path, include
from rooms.urls import urlpatterns_amenities
from experiences.urls import urlpatterns_perk

urlpatterns = [
    path("admin/", admin.site.urls),
    path("amenities/", include(urlpatterns_amenities)),
    path("perks/", include(urlpatterns_perk)),
]
