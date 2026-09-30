def add_book(library, id, book):
    library[id] = book


def search_book(library, title):
    for book in library.values():
        if book[0] == title:
            return book
    return None


def list_books(library):
    for id, book in library.items():
        print(id, book)
