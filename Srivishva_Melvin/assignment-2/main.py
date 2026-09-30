# Python Homework 2
# Srivishva Melvin - sm25017
# Program created on: 29/09/2026

import library_utils

books = ["Python 101", "Data Science", "Machine Learning"]
book1 = ("Python 101", "John Smith", 2020)
book2 = ("Data Science", "Alice Brown", 2021)
book3 = ("Machine Learning", "Bobby Black", 2022)
genres = {"Programming", "AI", "Math"}

library = {
    1: book1,
    2: book2
}
print("Titles:", books)
print("Genres:", genres)

print("\nAdding a book:")
library_utils.add_book(library, 3, book3)
library_utils.add_book(library, 3, book3) # for testing duplicate case

print("\nAll books:")
library_utils.list_books(library)

print("\nSearching for Data Science:")
library_utils.search_book(library, "Data Science")

print("\nSearching for AI Books:")
library_utils.search_book(library, "AI") # for testing book not found case

print("\nRandom book:")
randomBook = library_utils.random_book(library)
if randomBook: 
    print("Here is a random book to read:", randomBook[0], "by", randomBook[1])
