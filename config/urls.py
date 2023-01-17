from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("categories/", include("categories.urls")),
    path("rooms/", include("rooms.urls")),
    path("experiences/", include("experiences.urls")),
    path("medias/", include("medias.urls")),
    path("wishlists/", include("wishlists.urls")),
    path("users/", include("users.urls")),
    path("bookings/", include("bookings.urls")),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
