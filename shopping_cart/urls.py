from django.urls import path

from shopping_cart.views import DeleteFromCart, CartView, Checkout, ShippingAddressView, ShippingItella, \
    ShippingIOmniva, ShippingDPD

app_name = "shopping_cart"

urlpatterns = [
    path("delete/<int:pk>", DeleteFromCart.as_view(), name="delete_from_cart"),

    path("cart/", CartView.as_view(), name="cart"),
    path("checkout/", Checkout.as_view(), name="checkout"),
    path("shipping/", ShippingAddressView.as_view(), name="shipping"),
    path("shipping_dpd/", ShippingDPD.as_view(), name="dpd"),
    path("shipping-itella/", ShippingItella.as_view(), name="itella"),
    path("shipping-omniva/", ShippingIOmniva.as_view(), name="omniva"),
]
