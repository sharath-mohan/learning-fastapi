from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    category: str


app = FastAPI()
BOOKS = [
    {'title': 'title 1', 'author': 'author 1', 'category': 'science'},
    {'title': 'title 2', 'author': 'author 2', 'category': 'science'},
    {'title': 'title 3', 'author': 'author 3', 'category': 'history'},
    {'title': 'title 4', 'author': 'author 4', 'category': 'math'},
    {'title': 'title 5', 'author': 'author 5', 'category': 'science'},
]


@app.get("/")
async def first_api():
    return {"message": "Hello from fastapi"}


@app.get("/books/")
async def filter_book(category: str):
    books = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books.append(book)
    return books


@app.get("/books")
async def get_books():
    return BOOKS


@app.get("/books/{id}")
async def get_book(id: int):
    if id > len(BOOKS):
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return BOOKS[id]


@app.post("/books")
async def create_post(new_book: Book):
    BOOKS.append(dict(new_book))
    return JSONResponse(status_code=201, content={"message": "create successfully"})


@app.put("/books/{id}")
async def update_post(id: int, book: Book):
    BOOKS[id] = book
    return JSONResponse(status_code=200, content={"message": "updated successfully"})


@app.delete("/books/{id}")
async def delete_book(id: int):
    BOOKS.pop(id)
    return JSONResponse(status_code=200, content={"message": "Deleted Successfully"})
