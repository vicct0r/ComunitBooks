from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('ordering/<int:book_id>/', views.OrderRequestCreateView.as_view(), name='order_create')
]