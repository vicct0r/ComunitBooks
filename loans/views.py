from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic

from .models import Loan
from .services import notification, loan_service
from .services.loan_service import LoanService
from orders.models import Order


class LoanCreateView(LoginRequiredMixin, generic.View):

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        action = self.request.POST.get('action')
        NOT_SUCCESS_REDIRECT = redirect(reverse('orders:submitted'))

        if Loan.objects.filter(book=order.book, status__in=[Loan.ACTIVE, Loan.OVERDUE]).exists() and action:
            messages.warning(self.request, f"O livro {order.book.title} não está disponível para emprestimo!")
            return NOT_SUCCESS_REDIRECT

        if action == 'approve':
            loan = Loan.objects.create(
                borrower=order.borrower,
                book=order.book,
                owner=order.book.owner if order.book.owner else None,
                max_loan_period=order.required_days,
            )

            loan_service.update_order_status(order, action)
            messages.success(request, "Pedido aprovado, emprestimo criado!")
            notification.approve(loan)
        else:
            loan_service.update_order_status(order, action) 
            messages.info(request, "Este pedido foi recusado e arquivado!")
        return NOT_SUCCESS_REDIRECT


class LoanStatusMixin:
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id

        loans_with_actions = []
        for loan in context['loans']:
            loans_with_actions.append({
                'loan': loan,
                'allowed_actions': LoanService.allowed_actions(loan, user_id=user_id)
            })
        
        context['usuario'] = user_id
        context['allowed_actions'] = loans_with_actions
        return context


class LoansSubmittedListView(LoginRequiredMixin, LoanStatusMixin, generic.ListView):
    template_name = 'loans/submitted.html'
    model = Loan
    context_object_name = 'loans'

    def get_queryset(self):
        query = super().get_queryset()
        return query \
        .filter(borrower=self.request.user) \
        .exclude(status__in=[Loan.COMPLETED, Loan.CANCELLED]) \
        .order_by('-approved_date')


class LoansReceivedListView(LoginRequiredMixin, LoanStatusMixin, generic.ListView):
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
    
    def post(self, request, loan_id):
        action = request.POST.get('action')
        user = request.user
        loan = Loan.objects.get(id=loan_id)
        
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
