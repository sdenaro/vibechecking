
from flask import render_template, redirect, url_for, flash, request
from app import db
from app.models.models import User, Book, Checkout
from app.forms import UserForm, BookForm, CheckoutForm, ReturnForm
from datetime import datetime

from flask import current_app as app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully!')
        return redirect(url_for('users'))
    return render_template('add_user.html', form=form)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            publish_date=datetime.strptime(form.publish_date.data, '%Y-%m-%d').date(),
            author=form.author.data,
            isbn=form.isbn.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('books'))
    return render_template('add_book.html', form=form)

@app.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        book = Book.query.get(form.book_id.data)
        if not book:
            flash('Book not found!')
            return redirect(url_for('checkout'))

        existing_checkout = Checkout.query.filter_by(book_id=book.id, returned_date=None).first()
        if existing_checkout:
            flash('Book is already checked out!')
            return redirect(url_for('checkout'))

        checkout = Checkout(user_id=form.user_id.data, book_id=form.book_id.data)
        db.session.add(checkout)
        db.session.commit()
        flash('Book checked out successfully!')
        return redirect(url_for('index'))
    return render_template('checkout.html', form=form)

@app.route('/return', methods=['GET', 'POST'])
def return_book():
    form = ReturnForm()
    if form.validate_on_submit():
        checkout = Checkout.query.get(form.checkout_id.data)
        if not checkout:
            flash('Checkout not found!')
            return redirect(url_for('return_book'))

        if checkout.returned_date:
            flash('Book already returned!')
            return redirect(url_for('return_book'))

        checkout.returned_date = datetime.utcnow()
        db.session.commit()
        flash('Book returned successfully!')
        return redirect(url_for('index'))
    return render_template('return.html', form=form)

@app.route('/overdue_books')
def overdue_books():
    overdue_checkouts = Checkout.query.filter(Checkout.due_date < datetime.utcnow(), Checkout.returned_date == None).all()
    return render_template('overdue_books.html', checkouts=overdue_checkouts)

@app.route('/user_checkouts')
def user_checkouts():
    users = User.query.all()
    return render_template('user_checkouts.html', users=users, now=datetime.utcnow())

@app.route('/book_popularity')
def book_popularity():
    books = Book.query.all()
    return render_template('book_popularity.html', books=books)

