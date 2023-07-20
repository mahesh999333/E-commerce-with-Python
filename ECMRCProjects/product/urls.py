from django.urls import path
from .views import AddProduct
from .cart_views import AddToCart





urlpatterns = [
    path('add', AddProduct.as_view(), name="add_product"),
    path('cart/add', AddToCart.as_view(), name="add_to_cart"),
]