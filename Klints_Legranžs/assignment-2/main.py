import library_utils as lu
import random as rand

books = ["Python 101", "Data Science", "Machine Learning"]
books1 = ("Python 101", "John Smith", 2020)
genres = {"Programming", "AI", "Math"}

library = {
    1: ("Python 101", "John Smith", 2020),
    2: ("Data Science", "Alice Brown", 2021)
}


lu.list_books(library)
lu.add_book(library, 3, ("Java 101", "Jane Doe", 2013))

print("\n")

lu.search_book(library, "Java 101")

print("\n")

lu.list_books(library)

print("\n")

print(rand.choice(list(library.values())))
