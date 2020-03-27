from django.urls import path
from . import views
from django.conf.urls import url
from . import views as core_views

urlpatterns = [

    path('', views.index, name='index'),
    path('author/', views.author, name='author'),
    path('topsellers/', views.topsellers, name='topsellers'),
    path('search/', views.search, name='search'),
    path('search/searchresults/',
         views.SearchResultsView.as_view(), name='search_results'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.editprofile, name='editprofile'),
    path('signup/', views.signup, name='signup'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(),
         name='book-detail'),  # may need to change back to slug
    path('book/<slug>', views.BookDetailView.as_view(),
         name='book-detail'),  # may need to change back to slug
    path('shoppingcart/', views.shop_cart, name='shoppingcart'),
    path('wishlists/', views.WishlistsView.as_view(), name='wishlists'),
    # need to figure how to get this link to work
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('shipaddr/', views.shipaddr, name='shipaddr'),
    path('shipaddr/addshipaddr/', views.addshippingaddress, name='addshippingaddr'),
    path('shipaddr/editshipaddr/<str:pk>/',
         views.editshippingaddress, name='editshippingaddr'),
    path('shipaddr/deleteshipaddr/<str:pk>/',
         views.deleteshippingaddress, name='deleteshippingaddr'),
    path('shipaddr/newdefaultshipaddr/<str:pk>/',
         views.setdefaultaddress, name='setdefaultaddr'),
    path('creditcards/', views.creditcards, name='creditcards'),
    path('creditcards/addcreditcard/', views.addcreditcard, name='addcreditcard'),
    path('remove-from-cart/<slug>',
         views.remove_from_cart, name='remove-from-cart'),
    path('remove-book-from-cart/<slug>',
         views.remove_single_book_from_cart, name='remove-single-book-from-cart'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/new/<slug>', views.post_newrating, name='new_book_rating'),
    path('add-to-wishlist/<slug>', views.add_to_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/<slug>',
         views.remove_from_wishlist, name='remove-from-wishlist'),
    path('wishlists/newwish/', views.newwish, name='newwish'),
    path('add-to-save-for-later/<slug>',
         views.add_save_for_later, name='add-to-save-for-later'),
    path('transfer-wishlist/<slug>',
         views.transfer_wishlist, name='transfer-wishlist'),
    path('delete-wishlist', views.delete_wishlist, name='delete-wishlist'),
]
