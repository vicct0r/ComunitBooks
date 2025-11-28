from django.db import models
from django.db.models import Q
from django.conf import settings

from books.models import Book


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

    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_borrower', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_owner', on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, related_name='book_orders', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    required_days = models.PositiveIntegerField(choices=LOAN_PERIOD_CHOICES, default=7)
    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default=SUBMITTED)

    def __str__(self):
        return f"Borrower: {self.borrower} - Book: {self.book.title}"


class Loan(models.Model):
    APPROVED = 'ap'
    ON_ROUTE = 'or'
    ACTIVE = 'ac'
    COMPLETED = 'cm'
    CANCELLED = 'cn'
    IN_RETURN = 'rt'
    OVERDUE = 'ov'

    LOAN_STATUS_CHOICES = (
        (APPROVED, 'Aprovado'),
        (ACTIVE, 'Ativo'),
        (ON_ROUTE, 'Em Rota'),
        (IN_RETURN, 'Em Devolução'),
        (COMPLETED, 'Completo'),
        (CANCELLED, 'Cancelada'),
        (OVERDUE, 'Atraso'),
    )
    
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_borrower')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_owner')
    book = models.ForeignKey(Book, related_name='book_loans', on_delete=models.CASCADE)
    approved_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    returned_date = models.DateField(blank=True, null=True)
    max_loan_period = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(choices=LOAN_STATUS_CHOICES, max_length=9, default=APPROVED)
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor cobrado para o empréstimo"
    )
    allows_renewal = models.BooleanField(default=True)
    custom_terms = models.TextField(help_text="Condições adicionais para o emprestimo.", blank=True, null=True)

    def __str__(self):
        return f"Loan: {self.book.title} to {self.book.owner.full_name}"

    def clean(self):
        if self.book_id and Loan.objects.filter(book_id=self.book_id, status__in=[Loan.ACTIVE, Loan.ON_ROUTE, Loan.OVERDUE]).exists():
            raise ValueError('Este livro já tem um Emprestimo!')
        return super().clean()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['book'],
                condition=Q(status__in=['ac', 'or', 'ov']),
                name='unique_active_loan_per_book',
            ),
        ]
