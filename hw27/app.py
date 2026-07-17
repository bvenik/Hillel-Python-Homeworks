"""
Flask application module for managing a collection of books.
"""

import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, NumberRange

db = SQLAlchemy()


class Book(db.Model):
    """
    SQLAlchemy model representing a Book entity.
    """

    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """
        Returns string representation of the Book object.
        :return: string representation containing title
        """
        return f'<Book {self.title}>'


class BookForm(FlaskForm):
    """
    WTForm class for adding and editing a Book.
    """

    title = StringField('Назва', validators=[
        DataRequired(), Length(max=100)
    ])
    author = StringField('Автор', validators=[
        DataRequired(), Length(max=100)
    ])
    year = IntegerField('Рік', validators=[
        DataRequired(), NumberRange(min=0, max=3000)
    ])
    genre = StringField('Жанр', validators=[
        Optional(), Length(max=50)
    ])
    submit = SubmitField('Зберегти книгу')


def create_app(config: dict | None = None) -> Flask:
    """
    Application factory for creating and configuring Flask app.
    :param config: dictionary of configuration overrides
    :return: configured Flask app object
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'dev-secret'
    )

    db_path = os.path.join(app.instance_path, 'books.db')
    os.makedirs(app.instance_path, exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', f'sqlite:///{db_path}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config:
        app.config.update(config)

    db.init_app(app)
    CSRFProtect(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def list_books():
        """
        Renders the list of all stored books.
        :return: rendered HTML page with books table
        """
        books = Book.query.all()
        return render_template('list_books.html', books=books)

    @app.route('/add', methods=['GET', 'POST'])
    def add_book():
        """
        Renders the form to add a new book and handles submission.
        :return: redirect to book list on success, or form page
        """
        form = BookForm()
        if form.validate_on_submit():
            new_book = Book(
                title=form.title.data,
                author=form.author.data,
                year=form.year.data,
                genre=form.genre.data or None
            )
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('list_books'))
        return render_template('add_book.html', form=form)

    @app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
    def edit_book(book_id: int):
        """
        Renders the edit form and updates book data upon submission.
        :param book_id: primary key ID of the book to edit
        :return: redirect to book list on success, or form page
        """
        book = db.get_or_404(Book, book_id)
        if request.method == 'GET':
            form = BookForm(obj=book)
        else:
            form = BookForm()

        if form.validate_on_submit():
            book.title = form.title.data
            book.author = form.author.data
            book.year = form.year.data
            book.genre = form.genre.data or None
            db.session.commit()
            return redirect(url_for('list_books'))
        return render_template('add_book.html', form=form)

    @app.route('/delete/<int:book_id>', methods=['POST'])
    def delete_book(book_id: int):
        """
        Deletes a book from the database by its ID.
        :param book_id: primary key ID of the book to delete
        :return: redirect to book list
        """
        book = db.get_or_404(Book, book_id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('list_books'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
