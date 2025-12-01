#from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic

from .models import Order
from . import services
from books.models import Book


class OrderCancelView(LoginRequiredMixin, generic.View):
    def post(self, request, uuid):
        order = Order.objects.get(id=uuid)
        services.cancel_order(order)
        messages.success(request, 'O pedido foi cancelado.')
        return redirect('orders:submitted')


class OrderCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'orders/create.html'
    model = Order
    fields = ['description', 'required_days']
    success_url = reverse_lazy('orders:submitted')
    success_message = 'Pedido enviado com sucesso!'
    
    def form_valid(self, form):
        book = get_object_or_404(Book, id=self.kwargs.get('book_id'))

        if Order.objects.filter(borrower=self.request.user, book=book, status=Order.SUBMITTED).exists():
            messages.info(f'Você já possui um pedido em andamento para o livro {book.title} de {book.owner.email}!')
            return redirect(reverse('loans:submitted'))

        order = form.save(commit=False)
        order.book = book
        order.borrower = self.request.user
        order.owner = book.owner
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, id=self.kwargs.get('book_id'))
        return context


class OrdersReceivedListView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/received.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(owner=self.request.user, status=Order.SUBMITTED)
     

class OrdersSubmittedListView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/submitted.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(borrower=self.request.user, status=Order.SUBMITTED)

