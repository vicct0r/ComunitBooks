from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.template.defaultfilters import slugify

from stdimage import StdImageField


class Metadata(models.Model):
    access_count = models.IntegerField(default=0, editable=False)
    favorite_count = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return f"access count: {self.access_count}"

    class Meta:
        abstract = True

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(Metadata):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BookQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) |\
        Q(author__icontains=query) |\
        Q(owner__full_name__icontains=query) |\
        Q(slug__icontains=query)
        return self.filter(lookups)
    
    def filter_by_params(self, title=None, author=None, owner=None, status=None, condition=None, popularity=None):
        query = self.all()

        if title:
            query = query.filter(title__icontains=title)
        
        if author:
            query = query.filter(author__icontains=author)

        if owner:
            query = query.filter(owner__full_name__icontains=owner)
        
        if status:
            query = query.filter(status=status)
        
        if condition:
            query = query.filter(condition=condition)
        
        if popularity:
            return query.order_by('+acess_count')
        return query


class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)
    
    def search(self, query=None):
        return self.get_queryset().search(query)
    
    def filter_by_params(self, **kwargs):
        return self.get_queryset().filter_by_params(**kwargs)


class Book(Base, Metadata):
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
    category = models.ManyToManyField(Category, related_name='books')

    def __str__(self):
        return self.title
    
    def get_categories(self):
        return self.category

    def get_absolute_url(self):
        return reverse(viewname="books:detail", args=[self.pk, self.slug])
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    objects = BookManager()


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


