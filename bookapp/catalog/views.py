from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import datetime
from django.db.models import Sum, ExpressionWrapper
from django.db.models import FloatField, Q
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
from .models import Book, Wishlist, Shopping_Cart, Order, OrderBook, BookRating, ShippingAddr, CreditCard, Saved_for_later, Save, SaveBook
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from catalog.forms import RegistrationForm, EditProfileForm, ProfileForm, ReviewForm, WishForm, ShippingAddressForm, CreditCardForm
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
        return object_list.order_by('genre')


class WishlistsView(generic.ListView):
    model = Wishlist
    template_name = 'catalog/wishlists.html'
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['wishlist'] = Wishlist.objects.filter(
                user=self.request.user)
        return context


class ShoppingCart(generic.ListView):
    model = Shopping_Cart
    paginate_by = 10
    ordering = ['title', 'author', 'price']


class SavedForLater(generic.ListView):
    model = Saved_for_later
    paginate_by = 10
    ordering = ['title', 'author', 'price']


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    class Meta:
        ordering = ['genre', 'title', 'price']

    def get_queryset(self):
        order = self.request.GET.get('orderby', 'genre')
        new_context = Book.objects.filter().order_by(order)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['orderby'] = self.request.GET.get('orderby', 'genre')
        return context


class BookDetailView(generic.DetailView):
    model = Book
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['rating'] = BookRating.objects.filter(book=self.get_object())
        context['average'] = BookRating.objects.filter(
            book=self.get_object()).aggregate(avge=Avg('rating'))
        context['wishlists'] = Wishlist.objects.all()
        return context


def add_to_wishlist(request, slug):
    if request.method == 'POST':
        form = Wishlist(request.POST)
        if form.is_valid():
            return redirect("book-detail", slug=slug)


def shop_cart(request):
    user = request.user
    orders = OrderBook.objects.filter(user=user)
    subtotal = OrderBook.objects.filter(user=user).aggregate(
        total=Sum('book__price'))  # OrderBook.get_total_book_price))
    args = {'user': request.user,
            'shopping_cart': orders,
            'subtotal': subtotal}
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


def newwish(request):
    # Restricts maximum number of wishlists to three
    wl = Wishlist.objects.filter(user=request.user)
    if len(wl) >= 3:
        messages.info(request, "You may only have 3 wishlists at a time.")
        return redirect('wishlists')

    if request.method == 'POST':
        form = WishForm(request.POST)
        if form.is_valid():
            wishlist = form.save(commit=False)
            wishlist.user = request.user
            wishlist.save()
            return redirect('wishlists')
    else:
        form = WishForm()
        args = {
            'form': form,
            'user': request.user
        }

    return render(request, 'addwish.html', args)


def shipaddr(request):
    user = request.user.userprofile
    ships = ShippingAddr.objects.filter(username=user)
    args = {'user': request.user,
            'ships': ships
            }
    return render(request, 'shipaddr.html', args)


