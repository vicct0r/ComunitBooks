from django.db import transaction
from django.utils import timezone
from django.utils.timezone import timedelta

from books.models import Book
from .notification import sent, approve, completed, returned, delivered 
from ..models import Loan, Order


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
        order.book.status = 'RESERVED' if accepted else order.book.status
        order.save()
        order.book.save()


class LoanService:

    @staticmethod
    @transaction.atomic
    def deny_delivery(loan_id: int) -> str:
        loan = Loan.objects.select_for_update().get(id=loan_id)

        if not loan.status == Loan.APPROVED:
            raise ValueError('Action not allowed.')

        loan.status = Loan.CANCELLED
        loan.book.status = Book.AVAILABLE
        loan.save()
        loan.book.save()
        return f"O emprestimo do livro {loan.book.title} para {loan.borrower.email} foi cancelado."

    @staticmethod
    @transaction.atomic
    def send_book(loan_id: int) -> str:
        loan = Loan.objects.select_for_update().get(id=loan_id)

        if not loan.status == Loan.APPROVED:
            raise ValueError('Action not allowed.')

        loan.status = Loan.ON_ROUTE
        loan.book.status = Book.UNAVAILABLE
        loan.save()
        loan.book.save()
        sent(loan)
        return f"Envio confirmado. Emprestimo estará ativo assim que chegar para {loan.borrower.email}."

    @staticmethod
    @transaction.atomic
    def borrower_confirm_delivery(loan_id: int) -> str:
        loan = Loan.objects.select_for_update().get(id=loan_id)

        if not loan.status == Loan.ON_ROUTE:
            raise ValueError('Action not allowed.')

        loan.status = Loan.ACTIVE
        loan.start_date = timezone.now()
        loan.due_date = timezone.now().date() + timedelta(days=loan.max_loan_period)
        loan.save()
        loan.book.save()
        delivered(loan)
        return f"Entrega do livro {loan.book.title} foi confirmada."

    @staticmethod
    @transaction.atomic
    def borrower_return_book(loan_id: int) -> str:
        loan = Loan.objects.select_for_update().get(id=loan_id)

        if not loan.status == Loan.ACTIVE:
            raise ValueError('Action not allowed.')

        loan.status = Loan.IN_RETURN
        loan.save()
        loan.book.save()
        returned(loan)
        return f"Devolução do livro {loan.book.title} foi efetuada."

    @staticmethod
    @transaction.atomic
    def lender_confirm_delivery(loan_id: int) -> str:
        loan = Loan.objects.select_for_update().get(id=loan_id)

        if not loan.status == Loan.IN_RETURN:
            raise ValueError('Action not allowed.')

        loan.status = Loan.COMPLETED
        loan.book.status = Book.AVAILABLE
        loan.returned_date = timezone.now()
        loan.save()
        loan.book.save()
        completed(loan)
        return f"Seu livro {loan.book.title} foi marcado como devolvido."
    
    @staticmethod
    def allowed_actions(loan: Loan, user_id=None) -> list[str]:
        status = loan.status
        is_owner = (user_id == loan.owner.id)
        is_borrower = (user_id == loan.borrower.id)

        if is_owner:
            if status == Loan.APPROVED:
                return ['send', 'deny']  
            elif status == Loan.ON_ROUTE:
                return ['on_route']  
            elif status == Loan.IN_RETURN:
                return ['lender_confirm_delivery']  
            elif status == Loan.ACTIVE:
                return []  
    
        elif is_borrower:
            if status == Loan.ON_ROUTE:
                return ['confirm_delivery']
            elif status == Loan.ACTIVE:
                return ['return_book']  
            elif status == Loan.APPROVED:
                return ['waiting_confirm'] 
            elif status == Loan.IN_RETURN:
                return [] 
        
        return []