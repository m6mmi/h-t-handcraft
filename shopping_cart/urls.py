from django.urls import path

from shopping_cart.views import OrderView, DeleteFromCart, UserOrders, CartView, Checkout

app_name = "shopping_cart"

urlpatterns = [
    path("delete/<int:pk>", DeleteFromCart.as_view(), name="delete_from_cart"),

    path("cart/", CartView.as_view(), name="cart"),
    path("checkout/", Checkout.as_view(), name="checkout"),
]
