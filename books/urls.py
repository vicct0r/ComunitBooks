from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('register/', views.BookCreationCreateView.as_view(), name='creation'),
    path('find/', views.UserBooksListView.as_view(), name='find'),
    path('find/<int:pk>/', views.UserBooksListView.as_view(), name='find_user'),
]