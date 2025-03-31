## BOOK LIBRARY APP  

A Book Library App is a software application designed to manage a collection of books.

## Specification

## 1. Data Model

### 1.1. User model

- `id` (Primary Key)
- `full_name` (String)
- `username` (String, Unique)
- `password` (String, Hashed)
- `Role`  (Enum)

## 2.2 Book Model

- `id` (Primary Key)
- `author` (String Unique)
- `description` (Text)
- `image` (Blob)
- `isbn` (String Unique)
- `available` (Bool)
- `borrowed_by` (Foreign Key)
- `borrowed_unilt` (Date)

## 2. Activities [BL(Business Logic)]

- Register User by admin
- Add, Delete, Update a book as an admin
- Read/View Books as guest, admin or user
- Barrow/Return books as guest


## 3. REST API


## 3.1 User UPDATE AND DELETE Endpoints  [users.py]

| Method | Path                     | Description             | Roles               |
|--------|--------------------------|-------------------------|---------------------|
| POST   | `/users`                 | Register a new user     | Admin               |
| GET    | `/users`                 | View list of users      | Admin               |
| PUT    | `/users/<int:user_id>`   | Update a User  account  | Admin               |
| DELETE | `/users/<int:user_id>`   | Delete a User  account  | Admin               |
| PUT    | `/users/me`              | Update my User account  | Admin, User         |
| DELETE | `/users/me`              | Delete my User account  | Admin, User         |


## 3.3 Book CREATE AND READ Endpoints [books.py]

| Method  | Path                                 | Description              | Roles              |
|---------|--------------------------------------|--------------------------|--------------------|
| POST    | `/books`                             | Register a new book      | Admin              |
| GET     | `/books`                             | View list of books       | Admin, Guest, User |
| GET     | `/books/<int:book_id>`               | Update a book            | Admin              |
| PUT     | `/books/<int:book_id>`               | Update a book            | Admin              |
| DELETE  | `/books/<int:book_id>`               | Delete a book            | Admin              |
| GET     | `/books/<int:book_id>/image`         | De-Authenticate user     | Admin, Guest,User  |
| POST    | `/books/<int:book_id>/barrow`        | Borrow a book            | User               |
| POST    | `/books/<int:book_id>/return`        | Return a book            | User               |


# 3.4 Auth Management [auth.py]

| Method | Path         | Description             | Roles               |
|--------|--------------|-------------------------|---------------------|
| POST   | `/login`     |  De-Authenticate user   | Admin, User         |
| GET    | `/logout`    |  Authenticate user      | Admin, User         |

## 3.4 Schemas

### 3.3.1 User request Schema [json data]

- `id` (Integer, ReadOnly)
- `full_name` (String, Required)
- `username` (String, Required)
- `email` (String, Required, Unique)
- `password` (String)
- `Role` (String, Required)

#### 3.4.2 User login Schema  

- `username` (String, Required)
- `password` (String, Required)

### 3.4.3 User raw Schema [user_nested] [json data]

- `id` (Integer, ReadOnly)
- `full_name` (String, Required)
- `username` (String, Required)
- `email` (String, Required, Unique)

### 3.4.4 User response Schema [json data]

- `success` (Boolean, Required)
- `data` (Nested[user_nested], SkipNone=True)

### 3.4.5 User update response Schema [json data]

- `full_name` (String)
- `username` (String)
- `password` (String)
- `Role` (String)
  
### 3.4.6 User login response Schema[json data]

- `success` (Boolean)
- `data` (Nested[user_nested])
- `token` (String,)


### 3.4.7 Book Schema [form data]

- `book_schema_parser` (Parser, Required)
  - `id` (Integer, ReadOnly)
  - `title` (String, Required)
  - `description`  (String, Required)
  - `image` (Blob, Required)
  - `author` (String, Required)
  - `isbn` (String, Required)
  - `available` (Boolean, ReadOnly)
  - `borrowed_by` (Integer, ReadOnly)
  - `borrowed_unilt` (FileStorage, ReadOnly)


