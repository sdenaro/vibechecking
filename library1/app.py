
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    checkouts = db.relationship('Checkout', backref='book', lazy=True)

class Checkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    checkout_date = db.Column(db.Date, nullable=False, default=date.today)
    due_date = db.Column(db.Date, nullable=False, default=lambda: date.today() + timedelta(days=10))
    returned_date = db.Column(db.Date)
    user = db.relationship('User', backref='checkouts')


def pre_load_books():
    books = [
        {'title': 'The Great Gatsby', 'publish_date': date(1925, 4, 10), 'author': 'F. Scott Fitzgerald', 'isbn': '9780743273565'},
        {'title': 'To Kill a Mockingbird', 'publish_date': date(1960, 7, 11), 'author': 'Harper Lee', 'isbn': '9780061120084'},
        {'title': '1984', 'publish_date': date(1949, 6, 8), 'author': 'George Orwell', 'isbn': '9780451524935'},
        {'title': 'The Catcher in the Rye', 'publish_date': date(1951, 7, 16), 'author': 'J.D. Salinger', 'isbn': '9780316769488'},
        {'title': 'The Lord of the Rings', 'publish_date': date(1954, 7, 29), 'author': 'J.R.R. Tolkien', 'isbn': '9780618640157'},
        {'title': 'Pride and Prejudice', 'publish_date': date(1813, 1, 28), 'author': 'Jane Austen', 'isbn': '9780141439518'},
        {'title': 'The Diary of a Young Girl', 'publish_date': date(1947, 6, 25), 'author': 'Anne Frank', 'isbn': '9780553296983'},
        {'title': 'The Hobbit', 'publish_date': date(1937, 9, 21), 'author': 'J.R.R. Tolkien', 'isbn': '9780618260300'},
        {'title': 'One Hundred Years of Solitude', 'publish_date': date(1967, 5, 30), 'author': 'Gabriel Garcia Marquez', 'isbn': '9780060883287'},
        {'title': 'Brave New World', 'publish_date': date(1932, 8, 30), 'author': 'Aldous Huxley', 'isbn': '9780060850524'}
    ]
    for book_data in books:
        if not Book.query.filter_by(isbn=book_data['isbn']).first():
            book = Book(**book_data)
            db.session.add(book)
    db.session.commit()

from forms import UserForm, BookForm, CheckoutForm, ReturnForm


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, email=form.email.data, phone=form.phone.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('user_form.html', form=form, title='Add User')

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.phone = form.phone.data
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('user_form.html', form=form, title='Edit User')

@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

@app.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        publish_date = form.publish_date.data
        new_book = Book(title=form.title.data, author=form.author.data, publish_date=publish_date, isbn=form.isbn.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('book_form.html', form=form, title='Add Book')

@app.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.publish_date = form.publish_date.data
        book.isbn = form.isbn.data
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('book_form.html', form=form, title='Edit Book')

@app.route('/books/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books'))

@app.route('/checkouts')
def checkouts():
    checkouts = Checkout.query.all()
    return render_template('checkouts.html', checkouts=checkouts)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout_book():
    form = CheckoutForm()
    if form.validate_on_submit():
        checkout = Checkout.query.filter_by(book_id=form.book_id.data, returned_date=None).first()
        if checkout:
            return 'Book already checked out', 400
        new_checkout = Checkout(user_id=form.user_id.data, book_id=form.book_id.data)
        db.session.add(new_checkout)
        db.session.commit()
        return redirect(url_for('checkouts'))
    return render_template('checkout_form.html', form=form)

@app.route('/return', methods=['GET', 'POST'])
def return_book():
    form = ReturnForm()
    if form.validate_on_submit():
        checkout = Checkout.query.get_or_404(form.checkout_id.data)
        if checkout.returned_date:
            return 'Book already returned', 400
        checkout.returned_date = date.today()
        db.session.commit()
        return redirect(url_for('checkouts'))
    return render_template('return_form.html', form=form)

@app.route('/overdue_books')
def overdue_books():
    overdue_books = Checkout.query.filter(Checkout.due_date < date.today(), Checkout.returned_date == None).all()
    return render_template('overdue_books.html', overdue_books=overdue_books)

@app.route('/user_checkouts')
def user_checkouts():
    user_checkouts = Checkout.query.filter(Checkout.returned_date == None).all()
    return render_template('user_checkouts.html', user_checkouts=user_checkouts)

@app.route('/book_checkout_stats')
def book_checkout_stats():
    most_checked_out = Book.query.outerjoin(Checkout).group_by(Book.id).order_by(db.func.count(Checkout.id).desc()).all()
    fewest_checked_out = Book.query.outerjoin(Checkout).group_by(Book.id).order_by(db.func.count(Checkout.id).asc()).all()
    return render_template('book_checkout_stats.html', most_checked_out=most_checked_out, fewest_checked_out=fewest_checked_out)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        pre_load_books()
    app.run(host='0.0.0.0', port=8080, debug=True)
