from django.db import models
from django.contrib.auth import get_user_model
import uuid

from books.models import Book

User = get_user_model()

class Order(models.Model):
    SUBMITTED = 'pr'
    APPROVED = 'ap'
    DENIED = 'dn'
    CANCELED = 'cn'

    ORDER_STATUS_CHOICES = (
        (SUBMITTED, 'Enviado'),
        (APPROVED, 'Aprovado'),
        (CANCELED, 'Cancelado'),
        (DENIED, 'Negado')
    )

    LOAN_PERIOD_CHOICES = (
        (7, '1 semana'),
        (14, '2 semanas'),
        (21, '3 semanas'),
        (30, '1 mês')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    borrower = models.ForeignKey(User, related_name='order_borrower', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='order_owner', on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, related_name='book_orders', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    required_days = models.PositiveIntegerField(choices=LOAN_PERIOD_CHOICES, default=7)
    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default=SUBMITTED)

    def __str__(self):
        return f"Borrower: {self.borrower} - Book: {self.book.title}"