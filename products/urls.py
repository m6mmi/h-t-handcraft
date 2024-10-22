from django.urls import path
from .views import CategoryProductsView, ProductDetailView, AddToCart, ProductSearchView, CustomProductRequestView, \
    ThankYouView
from django.conf import settings
from django.conf.urls.static import static

app_name = "products"

urlpatterns = [
    path("category/<int:id>/", CategoryProductsView.as_view(), name="category_products"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    path("add_to_cart/<int:pk>/", AddToCart.as_view(), name="add_to_cart"),
    path("search/", ProductSearchView.as_view(), name="search"),
    path('custom-product-request/', CustomProductRequestView.as_view(), name='custom_product_request'),
    path('thank-you/', ThankYouView.as_view(), name='thank_you')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
