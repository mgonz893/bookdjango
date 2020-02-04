from django.urls import path
from . import views
from django.conf.urls import url
from . import views as core_views

urlpatterns = [

    path('', views.index, name='index'),
    path('author/', views.author.as_view(), name='author'),
    path('search/', views.search, name='search'),
    path('search/searchresults/',
         views.SearchResultsView.as_view(), name='search_results'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.editprofile, name='editprofile'),
    path('signup/', views.signup, name='signup'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

]
