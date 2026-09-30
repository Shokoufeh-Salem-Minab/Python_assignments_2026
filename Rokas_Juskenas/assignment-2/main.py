import random
import library_utils as utils

# List of titles
books = ["Python 101" , "Data Science" ,"Machine Learning"]

# Set of unique genres
genres = { "Programming" , "AI", "Math" }

# Tuples for initial books
book1= ("Python 101", "John Smith", 2020)
book2 = ("Data Science" , "Alice Brown" , 2021)

# Dictionary library
library= {
    1: book1,
    2: book2
}

# Functions testing
utils.list_books( library )

# add new book (tuple)
book3 = ( "Machine Learning", "Andrew Ng" , 2018 )
utils.add_book(library,3, book3)

# list again after adding
utils.list_books( library)

# search books
utils.search_book( library,"Python 101" )
utils.search_book( library ,"Non Existing Book" )

# Standard library random suggestion
random_id = random.choice( list( library.keys() ) )
suggested = library[ random_id ]
print("Random book recommendation:" , suggested[0] , "by" , suggested[ 1 ])