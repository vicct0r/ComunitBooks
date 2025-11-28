from django.test import TestCase
from django.contrib.auth import get_user_model

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
    


