from http import HTTPStatus
import logging
import mimetypes
import os
from flask_restx import Namespace, Resource
from flask import Response, g, request

from app.models.books import Book
from app.models import db
from app.models.user import User

from app.schemas.book_schema import (
    book_list_schema,
    book_schema_parser,
    book_response_schema,
    book_borrow_schema,
    book_request_schema_parser,
    book_query_parser,
)
from app.models.user import UserRole

from app.utils.auth_utils import auth_required
from app.utils.files import is_allowed_file

# Correct the logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

books_ns = Namespace("Book", description="Book management")


@books_ns.route("/")
class BooksList(Resource):

    @books_ns.expect(book_query_parser, validate=True)
    @books_ns.response(HTTPStatus.OK, "Books retrieved", book_list_schema)
    def get(self) -> Response:
        """Retrieve a list of books with pagination and filtering."""
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        title = request.args.get("title", type=str)
        author = request.args.get("author", type=str)
        description = request.args.get("description", type=str)

        query = Book.query
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if description:
            query = query.filter(Book.genre.ilike(f"%{description}%"))

        books_query = query.paginate(page=page, per_page=per_page, error_out=False)
        books = books_query.items

        return {
            "success": True,
            "data": [book.to_dict() for book in books],
            "total": books_query.total,
            "pages": books_query.pages,
            "current_page": books_query.page,
            "per_page": books_query.per_page,
        }, HTTPStatus.OK

    @books_ns.expect(book_schema_parser, validate=True)
    @books_ns.response(HTTPStatus.CREATED, "Book added", book_response_schema)
    @books_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN])
    def post(self) -> Response:
        """Add a new book to the database (admin only)."""
        try:

            args = book_schema_parser.parse_args()

            image_file = args["image"]
            if not is_allowed_file(image_file.filename):
                return {
                    "success": False,
                    "message": "Invalid file type. Allowed types are: png, jpg, jpeg, gif.",
                }, HTTPStatus.BAD_REQUEST

            image_data = image_file.read()
            title = args["title"]
            author = args["author"]
            description = args["description"]
            isbn = args["isbn"]

            book = Book(
                title=title,
                author=author,
                description=description,
                isbn=isbn,
                image=image_data,
            )
            db.session.add(book)
            db.session.commit()

            return {"success": True, "data": book.to_dict()}, HTTPStatus.CREATED
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {
                "success": False,
                "message": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@books_ns.route("/<int:book_id>")
class BooksResource(Resource):
    @books_ns.response(HTTPStatus.OK, "Book retrieved", book_response_schema)
    @books_ns.response(HTTPStatus.NOT_FOUND, "Book not found")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN, UserRole.USER])
    def get(self, book_id: int) -> Response:
        """Retrieve a specific book by ID."""
        book = Book.query.get(book_id)
        if book:
            return {"success": True, "data": book.to_dict()}, HTTPStatus.OK
        return {"success": False, "message": "Book not found"}, HTTPStatus.NOT_FOUND

    @books_ns.expect(book_request_schema_parser, validate=True)
    @books_ns.response(HTTPStatus.CREATED, "Book updated", book_response_schema)
    @books_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN])
    def put(self, book_id: int) -> Response:
        """Update an existing book (admin only)."""
        args = book_request_schema_parser.parse_args()
        book = Book.query.get(book_id)
        try:
            if book:
                if image := args.get("image"):
                    book.image = image.read()
                if title := args.get("title"):
                    book.title = title
                if author := args.get("author"):
                    book.author = author
                if description := args.get("description"):
                    book.description = description
                if isbn := args.get("isbn"):
                    book.isbn = isbn
                if available := args.get("available"):
                    book.available = available
                db.session.commit()
                return {"success": True, "data": book.to_dict()}, HTTPStatus.OK
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {
                "message": f"An error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        return {"success": False}, HTTPStatus.NOT_FOUND

    @books_ns.response(HTTPStatus.OK, "Book deleted")
    @books_ns.response(HTTPStatus.NOT_FOUND, "Book not found")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN])
    def delete(self, id: int) -> Response:
        """Delete a book from the database (admin only)."""
        book = Book.query.get(id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {"success": True}, HTTPStatus.OK
        return {"success": False, "message": "Book not found"}, HTTPStatus.NOT_FOUND


@books_ns.route("/<int:book_id>/image")
class BookServeImage(Resource):
    @books_ns.response(
        HTTPStatus.OK, "Image retrieved as binary data (e.g., image/jpeg)"
    )
    @books_ns.response(HTTPStatus.NOT_FOUND, "Image not found")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.produces(["image/jpeg"])  # Specify the MIME type of the response
    def get(self, book_id: int) -> Response:
        """Serve the image of a specific book."""
        book = Book.query.get(book_id)
        if not book:
            return {"message": "Book not found"}, HTTPStatus.NOT_FOUND

        try:
            mime_type = "image/jpeg"
            return Response(book.image, mimetype=mime_type)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {
                "message": f"An error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@books_ns.route("/<int:book_id>/barrow")
class BookBorrowResrouce(Resource):
    @books_ns.response(HTTPStatus.CREATED, "Book borrowed", book_borrow_schema)
    @books_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.doc(security=["basic, jwt"])
    @auth_required([UserRole.ADMIN, UserRole.USER])
    def put(self, book_id: int) -> Response:
        """Borrow a book from the library."""
        try:
            args = book_schema_parser.parse_args()
            book = Book.query.get(book_id)
            user_id = g.current_user["user_id"]
            user = User.query.get(user_id)
            if book and user:
                book.borrowed_by = user.id
                book.borrowed_until = args["borrowed_until"]
                book.available = False
                db.session.commit()
                return {
                    "message": "Book borrowed",
                    "user": user.username,
                    "book": book.title,
                    "borrowed_until": book.borrowed_until,
                }, HTTPStatus.CREATED
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {
                "message": f"An error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        return {"message": "Book not found"}, HTTPStatus.NOT_FOUND


@books_ns.route("/<int:book_id>/return")
class BookReturnResrouce(Resource):
    @books_ns.response(HTTPStatus.CREATED, "Book returned")
    @books_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.doc(security=["basic, jwt"])
    @auth_required([UserRole.ADMIN, UserRole.USER])
    def put(self, id: int) -> Response:
        """Return a borrowed book to the library."""
        book = Book.query.get(id)
        if book:
            book.borrowed_by = None
            book.borrowed_until = None
            book.available = True
            db.session.commit()
            return {"message": "Book returned"}, HTTPStatus.CREATED
        return {"message": "Book not found"}, HTTPStatus.NOT_FOUND
