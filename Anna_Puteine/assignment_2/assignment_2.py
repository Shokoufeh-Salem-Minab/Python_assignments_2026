# Anna Puteine ap24096

import ap24096_library_utils as utils
import random

books = [
    "Pride and Prejudice",
    "Jane Eyre",
    "Frankenstein",
    "Little Women",
    "Middlemarch"
]

book1 = ("Pride and Prejudice", "Jane Austen", 1813)
book2 = ("Jane Eyre", "Charlotte Brontë", 1847)
book3 = ("Frankenstein", "Mary Shelley", 1818)
book4 = ("Little Women", "Louisa May Alcott", 1868)
book5 = ("Middlemarch", "George Eliot", 1871)

genres = {"Romance", "Gothic", "Realist Novel"}

library = {
    1: book1,
    2: book2,
    3: book3,
    4: book4,
}

print('Inital library:')

utils.list_books(library)

print('\n New book added:')

utils.add_book(library, 5, book5)

utils.list_books(library)

print('\n Find book by name:')

utils.search_book(library, "Pride and Prejudice")

print('\n Suggest random book:')

utils.print_book(library[random.randint(1,5)])