from django.db import transaction
from django.utils import timezone
from django.utils.timezone import timedelta
from django.db import transaction

from books.models import Book
from ..models import Loan
from . import notification
from orders.models import Order
from books.models import Book

from usuarios.services import UserService


def update_order_status(order: 'Order', accepted=False):
    """
    Aceitar ou Recusar um pedido.
    """
    with transaction.atomic():
        order.status = Order.APPROVED if accepted else Order.DENIED
        order.book.status = Book.RESERVED if accepted else order.book.status
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
        UserService.increase_user_score(loan.owner.id, quantity=1)
        notification.sent(loan)
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
        notification.delivered(loan)
        return f"Entrega do livro {loan.book.title} foi confirmada."

    @staticmethod
    @transaction.atomic
    def borrower_return_book(loan_id: int) -> str:
        loan = Loan.objects.select_for_update().get(id=loan_id)

        if not loan.status in [Loan.ACTIVE, Loan.OVERDUE]:
            raise ValueError('Action not allowed')

        loan.status = Loan.IN_RETURN
        loan.save()
        loan.book.save()

        # se User devolveu mais cedo, então + pontos
        if loan.due_date > timezone.now().date():
            UserService.increase_user_score(loan.borrower.id, quantity=2)
        else:
            UserService.increase_user_score(loan.borrower.id, quantity=1)

        notification.returned(loan)
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
        notification.completed(loan)
        return f"Seu livro {loan.book.title} foi marcado como devolvido."
    
    @staticmethod
    def allowed_actions(loan: Loan, user_id=None) -> list[str]:
        """
        Delegando ações para Owner e Borrower de acordo com o estado do Loan_obj
        """

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
            elif status in [Loan.ACTIVE, Loan.OVERDUE]:
                return ['return_book']  
            elif status == Loan.APPROVED:
                return ['waiting_confirm'] 
            elif status == Loan.IN_RETURN:
                return [] 
        
        return []
