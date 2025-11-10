from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
from django.utils import timezone

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.views import generic
from .models import Order, Loan

from . import services
from books.models import Book


class OrderRequestCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'orders/order_creation.html'
    model = Order
    fields = ['description', 'required_days']
    success_url = reverse_lazy('loans:orders_made_list')
    success_message = 'Pedido enviado com sucesso!'
    
    def form_valid(self, form):
        book = get_object_or_404(Book, id=self.kwargs.get('book_id'))

        if Order.objects.filter(borrower=self.request.user, book=book, status=Order.SUBMITTED).exists():
            messages.info(f'Você já possui um pedido em andamento para o livro {book.title} de {book.owner.email}!')
            return redirect(reverse('loans:orders_made_list'))

        order = form.save(commit=False)
        order.book = book
        order.borrower = self.request.user
        order.owner = book.owner
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
        return Order.objects.filter(borrower=self.request.user.id).order_by('-date_created')


class OrdersRequestedListView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/requested_orders.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        query = Order.objects.filter(owner=self.request.user).order_by('-date_created')
        
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
    """
    **Accept or Deny Orders Request**
    - Accept: Create Loan instance
    - Deny: Update Order status and do not create Loan instance
    """

    template_name = 'loans/create_loan.html'
    model = Loan
    fields = ['deposit_amount', 'allows_renewal', 'custom_terms'] 

    def form_valid(self, form):

        _action = self.request.POST.get('action')
        action = True if _action == "approve" else False
        
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        
        if Loan.objects.filter(book=order.book, status__in=[Loan.ACTIVE, Loan.OVERDUE]).exists() and action:
            messages.warning(self.request,f"O livro {order.book.title} não está disponível para emprestimo!")
            return redirect(reverse('loans:orders_request_list'))

        if action:
            loan = form.save(commit=False) # atribuindo info do pedido para o emprestimo
            loan.borrower=order.borrower
            loan.book=order.book
            loan.owner=order.book.owner if order.book.owner else None
            loan.due_date=timezone.now().date() + timedelta(days=order.required_days)
            loan.max_loan_period=order.required_days
            loan.save()

            services.update_order_status(order, action)
            messages.success(self.request, "Pedido aprovado, emprestimo criado!")
            return super().form_valid(form)
        else:
            services.update_order_status(order, action) 
            messages.info(self.request, "Este pedido foi recusado e arquivado!")
            return redirect(reverse('loans:orders_request_list'))
    
    def get_success_url(self):
        return reverse('loans:orders_request_list')


class LoansListView(LoginRequiredMixin, generic.ListView):
    template_name = 'loans/user_loans_list.html'
    model = Loan
    context_object_name = 'loans'

    def get_queryset(self):
        return Loan.objects.filter(borrower=self.request.user).order_by('-approved_date')


class BookLoansListView(LoginRequiredMixin, generic.ListView):
    template_name = 'loans/books_loans_list.html'
    model = Loan
    context_object_name = 'loans'

    def get_queryset(self):
        return Loan.objects.filter(owner=self.request.user).order_by('-approved_date')
