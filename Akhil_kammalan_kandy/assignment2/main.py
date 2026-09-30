# Akhil Kammalan Kandy, ak23204
# main.py - Library Management System
from assignment2.utils import add_book, search_book, list_books, suggest_random_book

# List of book titles
books = ["Lord of the Rings", "Dune", "Narnia", "Sherlock Holmes", "The Hobbit"]

# Tuples: (title, author, year)
book1 = ("Lord of the Rings", "JRR Tolkein", 1954)
book2 = ("Dune", "Frank Herbert", 1965)
book3 = ("Narnia", "C.S. Lewis", 1950)
book4 = ("Sherlock Holmes", "Arthur Conan Doyle", 1892)
book5 = ("The Hobbit", "JRR Tolkein", 1937)

# Set of unique genres
genres = {"Fantasy", "Ficton", "Detective"}

# Dictionary: key = book ID, value = book tuple
library = {
    1: book1,
    2: book2,
    3: book3,
    4: book4,
    5: book5
}

print(" Titles list ")
print(books)

print("Genres")
print(genres)
genres.add("Fantasy")  # duplicate, sets keep only unique values
genres.add("Fiction")
genres.add("Mystery")

print(genres)

print("Adding a book")
add_book(library, 3, book3)
add_book(library, 3, ("Duplicate", "Nobody", 2000))  # same ID, rejected

print("All books")
list_books(library)

print("Search")
title = input("Enter a title to search for: ")
found = search_book(library, title)
if found:
    for book_id, (t, author, year) in found:
        print(f"Found (ID {book_id}): {t} by {author} ({year})")
else:
    print("No book found with that title.")

print("Random suggestion")
suggestion = suggest_random_book(library)
if suggestion:
    book_id, (t, author, year) = suggestion
    print(f"Why not read '{t}' by {author} ({year})?")