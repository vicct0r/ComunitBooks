from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.template.defaultfilters import slugify

from stdimage import StdImageField


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BookQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) |\
        Q(author__icontains=query) |\
        Q(slug__icontains=query) |\
        Q(category__icontains=query)
        return self.filter(lookups)
    
    def filter_by_params(self, title=None, author=None, status=None, condition=None, popularity=None, category=None):
        query = self.all()

        if title:
            query = query.filter(title__icontains=title)
        
        if author:
            query = query.filter(author__icontains=author)
        
        if status:
            query = query.filter(status=status)
        
        if condition:
            query = query.filter(condition=condition)
        
        if category:
            query = query.filter(category=category)
        
        if popularity:
            if popularity == "newest":
                query = query.order_by('-created')
            elif popularity == "views":
                query = query.order_by('-access_count')
            elif popularity == "favorites":
                query = query.order_by('-favorite_count')
            elif popularity == "oldest":
                query = query.order_by('created')        
        return query


class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)
    
    def search(self, query=None):
        return self.get_queryset().search(query)
    
    def filter_by_params(self, **kwargs):
        return self.get_queryset().filter_by_params(**kwargs)


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

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_books', on_delete=models.CASCADE)
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
    category = models.ManyToManyField('Category', related_name='books_categories', null=True, blank=True)
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_books',blank=True, editable=False)

    def __str__(self):
        return self.title
    
    def get_categories(self):
        return self.category

    def get_absolute_url(self):
        return reverse(viewname="books:detail", args=[self.pk])
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    objects = BookManager()

