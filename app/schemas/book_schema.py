from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage


from app.schemas import api


# Define the schema parser for query parameters
book_query_parser = reqparse.RequestParser()
book_query_parser.add_argument(
    "page", type=int, default=1, help="Page number for pagination"
)
book_query_parser.add_argument(
    "per_page", type=int, default=10, help="Number of items per page"
)
book_query_parser.add_argument(
    "title", type=str, required=False, help="Filter by book title"
)
book_query_parser.add_argument(
    "author", type=str, required=False, help="Filter by book author"
)
book_query_parser.add_argument(
    "description", type=str, required=False, help="Filter by book description"
)

book_schema_parser = reqparse.RequestParser()  # form data schema
#  input text
book_schema_parser.add_argument(
    "title", type=str, required=True, help="Book title is required"
)
#  input text
book_schema_parser.add_argument(
    "description", type=str, required=True, help="Book description is requireed"
)
#  input file/upload
book_schema_parser.add_argument(
    "image",
    type=FileStorage,
    required=True,
    location="files",
    help="Image file is required",
)
#  input text
book_schema_parser.add_argument(
    "author", type=str, required=True, help="Book author is requireed"
)
#  input text
book_schema_parser.add_argument(
    "isbn", type=str, required=True, help="Book isbn number is requireed"
)


book_request_schema_parser = reqparse.RequestParser()  # form data schema
#  input text
book_request_schema_parser.add_argument(
    "title", type=str, required=False, help="Book title is required"
)
#  input text
book_request_schema_parser.add_argument(
    "description", type=str, required=False, help="Book description is requireed"
)
#  input file/upload
book_request_schema_parser.add_argument(
    "image",
    type=FileStorage,
    required=False,
    location="files",
    help="Image file is required",
)
#  input text
book_request_schema_parser.add_argument(
    "author", type=str, required=False, help="Book author is requireed"
)
#  input text
book_request_schema_parser.add_argument(
    "isbn", type=str, required=False, help="Book isbn number is requireed"
)


book_schema = api.model(
    "BookModel",
    {
        "id": fields.Integer(readonly=True),
        "title": fields.String(required=True),
        "author": fields.String(required=True),
        "description": fields.String(required=True),
        "isbn": fields.String(required=True),
        "available": fields.Boolean(readonly=True),
        "borrowed_by": fields.Integer(readonly=True),
        "borrowed_unilt": fields.String(readonly=True),
    },
)


# json data schema
book_response_schema = api.model(
    "BookResponseModel",
    {
        "success": fields.Boolean(),
        "data": fields.Nested(book_schema, skip_none=True),
    },
)

# json data schema
book_list_schema = api.model(
    "BookListResponseModel",
    {
        "success": fields.Boolean(),
        "data": fields.List(fields.Nested(book_schema)),
        "total": fields.Integer(),
        "pages": fields.Integer(),
        "current_page": fields.Integer(),
        "per_page": fields.Integer(),
    },
)

# json data schema
book_borrow_schema = api.model(
    "BookBorrowResponseModel",
    {
        "message": fields.String(required=True),
        "user": fields.String(required=True),
        "book": fields.String(required=True),
        "borrowed_unilt": fields.Date(required=True),
    },
)
