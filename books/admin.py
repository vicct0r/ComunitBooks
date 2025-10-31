from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'author', 'cover_image', 'condition', 'status', 'slug']