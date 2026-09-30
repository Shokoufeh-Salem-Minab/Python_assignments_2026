import random

#adds book to library
def add_book(library, id, book):
    if id in library:
        return False
    else:
        library[id] = book
        return True

#searches if book title exists in library
def search_book(library,title):
    found = []
    for book_title in library.values():
        if book_title[0].lower() == title.lower():
            found.append(book_title[0])
    return found

#Prints all the books
def list_books(library):
    for book in library:
        print(book, library[book])

#Generates a random book
def random_book(library):
    return random.choice(list(library.values()))



