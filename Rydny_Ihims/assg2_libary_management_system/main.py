import random
from library_utils import add_book, search_book, list_books

# list of book titles
books = ["Python 101", "Data Science", "Machine Learning"]

# books stored as tuples (title, author, year)
book1 = ("Python 101", "John Smith", 2020)
book2 = ("Data Science", "Alice Brown", 2021)
book3 = ("Machine Learning", "Sam Lee", 2022)

# set of unique genres
genres = {"Programming", "AI", "Math"}

# dictionary with book ID as key and book tuple as value
library = {
    1: book1,
    2: book2,
}

print("Genres:", genres)
print("Titles:", books)

print("\nAdding a book")
add_book(library, 3, book3)

print("\nAll books")
list_books(library)

print("\nSearching for a book")
title = input("Enter a title to search: ")
result = search_book(library, title)

if result is None:
    print("Book not found.")
else:
    book_id, book = result
    print("Found book", book_id, ":", book[0], "by", book[1], "(" + str(book[2]) + ")")

print("\nRandom book suggestion")
suggestion = random.choice(list(library.values()))
print("You should read", suggestion[0], "by", suggestion[1])