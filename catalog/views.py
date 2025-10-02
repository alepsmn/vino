from django.shortcuts import render, get_object_or_404
from core.models import Product, ProductVariant, Price, StockBalance
from django.db.models import Prefetch, Q, Min  # Para filtros y prefetch

# Create your views here.

def product_list(request):
    queryset = Product.objects.filter(active=True)
    
    # Filtros dinámicos (ej. ?grape=tempranillo&volume_min=750)
    grape = request.GET.get('grape')
    volume_min = request.GET.get('volume_min')
    if grape:
        queryset = queryset.filter(grape__icontains=grape)
    if volume_min:
        queryset = queryset.filter(variants__volume_ml__gte=volume_min)
    
    # Prefetch variants, prices y stock para eficiencia (evita N+1 queries)
    queryset = queryset.prefetch_related(
        Prefetch('variants', queryset=ProductVariant.objects.all(), to_attr='prefetched_variants'),
        Prefetch('variants__price_set', queryset=Price.objects.all(), to_attr='prefetched_prices'),  # Asume related_name en Price si lo agregas
        Prefetch('variants__stockbalance_set', queryset=StockBalance.objects.all(), to_attr='prefetched_stock')
    )
    
    # Agrega aggregate para min volume (opcional, sin helper en modelo)
    queryset = queryset.annotate(min_volume=Min('variants__volume_ml'))
    
    return render(request, 'catalog/product_list.html', {'products': queryset})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    
    # Prefetch para detalle (variantes, precios, stock)
    product.prefetched_variants = product.variants.all()
    for variant in product.prefetched_variants:
        variant.prefetched_prices = variant.price_set.all()  # Precios por variant
        variant.prefetched_stock = variant.stockbalance_set.all()  # Stock por variant/store
    
    return render(request, 'catalog/product_detail.html', {'product': product})