# Homework 2 - Library Management System (module)
# Lasse Johannis

import random


# add a new book, but only if the ID is not used yet
def add_book(library, book_id, book):
    if book_id in library:
        print("ID", book_id, "is already taken by", library[book_id][0])
    else:
        library[book_id] = book
        print("Added:", book[0])


# search a book by title, return the book or None if not found
def search_book(library, title):
    for book_id, book in library.items():
        if book[0].lower() == title.lower():
            print("Found:", book[0], "by", book[1], "- ID", book_id)
            return book
    print(title, "is not in the library.")
    return None


# print all books
def list_books(library):
    print("All books:")
    for book_id, book in library.items():
        print(book_id, "-", book[0], "by", book[1] + ",", book[2])


# pick a random book with the random module
def suggest_random_book(library):
    books = list(library.values())
    return random.choice(books)
