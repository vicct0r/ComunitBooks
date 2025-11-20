from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.AllBookListView.as_view(), name='library'),
    path('add/', views.BookCreateView.as_view(), name='create'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='detail'),
    path('favorite/', views.BookFavoriteView.as_view(), name='favorite'),
    path('user/<int:pk>/', views.UserBookListView.as_view(), name='user_library'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='update')
]