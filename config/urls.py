from django.contrib import admin
from django.urls import path, include
from categories.urls import urlpatterns__categories
from rooms.urls import urlpatterns_amenities, urlpatterns_rooms
from experiences.urls import urlpatterns_perk

urlpatterns = [
    path("admin/", admin.site.urls),
    path("categories/", include(urlpatterns__categories)),
    path("amenities/", include(urlpatterns_amenities)),
    path("perks/", include(urlpatterns_perk)),
    path("rooms/", include(urlpatterns_rooms)),
]
