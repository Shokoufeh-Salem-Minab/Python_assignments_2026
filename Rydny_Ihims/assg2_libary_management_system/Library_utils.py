def add_book(library, book_id, book):
    library[book_id] = book
    print("Added:", book[0])


def search_book(library, title):
    for book_id, book in library.items():
        if book[0].lower() == title.lower():
            return book_id, book
    return None


def list_books(library):
    for book_id, book in library.items():
        print(book_id, ":", book[0], "by", book[1], "(" + str(book[2]) + ")")