from django.contrib import admin

# Register your models here.
from .models import Book, Author, Recommendation, Genre

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Recommendation)
admin.site.register(Genre)