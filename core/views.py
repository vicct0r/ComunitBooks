from django.shortcuts import render
from django.views import generic
from django.db.models import Count, F, Q
from books.models import Book
from loans.models import Loan
from django.contrib.auth import get_user_model

User = get_user_model()


class HomePageView(generic.TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Livros recentes e populares
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

        # Estatísticas do banco de dados
        total_books = Book.objects.filter(is_visible=True).count()

        # Contagem de usuários ativos (que possuem livros ou possuem empréstimos)
        active_users = User.objects.filter(
            Q(user_books__is_visible=True) | Q(loan_borrower__isnull=False)
        ).distinct().count()

        # Total de empréstimos completados
        total_loans = Loan.objects.filter(status=Loan.COMPLETED).count()

        context['recent_books'] = Book.objects.filter(is_visible=True).select_related('owner').order_by('-created')[:6]
        context['popular_books'] = popular_books
        context['total_books'] = total_books
        context['active_users'] = active_users
        context['total_loans'] = total_loans

        return context