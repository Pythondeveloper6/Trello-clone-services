from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.UserRegisterationView.as_view(), name="user_register"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("profile/", views.UserProfileView.as_view(), name="user_profile"),
    path(
        "change-password/", views.PasswordChangeView.as_view(), name="password_change"
    ),
]
