from django.db import models
import re 
from django.contrib import messages
import bcrypt
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class UserManger(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if (len(postData['register-username']) == 0 or
            len(postData['useralice']) == 0 or
            len(postData['regesterd-useremail']) == 0 or
            len(postData['regesterd-userpassword']) == 0):
            errors['empty_field'] = "All fields must be completed for registration."
        
        if len(postData['register-username']) < 2:
            errors['register-username'] = 'Name has to be at least 2 characters.'
        if len(postData['useralice']) < 2:
            errors['useralice'] = 'The Alice name has to be at least 2 characters.'
        if not EMAIL_REGEX.match(postData['regesterd-useremail']):         
            errors['email'] = "Invalid email address!"
        if postData['regesterd-userpassword'] != postData['regesterd-C-userpassword']:
            errors['password_no_match'] = 'Your passwords do not match.'
        if len(postData['regesterd-userpassword']) < 8:
            errors['short_password'] = 'The password has to be at least 8 characters.'
        
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if (len(postData['login-useremail']) ==0):
            errors['email'] = "Email address should be filled" 
        if (len(postData['login-userpassword']) ==0):
            errors['password'] = "Password address should be filled" 

        return errors

class BookManager(models.Manager):
    def Book_validator(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = 'Please fill out the Book title field.'
        return errors

class User(models.Model):
    name = models.CharField(max_length=65)
    alias = models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManger()

class Book(models.Model):
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()

class Review(models.Model):
    rating =models.FloatField()
    review = models.TextField()
    user = models.ForeignKey(User, related_name = "user_reviews" ,on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name = "book_reviews" , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

class Author(models.Model):
    name = models.CharField(max_length = 255)
    books = models.ManyToManyField(Book, related_name="authors")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    





def create_user(name , alias , email , password):
    return User.objects.create(name=name , alias=alias , email=email , password=password)

def createbook(title):
    return Book.objects.create(title = title)

# success_login
def get_user_id(id):
    return User.objects.get(id=id)
# success_login
def get_reviews():
    query = 'SELECT * FROM Reads_App_Review ORDER BY created_at DESC LIMIT 3'
    return Review.objects.raw(query)
# success_login
def get_all_books():
    return Book.objects.all().order_by("-created_at")
# login_user 
def get_users_list(email):
    return User.objects.filter(email=email)

def get_all_authors(request):
    return Author.objects.all()

def get_number_bookexist(title):
    return Book.objects.filter(title=title)

def get_book(title):
    return Book.objects.get(title=title)

def get_number_authorsexist(name):
    return Author.objects.filter(name=name)

def create_author(name):
    return Author.objects.create(name=name)

def get_author(name):
    return Author.objects.get(name=name)

def create_review(rating , review , user , book):
    return Review.objects.create(rating=rating ,review=review ,user = user , book = book)

def get_book_by_id(book_id):
    Book.objects.get(book_id=book_id)

def book_reviews(book):
    Review.objects.filter(book=book)

def get_review(review_id):
    Review.objects.get(review_id = review_id)







