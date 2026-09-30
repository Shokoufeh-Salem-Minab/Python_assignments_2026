# Import functions from library_utils module
from library_utils import add_book, list_books, search_book, suggest_random_book

# 1. LIST: Simple list of book titles
books = ["Python 101", "Data Science", "Machine Learning"]

# 2. TUPLE: Book represented as (title, author, year)
book1 = ("Python 101", "John Smith", 2020)
book2 = ("Data Science", "Alice Brown", 2021)

# 3. SET: Unique genres in the library
genres = {"Programming", "AI", "Math"}

# 4. DICTIONARY: Library mapping book ID -> book tuple
library = {
    1: book1,
    2: book2,
}
# 5. FUNCTIONS IN ACTION: List all books
print("\n--- Current Library ---")
list_books(library)

# 6. FUNCTIONS IN ACTION: Add a new book
print("\n--- Adding New Book ---")
new_book = ("Machine Learning", "Alan Turing", 2023)
add_book(library, 3, new_book)

# 7. FUNCTIONS IN ACTION: Search for a book
print("\n--- Searching for 'Data Science' ---")
matches = search_book(library, "Data Science")
if matches:
    for book_id, (title, author, year) in matches:
        print(f"Found [ID {book_id}]: '{title}' by {author} ({year})")
else:
    print("Book not found.")

# 8. STANDARD LIBRARY: Pick a random recommendation
print("\n--- Random Recommendation ---")
recommendation = suggest_random_book(library)
if recommendation:
    rec_id, (rec_title, rec_author, rec_year) = recommendation
    print(f"Today's pick: '{rec_title}' by {rec_author} ({rec_year}) [ID: {rec_id}]")