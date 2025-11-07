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
    success_url = reverse_lazy('loans:orders_made_list')
    
    def form_valid(self, form):
        book = get_object_or_404(Book, id=self.kwargs.get('book_id'))

        order = form.save(commit=False)
        order.book = book
        order.user = self.request.user
        order.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, id=self.kwargs.get('book_id'))
        return context


class OrdersMadeListView(LoginRequiredMixin, generic.ListView):
    template_name = 'loans/order_list.html'
    model = Order
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id).order_by('-date_created')


class OrdersRequestedListView(LoginRequiredMixin, generic.ListView):
    template_name = 'loans/requested_orders.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        query = Order.objects.filter(book__owner=self.request.user).order_by('-date_created')
        
        if self.request.GET.get('book'):
            query = query.filter(book_id=self.request.GET.get('book'))
        if self.request.GET.get('status'):
            query = query.filter(status=self.request.GET.get('status'))
        if self.request.GET.get('duration'):
            query = query.filter(required_days=self.request.GET.get('duration'))
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_books'] = Book.objects.filter(owner=self.request.user)
        return context