from django.urls import path
from .views import ChangePassword, Login, Logout, Me, Users, UserDetail

urlpatterns = [
    # users/
    path("", Users.as_view()),
    # users/me
    path("me", Me.as_view()),
    # users/:username
    path("@<str:username>", UserDetail.as_view()),
    # users/change-password
    path("change-password", ChangePassword.as_view()),
    # users/login
    path("login", Login.as_view()),
    # users/logout
    path("logout", Logout.as_view()),
]
