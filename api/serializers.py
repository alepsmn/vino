from rest_framework import serializers
from core.models import *  # O importa explícitamente para mejor control

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'type', 'brand', 'country', 'do', 'grape', 'notes', 'created_at', 'updated_at']  # Explícito para seguridad
        read_only_fields = ['created_at', 'updated_at']  # No editables

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'sku', 'vintage', 'volume_ml', 'abv', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

# Resto similar, con fields explícitos y read_only
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'code', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'variant', 'store', 'channel', 'currency', 'cost_amount', 'margin_percentage', 'sale_amount', 'valid_from', 'valid_to', 'created_at', 'updated_at']
        read_only_fields = ['sale_amount', 'created_at', 'updated_at']  # sale_amount se calcula automáticamente

class StockLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockLedger
        fields = ['id', 'variant', 'store', 'qty', 'type', 'occurred_at', 'ref_type', 'ref_id', 'idempotency_key', 'created_at', 'updated_at']
        read_only_fields = ['occurred_at', 'created_at', 'updated_at']

class StockBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockBalance
        fields = ['id', 'variant', 'store', 'on_hand', 'reserved', 'updated_at']
        read_only_fields = ['updated_at']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'store', 'channel', 'status', 'totals', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = ['id', 'order', 'variant', 'qty', 'unit_price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['id', 'store_from', 'store_to', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TransferLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferLine
        fields = ['id', 'transfer', 'variant', 'qty', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
