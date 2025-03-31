import logging
import requests
from flask import Flask
from app.models import db
from sqlalchemy.dialects.mysql import LONGBLOB


# Correct the logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(LONGBLOB, nullable=True)  # Store image as binary data
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    available = db.Column(db.Boolean, default=True)
    borrowed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    borrowed_unilt = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "isbn": self.isbn,
            "available": self.available,
            "borrowed_by": self.borrowed_by,
            "borrowed_unilt": (
                self.borrowed_unilt.isoformat()
                if self.borrowed_unilt is not None
                else ""
            ),
        }

    @staticmethod
    def creat_inital_books(app: Flask) -> None:
        books = [
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "isbn": "9780061120084",
                "description": "A novel about racial injustice in the Deep South.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg/800px-To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg",
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "isbn": "9780451524935",
                "description": "A dystopian novel about totalitarianism and surveillance.",
                "image": "https://tankmuseumshop.org/cdn/shop/products/1984.jpg",
            },
            {
                "title": "Animal Farm",
                "author": "George Orwell",
                "isbn": "9780451526342",
                "description": "A satirical allegory about the Russian Revolution.",
                "image": "https://www.tronsmo.no/wp-content/uploads/2024/04/animal-farm.jpg",
            },
            {
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "isbn": "9780141439518",
                "description": "A classic romance novel about love and social class.",
                "image": "https://www.printspublications.com/public/upload/product/1674117753.png",
            },
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "isbn": "9780743273565",
                "description": "A novel about the American Dream and 1920s excess.",
                "image": "https://images-na.ssl-images-amazon.com/images/I/81af+MCATTL.jpg",
            },
            {
                "title": "Moby-Dick",
                "author": "Herman Melville",
                "isbn": "9781503280786",
                "description": "A whaling adventure and a study of obsession.",
                "image": "https://cdn11.bigcommerce.com/s-5uqrjcd/images/stencil/1280x1280/products/39882/57942/9781612474519__15114.1589553997.jpg?c=2",
            },
            {
                "title": "War and Peace",
                "author": "Leo Tolstoy",
                "isbn": "9781400079988",
                "description": "A historical epic about Napoleon's invasion of Russia.",
                "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1686602284i/177106015.jpg",
            },
            {
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "isbn": "9780316769488",
                "description": "A coming-of-age novel about teenage rebellion.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Catcher-in-the-rye-red-cover.jpg",
            },
            {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "isbn": "9780547928227",
                "description": "A fantasy adventure about Bilbo Baggins and a dragon.",
                "image": "https://medien.umbreitkatalog.de/bildzentrale_original/978/360/810/1386.jpg",
            },
            {
                "title": "Crime and Punishment",
                "author": "Fyodor Dostoevsky",
                "isbn": "9780486454115",
                "description": "A psychological novel about guilt and redemption.",
                "image": "https://cdn.kobo.com/book-images/644e222d-8074-4cd8-a568-0ee830476007/353/569/90/False/crime-and-punishment-150.jpg",
            },
            {
                "title": "Brave New World",
                "author": "Aldous Huxley",
                "isbn": "9780060850524",
                "description": "A dystopian novel about a future society controlled by science.",
                "image": "https://images.thalia.media/00/-/d6adb59c9940430f937a27a1b76ae4a1/brave-new-world-taschenbuch-aldous-huxley-englisch.jpeg",
            },
            {
                "title": "The Lord of the Rings",
                "author": "J.R.R. Tolkien",
                "isbn": "9780544003415",
                "description": "An epic fantasy about the battle against evil in Middle-earth.",
                "image": "https://funfandomblog.wordpress.com/wp-content/uploads/2018/08/lord-of-the-rings.jpg?w=273&h=409",
            },
            {
                "title": "Fahrenheit 451",
                "author": "Ray Bradbury",
                "isbn": "9781451673319",
                "description": "A novel about a future where books are banned and burned.",
                "image": "https://images.thalia.media/00/-/3d0a71ea9ac64678958b83c6ff20d0e1/fahrenheit-451-taschenbuch-ray-bradbury-englisch.jpeg",
            },
            {
                "title": "Jane Eyre",
                "author": "Charlotte Brontë",
                "isbn": "9780141441146",
                "description": "A novel about a young woman's journey to independence.",
                "image": "https://media.suhrkamp.de/mediadelivery/rendition/ffd6032948764d4ca589322e5d18074d/-B2160/jane-eyre_9783458364252_cover.jpg",
            },
            {
                "title": "The Odyssey",
                "author": "Homer",
                "isbn": "9780140268867",
                "description": "An epic poem about the adventures of Odysseus.",
                "image": "https://d28hgpri8am2if.cloudfront.net/book_images/cvr9781416500360_9781416500360_lg.jpg",
            },
            {
                "title": "Wuthering Heights",
                "author": "Emily Brontë",
                "isbn": "9780141439556",
                "description": "A gothic romance about love and revenge.",
                "image": "https://wordsworth-editions.com/wp-content/uploads/2019/03/Wuthering-Heights-Front-Cover-scaled.jpg",
            },
            {
                "title": "The Divine Comedy",
                "author": "Dante Alighieri",
                "isbn": "9780142437223",
                "description": "A poetic journey through Hell, Purgatory, and Paradise.",
                "image": "https://prodimage.images-bn.com/pimages/9788027339709_p0_v1_s1200x1200.jpg",
            },
            {
                "title": "Frankenstein",
                "author": "Mary Shelley",
                "isbn": "9780486282114",
                "description": "A gothic novel about the consequences of playing God.",
                "image": "https://assets.nationbuilder.com/tgbc/pages/3778/attachments/original/1725856996/Frankenstein-cover.jpg?1725856996",
            },
            {
                "title": "Dracula",
                "author": "Bram Stoker",
                "isbn": "9780486411095",
                "description": "A classic horror novel about the legendary vampire Count Dracula.",
                "image": "https://npr.brightspotcdn.com/dims4/default/b95f426/2147483647/strip/true/crop/314x500+0+0/resize/1760x2802!/format/webp/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2Flegacy%2Fsites%2Fwkar%2Ffiles%2Fdracula_book_cover.jpg",
            },
        ]

        with app.app_context():
            db.create_all()
            for book_data in books:
                existing_book = Book.query.filter_by(isbn=book_data["isbn"]).first()
                if not existing_book:
                    try:
                        # Download the image and store it as binary
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                        }
                        response = requests.get(book_data["image"], headers=headers)
                        response.raise_for_status()
                        image_binary = response.content

                        new_book = Book(
                            title=book_data["title"],
                            author=book_data["author"],
                            isbn=book_data["isbn"],
                            description=book_data["description"],
                            image=image_binary,
                        )
                        db.session.add(new_book)
                        db.session.commit()
                        logging.info(f"Added book: {book_data['title']}")
                    except requests.RequestException as e:
                        logging.info(
                            f"Failed to download image for {book_data['title']}: {e}"
                        )
