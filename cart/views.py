from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .utils import CartHandler
from .models import Order, OrderItem, Payment
from core.models import ProductVariant, StockBalance

# Create your views here.

def cart_detail(request):
    cart = CartHandler(request)
    return render(request, 'cart/detail.html', {
        'items': cart.get_items(),
        'total': cart.total()
    })

@require_POST
def add_to_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    quantity = int(request.POST.get('quantity', 1))  # Lee del POST, default 1
    if quantity < 1:
        quantity = 1
    
    # Validación de stock (opcional pero recomendada)
    stock = StockBalance.objects.filter(variant=variant).first()
    if stock and quantity > stock.on_hand:
        messages.error(request, f"Solo hay {stock.on_hand} unidades disponibles.")
        return redirect('product_detail', product_id=variant.product.id)  # Redirige de vuelta
    
    cart = CartHandler(request)
    cart.add(variant, quantity=quantity)
    messages.success(request, f"{quantity} unidades añadidas al carrito.")
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

def update_cart(request, vid):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        cart = CartHandler(request)
        variant = get_object_or_404(ProductVariant, pk=vid)  # Obtén el objeto aquí
        if quantity > 0:
            cart.add(variant, quantity=quantity, override=True)  # Pasa el objeto variant
        else:
            if vid in cart.cart:
                del cart.cart[vid]
            cart.save()
    return redirect('cart:cart_detail')

def remove_from_cart(request, vid):
    cart = CartHandler(request)
    if vid in cart.cart:
        del cart.cart[vid]
        cart.save()
    return redirect('cart:cart_detail')