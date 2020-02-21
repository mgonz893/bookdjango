from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import datetime
from django.db.models import Q
from django.utils import timezone
from django.db.models.query import QuerySet
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.views import generic
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Book, Wishlist, Shopping_Cart, Order, OrderBook, BookRating
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from catalog.forms import RegistrationForm, EditProfileForm, ProfileForm
from django.contrib.auth.models import User
import random


# Create your views here.
from catalog.models import Book, Author, Genre, UserProfile
from django.db.models.aggregates import Avg


def products(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, "book_list.html", context)


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def author(request):
    model = Book
    paginate_by = 10

    query = request.GET.get('q')
    object_list = Book.objects.filter(
        Q(author__fullname__icontains=query)
    )
    context = {
        'book_list': object_list,
        'author': object_list[0],
    }
    return render(request, 'author.html', context)


def search(request):
    return render(request, 'search.html')


def topsellers(request):
    num_books = Book.objects.all()
    list_books = random.sample(list(num_books), 3)

    context = {
        'book_list': list_books,
    }

    return render(request, 'top_sellers.html', context)


class SearchResultsView(generic.ListView):
    model = Book
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(genre__name__icontains=query)
        )
        return object_list


class WishlistsView(generic.ListView):
    model = Wishlist
    template_name = 'catalog/wishlists.html'
    context_object_name = 'wishlists_list'
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['wishlists'] = Wishlist.objects.filter(
                user=self.request.user)
        return context


class ShoppingCart(generic.ListView):
    model = Shopping_Cart
    paginate_by = 10
    ordering = ['title', 'author', 'price']


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    ordering = ['title', 'author', 'price']


class BookDetailView(generic.DetailView):
    model = Book
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['rating'] = BookRating.objects.filter(book=self.get_object())
        context['average'] = BookRating.objects.filter(
            book=self.get_object()).aggregate(avge=Avg('rating'))
        return context


def shop_cart(request):
    args = {'user': request.user}
    return render(request, 'shopping_cart.html', args)


def login(request):
    args = {'user': request.user}
    return render(request, 'index.html', args)


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/catalog')
    else:
        form = RegistrationForm()

    args = {'form': form}
    return render(request, 'signup.html', args)


def profile(request):
    args = {'user': request.user}
    return render(request, 'profile.html', args)


def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, instance=request.user.userprofile)

        if form.is_valid():
            form.save()
            profile_form.save()
            return redirect('/catalog/profile/')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
    args = {'form': form,
            'profile_form': profile_form}

    return render(request, 'editprofile.html', args)


def shipaddr(request):
    args = {'user': request.user}
    return render(request, 'shipaddr.html', args)


def creditcards(request):
    args = {'user': request.user}
    return render(request, 'creditcards.html', args)


def add_to_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    order_book, created = OrderBook.objects.get_or_create(
        book=book,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(book__slug=book.slug).exists():
            order_book.quantity += 1
            order_book.save()
            messages.info(request, "This book quantity was updated.")
        else:
            order.items.add(order_book)
            messages.info(request, "This book was added to your cart.")
            return redirect("book-detail", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_book)
        messages.info(request, "This book was added to your cart.")
        return redirect("book-detail", slug=slug)

def remove_from_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(book__slug=book.slug).exists():
            order_book = OrderBook.objects.filter(
                            book=book,
                            user=request.user,
                            ordered=False
                            )[0]
            order.items.remove(order_book)
            messages.info(request, "This book was removed from your cart.")
            return redirect("book-detail", slug=slug)
        else:
            messages.info(request, "This book was not in your cart.")
            return redirect("book-detail", slug=slug)

    else:
        messages.info(request, "You do not have an active order.")
        return redirect("book-detail", slug=slug)

   
