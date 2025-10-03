from django.shortcuts import render, redirect
from .utils import CartHandler
from .models import Order, OrderItem, Payment
from core.models import ProductVariant

# Create your views here.

def cart_detail(request):
    cart = CartHandler(request)
    return render(request, 'cart/detail.html', {'cart': cart})

def add_to_cart(request, variant_id):
    variant = ProductVariant.objects.get(id=variant_id)
    cart = CartHandler(request)
    cart.add(variant)
    return redirect('cart:cart_detail')

def checkout(request):
    cart = CartHandler(request)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total=cart.total())
        for vid, item in cart.cart.items():
            variant = ProductVariant.objects.get(id=vid)
            OrderItem.objects.create(order=order, variant=variant, quantity=item['quantity'], unit_price=item['price'])
        # Integra pago (ej. Stripe aquí)
        Payment.objects.create(order=order, amount=order.total)
        cart.clear()  # Limpia cart
        return redirect('order_success')
    return render(request, 'cart/checkout.html', {'cart': cart})