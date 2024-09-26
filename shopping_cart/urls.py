from django.urls import path

from shopping_cart.views import CartView, DeleteFromCart, UserOrders

app_name = "shopping_cart"

urlpatterns = [
    path("cart/<int:cart_id>/", CartView.as_view(), name="cart"),
    path("delete/<int:pk>", DeleteFromCart.as_view(), name="delete_from_cart"),
    path("orders/<int:user_id>", UserOrders.as_view(), name="user_orders"),
]
