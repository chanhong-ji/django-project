from django.urls import path
from wishlists.views import WishlistDetail, WishlistToggle, Wishlists

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>", WishlistDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", WishlistToggle.as_view()),
]