def addshippingaddress(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            newaddress = form.save(commit=False)
            newaddress.username = request.user.userprofile
            newaddress.save()
            return redirect('/catalog/shipaddr')
    else:
        form = ShippingAddressForm()
        args = {
            'form': form,
            'username': request.user.userprofile
        }

    return render(request, 'addshippingaddr.html', args)


def editshippingaddress(request, pk):

    address = ShippingAddr.objects.get(id=pk)
    form = ShippingAddressForm(instance=address)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('/catalog/shipaddr')
    args = {
        'form': form
    }
    return render(request, 'addshippingaddr.html', args)


def deleteshippingaddress(request, pk):
    address = ShippingAddr.objects.get(id=pk)
    if request.method == 'POST':
        address.delete()
        return redirect('/catalog/shipaddr')

    args = {'item': address}
    return render(request, 'deleteshippingaddr.html', args)


def setdefaultaddress(request, pk):
    newdefault = ShippingAddr.objects.get(id=pk)
    currentdefault = UserProfile.objects.get(user=request.user)
    currenttemp = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        currentdefault.address = newdefault.address
        currentdefault.state = newdefault.state
        currentdefault.zipcode = newdefault.zipcode
        currentdefault.city = newdefault.city
        currentdefault.save()
        newdefault.address = currenttemp.address
        newdefault.state = currenttemp.state
        newdefault.zipcode = currenttemp.zipcode
        newdefault.city = currenttemp.city
        newdefault.save()
        return redirect('/catalog/shipaddr')

    args = {'item': newdefault}
    return render(request, 'newdefaultshippingaddr.html', args)


def creditcards(request):
    user = request.user.userprofile
    cards = CreditCard.objects.filter(username=user)
    args = {'user': request.user,
            'cards': cards
            }
    return render(request, 'creditcards.html', args)


def addcreditcard(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            newcard = form.save(commit=False)
            newcard.username = request.user.userprofile
            newcard.save()
            return redirect('/catalog/creditcards')
    else:
        form = CreditCardForm()
        args = {
            'form': form,
            'username': request.user.userprofile
        }
    return render(request, 'addcreditcard.html', args)


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
            return redirect("book-detail", slug=slug)
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
            if order_book.quantity > 1:
                order_book.delete()
            else:
                order_book.delete()
            messages.info(request, "This book was removed from your cart.")
            return redirect("book-detail", slug=slug)
        else:
            messages.info(request, "This book was not in your cart.")
            return redirect("book-detail", slug=slug)

    else:
        messages.info(request, "You do not have an active order.")
        return redirect("book-detail", slug=slug)


def remove_single_book_from_cart(request, slug):
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
            if order_book.quantity > 1:
                order_book.quantity -= 1
                order_book.save()
                messages.info(request, "This book quantity was updated.")
                return redirect("shoppingcart")
            else:
                messages.info(request, "Cannot decrease quantity.")
                return redirect("shoppingcart")
        else:
            messages.info(request, "This book was not in your cart.")
            return redirect("shoppingcart")

    else:
        messages.info(request, "You do not have an active order.")
        return redirect("shoppingcart")


def post_new(request):
    order_qs = Order.objects.filter(user=request.user, ordered=True)
    if order_qs.exists():
        form = ReviewForm()
        args = {
            'form': form,
            'user': request.user
        }
    else:
        messages.info(request, "You do not own this book!")
        return render(request, 'search.html')
    return render(request, 'createrev.html', args)


def add_to_wishlist(request, slug):
    wishvalue = request.POST['wish_value']
    book = get_object_or_404(Book, slug=slug)

    order_qs = Wishlist.objects.filter(id=wishvalue)
    if order_qs.exists():
        order = order_qs[0]
        if order.books.filter(slug=book.slug).exists():
            messages.info(request, "This book is already in wishlist.")
            return redirect("book-detail", slug=slug)
        else:
            order.books.add(book)
            messages.info(request, "This book was added to your wishlist.")
            return redirect("book-detail", slug=slug)
    else:
        messages.info(request, "There was an error.")
        return redirect("book-detail", slug=slug)


def Wishlists(request):
    model = Wishlist
    queryset = Wishlist.objects.filter(user=request.user)
    args = {'user': request.user,
            'wishlist': queryset,
            }
    return render(request, 'catalog/wishlists.html', args)


def remove_from_wishlist(request, slug):
    wishvalue = request.POST['wish_value']
    book = get_object_or_404(Book, slug=slug)

    order_qs = Wishlist.objects.filter(id=wishvalue)
    if order_qs.exists():
        order = order_qs[0]
        if order.books.filter(slug=book.slug).exists():
            order.books.remove(book)
            messages.info(request, "This book has been removed from wishlist.")
            return redirect("book-detail", slug=slug)
        else:
            messages.info(request, "This book is not in your wishlist.")
            return redirect("book-detail", slug=slug)
    else:
        messages.info(request, "There was an error.")
        return redirect("book-detail", slug=slug)


def save_for_later(request):
    user = request.user
    saves = SaveBook.objects.filter(user=user)
    subtotal = SaveBook.objects.all().aggregate(
        total=Sum('book__price'))
    args = {'user': request.user,
            'save_for_later': saves
            }
    return render(request, 'shopping_cart.html', args)


def add_save_for_later(request, slug):
    book = get_object_or_404(Book, slug=slug)
    save_book, created = SaveBook.objects.get_or_create(
        book=book,
        user=request.user,
        saved=False)
    save_qs = Save.objects.filter(user=request.user, saved=False)
    if save_qs.exists():
        save = save_qs[0]
        if save.items.filter(book__slug=book.slug).exists():
            save_book.quantity += 1
            save_book.save()
            messages.info(request, "This book quantity was updated.")
            return redirect("book-detail", slug=slug)
        else:
            save.items.add(save_book)
            messages.info(request, "This book was saved for later.")
            return redirect("book-detail", slug=slug)
    else:
        saved_date = timezone.now()
        save = Save.objects.create(
            user=request.user, saved_date=saved_date)
        save.items.add(save_book)
        messages.info(request, "This book was added to your cart.")
        return redirect("book-detail", slug=slug)
