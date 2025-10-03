from django.urls import path
from . import views

app_name = 'cart' # namespacing

urlpatterns = [
    path("cart/", views.cart_detail, name="cart_detail"),
    path("add/<int:variant_id>/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
    # path("success/", views.order_success, name=)
]