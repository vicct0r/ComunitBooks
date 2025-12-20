from django.db import transaction
from .models import Order
from loans.models import Loan

class OrdersPolicy:

    @staticmethod
    def cancel_order(order: Order):
        with transaction.atomic():
            order.status = Order.CANCELED
            order.save()

    @staticmethod
    def check_orders_limit(user):
        MAX_ORDERS_LIMIT = 3
        USER_ACTIVE_LOANS = Loan.objects.filter(borrower=user).exclude(status__in=[Loan.COMPLETED, Loan.CANCELLED]).count()
        return USER_ACTIVE_LOANS < MAX_ORDERS_LIMIT
    