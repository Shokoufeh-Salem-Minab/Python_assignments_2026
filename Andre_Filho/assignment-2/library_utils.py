# Assignment 2 - library module
# Andre Filho

import random

# library is a dictionary: id -> (title, author, year)
# genres is a set of book genres
genres = {"Fiction", "Programming", "Classic"}

def add_book(library, book_id, book):
    library[book_id] = book
    print("Book added:", book)

def search_book(library, title):
    for book in library.values():
        if book[0] == title:
            return book
    return "Book not found"

def list_books(library):
    print("Books in the library:")
    for book_id in library:
        print(book_id, "-", library[book_id])

def book_titles(library):
    # return a list with the titles of all books
    titles = []
    for book in library.values():
        titles.append(book[0])
    return titles

def suggest_random_book(library):
    book_id = random.choice(list(library))
    print("Random book to read:", library[book_id])
