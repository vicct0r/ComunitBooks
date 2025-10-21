from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book

class BookCreationCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'books/create.html'
    model = Book
    fields = ['title', 'author', 'cover_image', 'condition', 'status']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_succesres_url(self):
        return reverse('books:find_user', kwargs=self.request.user.id)


class UsersListView(generic.ListView):
    template_name = 'books/users_books.html'
    model = Book
    context_object_name = 'books'

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        if user_id:
            return Book.objects.filter(owner=user_id)
        return Book.objects.all()


class BookDetailView(generic.DetailView):
    template_name = 'books/detail.html'
    model = Book
    context_object_name = 'book'
    lookup_field = 'slug'
    