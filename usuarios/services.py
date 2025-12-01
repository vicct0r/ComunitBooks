from loans.models import Order, Loan

def orders_received(user) -> int:
    return Order.objects.filter(owner=user, status=Order.SUBMITTED).count()

def orders_submitted(user) -> int:
    return Order.objects.filter(borrower=user, status=Order.SUBMITTED).count()

def loans_received(user) -> int:
    return Loan.objects.filter(owner=user).exclude(status__in=[Loan.COMPLETED, Loan.CANCELLED]).count()

def loans_submitted(user) -> int:
    return Loan.objects.filter(borrower=user).exclude(status__in=[Loan.COMPLETED, Loan.CANCELLED]).count()