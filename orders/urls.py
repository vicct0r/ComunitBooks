from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('new/', views.OrderCreateView.as_view(), name='create'),
    path('cancel/', views.OrderCancelView.as_view(), name='cancel'),
    path('received/', views.OrdersReceivedListView.as_view(), 'received'),
    path('submitted/', views.OrdersSubmittedListView.as_view(), name='submitted')
]