from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'variants', ProductVariantViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'channels', ChannelViewSet)
router.register(r'prices', PriceViewSet)
router.register(r'stock-ledgers', StockLedgerViewSet)
router.register(r'stock-balances', StockBalanceViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-lines', OrderLineViewSet)
router.register(r'transfers', TransferViewSet)
router.register(r'transfer-lines', TransferLineViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Genera /api/products/, /api/products/<id>/, etc.
]
