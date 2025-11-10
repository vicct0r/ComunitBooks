from django.contrib import admin
from .models import Order, Loan


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['date_created', 'borrower__email', 'book', 'description', 'borrower__email', 'required_days', 'status']
    search_fields = ['date_created', 'borrower', 'owner', 'book']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['borrower', 'owner', 'book', 'approved_date', 'start_date', 'due_date', 'returned_date', 'max_loan_period', 'status', 'deposit_amount', 'allows_renewal', 'custom_terms']