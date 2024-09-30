from django.urls import path
from .views import CategoryProductsView, ProductDetailView, AddToCart

app_name = "products"

urlpatterns = [
    path("<int:id>/", CategoryProductsView.as_view(), name="category_products"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    path("add_to_cart/<int:pk>/", AddToCart.as_view(), name="add_to_cart"),
]
