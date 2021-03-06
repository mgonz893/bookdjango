# Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique book instances
from django.urls import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date, datetime
from django.db.models.signals import post_save
from django.conf import settings
from django.db.models import Avg
# Create your models here.



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=8, default='')
    nickname = models.CharField(max_length=10, default='')
    email = models.EmailField(max_length=50, default='')
    address = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=25, default='')
    state = models.CharField(max_length=25, default='')
    zipcode = models.IntegerField(default=0)
    wishlists = models.ManyToManyField('Wishlist')

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class CreditCard(models.Model):
    username = models.ForeignKey(
        'UserProfile', on_delete=models.SET_NULL, null=True)
    ccnumber = models.PositiveIntegerField(validators=[
                                           MaxValueValidator(9999999999999999)], blank = False)  # 16 digits for valid CC number
    ccv = models.PositiveIntegerField(validators=[MaxValueValidator(999)], blank = False)
    expiration = models.DateField(
        help_text="(YYYY-MM-DD)", auto_now_add=False, auto_now=False, blank = False, validators=[MinValueValidator(limit_value=date.today)])

    def __str__(self):
        return f'{self.username} - {self.ccnumber}'


class ShippingAddr(models.Model):
    username = models.ForeignKey(
        'UserProfile', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zipcode = models.IntegerField()

    def __str__(self):
        return f'{self.username} - {self.address}'


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    publisher = models.CharField(max_length=50, default='Publisher')
    publishing_date = models.DateTimeField()

    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book')

    price = models.FloatField(default="9.99")

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, help_text='Select a genre for this book')

    # requires to install Pillow to work: python -m pip install Pillow
    model_pic = models.ImageField(upload_to='pics/', blank=True, null=True)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "books"

    def __str__(self):
        """String for representing the Model object."""
        return self.title + " " + self.slug

    @property
    def average_rating(self):
        return self.bookrating_set.aggregate(Avg('rating'))['rating__avg']

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={
            'slug': self.slug
        })

    def get_remove_single_book_from_cart_url(self):
        return reverse('remove-single-book-from-cart', kwargs={
            'slug': self.slug
        })

    def get_add_to_wishlist_url(self):
        return reverse('add-to-wishlist', kwargs={
            'slug': self.slug
        })

    def get_remove_from_wishlist_url(self):
        return reverse('remove-from-wishlist', kwargs={
            'slug': self.slug
        })

    def get_add_to_save_for_later_url(self):
        return reverse('add-to-save-for-later', kwargs={
            'slug': self.slug
        })

    def new_book_rating_url(self):
        return reverse('new_book_rating', kwargs={
            'slug': self.slug
        })

    def get_transfer_wishlist_url(self):
        return reverse('transfer-wishlist', kwargs={
            'slug': self.slug
        })

    def get_move_to_cart_url(self):
        return reverse('move-to-cart', kwargs={
            'slug': self.slug
        })

    def remove_saved_list(self):
        return reverse('remove-saved-list', kwargs={
            'slug': self.slug
        })


class OrderBook(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.book} - Qty: {self.quantity}'

    def get_total_book_price(self):
        return self.quantity * self.book.price


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderBook)

    def __str__(self):
        return f'{self.user} - {self.items}'

    def get_total(self):
        total = 0
        for order_book in self.items.all():
            total += order_book.get_total_book_price(self)
        return total


class SaveBook(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    saved = models.BooleanField(default=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.book} - Qty: {self.quantity}'


class Save(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    saved_date = models.DateTimeField()
    saved = models.BooleanField(default=False)
    items = models.ManyToManyField(SaveBook)

    def __str__(self):
        return f'{self.user} - {self.items}'


class BookRating(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    review = models.TextField(max_length=1000)
    rating = models.SmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    anonymous = models.BooleanField("Post as anonymous", default=False)
    nickname = models.BooleanField("Post as nickname", default=False)

    def __str__(self):
        return f'{self.user} - {self.book} - {self.rating}'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    biography = models.CharField(max_length=500, default='')
    fullname = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'


class Wishlist(models.Model):
    # Model representing a wishlist

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    name = models.CharField(max_length=100, default='New Wishlist')

    def __str__(self):
        return f'{self.user} - {self.name}'


class Shopping_Cart(models.Model):
    # Shopping Cart Model

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    quantity = models.IntegerField(default="1")
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book')
    subtotal = models.FloatField(default='9.99')
    name = models.CharField(max_length=100, default='Shopping Cart')

    def __str__(self):
        return self.name


class Saved_for_later(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    quantity = models.IntegerField(default="1")
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book')
    subtotal = models.FloatField(default='9.99')
    name = models.CharField(max_length=100, default='Saved For Later')

    def __str__(self):
        return self.name
