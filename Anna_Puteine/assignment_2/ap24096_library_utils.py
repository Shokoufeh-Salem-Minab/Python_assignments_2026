def add_book(library, id, title):
    library[id] = title  

def search_book(library, title):
    for book in library.values():
        if book[0] ==title:
            print_book(book)
            return
    print("Book not found")

def list_books(library):
    for book in library.values():
        print_book(book)

def print_book(book):
    print(book[0], book[1], book[2], sep=', ')