from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('new/<uuid:book_id>/', views.OrderCreateView.as_view(), name='create'),
    path('cancel/<uuid:order_id>/', views.OrderCancelView.as_view(), name='cancel'),
    path('received/', views.OrdersReceivedListView.as_view(), name='received'),
    path('submitted/', views.OrdersSubmittedListView.as_view(), name='submitted')
]