def add_book(library, id, book):
    library[id]=book

def search_book(library, title):
    for i in library:
        if library[i][0] == title:
            return library[i]
    print('Book not found')

def list_books(library):
    for i in library:
        print(library[i])

