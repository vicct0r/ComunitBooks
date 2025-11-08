from .models import Loan, Order
from django.db import transaction


def update_order_status(order: 'Order', operation=False) -> None:
    """
    Update models.Order.status and models.Book.status depending on the Operation (Bool).
    """
    with transaction.atomic():
        order.status = Order.APPROVED if operation else Order.DENIED
        order.book.status = 'RESERVED' if operation else order.book.status
        order.save()
        order.book.save()
