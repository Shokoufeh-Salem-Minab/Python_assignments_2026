import random

def add_book(library, book_id, book):
    if book_id in library:
        print(f"Book ID {book_id} exists. Choose a different ID")
    else:
        library[book_id] = book
        print(f"Book {book} with ID {book_id} added.")

def search_book(library, title):
    in_library = False
    for book_id, book in library.items():
        if book[0].lower() == title.lower():
            print(f"Book: {book}, ID: {book_id}")
            in_library = True
    if in_library == False:
        print(f"Book {title} isn't in this library. Choose another one")

def list_books(library):
    for book_id, book in library.items():
        print(f"ID: {book_id}, Book: {book}")

def random_book(library):
    book = random.choice(list(library.values()))
    print(f"Random book to read: {book}")
