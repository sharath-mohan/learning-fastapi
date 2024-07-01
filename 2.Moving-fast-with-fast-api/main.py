from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookPayload(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1, title="this field is required")
    author: str = Field(min_length=1)
    description: str = Field(max_length=255)
    rating: int = Field(gt=0, le=5)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'Harry Potter',
                'author': 'JK Rowling',
                'description': 'A magical story',
                'rating': 5
            }
        }


BOOKS = [
    Book(1, 'Learning ruby', 'Sharath', 'a good book on ruby', 5)
]


@app.get("/")
async def root():
    return {"message": "Hello from fast api"}


@app.get("/books")
async def get_all_books():
    return {"books": BOOKS}


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookPayload):
    new_book = Book(**book.model_dump())
    BOOKS.append(generate_book_id(new_book))


def generate_book_id(book: Book):
    if len(BOOKS) == 0:
        book.id = 1
    else:
        book.id = BOOKS[-1].id + 1
    return book


@app.get("/books/{book_id}")
def get_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Not found")


@app.get("/books/")
def get_book_details(rating: int = Query(gt=0, le=5)):
    books = []
    for book in BOOKS:
        print(rating, book.rating)
        if book.rating == rating:
            books.append(book)
        return books


@app.put("/book", status_code=status.HTTP_204_NO_CONTENT)
def update_book(book: BookPayload):
    book_updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_updated = True
    if not book_updated:
        raise HTTPException(status_code=404, detail="Not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Not found")