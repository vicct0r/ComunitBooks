from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('create/<uuid:order_id>/', views.LoanCreateView.as_view(), name='create'),
    path('submitted/', views.LoansSubmittedListView.as_view(), name='submitted'),
    path('received/', views.LoansReceivedListView.as_view(), name='received'),
    path('update/<uuid:loan_id>/', views.LoanStatusUpdate.as_view(), name='update_status')
]
