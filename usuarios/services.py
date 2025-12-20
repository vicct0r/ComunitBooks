from loans.models import Loan
from orders.models import Order
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F


# retirar estes valores 
# possivelmente serao parte do ModelManager
# estes valores estao aqui somente para traze-los como 'metadados' da seção de UserProfile

def orders_received(user) -> int:
    return Order.objects.filter(owner=user, status=Order.SUBMITTED).count()

def orders_submitted(user) -> int:
    return Order.objects.filter(borrower=user, status=Order.SUBMITTED).count()

def loans_received(user) -> int:
    return Loan.objects.filter(owner=user).exclude(status__in=[Loan.COMPLETED, Loan.CANCELLED]).count()

def loans_submitted(user) -> int:
    return Loan.objects.filter(borrower=user).exclude(status__in=[Loan.COMPLETED, Loan.CANCELLED]).count()

User = get_user_model() # settings.AUTH_USER_MODEL ?

class UserService:

    @staticmethod
    @transaction.atomic
    def decrease_user_score(user_id: int, quantity: int = 2) -> None:
        User.objects.filter(id=user_id).update(
            score=F('score') - quantity
        )

    @staticmethod
    @transaction.atomic
    def increase_user_score(user_id: int, quantity: int) -> None:
        User.objects.filter(id=user_id).update(
            score=F('score') + quantity
        )
