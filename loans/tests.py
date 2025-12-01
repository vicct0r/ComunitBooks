from django.test import TestCase
from django.contrib.auth import get_user_model

from .services.loan_service import LoanService
from .models import Loan, Order
from books.models import Book

User = get_user_model()

class OrderTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create(
            email='vic@hotmail.com',
            telefone='100001200',
            full_name='Vue Js. Mota'
        )

        self.borrower = User.objects.create(
            email='jvc@gmail.com',
            telefone='103022200',
            full_name='C. Sharp Linode'
        )

        self.book = Book.objects.create(
            owner=self.owner,
            title="Os Três Carneirinhos III",
            author="Garen P. Philipis",
            condition='NEW',
            status='AVAILABLE',
        )

        self.order = Order.objects.create(
            borrower=self.borrower,
            owner=self.owner,
            book=self.book,
            description="Order for the ChristmasX. We'll keep in touch!",
            required_days=7
        )

    def test_order_info(self):
        self.assertNotIn(self.order.required_days, [14, 21, 30])
        self.assertEqual(self.order.status, 'pr')
        self.assertEqual(self.order.owner, self.order.book.owner)
        self.assertEqual(self.order.borrower.email, self.borrower.email)
        self.assertNotEqual(self.order.owner.email, self.borrower.email)

    def test_order_creation(self):
        self.assertEqual(self.order.status, Order.SUBMITTED)
        self.assertEqual(self.borrower.id, self.order.borrower.id)


class LoanTests(TestCase):
    User = get_user_model()
    
    def setUp(self):

        self.owner_user = self.User.objects.create_user(
            email='owner@example.com',
            password='owner_password',
            telefone='(61)1111-2222',
        )

        self.borrower_user = self.User.objects.create_user(
            email='borrower@example.com',
            password='borrower_password',
            telefone='(61)3333-4444',
        )

        self.book_instance = Book.objects.create(
            title="O Nome do Vento",
            author="Patrick Rothfuss",
            owner=self.owner_user,
            condition=Book.NEW,
            status=Book.AVAILABLE
        )

        self.loan_instance = Loan.objects.create(
            borrower=self.borrower_user,
            owner=self.owner_user, 
            book=self.book_instance,
            status=Loan.APPROVED,
            max_loan_period=14, 
            allows_renewal=True,
            deposit_amount=10.00
        )

    def test_deny_loan(self):
        service_instance = LoanService.deny_delivery(self.loan_instance.id)
        self.loan_instance.refresh_from_db()
        self.assertNotIn(self.loan_instance.status, [Loan.ACTIVE, Loan.ON_ROUTE])
        self.assertEqual(self.loan_instance.status, Loan.CANCELLED)
        self.assertEqual(self.loan_instance.book.status, Book.AVAILABLE)
        self.assertNotEqual(self.loan_instance.book.status, Book.UNAVAILABLE)
        self.assertIn('cancelado', service_instance)
    
    def test_accept_loan(self):
        self.loan_instance.status = Loan.APPROVED
        service_instance = LoanService.send_book(self.loan_instance.id)
        self.loan_instance.refresh_from_db()
        self.assertEqual(self.loan_instance.status, Loan.ON_ROUTE)
        self.assertEqual(self.loan_instance.book.status, Book.UNAVAILABLE)
        self.assertNotEqual(self.loan_instance.status, Loan.APPROVED)
        self.assertNotEqual(self.loan_instance.book.status, Book.RESERVED)
        self.assertIn('Envio', service_instance)

    def test_confirm_delivery(self):
        service_instance = LoanService.borrower_confirm_delivery(self.loan_instance.id)
        self.loan_instance.refresh_from_db()
        self.assertEqual(self.loan_instance.status, Loan.ACTIVE)
        self.assertNotEqual(self.loan_instance.status, Loan.ON_ROUTE)
        self.assertTrue(self.loan_instance.start_date)
        self.assertTrue(self.loan_instance.due_date)
        self.assertIn('Entrega', service_instance)

    def test_return_book(self):
        self.loan_instance.status = Loan.ACTIVE
        service_instance = LoanService.borrower_return_book(self.loan_instance.id)
        self.loan_instance.refresh_from_db()
        self.assertEqual(self.loan_instance.status, Loan.IN_RETURN)
        self.assertNotIn(self.loan_instance.status, [Loan.ACTIVE, Loan.ON_ROUTE, Loan.APPROVED])
    
    def test_confirm_return(self):
        self.loan_instance.status = Loan.IN_RETURN
        service_instance = LoanService.lender_confirm_delivery(self.loan_instance.id)
        self.loan_instance.refresh_from_db()
        self.assertTrue(self.loan_instance.returned_date)
        self.assertEqual(self.loan_instance.status, Loan.COMPLETED)
        self.assertEqual(self.loan_instance.book.status, Book.AVAILABLE)