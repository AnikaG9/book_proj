from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book, Genre, Author, Recommendation, User
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
from django.template import loader
from django.utils import timezone
import csv

#ASK ABOUT GENRE AND HOW ITS ONLY CONNECTED TO BOOK


# Create your views here.
def home(request):
    try:
        posted = request.GET['post']
    except:
        posted = None
    try:
        like = request.GET['warning']
    except:
        like = None
    reviews = Recommendation.objects.all()
    genres = Genre.objects.all()
    books = Book.objects.all()
    i = 0
    
    trending_books = Book.objects.order_by('-likes')[:6]
    review_list = []
    book_author_list = []

    cards = []
    for i in trending_books:
        card = [i.book_text]
        for author in i.book_authors.all():
            authorlist = []
            authorlist.append(author.author_name)
        card.append(authorlist)
        # add genre
        cards.append(card)

    
    context = {'cardbooks': trending_books, 'review_list':review_list, 'author_list':book_author_list, 'cards':cards, 'posted':posted, 'like':like}
    
    return render(request, 'fluffyBooks/home.html', context)

def index(sequence, position):
    return sequence[position]

def review_book(request):
    booko = request.GET['reviewb']#book_id value, key=book in URL
    book_obj = Book.objects.get(pk=booko)
    
    context = {'book': book_obj}
    return render(request, f'fluffyBooks/', context)
    
def recent_reviews(request):
    reviews = Recommendation.objects.all()

    books = Book.objects.all()
    # first_book = books[0]
    # try:
    #     for x in books:
    #         print(x)
    # except:
    #     x.delete()
    # print(first_book.book_text)
    # first_book_authors = first_book.book_authors.all()
    # print(first_book_authors)

    # print(first_book_authors[0].author_name)
    # print(first_book)
    # print('**************************')
    
    str_request = request.user.username
    recent = Recommendation.objects.order_by('-review_date')[:8]
    context = {'recommendations' : reviews, 'books' : books, 'request_help' : str_request, 'recent_reviewl' : recent}
    return render(request, 'fluffyBooks/recent_recs.html', context)

def load_login(request):
    
    return render(request, 'fluffyBooks/login_signup.html')

def load_signup(request):
    
    return render(request, 'fluffyBooks/signup.html')

def verify_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    print('hello')
    print(user)
    if user is not None:
        print('here')
        login(request, user)
        return redirect('fluffyBooks:home')
    else:
        print('got it')
        return render(request, 'fluffyBooks/login_signup.html')

def signup(request):
      username= request.POST["username"]
      password = request.POST["password"]
      user = User.objects.create_user(username, password=password)
      print('create user')

      if user is not None:
          
          return(verify_login(request))
        
      else:
          print('hmmm')
          return render(request, 'fluffyBooks/login_signup.html')

def logout_mine(request):
    logout(request)
    return redirect('fluffyBooks:home')

def like(request):
    if not request.user.is_authenticated:
        return redirect('/fluffyBooks/?warning=true')
    print('in like...')
    print(request.GET)
    book_id = request.GET.get('book')
    print(book_id)
    b = Book.objects.get(id=book_id)# getting from actual database
    userlikes = b.userlikes.all()
    print(userlikes)
    if request.user in b.userlikes.all():
        print('hi')
        b.likes -= 1
        b.userlikes.remove(request.user)
        b.save()
    else:
        print('hello')
        b.likes += 1
        b.userlikes.add(request.user)
        b.save()
        print('hello')

    print(request.path_info)
    # return home(request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def review_page(request):
    try:
        logged = request.GET['logged']
    except:
        logged = None
    genres = Genre.objects.all()
    context = {'genres' : genres, 'logged':logged}
    return render(request, 'fluffyBooks/post.html', context)

def profile(request):
    username = request.GET['user']
    recommendations = Recommendation.objects.filter(review_user=username)
    
    
    context = {'recommendations':recommendations, 'username':username}
    return render(request, 'fluffyBooks/profile.html', context)

def your_profile(request):
    recs = Recommendation.objects.filter(review_user=request.user.username)
    context = {'recommendations': recs}
    return render(request, 'fluffyBooks/your_profile.html', context)

def account_reviews(request):
    if Recommendation.objects.filter(review_user=request.user.username):
        recs = Recommendation.objects.filter(review_user=request.user.username)
        for rec in recs:
            review_bk = rec.review_book
            reviewstr = str(review_bk)
            splitsi = reviewstr.split(',')
            #splitsiauth = splitsi[1]
            splitbook = splitsi[0]
            
            context = {'recommendations': recs, 'split1': splitbook}
            return render(request, 'fluffyBooks/account_reviews.html', context)
    else:
        recs = None
        context = {'recommendations': recs}
        return render(request, 'fluffyBooks/account_reviews.html', context)

#def populate_data(request):
    # read the csv and refresh your databalse
    #with open('bookdata.csv', newline='') as f:
        #reader = csv.reader(f, delimiter=',')
        #for row in reader:
    #pass

    

