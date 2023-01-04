from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index),
    path('register' , views.register_user),
    path('books' , views.success_login),
    path ('login' , views.login_user), 
    path('logout' , views.logout_user),
    path('books/addbook' , views.add_book_page),
    path('books/addbook/add' , views.create_book),
    path('books/<int:book_id>' , views.bookdetails),
    path('books/<int:book_id>/addreview', views.addreview),
    path('users/<int:user_id>',views.user_info),
    path('books/<int:review_id>/<int:book_id>/delete' , views.delete_review),
    path("books/<int:review_id>/delete", views.delete_review2),
    #path("books/<int:book_id>/delete" , views.delete_book)
    

]
