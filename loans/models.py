from django.db import models
from django.db.models import Q
from django.conf import settings

from books.models import Book


class Order(models.Model):
    SUBMITTED = 'pr'
    APPROVED = 'ap'
    DENIED = 'dn'

    ORDER_STATUS_CHOICES = (
        (SUBMITTED, 'Submitted'),
        (DENIED, 'Denied'),
        (APPROVED, 'Approved')
    )

    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_orders', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='book_orders', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    required_days = models.PositiveIntegerField()
    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default=SUBMITTED)


class Loan(models.Model):
    LOAN_PERIOD_CHOICES = (
        (7, '1 week'),
        (14, '2 weeks'),
        (21, '3 weeks'),
        (30, '1 month')
    )

    LOAN_STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('OVERDUE', 'Overdue'),
    )
    
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_loans')
    book = models.ForeignKey(Book, related_name='book_loans', on_delete=models.CASCADE)
    approved_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    returned_date = models.DateField(blank=True, null=True)
    max_loan_period = models.PositiveIntegerField(choices=LOAN_PERIOD_CHOICES, default=7)
    requires_deposit = models.BooleanField(default=True)
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor cobrado para o empréstimo"
    )
    allows_renewal = models.BooleanField(default=True)
    status = models.CharField(choices=LOAN_STATUS_CHOICES, max_length=9, default='ACTIVE')
    custom_terms = models.TextField(help_text="Condições adicionais para o emprestimo.", blank=True, null=True)

    def __str__(self):
        return f"Loan: {self.book.title} to {self.borrower.email}"
    
    @property
    def lender(self):
        return self.book.owner

    constraints = [
            models.UniqueConstraint(
                fields=['borrower', 'book'],
                condition=Q(status='ACTIVE'),
                name='unique_active_loan_per_book_and_client'
            )
        ]