def add_book( library,id, book ):
    library[ id ] = book
    print("added book id:",id)

def search_book(library,title):
    found = False
    for k,v in library.items():
        if v[0].lower() == title.lower( ):
            print("Found book:",v)
            found=True
            break
    if not found:
        print( "Book not found:" , title)

def list_books( library ):
    print("--- ALL BOOKS ---")
    for b_id,info in library.items():
        print( f"ID {b_id}: Title = {info[0]} , Author = {info[1]} , Year = {info[2]}" )