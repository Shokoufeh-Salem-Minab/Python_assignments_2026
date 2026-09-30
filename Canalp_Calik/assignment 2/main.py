import library_utils
import random

books = ["Python 101", "Data Science", "Machine Learning"]

book1 = ("Python 101", "John Smith", 2020)

genres = {"Programming", "AI", "Math"}

library = {
    1: ("Python 101", "John Smith", 2020),
    2: ("Data Science", "Alice Brown", 2021)
}

library_utils.add_book(library, 3, ("Machine Learning", "David Clark", 2022))

library_utils.list_books(library)

result = library_utils.search_book(library, "Data Science")
print(result)

random_suggestion = random.choice(books)
print(random_suggestion)
