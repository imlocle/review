from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager, Book, Review
from django.db.models import Count
import bcrypt

def index(request):
    return render(request, 'beltreview/index.html')

def register(request):
    name = request.POST['name']
    alias = request.POST['alias']
    email = request.POST['email']
    password = request.POST['password']
    conpass = request.POST['conpass']
    check = User.objects.register(name, alias, email, password, conpass)
    if check == True:
        pwhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(name = name, alias = alias, email = email, password = pwhash)
        request.session['current_user'] = user.id
        return redirect ('/books')
    else:
        for i in range(0, len(check)):
            messages.warning(request, check[i])
        return redirect ('/')

def books(request): #illustrating to the user the books
    user = User.objects.get(id = request.session['current_user'])
    first_three = Book.objects.all()[0:3]
    book = Book.objects.all()[3:]
    context = {'user': user, 'books': book, 'first_three':first_three}
    return render(request, 'beltreview/books.html', context)

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    check = User.objects.login(email, password)
    if check == True:
        user = User.objects.get(email = email)
        request.session['current_user'] = user.id
        return redirect('/books')
    else:
        messages.warning(request, check[0])
        return redirect('/')

def logout(request):
    request.session['current_user'] = 0
    return redirect('/')

def add(request):
    user = User.objects.get(id = request.session['current_user'])
    author = Book.objects.values('author').annotate(count = Count('author'))#annotate groups an author with multiple books using the count
    context = {'users':user, 'authors':author}
    return render(request, 'beltreview/add.html', context)

def addbook(request):
    user = User.objects.get(id = request.session['current_user'])
    book = request.POST['book']
    if len(request.POST['oldauthor']) > 0:
        author = request.POST['oldauthor']
    else:
        author = request.POST['newauthor']
    rating = request.POST['rating']
    review = request.POST['review']
    new_book = Book.objects.create(book = book, author = author)
    Review.objects.create(book = new_book, name = user,rating = rating, review = review)
    book_id = new_book.id
    return redirect('/bookprofile/%s' % book_id) #linking redirect with ID

def bookprofile(request, id):
    book = Book.objects.get(id = id)
    context = {'books': book}
    return render(request, 'beltreview/bookprofile.html', context)

def addreview(request):
    book = Book.objects.get(id = request.POST['book'])
    user = User.objects.get(id = request.session['current_user'])
    rating = request.POST['rating']
    review = request.POST['review']
    Review.objects.create(book = book, name = user,rating = rating, review = review)
    return redirect('/bookprofile/%s' % book.id)

def userprofile(request, id):
    user = User.objects.get(id = id)
    books = []
    user_count = Review.objects.filter(name = user).annotate(count = Count('review'))
    user_review = Review.objects.annotate(count = Count('review')).filter(name = user).values('book')
    for b in user_review:
        the_book = Book.objects.get(id = b['book'])
        books.append(the_book.book)
    non_repeating = []
    for a in range(0, len(books)):
        if a+1<len(books) and books[a] != books[a+1]:
            book = Book.objects.get(book = books[a])
            non_repeating.append({'name':books[a], 'id': book.id})
    book = Book.objects.get(book = books[len(books)-1])
    non_repeating.append({'name':books[len(books)-1], 'id': book.id})
    context = {'user':user, 'user_count':user_count, 'user_review':user_review, 'all': non_repeating}
    return render(request, 'beltreview/user.html', context)
