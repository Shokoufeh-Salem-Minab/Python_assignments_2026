# Import the random standard library
import random

# Import functions from our library_utils module
from library_utils import add_book, search_book, list_books


# List containing book titles
books = ["Python 101", "Data Science", "Machine Learning"]

# Tuple containing information about one book
book1 = ("Python 101", "John Smith", 2020)

# Set containing unique library genres
genres = {"Programming", "AI", "Math"}

# Dictionary containing books
# The key is the book ID and the value is the book tuple
library = {
    1: ("Python 101", "John Smith", 2020),
    2: ("Data Science", "Alice Brown", 2021),
    3: ("Machine Learning", "David Lee", 2022)
}


# Print the initial library information
print("Library Management System")
print("-------------------------")

print("\nBook titles:")
print(books)

print("\nGenres:")
print(genres)

# Display all books
list_books(library)


# Add a new book using the function from library_utils.py
new_book = ("Python Programming", "Robert Green", 2023)
add_book(library, 4, new_book)


# Display the library after adding the new book
list_books(library)


# Search for a book by title
search_book(library, "Data Science")


# Get a random book from the library
random_book_id = random.choice(list(library.keys()))
random_book = library[random_book_id]

print("Random book suggestion:")
print(random_book[0], "by", random_book[1])
