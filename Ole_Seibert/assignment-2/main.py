from library_utils import add_book, list_books, search_book
import random


books = ["Python 101", "Data Science", "Machine Learning"]
book1 = (books[0], "John Smith", 2020)
book2 = (books[1], "Alice Brown", 2021)
book3 = (books[2], "Emily Clark", 2022)
genres = {"Programming", "AI", "Math"}
library = {
    1: book1,
    2: book2,
    3: book3
}

# Show all books
print("All books:")
list_books(library)

# Add a new book
add_book(library, 4, ("Statistics Basics", "Maria Lopez", 2019))

print("\nAfter adding a book:")
list_books(library)

# Search for books
print("\nSearch results:")
result = search_book(library, "Data Science")
print(result)

result = search_book(library, "Harry Potter")
print(result)


print("\nRandom suggestion:")
suggestion = random.choice(list(library.values()))
print(suggestion)