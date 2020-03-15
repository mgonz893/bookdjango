from django.contrib import admin
from .models import UserProfile, Book, Author, BookRating, CreditCard, ShippingAddr, Genre, Wishlist, Shopping_Cart, Order, OrderBook, Saved_for_later

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(CreditCard)
admin.site.register(ShippingAddr)
admin.site.register(BookRating)
admin.site.register(Wishlist)
admin.site.register(Shopping_Cart)
admin.site.register(Order)
admin.site.register(OrderBook)
admin.site.register(Saved_for_later)
