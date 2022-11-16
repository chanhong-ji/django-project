from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from categories.urls import urlpatterns__categories
from rooms.urls import urlpatterns_amenities, urlpatterns_rooms
from experiences.urls import urlpatterns_perk
from medias.urls import url_patterns as urlpatterns__medias


urlpatterns = [
    path("admin/", admin.site.urls),
    path("categories/", include(urlpatterns__categories)),
    path("amenities/", include(urlpatterns_amenities)),
    path("perks/", include(urlpatterns_perk)),
    path("rooms/", include(urlpatterns_rooms)),
    path("medias/", include(urlpatterns__medias)),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
