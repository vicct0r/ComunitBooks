from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.PublicBookListView.as_view(), name='library'),
    path('book/add/', views.BookCreateView.as_view(), name='create'),
    path('book/favorite/', views.FavoriteBookView.as_view(), name='favorite'),
    path('book/<uuid:book_id>/', views.PublicBookDetailView.as_view(), name='detail'),
    path('book/<uuid:book_id>/edit/', views.BookUpdateView.as_view(), name='update'),
    
    path('user/<uuid:user_id>/', views.UserBookListView.as_view(), name='user_library'),
]