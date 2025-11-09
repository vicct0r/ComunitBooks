from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('order/book/<int:book_id>/', views.OrderRequestCreateView.as_view(), name='order_create'),
    path('order/my-orders/', views.OrdersMadeListView.as_view(), name='orders_made_list'),
    path('order/requested-orders/', views.OrdersRequestedListView.as_view(), name='orders_request_list'),
    path('order/answer/<int:order_id>/', views.LoanCreateView.as_view(), name='loan_create'),
    path('request/list/', views.LoansListView.as_view(), name='user_loans_list'),
    path('books/list/', views.BookLoansListView.as_view(), name='books_loans_list')
]