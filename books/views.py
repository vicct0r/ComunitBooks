from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book


class BookCreationCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'books/create.html'
    model = Book

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('books:list', kwargs=self.request.user.id)


class UserBooksListView(generic.ListView):
    template_name = 'books/users_books.html'
    model = Book
    context_object_name = 'books'

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        if user_id:
            return Book.objects.filter(owner=user_id)
        return Book.objects.all()
        
    