from django.shortcuts import render
from django.views import generic
from django.db.models import Count, F
from books.models import Book


class HomePageView(generic.TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # considerando favoritos e quantidade de pedidos para o mesmo Livro
        popular_books = Book.objects.filter(is_visible=True) \
        .select_related('owner') \
        .annotate(
            total_favorites=Count('favorited_by', distinct=True),
            total_orders=Count('book_orders', distinct=True),
        ) \
        .annotate(
            score=F('total_favorites') + F('total_orders')
        ) \
        .order_by('-score')[:6]

        context['recent_books'] = Book.objects.filter(is_visible=True).select_related('owner').order_by('-created')[:6]
        context['popular_books'] = popular_books
        return context