from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, Category


class BooksFiltersMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        category = self.request.GET.get('category')
        popularity = self.request.GET.get('popularity')
        condition = self.request.GET.get('condition')
        status = self.request.GET.get('status')

        queryset = Book.objects.select_related('owner').filter_by_params(
            title=title,
            author=author,
            popularity=popularity,
            condition=condition,
            status=status,
            category=category,
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'books/create.html'
    model = Book
    fields = ['title', 'author', 'cover_image', 'condition', 'status', 'category']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('books:user_library', kwargs={'pk': self.request.user.pk})


class AllBookListView(BooksFiltersMixin, generic.ListView):
    template_name = 'books/library.html'
    model = Book
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class UserBookListView(BooksFiltersMixin, generic.ListView):
    template_name = 'books/user_books.html'
    model = Book
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        if self.kwargs.get('pk'):
            return super().get_queryset().filter(is_visible=True, owner=self.kwargs.get('pk'))
        return super().get_queryset().filter(is_visible=True, owner=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    

class BookDetailView(generic.DetailView):
    template_name = 'books/detail.html'
    model = Book
    context_object_name = 'book'
    queryset = Book.objects.select_related('owner')
    lookup_field = 'slug'


class BookFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        if book.favorited_by.filter(id=request.user.id).exists():
            book.favorited_by.remove(request.user)
            messages.success(request, "Livro removido dos favoritos")
        else:
            book.favorited_by.add(request.user)
            messages.success(request, "Livro adicionado aos favoritos")
        return redirect(book.get_absolute_url())


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'books/update.html'
    model = Book
    fields = ['title', 'author', 'cover_image', 'condition', 'category', 'is_visible']

    def form_valid(self, form):
        messages.success(self.request, 'O livro foi atualizado com sucesso!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('books:detail', kwargs={'pk': self.kwargs.get('pk')})