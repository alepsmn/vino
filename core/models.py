from django.db import models
from django.utils.text import slugify

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, blank=True)
    brand = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    do = models.CharField(max_length=100, blank=True)
    grape = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # Nuevos para SEO
    slug = models.SlugField(unique=True, blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = f"{self.name} - {self.brand} ({self.grape})"
        super().save(*args, **kwargs)

class ProductVariant(models.Model): 
    # con related name puedo acceder como product.variants - related name: expandirlo al resto de FK
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=50, unique=True)
    vintage = models.IntegerField(blank=True, null=True)
    volume_ml = models.IntegerField(blank=True, null=True)
    abv = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

class Store(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"

class Channel(models.Model):
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"

class Price(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.CharField(max_length=3, default='EUR')
    cost_amount = models.DecimalField(max_digits=10, decimal_places=2)
    margin_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    sale_amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.cost_amount and self.margin_percentage:
            self.sale_amount = self.cost_amount*(1 + self.margin_percentage/100)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Prices"

class StockLedger(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    qty = models.IntegerField()
    type = models.CharField(max_length=50)  # ej. 'entrada', 'salida'
    occurred_at = models.DateTimeField(auto_now_add=True)
    ref_type = models.CharField(max_length=50, blank=True)
    ref_id = models.IntegerField(blank=True, null=True)
    idempotency_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Stock Ledger"
        verbose_name_plural = "Stock Ledgers"

class StockBalance(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    on_hand = models.IntegerField(default=0)
    reserved = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('variant', 'store')
        verbose_name = "Stock Balance"
        verbose_name_plural = "Stock Balances"

class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    totals = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lines')
    variant = models.ForeignKey(ProductVariant, on_delete=models.RESTRICT)
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order Line"
        verbose_name_plural = "Order Lines"

class Transfer(models.Model):
    store_from = models.ForeignKey(Store, related_name='transfers_from', on_delete=models.CASCADE)
    store_to = models.ForeignKey(Store, related_name='transfers_to', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transfer"
        verbose_name_plural = "Transfers"

class TransferLine(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.RESTRICT)
    qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transfer Line"
        verbose_name_plural = "Transfer Lines"