from django.shortcuts import render , redirect
from . import models
import bcrypt
from .models import User, Book , Author , Review
from django.contrib import messages



# Create your views here.


def index(request):
    return render (request , 'loginpage.html')

def register_user(request):
    errors = User.objects.reg_validator(request.POST)
    if request.method == 'POST':
        if len(errors) >0 : 
            for key, valuee in errors.items():
                messages.error(request ,valuee)
                return redirect('/')
        else:
            user = request.POST
            password =user['regesterd-userpassword']
            PW_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            models.create_user(user['register-username'] ,user['useralice'] , user['regesterd-useremail'] , PW_hash )
            return redirect('/')

def success_login(request ):
    if 'user_id' not in request.session:
        messages.error(request ,'You must login to view that page')
        return redirect('/')
    else:
        context = {
            "user": models.get_user_id(request.session['user_id']),
            "reviews" : models.get_reviews,
            "books" : models.get_all_books,
        }
        return render(request ,'books.html', context )

def login_user(request):
    errors = User.objects.login_validator(request.POST)
    if request.method == 'POST':
        if len(errors) >0 :
            for key, valuee in errors.items():
                messages.error(request ,valuee)
                return redirect('/')
        else:
            users_list = models.get_users_list(request.POST['login-useremail'])
            if len (users_list) == 0 :
                messages.error(request , 'please check your Email/Password')
            if not bcrypt.checkpw(request.POST['login-userpassword'].encode() , users_list[0].password.encode()):
                messages.error(request , 'please check your password')
                return redirect('/')        
            request.session['user_id'] = users_list[0].id
            return redirect('/books')

def logout_user(request):
    request.session.clear()
    return redirect("/")

def add_book_page(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must login to view that page!")
        return redirect("/")
    else:
        context = {
            "authors" : models.get_all_authors(request),}
        return render(request, "addbook.html", context)

def create_book(request):
    errors = Book.objects.Book_validator(request.POST)
    if request.method == "POST":
        if len(errors)> 0 : 
            for key , value in errors.items():
                messages.error(request, value)
            return redirect('/books/addbook')
        else:
            if len(models.get_number_bookexist(request.POST["title"]))>0:
                book = Book.objects.get(title =request.POST['title'])
            else:
                bookk = request.POST
                models.createbook(bookk['title'])
                book = models.get_book(bookk['title'])
                if len(models.get_number_authorsexist(request.POST["new-author"])) < 1:
                    models.create_author(request.POST["new-author"])
                    author=models.get_author(request.POST["new-author"])
                    author.books.add(book)
                else:
                    author = models.get_author(request.POST["exist-author"])
                    author.books.add(book)
            models.create_review(request.POST["rating"],request.POST["review"],models.get_user_id(request.session['user_id']),book)
            return redirect(f'/books/{book.id}')

def bookdetails(request , book_id):
    if 'user_id' not in request.session:
        messages.error(request, "You must login to view that page!")
        return redirect("/")
    else:
        context = {
            "book" : Book.objects.get(id=book_id),
            "user": models.get_user_id(id=request.session['user_id']),
            "book_authors":Book.objects.get(id=book_id).authors.all(),
            "reviews" : Review.objects.filter(book = Book.objects.get(id=book_id)).order_by("-created_at"),
        }
        return render ( request , 'bookdetails.html' , context)

# add review from the form at book detail review 
def addreview(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    Review.objects.create(rating=request.POST["rating"], review=request.POST["review"], user=user, book = book)
    return redirect(f"/books/{book.id}")


def user_info(request,user_id):
    if 'user_id' not in request.session:
        messages.error(request, "You must login to view that page!")
        return redirect('/')
    else:
        context = {
            "user":User.objects.get(id=request.session["user_id"]),
            "total_review":User.objects.get(id=request.session["user_id"]).user_reviews.all().count(),
            "reviews":User.objects.get(id=request.session["user_id"]).user_reviews.all(),
        }
        return render(request , 'user_info.html' , context)
def delete_review(request , review_id ,book_id):

    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect(f'/books/{book_id}')

def delete_review2(request , review_id):

    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect('/books')


