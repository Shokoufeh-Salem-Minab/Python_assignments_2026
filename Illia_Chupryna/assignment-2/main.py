import library_utils as lib

book1 = ("Python 101", "John Smith", 2021)
book2 = ("Dune", "Frank Herbert", 1965)
book3 = ("Discrete Mathematics 666", "Some Turkish-Dude", 2000)
book4 = ("1984", "George Orwell", 1949)

print("-add_book test")
lib.add_book(lib.library, 1, book1)
lib.add_book(lib.library, 2, book2)
lib.add_book(lib.library, 3, book3)
lib.add_book(lib.library, 4, book4)

print("-search_book test")
print(lib.search_book(lib.library, "Python 101"))
print(lib.search_book(lib.library, "1984"))
print(lib.search_book(lib.library, "Discrete Mathematics 666"))

print("-list_books test")
lib.list_books(lib.library)

print("-return_random_book test")
lib.return_random_book(lib.books)
lib.return_random_book(lib.books)
lib.return_random_book(lib.books)