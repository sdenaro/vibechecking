from app import create_app, db
from app.models.models import Book
from datetime import date

def seed_data():
    app = create_app()
    with app.app_context():
        db.create_all()

        if Book.query.first():
            return

        books = [
            Book(title='The Great Gatsby', publish_date=date(1925, 4, 10), author='F. Scott Fitzgerald', isbn='9780743273565'),
            Book(title='To Kill a Mockingbird', publish_date=date(1960, 7, 11), author='Harper Lee', isbn='9780061120084'),
            Book(title='1984', publish_date=date(1949, 6, 8), author='George Orwell', isbn='9780451524935'),
            Book(title='The Catcher in the Rye', publish_date=date(1951, 7, 16), author='J.D. Salinger', isbn='9780316769488'),
            Book(title='The Lord of the Rings', publish_date=date(1954, 7, 29), author='J.R.R. Tolkien', isbn='9780618640157'),
            Book(title='Pride and Prejudice', publish_date=date(1813, 1, 28), author='Jane Austen', isbn='9780141439518'),
            Book(title='The Diary of a Young Girl', publish_date=date(1947, 6, 25), author='Anne Frank', isbn='9780553296983'),
            Book(title='The Hobbit', publish_date=date(1937, 9, 21), author='J.R.R. Tolkien', isbn='9780618260300'),
            Book(title='Fahrenheit 451', publish_date=date(1953, 10, 19), author='Ray Bradbury', isbn='9781451673319'),
            Book(title='Jane Eyre', publish_date=date(1847, 10, 16), author='Charlotte Brontë', isbn='9780141441146')
        ]

        db.session.bulk_save_objects(books)
        db.session.commit()

if __name__ == '__main__':
    seed_data()
