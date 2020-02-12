from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import datetime
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.views import generic
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Book, Wishlist, Shopping_Cart
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from catalog.forms import RegistrationForm, EditProfileForm, ProfileForm
from django.contrib.auth.models import User
import random


# Create your views here.
from catalog.models import Book, Author, Genre, UserProfile


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
    # paginate_by = 10
    # ordering = ['title', 'author', 'price']


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    ordering = ['title', 'author', 'price']


class BookDetailView(generic.DetailView):
    model = Book


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
