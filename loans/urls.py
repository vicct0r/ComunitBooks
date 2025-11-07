from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('order/book/<int:book_id>/', views.OrderRequestCreateView.as_view(), name='order_create'),
    path('order/my-orders/', views.OrdersMadeListView.as_view(), name='orders_made_list'),
    path('order/requested-orders/', views.OrdersRequestedListView.as_view(), name='orders_request_list')
]