from django.contrib import admin
from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['borrower', 'owner', 'book', 'approved_date', 'start_date', 'due_date', 'returned_date', 'max_loan_period', 'status', 'deposit_amount', 'allows_renewal', 'custom_terms']