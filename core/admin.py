from django.contrib import admin
from .models import (Product, ProductVariant, Store, Channel, Price,
                     StockBalance, StockLedger, Order, OrderLine, Transfer, TransferLine)

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "grape", "active", "created_at")  # Campos visibles en lista
    list_filter = ("active", "grape", "brand")  # Filtros laterales
    search_fields = ("name", "brand", "grape")  # Búsqueda
    prepopulated_fields = {"slug": ("name",)}  # Auto-genera slug de name

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "sku", "vintage", "volume_ml", "abv")
    list_filter = ("vintage",)
    search_fields = ("sku", "product__name")

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("code", "created_at")
    search_fields = ("code",)

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("variant", "store", "channel", "sale_amount", "valid_from")
    list_filter = ("currency", "valid_from")
    search_fields = ("variant__sku",)

@admin.register(StockLedger)
class StockLedgerAdmin(admin.ModelAdmin):
    list_display = ("variant", "store", "qty", "type", "occurred_at")
    list_filter = ("type", "occurred_at")
    search_fields = ("variant__sku", "store__name")

@admin.register(StockBalance)
class StockBalanceAdmin(admin.ModelAdmin):
    list_display = ("variant", "store", "on_hand", "reserved", "updated_at")
    list_filter = ("store",)
    search_fields = ("variant__sku", "store__name")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("store", "channel", "status", "totals", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("store__name", "channel__code")

@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ("order", "variant", "qty", "unit_price", "created_at")
    search_fields = ("order__id", "variant__sku")

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("store_from", "store_to", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("store_from__name", "store_to__name")

@admin.register(TransferLine)
class TransferLineAdmin(admin.ModelAdmin):
    list_display = ("transfer", "variant", "qty", "created_at")
    search_fields = ("transfer__id", "variant__sku")