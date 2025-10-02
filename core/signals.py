from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockLedger, StockBalance

@receiver(post_save, sender=StockLedger)
def update_stock_balance(sender, instance, **kwargs):  # Quité 'created' para actualizar siempre
    balance, _ = StockBalance.objects.get_or_create(
        variant=instance.variant,
        store=instance.store,
        defaults={'on_hand': 0, 'reserved': 0}
    )
    if instance.type == 'entrada':
        balance.on_hand += instance.qty
    elif instance.type == 'salida':
        balance.on_hand -= instance.qty
    # en caso de necesitar mas tipos, agregar como:
    # elif instance.type == 'reserva':
    #     balance.reserved += instance.qty
    balance.save()
