from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.AllBookListView.as_view(), name='library'),
    path('add/', views.BookCreateView.as_view(), name='create'),
    path('<int:pk>/<slug:slug>/', views.BookDetailView.as_view(), name='detail'),
    path('library/user/<int:pk>/', views.UserBookListView.as_view(), name='user_library')
]