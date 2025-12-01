from django.db import transaction
from .models import Order


def cancel_order(order: Order):
    with transaction.atomic():
        order.status = Order.CANCELED
        order.save()
