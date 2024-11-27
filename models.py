from app import db

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    genre = db.Column(db.String)
    language = db.Column(db.String)
    downloads = db.Column(db.Integer, default=0)
    author = db.relationship('Author', backref='books')

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

class Bookshelf(db.Model):
    __tablename__ = 'bookshelves'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

class Download(db.Model):
    __tablename__ = 'downloads'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    mime_type = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
