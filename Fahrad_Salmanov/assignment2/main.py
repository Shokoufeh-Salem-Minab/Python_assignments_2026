from library_utils import add_book, search_book, list_books, suggest_book

# each book is a tuple: (title, author, year)
library = {
    1: ("Python 101", "John Smith", 2020),
    2: ("Data Science", "Alice Brown", 2021),
    3: ("Machine Learning", "David Miller", 2022),
}

books = [book[0] for book in library.values()]
genres = {"Programming", "AI", "Math"}

while True:
    print()
    print("--- Library Menu ---")
    print("1. Show all books")
    print("2. Add a book")
    print("3. Search for a book")
    print("4. Suggest a random book")
    print("5. Show genres")
    print("6. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        list_books(library)

    elif choice == "2":
        title = input("Title: ")
        author = input("Author: ")
        year = input("Year: ")
        genre = input("Genre: ")
        if not year.isdigit():
            print("Year must be a number.")
            continue
        book_id = max(library.keys()) + 1
        book = (title, author, int(year))
        if add_book(library, book_id, book):
            books.append(title)
            genres.add(genre)

    elif choice == "3":
        title = input("Enter the title: ")
        result = search_book(library, title)
        if result is None:
            print("Book not found.")
        else:
            book_id, book = result
            print(f"Found: ID {book_id} - {book[0]} by {book[1]} ({book[2]})")

    elif choice == "4":
        title, author, year = suggest_book(library)
        print(f"You should read: {title} by {author} ({year})")

    elif choice == "5":
        print("Genres:", ", ".join(sorted(genres)))

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid option, try again.")
