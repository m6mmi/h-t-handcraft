from django.urls import path

from shopping_cart.views import OrderView, DeleteFromCart, UserOrders, CartView, Checkout

app_name = "shopping_cart"

urlpatterns = [
    path("order/<int:cart_id>/", OrderView.as_view(), name="order"),
    path("delete/<int:pk>", DeleteFromCart.as_view(), name="delete_from_cart"),
    path("orders/", UserOrders.as_view(), name="user_orders"),
    path("cart/", CartView.as_view(), name="cart"),
    path("checkout/", Checkout.as_view(), name="checkout"),
]
