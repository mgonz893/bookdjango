from django.contrib import admin
from .models import UserProfile, Book, Author, BookInstance, BookRating, CreditCard, ShippingAddr, Genre

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(CreditCard)
admin.site.register(ShippingAddr)
admin.site.register(BookRating)
