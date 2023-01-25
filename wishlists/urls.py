from django.urls import path
from wishlists.views import (
    WishlistDetail,
    WishlistExperienceToggle,
    WishlistRoomToggle,
    Wishlists,
)

urlpatterns = [
    # wishlists/
    path("", Wishlists.as_view()),
    # wishlists/:int
    path("<int:pk>", WishlistDetail.as_view()),
    # wishlists/:int/rooms/:int
    path("<int:pk>/rooms/<int:room_pk>", WishlistRoomToggle.as_view()),
    # wishlists/:int/experiences/int
    path(
        "<int:pk>/experiences/<int:experience_pk>", WishlistExperienceToggle.as_view()
    ),
]
