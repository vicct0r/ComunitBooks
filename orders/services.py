from django.db import transaction
from .models import Order

from books.models import Book


def cancel_order(order: Order):
    with transaction.atomic():
        order.status = Order.CANCELED
        order.save()


def update_order_status(order: 'Order', accepted=False):
    """
    Update models.Order.status and models.Book.status depending on the decision. (Bool).
    """
    with transaction.atomic():
        order.status = Order.APPROVED if accepted else Order.DENIED
        order.book.status = Book.RESERVED if accepted else order.book.status
        order.save()
        order.book.save()