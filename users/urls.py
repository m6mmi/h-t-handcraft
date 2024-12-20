from django.urls import path
from shopping_cart.views import UserOrders, OrderView
from .views import RegisterView, LoginView, LogoutView, ChangePasswordView, UserProfileView, UserProfileUpdateView, \
    FeedbackView, FeedbackListView, InvoiceView

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path("orders/", UserOrders.as_view(), name="user_orders"),
    path("order/<int:id>/", OrderView.as_view(), name="order"),
    path('profile/update/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('feedback/list/', FeedbackListView.as_view(), name='feedback_list'),
    path('invoice/<int:order_id>/', InvoiceView.as_view(), name='invoice'),
]
