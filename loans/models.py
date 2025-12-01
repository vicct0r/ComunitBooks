from django.db import models
from django.db.models import Q
from django.conf import settings
import uuid

from books.models import Book


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
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
