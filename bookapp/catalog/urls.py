from django.urls import path
from . import views
from django.conf.urls import url
from . import views as core_views

urlpatterns = [

    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]
