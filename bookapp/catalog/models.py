# Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique book instances
from django.urls import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import date
# Create your models here.


class User(models.Model):
    nickname = models.CharField(
        max_length=8, help_text='Enter a nickname (max 8 characters)')
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=8)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zipcode = models.IntegerField()

    def __str__(self):
        """String for representing the Model object."""
        return self.nickname


class CreditCard(models.Model):
    nickname = models.ForeignKey(
        'User', on_delete=models.SET_NULL, null=True)
    ccnumber = models.IntegerField()

    def __str__(self):
        return self.ccnumber


class ShippingAddr(models.Model):
    nickname = models.ForeignKey(
        'User', on_delete=models.SET_NULL, null=True)
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
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    ratings = models.ManyToManyField(User, through='BookRating')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, help_text='Select a genre for this book')

    # requires to install Pillow to work: python -m pip install Pillow
    model_pic = models.ImageField(upload_to='pics/', default='')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])


class BookRating(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    review = models.TextField(max_length=1000)
    rating = models.SmallIntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return self.review


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