#### 3.4.8 Book Request Schema [book_request_schema] [form data]

- `book_request_schema_parser` (Parser, Required)
  - `title` (String, Required)
  - `author` (String, Required)
  - `description`  (String, Required)
  - `image` (String, Required)
  - `isbn` (String, Required)



#### 3.4.9 Book Response Schema

- `success` (Boolean)
- `data` (Nested[book_request_schema],  SkipNone=True)

#### 3.4.10 Book List Schema

- `success` (Boolean)
- `data` (List, Nested Book Schema)
- `total` (Integer)
- `pages` (Integer)

#### 3.4.11 Book Borrow Schema

- `user` (Integer, Required)
- `book` (Integer, Required)
- `borrowed_unilt`  (Date, Required)

#### 3.4.12 Book Image Schema

- `upload_parser` (Parser, Required)
  - `image` (Blob)  
  - `full_name`  (String)  
  - `username`  (String, Unique)  
  - `password`  (String, Unique)  
  - `email` (String, Required, Unique)
  - `Role` (String, Choice[ADMIN, USER, GUEST])


## 5. Scaffold Structure

```text
book-library-app/
├── .gitignore                                  # Ignore unnecessary files
├── .env                                        # Environment variables
├── .vscode/                                    # VSCode settings
│   ├── settings.json                           # Workspace settings
│   └── launch.json                             # Debugging configurations
├── app/                                        # Application logic
│   ├── __init__.py                             # Initialize Flask app
│   ├── email_templates/                        # html jinja email templates direcotry
│   │   └── registration_email_template.html    # registration email jinja template file
│   ├── utils/                                  # Database models
│   │   ├── __init__.py                         # package file
│   │   ├── auth_utils.py                       # User authentication utilities
|   |   ├── date_utils.py                       # date retated utility functions 
│   │   ├── file_utils.py                       # files retated utility functions 
|   |   └── email_utils.py                      # email retated utility functions 
│   ├── models/                                 # Database models
│   │   ├── __init__.py                         # Initialize models
│   │   ├── user.py                             # User model
│   │   └── books.py                            # Book model
│   ├── routes/                                 # Application routes
│   │   ├── __init__.py                         # Initialize routes
│   │   ├── auth.py                             # Authentication routes
|   |   ├── book.py                             # Book borrow and return
|   |   ├── users.py                            # User crud
│   ├── schemas/                                # API schemas
│   │   ├── __init__.py                         # Initialize schemas
│   │   ├── user_schema.py                      # User schema
│   │   └── book_schema.py                      # ToDo schema
├── migrations/                                 # Flask-Migrate folder
├── requirements.txt                            # Python dependencies
├── run.py                                      # Application entry point
└── README.md                                   # Project documentation
```

## 6. JSON version of the scaffold

```json
{
    ".gitignore": "",
    ".env": "",
    ".vscode": {
        "settings.json": "",
        "launch.json": ""
    },
    "app": {
        "__init__.py": "",
        "email_templates": {
            "registration_email_template.html": ""
        },
        "config.py": {
            "database.py": "",
            "email.py": "",
            "upload.py": ""
        },
        "utils": {
            "__init__.py": "",
            "auth_utils.py": "",
            "date_utils.py": "",
            "email_utils.py": "",
            "file_utils.py": ""
        },
        "models": {
            "__init__.py": "",
            "user.py": "",
            "books.py": ""
        },
        "routes": {
            "__init__.py": "",
            "auth.py": "",
            "book.py": "",
            "users.py": ""
        },
        "schemas": {
            "__init__.py": "",
            "user_schema.py": "",
            "book_schema.py": ""
        }
    },
    "migrations": {},
    "requirements.txt": "",
    "run.py": "",
    "README.md": ""
}
```