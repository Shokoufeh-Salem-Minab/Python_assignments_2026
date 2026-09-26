def add_book(library, id, book):
    library.update({id: book})


def search_book(library, title):
    for book in library.values():
        if title in book:
            print(book)


def list_books(library):
    for book in library:
        print(library[book])
