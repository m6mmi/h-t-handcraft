from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, LoginView, LogoutView, ChangePasswordView, UserProfileView

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path('profile/', UserProfileView.as_view(), name='profile'),

    path('reset_password/', auth_views.PasswordResetView.as_view
         (template_name="reset_password.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view
         (template_name="password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view
         (template_name="password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view
         (template_name="password_reset_done.html"), name='password_reset_complete')
]
