from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    genre_text = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.genre_text}'



class Author(models.Model):
    author_name = models.CharField(max_length=200)
    #author_books = models.ManyToManyField('Book', blank=True)
    
    def __str__(self):
        return f'{self.author_name}'

class Book(models.Model):
    book_text = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    book_genres = models.ManyToManyField(Genre, blank=True)
    userlikes = models.ManyToManyField(User, blank=True)
    book_authors = models.ManyToManyField(Author, blank=True)

    def __str__(self):
        return f'{self.book_text}' #{self.book_genres.all()[0].genre_text}'



class Recommendation(models.Model):
    review_text = models.CharField(max_length=5000)
    review_date = models.DateTimeField('Date published')
    review_user = models.CharField(max_length=100)
    review_book = models.ForeignKey(Book, on_delete=models.CASCADE, default='')

    def __str__(self):
        return f'{self.review_text}, {self.review_user}, {self.review_book}'
