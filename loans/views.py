from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic
from .models import Order, Loan

from books.models import Book


class OrderRequestCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'loans/order_creation.html'
    model = Order
    fields = ['description', 'required_days']
    
    def form_valid(self, form):
        book = get_object_or_404(Book, id=self.kwargs.get('book_id'))

        form.instance.book = book
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse('books:detail', kwargs={'pk': self.kwargs.get('book_id')})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, id=self.kwargs.get('book_id'))
        return context