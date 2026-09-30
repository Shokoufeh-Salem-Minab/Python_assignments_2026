#Library management system
#Evelina Sadurska es25198
import library_utils as utils

books = ["Alice's Adventures in Wonderland","The Picture of Dorian Gray","To Kill a Mockingbird"]

book1 = ("Alice's Adventures in Wonderland", "Lewis Carroll", 1865)
book2 = ("The Picture of Dorian Gray","Oscar Wilde", 1945)
book3 = ("To Kill a Mockingbird","Harper Lee", 1960)
book4 = ("Pippi Longstocking", "Astrid Lindgren", 1945)

genres = {"Coming of age","Fantasy","Classic"}

library = {
    1:book1,
    2:book2,
    3:book3}

#Adding books
id_state = utils.add_book(library,4 ,book4)
if id_state:
    print("Book Added")
else:
    print("ID already is taken")

#Checks if book is in library
found = utils.search_book(library, "Pippi Longstocking")
if found:
    print(f"Book found in library: {found}")
else:
    print("No book found in the library")

#Prints all books
print("Books in library:")
utils.list_books(library)

#Random book
random_book = utils.random_book(library)
print(f"Random suggested book: {random_book}")


