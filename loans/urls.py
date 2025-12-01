from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('submitted/', views.LoansListView.as_view(), name='submitted'),
    path('received/', views.BookLoansListView.as_view(), name='received'),
    path('update/<int:pk>/', views.LoanStatusUpdate.as_view(), name='update_status')
]
