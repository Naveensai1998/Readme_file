from flask import request, jsonify
from app import app, db
from models import Book, Author, Subject, Bookshelf, Download

@app.route('/books', methods=['GET'])
def get_books():
    query = Book.query

    # Filters
    book_ids = request.args.getlist('book_id')
    if book_ids:
        query = query.filter(Book.id.in_(book_ids))

    languages = request.args.getlist('language')
    if languages:
        query = query.filter(Book.language.in_(languages))

    mime_types = request.args.getlist('mime_type')
    if mime_types:
        query = query.join(Download).filter(Download.mime_type.in_(mime_types))

    topics = request.args.getlist('topic')
    if topics:
        topic_filter = [Subject.name.ilike(f"%{topic}%") | Bookshelf.name.ilike(f"%{topic}%") for topic in topics]
        query = query.join(Subject).join(Bookshelf).filter(db.or_(*topic_filter))

    authors = request.args.getlist('author')
    if authors:
        query = query.join(Author).filter(Author.name.ilike(f"%{author}%") for author in authors)

    title = request.args.get('title')
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = 25
    books = query.order_by(Book.downloads.desc()).paginate(page, per_page, False)

    # Response
    return jsonify({
        "count": books.total,
        "books": [{
            "title": book.title,
            "author": book.author.name,
            "genre": book.genre,
            "language": book.language,
            "subjects": [subject.name for subject in book.subjects],
            "bookshelves": [bookshelf.name for bookshelf in book.bookshelves],
            "downloads": [{"mime_type": d.mime_type, "link": d.link} for d in book.downloads]
        } for book in books.items]
    })
