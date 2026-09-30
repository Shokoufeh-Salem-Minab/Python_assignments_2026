# Homework 2 - Library Management System
# Lasse Johannis

from library_utils import add_book, search_book, list_books, suggest_random_book

# ----- list: book titles -----
books = ["Clean Code", "The Pragmatic Programmer", "Thinking, Fast and Slow"]
print("Book titles:", books)

# ----- tuple: one book = (title, author, year) -----
book1 = ("Clean Code", "Robert C. Martin", 2008)
book2 = ("The Pragmatic Programmer", "Andrew Hunt", 1999)
book3 = ("Thinking, Fast and Slow", "Daniel Kahneman", 2011)
print("First book:", book1)

# ----- set: unique genres -----
genres = {"Programming", "Software Engineering", "Psychology"}
genres.add("Programming")  # duplicate is ignored
genres.add("Economics")
print("Genres:", genres)

# ----- dictionary: book ID -> book tuple -----
library = {
    1: book1,
    2: book2,
    3: book3,
}

# ----- functions from the module -----
print()
add_book(library, 4, ("Freakonomics", "Steven D. Levitt", 2005))
add_book(library, 1, ("Duplicate Book", "Nobody", 2000))  # ID 1 exists
books.append("Freakonomics")
print("Book titles:", books)

print()
list_books(library)

print()
search_book(library, "clean code")
search_book(library, "Harry Potter")

# ----- standard library: random -----
print()
suggestion = suggest_random_book(library)
print("Random suggestion for reading:", suggestion[0], "by", suggestion[1])
