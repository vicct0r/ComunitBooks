from django.shortcuts import render
from django.views import generic

from books.models import Book


class HomePageView(generic.TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_books'] = Book.objects.filter(is_visible=True).select_related('owner').order_by('-created')[:6]
        return context