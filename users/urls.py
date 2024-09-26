from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ChangePasswordView, UserProfileView

app_name = "templates"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path('profile/', UserProfileView.as_view(), name='profile'),
    ]
