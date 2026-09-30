import random

def add_book(library, id, book):
    if id in library:
        print("This ID already has a book")
    else:
        library[id] = book
        print(book[0], "was added to the library")

def search_book(library, title):
    for id in library:
        book = library[id]
        if book[0] == title:
            print("Found in index", id, "and book name is", book[0])
            return book
    print("Book not found")
    return None

def list_books(library):
    for id in library:
        book = library[id]
        print(id, "-", book[0], "by", book[1], "(" + str(book[2]) + ")")

def random_book(library):
    randomid = []
    for id in library:
        randomid.append(id)
    if not library:
        print("Library is empty")
        return None
    chosen_id = random.choice(randomid)
    return library[chosen_id]
