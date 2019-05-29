import datetime
import bcrypt

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from .models import Users, Books, Reviews


def index(request):
    return render(request, 'dojo/index.html')


def register(request):

    errors = Users.objects.check_registration_data(request.POST)
    extra_tags = 'registration_message'
    if len(errors) > 0:
        for _, value in errors.items():
            messages.error(request, value, extra_tags=extra_tags)
        return redirect('/')
    else:
        password_hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())

        new_user = Users.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=password_hash.decode())

        request.session['user_id'] = new_user.id

        messages.success(request, "Thanks for joining us!")
        return redirect('/books')


def login(request):
    extra_tags = 'login_message'

    # Step 1 Check Email
    user_list = Users.objects.filter(email=request.POST['email'])

    if not user_list:
        messages.error(request, 'Email not registered', extra_tags=extra_tags)
        return redirect('/')

    # Step 2 Email found, check password
    user = user_list[0]
    password_matched = bcrypt.checkpw(
        request.POST['password'].encode('utf-8'), user.password.encode('utf-8'))

    if not password_matched:
        messages.error(request, 'Password not correct',
                       extra_tags=extra_tags)
        return redirect('/')

    # Step 3 Email and Password all matched, logging in now!
    request.session['user_id'] = user.id

    return redirect('/books')


def logout(request):
    del request.session['user_id']
    return redirect('/')


def display_book_list(request):
    current_user = Users.objects.get(id=int(request.session['user_id']))
    book_list = []
    all_reviews = Reviews.objects.all()
    for review in all_reviews:
        if review.book not in book_list:
            book_list.append(review.book)

    latest_review = Reviews.objects.all().order_by('-id')[:3]
    context = {
        'current_user': current_user,
        'latest_review': latest_review,
        'book_list': book_list
    }

    return render(request, 'dojo/display_book_list.html', context)


def display_add_book(request):
    current_user = Users.objects.get(id=int(request.session['user_id']))
    context = {
        'current_user': current_user
    }

    return render(request, 'dojo/display_add_book.html', context)


def process_add_book(request):
    current_user = Users.objects.get(id=int(request.session['user_id']))

    # Add a new book
    title = request.POST['title']
    author = request.POST['author']
    book = Books.objects.create(
        title=title, author=author, user=current_user
    )
    book_id = book.id

    # Add a new review for this book
    text = request.POST['review']
    rating = int(request.POST['rating'])

    review = Reviews.objects.create(
        book=book, text=text, user=current_user, rating=rating
    )

    return redirect('/books/' + str(book_id))


def display_book(request, book_id):
    request.session['book_id'] = book_id
    current_user = Users.objects.get(id=int(request.session['user_id']))

    book = Books.objects.get(id=book_id)
    book_list = Books.objects.all()
    context = {
        'current_user': current_user,
        'book': book,
        'book_list': book_list
    }
    return render(request, 'dojo/display_book.html', context)


def add_review(request):
    text = request.POST['review']
    rating = request.POST['rating']

    current_user = Users.objects.get(id=int(request.session['user_id']))
    book = Books.objects.get(id=int(request.POST['book_id']))

    Reviews.objects.create(text=text, rating=rating,
                           user=current_user, book=book)

    book_id = request.POST['book_id']
    return redirect('/books/' + book_id)


def delete_review(request):
    if request.session['user_id'] == request.POST['review_user_id']:
        this_review = Reviews.objects.get(id=request.POST['review_id'])
        this_review.delete()
        book_id = request.session['book_id']
        return redirect('/books/' + book_id)
    else:
        return HttpResponse("Stop doing it !!")


def display_user(request, user_id):
    current_user = Users.objects.get(id=int(request.session['user_id']))

    this_user = Users.objects.get(id=user_id)
    this_user_reviews = Reviews.objects.filter(user=this_user)

    this_user_books = []
    for review in this_user_reviews:
        if review.book not in this_user_books:
            this_user_books.append(review.book)

    context = {
        'current_user': current_user,
        'this_user': this_user,
        'review_list': this_user_reviews,
        'book_list': this_user_books,
        'reviews_num': str(len(this_user_reviews))
    }
    return render(request, 'dojo/display_user.html', context)
