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
    success_url = reverse_lazy('loans:order_list')
    
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


class OrderRequestsListView(LoginRequiredMixin, generic.ListView):
    template_name = 'loans/order_list.html'
    model = Order
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id).order_by('-date_created')
    