import random

books = []
book1 = ("Python 101", "John Smith", 2020)
genres = {"Programming", "AI", "Math"}
library = {}

def add_book(library, id, book):
    library[id] = book
    print(f"Book added: {library[id]}")
    books.append(book[0])

def search_book(library, title):
    for book in library:
        if library[book][0] == title:
            return library[book]

def list_books(library):
    print("List of all books:")
    for book in library:
        print(library[book])

def return_random_book(books):
    random_book_id = random.choice(list(library.keys()))
    print(f"Random book to read: {library[random_book_id]}")