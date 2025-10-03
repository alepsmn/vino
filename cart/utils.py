# cart/utils.py
from decimal import Decimal
from django.conf import settings

class CartHandler:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, variant, quantity=1, override=False):
        vid = str(variant.id)
        if vid not in self.cart:
            self.cart[vid] = {'quantity': 0, 'price': str(variant.price_set.latest('valid_from').sale_amount)}
        if override:
            self.cart[vid]['quantity'] = quantity
        else:
            self.cart[vid]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def total(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
