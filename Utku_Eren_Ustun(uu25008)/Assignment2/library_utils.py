import random

def add_book(library, book_id, book_tuple):
    """
    Adds a new book tuple (title, author, year) to the library under the given ID.
    """
    library[book_id] = book_tuple
    print(f"Successfully added: '{book_tuple[0]}' (ID: {book_id})")

def search_book(library, title):
    """
    Searches for a book by title (case-insensitive).
    Returns a list of matching entries formatted as (ID, (title, author, year)).
    """
    results = []
    for book_id, book_data in library.items():
        if book_data[0].strip().lower() == title.strip().lower():
            results.append((book_id, book_data))
    return results

def list_books(library):
    """
    Prints all books currently stored in the library dictionary.
    """
    print(f"{'ID':<6}{'Title':<22}{'Author':<16}{'Year'}")
    for book_id, (title, author, year) in library.items():
        print(f"{book_id:<6}{title:<22}{author:<16}{year}")

def suggest_random_book(library):
    """
    Uses the random module to pick and return a random book from the library.
    """
    if not library:
        return None
    random_id = random.choice(list(library.keys()))
    return random_id, library[random_id]