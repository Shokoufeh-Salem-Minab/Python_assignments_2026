# Library Management System

# Function to add a new book to the library
def add_book(library, book_id, book):
    library[book_id] = book
    print("Book added successfully.")


# Function to search for a book by title
def search_book(library, title):
    for book_id, book in library.items():
        if book[0].lower() == title.lower():
            print("Book found:")
            print("ID:", book_id)
            print("Title:", book[0])
            print("Author:", book[1])
            print("Year:", book[2])
            return

    print("Book not found.")


# Function to display all books in the library
def list_books(library):
    print("\nAll books in the library:")

    for book_id, book in library.items():
        print("ID:", book_id)
        print("Title:", book[0])
        print("Author:", book[1])
        print("Year:", book[2])
        print()
