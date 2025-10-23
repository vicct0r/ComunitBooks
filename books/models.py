from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify

from stdimage import StdImageField


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Book(Base):
    CONDITION_CHOICES = (
        ('NEW', 'New'),
        ('GOOD', 'Good'),
        ('FAIR', 'Regular'),
        ('DAMAGED', 'Damaged')
    )

    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('UNAVAILABLE', 'Unavailable'),
        ('RESERVED', 'Reserved'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text="Título do livro")
    author = models.CharField(max_length=200, blank=True, null=True)
    cover_image = StdImageField(
        upload_to="books/",
        blank=True,
        null=True,
        variations={
            'optimized': {  
                'width': 400,
                'height': 560,
                'crop': False
            }
        },
        delete_orphans=True
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=7, help_text="Condição do livro")
    status = models.CharField(choices=STATUS_CHOICES, max_length=12)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(viewname="books:detail", args=[self.pk, self.slug])
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Loan(models.Model):
    LOAN_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('OVERDUE', 'Overdue'),
    )
    
    approved_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    returned_date = models.DateField(blank=True, null=True)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loans_taken')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    max_loan_period = models.PositiveIntegerField(default=14, help_text="Duração máxima do emprestimo em dias")
    requires_deposit = models.BooleanField(default=True)
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor cobrado para o empréstimo"
    )
    allows_renewal = models.BooleanField(default=True)
    status = models.CharField(choices=LOAN_STATUS_CHOICES, max_length=9, default='PENDING')
    custom_terms = models.TextField(help_text="Condições adicionais para o emprestimo")

    def __str__(self):
        return f"Loan: {self.book.title} to {self.borrower.email}"
    
    @property
    def lender(self):
        return self.book.owner
    
   