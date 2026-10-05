# library_utils.py

def add_book(library, book_id, book):
    if book_id in library:
        print("Book ID already exists.")
    else:
        library[book_id] = book
        print("Book added successfully!")


def search_book(library, title):
    for book_id, book in library.items():
        if book[0].lower() == title.lower():
            print("Book found!")
            print("Book ID:", book_id)
            print("Title:", book[0])
            print("Author:", book[1])
            print("Year:", book[2])
            return book

    print("Book not found.")
    return None


def list_books(library):
    if not library:
        print("The library is empty.")
        return

    print("\n--- All Books ---")

    for book_id, book in library.items():
        print("ID:", book_id)
        print("Title:", book[0])
        print("Author:", book[1])
        print("Year:", book[2])
        print("----------------")