def book(request):
    booko = request.GET['book']#book_id value, key=book in URL
    book_obj = Book.objects.get(pk=booko)
    
    recommendations = Recommendation.objects.filter(review_book=booko)
    context = {'recommendations': recommendations, 'book': book_obj}
    return render(request, f'fluffyBooks/book_detail.html', context)

def genres(request):
    genres = Genre.objects.all()
    context = {'genres':genres}
    return render(request, 'fluffyBooks/genres.html', context)

def post_review(request):


    if request.user.is_authenticated:
        print('in POST section')
        text = request.POST['review_text']
        print(text)
        book_text = request.POST['book_text']
        genre_text = request.POST.getlist('genres')
        print(genre_text, 'genre_text')
        author_text = request.POST['author']
    #print(author_text)

            
        if Author.objects.filter(author_name=author_text).exists():
            author_txt = Author.objects.filter(author_name=author_text)
            author = Author.objects.get(pk=author_txt[0].id)
            print(author)
        else:
             authorqs = Author(author_name=author_text)
             authorqs.save()
             author = Author.objects.get(pk=authorqs.id)
             print(author)

        # genre_txt = Genre.objects.filter(genre_text=genre_text)
        # genre = genre_txt[0]
        # author_txt = Author.objects.filter(author_name=author_text)
        # author = author_txt[0]

        if Book.objects.filter(book_text=book_text).exists():
            book = Book.objects.get(book_text=book_text)
            review = Recommendation(review_text=text, review_user=request.user.username, review_date=timezone.now(), review_book=book)
            book.book_authors.add(author.id)
            for i in genre_text:
                print(i, 'genre_txt')
                if Genre.objects.filter(genre_text=i).exists():
                    genreqs = Genre.objects.filter(genre_text=i)
                    genre = Genre.objects.get(pk=genreqs[0].id)
                    book.book_genres.add(genre)
            review.save()

            messages.success(request, 'You successfully shared a book review!')
            return redirect('/fluffyBooks/')
        else:
            book = Book(book_text=book_text, likes=0)
            review = Recommendation(review_text=text, review_user=request.user.username, review_date=timezone.now(), review_book=book)
            
            book.save()
            
            print(book)
            print(author)
            book.book_authors.add(author.id)
            book.save()
            print(book)
            review.save()
            
            for i in genre_text:
                print(i)
                if Genre.objects.filter(genre_text=i).exists():
                    genre = Genre.objects.filter(genre_text=i)[0]
                    print(genre)
                    book.book_genres.add(genre)

            messages.success(request, 'You successfully shared a book review!')
            return redirect('/fluffyBooks/')
            
    else:
        return redirect('/fluffyBooks/review?logged=false')
        
        

    #book = Book(book_text=book_text, likes=0, book_genre=genre)



    


def books(request):
    books = Book.objects.all()
    context = {'books' : books}
    return render(request, 'fluffyBooks/books.html', context)


def delete_review(request):
    review = request.GET['review']
    reviewo = Recommendation.objects.get(pk=review)
    string_review = str(request.user)

   # if reviewo.review_user != string_review:
      #  print(request.user, reviewo.review_user, type(request.user), type(reviewo.review_user))
       # return HttpResponse('Oopsie, nu uh')
    
    reviewo.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def search(request):
    print('in search...')
    words_searched = request.GET['search']
    key_lis = words_searched.split()
    recommendations = Recommendation.objects.all()
    authors = Author.objects.all()
    
    end_results = []
    for word in key_lis:

        txtbook = Book.objects.filter(book_text__contains=word)
        
        end_results += txtbook
        txtgenre = Genre.objects.filter(genre_text__contains=word)
        print(txtgenre)
        end_results += txtgenre
        
        txtauthor = Author.objects.filter(author_name__contains=word)
        #end_results += txtauthor
        if txtauthor:
            context = {'authors': txtauthor, 'searched':words_searched}
            return render(request, 'fluffyBooks/author.html', context)
        elif txtgenre:
             genre = Genre.objects.get(pk=txtgenre[0].id)
             books = Book.objects.filter(book_genres=genre)
             context = {'subject':genre, 'author': txtauthor, 'cardbooks': books, 'searched':words_searched}
             return render(request, 'fluffyBooks/book_display.html', context)
        elif txtbook:
            book = Book.objects.get(pk=txtbook[0].id)
            context = {'subject':book, 'author': txtauthor, 'cardbooks': txtbook, 'searched':words_searched}
            return render(request, 'fluffyBooks/book_display.html', context)
        else:
            context = {'searched': words_searched}
            return render(request, 'fluffyBooks/search.html', context)
    
    #end_results.sort(reverse=True)

   

def author_detail(request):
    author = request.GET['author']#author id
    print(author,"author_id")
    author_obj = Author.objects.get(pk=author)

    author_books = Book.objects.filter(book_authors=author)
    print(author_books)
    context = {'cardbooks':author_books, 'author':author_obj}
    return render(request, 'fluffyBooks/author_detail.html', context)

def genre_pages(request):
    genre = request.GET['genre']

    genre_obj = Genre.objects.get(pk=genre)

    books = Book.objects.filter(book_genres=genre)

    context = {'cardbooks' : books, 'subject' : genre_obj}

    return render(request, 'fluffyBooks/book_display.html', context)
