# Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique book instances
from django.urls import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import post_save
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=8, default='')
    email = models.EmailField(max_length=50, default='')
    address = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=25, default='')
    state = models.CharField(max_length=25, default='')
    zipcode = models.IntegerField(default=0)

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
    ccnumber = models.IntegerField()

    def __str__(self):
        return self.ccnumber


class ShippingAddr(models.Model):
    username = models.ForeignKey(
        'UserProfile', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zipcode = models.IntegerField()


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

    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book')

    ratings = models.ManyToManyField(UserProfile, through='BookRating')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, help_text='Select a genre for this book')

    # requires to install Pillow to work: python -m pip install Pillow
    model_pic = models.ImageField(upload_to='pics/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "books"

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])


class BookRating(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    review = models.TextField(max_length=1000)
    rating = models.SmallIntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return self.review


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
