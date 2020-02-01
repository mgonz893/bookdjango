from django.contrib import admin
from .models import Book, Author, BookInstance, BookRating, CreditCard, ShippingAddr, Genre, User

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(CreditCard)
admin.site.register(ShippingAddr)
admin.site.register(BookRating)
admin.site.register(User)


''' @admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    ) '''
