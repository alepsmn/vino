from django.urls import path
from . import views

app_name = 'cart' # namespacing

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:variant_id>/", views.add_to_cart, name="add_to_cart"),
    path("update/<str:vid>/", views.update_cart, name="update_cart"),
    path("remove/<str:vid>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    # path("success/", views.order_success, name=)
]