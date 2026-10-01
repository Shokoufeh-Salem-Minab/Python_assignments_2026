# Assignment 2 - library module
# Andre Filho

import library_utils as lib

library = {}

# each book is a tuple: (title, author, year)
book1 = ("Dom Casmurro", "Machado de Assis", 1899)
book2 = ("The Little Prince", "Antoine de Saint-Exupery", 1943)
book3 = ("1984", "George Orwell", 1949)

lib.add_book(library, 1, book1)
lib.add_book(library, 2, book2)
lib.add_book(library, 3, book3)

print()
lib.list_books(library)

# add a new book and list the library again
print()
lib.add_book(library, 4, ("Clean Code", "Robert C. Martin", 2008))
lib.list_books(library)

print()
print("Search for 1984:", lib.search_book(library, "1984"))
print("Search for Harry Potter:", lib.search_book(library, "Harry Potter"))

print()
print("All titles (list):", lib.book_titles(library))
print("Genres (set):", lib.genres)

print()
lib.suggest_random_book(library)
