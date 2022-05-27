from django.urls import path

from . import views

app_name = 'fluffyBooks'

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.load_login, name='load_login'),
    path('signup', views.load_signup, name='load_signup'),
    path('signuph', views.signup, name='signup'),
    path('verify', views.verify_login, name='verify'),
    path('logout', views.logout_mine, name='logout_user'),
    path('book', views.book, name='book'),
    path('reviewbook', views.review_book, name='review_book'),
    path('search', views.search, name='search'),
    path('books', views.books, name='books'),
    path('account', views.your_profile, name='your_profile' ),
    path('genres', views.genres, name='genres'),
    path('profile', views.profile, name='profile'),
    path('like', views.like, name='like'),
    path('post', views.post_review, name='review'),
    path('delete', views.delete_review, name='delete'),
    path('reviews', views.recent_reviews, name='reviews'),
    path('genre', views.genre_pages, name='genre_page'),
    path('review', views.review_page, name='review_page'),
    path('accreviews', views.account_reviews, name='account_reviews'),
    path('authorbooks', views.author_detail, name='author_detail')
    #path('genre', views.genre_pages, name='genres'),
]