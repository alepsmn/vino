from django.shortcuts import render  # Si usas templates, pero para API pura no es necesario
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly  # Ejemplo de permiso
from core.models import *  # O importa explícitamente
from .serializers import *  # Asumiendo serializers.py en api/

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lectura para todos, escritura autenticada

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class StockLedgerViewSet(viewsets.ModelViewSet):
    queryset = StockLedger.objects.all()
    serializer_class = StockLedgerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class StockBalanceViewSet(viewsets.ModelViewSet):
    queryset = StockBalance.objects.all()
    serializer_class = StockBalanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Ejemplo de filtrado: ?store=1 para balances por tienda
        store_id = self.request.query_params.get('store')
        if store_id:
            return StockBalance.objects.filter(store=store_id)
        return super().get_queryset()  # Filtrado dinámico [63]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Custom: Calcula totals automáticamente si necesitas
        serializer.save(totals=0)  # Ejemplo, expande con lógica real [67]

class OrderLineViewSet(viewsets.ModelViewSet):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TransferLineViewSet(viewsets.ModelViewSet):
    queryset = TransferLine.objects.all()
    serializer_class = TransferLineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
