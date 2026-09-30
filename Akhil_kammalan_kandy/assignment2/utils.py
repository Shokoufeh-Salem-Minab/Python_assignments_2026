# Akhil Kammalan Kandy, ak23204
# library_utils.py - helper functions for the library management system
import random

 #Add a new book under book_id. Returns True if added.
def add_book(library, book_id, book):
    if book_id in library:
        print(f"ID {book_id} already exists, book not added.")
        return False
    library[book_id] = book
    print(f"Added: {book[0]} by {book[1]} ({book[2]})")
    return True

#Search for books by title 
def search_book(library, title):
    results = []
    for book_id, book in library.items():
        if title.lower() in book[0].lower():
            results.append((book_id, book))
    return results

#show all books in the library
def list_books(library):
    
    if not library:
        print("The library is empty.")
        return
    for book_id, (title, author, year) in library.items():
        print(f"{book_id}: {title} by {author} ({year})")

# Return a random book to read
def suggest_random_book(library):
    if not library:
        return None
    book_id = random.choice(list(library.keys()))
    return book_id, library[book_id]