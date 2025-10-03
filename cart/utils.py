from decimal import Decimal
from django.conf import settings
from core.models import ProductVariant

class CartHandler:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, variant, quantity=1, override=False):
        vid = str(variant.id)
        price_str = str(variant.price_set.latest('valid_from').sale_amount)  # String para sesión
        if vid not in self.cart:
            self.cart[vid] = {'quantity': 0, 'price': price_str}
        if override:
            self.cart[vid]['quantity'] = quantity
        else:
            self.cart[vid]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def total(self):
        total_amount = Decimal('0')
        for item in self.cart.values():
            total_amount += Decimal(item['price']) * item['quantity']  # Decimal para precisión
        return total_amount
    
    def get_items(self):
        items = []
        for vid, item in self.cart.items():
            variant = ProductVariant.objects.get(id=vid)  # Cachea si es necesario
            price = Decimal(item['price'])
            quantity = item['quantity']
            subtotal = price * Decimal(quantity)
            items.append({
                'vid': vid,
                'variant': variant,
                'price': price,
                'quantity': quantity,
                'subtotal': subtotal
            })
        return items

    def total(self):
        return sum(Decimal(item['price']) * Decimal(item['quantity']) for item in self.cart.values())

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.save()
