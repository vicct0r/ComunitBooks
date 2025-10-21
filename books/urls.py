from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('register/', views.BookCreationCreateView.as_view(), name='creation'),
    path('find/', views.UsersListView.as_view(), name='find'),
    path('find/<int:pk>/', views.UsersListView.as_view(), name='find_user'),
    path('find/<int:pk>/<slug:slug>/', views.BookDetailView.as_view(), name='find_user_slug'),
]