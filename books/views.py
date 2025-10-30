from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .models import Book, Category


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'books/create.html'
    model = Book
    fields = ['title', 'author', 'cover_image', 'condition', 'status']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('books:user_library', kwargs={'pk': self.request.user.pk})


class AllBookListView(generic.ListView):
    template_name = 'books/library.html'
    model = Book
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        category = self.request.GET.get('category')
        popularity = self.request.GET.get('popularity')
        condition = self.request.GET.get('condition')
        status = self.request.GET.get('status')

        queryset = Book.objects.filter_by_params(
            title=title,
            author=author,
            popularity=popularity,
            condition=condition,
            status=status,
            category=category
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class UserBookListView(generic.ListView):
    template_name = 'books/user_books.html'
    model = Book
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        category = self.request.GET.get('category')
        popularity = self.request.GET.get('popularity')
        condition = self.request.GET.get('condition')
        status = self.request.GET.get('status')
    
        queryset = Book.objects.filter_by_params(
            title=title,
            author=author,
            popularity=popularity,
            condition=condition,
            status=status,
            category=category
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BookDetailView(generic.DetailView):
    template_name = 'books/detail.html'
    model = Book
    context_object_name = 'book'
    lookup_field = 'slug'