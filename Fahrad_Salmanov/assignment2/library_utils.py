import random


def add_book(library, book_id, book):
    if book_id in library:
        print("A book with this ID already exists.")
        return False
    library[book_id] = book
    print("Book added:", book[0])
    return True


def search_book(library, title):
    for book_id, book in library.items():
        if book[0].lower() == title.lower():
            return book_id, book
    return None


def list_books(library):
    if len(library) == 0:
        print("The library is empty.")
        return
    for book_id, book in library.items():
        title, author, year = book
        print(f"{book_id}. {title} by {author} ({year})")


def suggest_book(library):
    book_id = random.choice(list(library.keys()))
    return library[book_id]
