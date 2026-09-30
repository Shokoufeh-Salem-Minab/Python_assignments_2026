import random
from library import add_book, search_book, list_books

# ----- list -----
books = ["Mathematics", "Data Science", "Software Engineering"]
print("Books:", books)

# ----- tuple -----
book1 = ("Mathematics", "John Smith", 2020)
print("Book 1:", book1)

# ----- set -----
genres = {"Programming", "Data", "Math"}
print("Genres:", genres)

# ----- dictionary -----
library = {
    1: ("Mathematics", "John Smith", 2020),
    2: ("Data Science", "Alice Brown", 2021)
}

# ----- functions -----
add_book(library, 3, ("Software Engineering", "Bob Lee", 2022))

print("All books:")
list_books(library)

print("Search result:", search_book(library, "Data Science"))

# ----- random book suggestion -----
print("Random suggestion:", random.choice(list(library.values())))
