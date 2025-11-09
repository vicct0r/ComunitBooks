from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
from django.utils import timezone

from django.views import generic
from .models import Order, Loan

from . import services
from books.models import Book


class OrderRequestCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'orders/order_creation.html'
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
    template_name = 'orders/order_list.html'
    model = Order
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id).order_by('-date_created')


class OrdersRequestedListView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/requested_orders.html'
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


class LoanCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'loans/create_loan.html'
    model = Loan
    fields = ['deposit_amount', 'allows_renewal', 'custom_terms'] 

    def form_valid(self, form):

        _action = self.request.POST.get('action')
        action = True if _action == "approve" else False

        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        services.update_order_status(order, action) # update Order & Book status
        loan = form.save(commit=False) # atribuindo info do pedido para o emprestimo
        loan.user=order.user
        loan.book=order.book
        loan.due_date=timezone.now().date() + timedelta(days=order.required_days)
        loan.max_loan_period=order.required_days
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('loans:orders_request_list')


class LoansListView(LoginRequiredMixin, generic.ListView):
    template_name = 'loans/user_loans_list.html'
    model = Loan
    context_object_name = 'loans'

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user).order_by('-approved_date')


class BookLoansListView(LoginRequiredMixin, generic.ListView):
    template_name = 'loans/books_loans_list.html'
    model = Loan
    context_object_name = 'loans'

    def get_queryset(self):
        return Loan.objects.filter(book__owner=self.request.user).order_by('-approved_date')
