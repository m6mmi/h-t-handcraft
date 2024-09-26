from django.urls import path

from shopping_cart.views import CartView

app_name = "shopping_cart"

urlpatterns = [
    path("<int:cart_id>/", CartView.as_view(), name="cart"),
]
