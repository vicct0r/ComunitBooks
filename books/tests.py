from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Book

User = get_user_model()

class BookTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='v1ctor@gmail.com',
            full_name='victor inacio',
            telefone='10202031311',
        )

        self.client_user = User.objects.create(
            email='faaa21@hotmail.com',
            full_name='Fabio Jr. Mota Carvalho',
            telefone='2102031311',
        )

        self.book = Book.objects.create(
            owner=self.user,
            title='Data Structures II',
            author='Dijkstra C. King',
            condition='NEW',
            status='AVAILABLE',
        )

    def test_book_info(self):
        self.assertEqual(self.book.owner.email, self.user.email)
        self.assertEqual(self.user.id, self.book.owner.id)
        self.assertNotIn(self.book.condition, ['GOOD', 'FAIR', 'DAMAGED'])
        self.assertNotIn(self.book.status, ['UNAVAILABLE', 'RESERVED'])
