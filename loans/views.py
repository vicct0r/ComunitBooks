from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic

from .models import Loan
from .services import notification, loan_service
from .services.loan_service import LoanService
from orders.models import Order


class LoanCreateView(LoginRequiredMixin, generic.CreateView):
    """
    **Accept or Deny Orders Request**
    - Accept: Create Loan instance
    - Deny: Update Order status and do not create Loan instance
    """

    template_name = 'loans/create.html'
    model = Loan
    fields = ['deposit_amount', 'allows_renewal', 'custom_terms'] 

    def form_valid(self, form):
        _action = self.request.POST.get('action')
        action = True if _action == "approve" else False
        
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        
        if Loan.objects.filter(book=order.book, status__in=[Loan.ACTIVE, Loan.OVERDUE]).exists() and action:
            messages.warning(self.request,f"O livro {order.book.title} não está disponível para emprestimo!")
            return redirect(reverse('orders:submitted'))

        if action:
            loan = form.save(commit=False)
            loan.borrower=order.borrower
            loan.book=order.book
            loan.owner=order.book.owner if order.book.owner else None
            loan.max_loan_period=order.required_days
            loan.save()

            loan_service.update_order_status(order, action)
            messages.success(self.request, "Pedido aprovado, emprestimo criado!")
            notification.approve(loan)
            return super().form_valid(form)
        else:
            loan_service.update_order_status(order, action) 
            messages.info(self.request, "Este pedido foi recusado e arquivado!")
            return redirect(reverse('orders:submitted'))

    def get_success_url(self):
        return reverse('orders:submitted')


class LoansSubmittedListView(LoginRequiredMixin, generic.ListView):
    template_name = 'loans/submitted.html'
    model = Loan
    context_object_name = 'loans'

    def get_queryset(self):
        query = super().get_queryset()
        return query \
        .filter(borrower=self.request.user) \
        .exclude(status__in=[Loan.COMPLETED, Loan.CANCELLED]) \
        .order_by('-approved_date')


class LoansReceivedListView(LoginRequiredMixin, generic.ListView):
    template_name = 'loans/received.html'
    model = Loan
    context_object_name = 'loans'

    def get_queryset(self):
        query = super().get_queryset()
        return query \
        .filter(owner=self.request.user) \
        .exclude(status__in=[Loan.COMPLETED, Loan.CANCELLED]) \
        .order_by('-approved_date')


class LoanStatusUpdate(LoginRequiredMixin, generic.View):
    
    def post(self, request, pk):
        action = request.POST.get('action')
        user = request.user
        loan_id = pk
        loan = Loan.objects.get(id=pk)
        
        if action == "send":
            message = LoanService.send_book(loan_id)
            messages.success(request, message)
        elif action == "deny":
            message = LoanService.deny_delivery(loan_id)
            messages.success(request, message)
        elif action == "confirm_delivery":
            message = LoanService.borrower_confirm_delivery(loan_id)
            messages.success(request, message)
        elif action == "return_book":
            message = LoanService.borrower_return_book(loan_id)
            messages.success(request, message)
        elif action == "lender_confirm_delivery":  
            message = LoanService.lender_confirm_delivery(loan_id)
            messages.success(request, message)
        elif action == "renew": 
            message = LoanService.request_renewal(loan_id)
            messages.success(request, message)
        else:
            messages.error(request, "Ação inválida")
        
        if user == loan.borrower:
            return redirect('loans:submitted')
        
        if user == loan.owner:
            return redirect('loans:received')
