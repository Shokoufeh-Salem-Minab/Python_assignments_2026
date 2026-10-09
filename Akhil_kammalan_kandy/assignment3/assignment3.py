#Akhil Kammalan Kandy, ak23204, Assignment 3 - Movie Night

# Every movie is a dictionary, all movies live in one list.
library = [
    {
        "title": "Inception",
        "year": 2010,
        "genres": ("Sci-Fi", "Thriller", "Drama"),
        "actors": ["Leonardo DiCaprio", "Tom Hardy"],
        "languages": {"English", "French"},
        "rating": 8.8,
    }
]
state = {"current": 0}  # index of the movie we are working on


# helper_functions
def active(): ##current movie
    return library[state["current"]]

#ask user for input until they type something
def ask(prompt):
    text = ""
    while text == "":
        text = input(prompt).strip()
        if text == "":
            print("  (please type something)")
    return text

#ask user for a valid number choice
def ask_number(prompt, kind):
    while True:
        try:
            return kind(input(prompt))
        except ValueError:
            print("  (that is not a valid number, try again)")

#a, b ,c' -> ['a', 'b', 'c']
def split_words(text):
    return [part.strip() for part in text.split(",") if part.strip() != ""]

#return the first item in a list that matches the wanted string, ignoring case. If no match, return None
def find_ignore_case(wanted, items):
    for item in items:
        if item.lower() == wanted.lower():
            return item
    return None


#menu functions
def print_menu():
    movie = active()
    print("\n      MOVIE NIGHT      ")
    print(f"   Now working on: {movie['title']} ({movie['year']})")
    print("1. Show movie information")
    print("2. Show genres")
    print("3. Add an actor")
    print("4. Remove an actor")
    print("5. Add a language")
    print("6. Update a genre")
    print("7. Search for a genre")
    print("8. Show movie statistics")
    print("9. Exit")
    print("10. Add a new movie")
    print("11. Switch to another movie")
    print("12. List all movies")


def show_movie():
    movie = active()
    print()
    for field, value in movie.items():
        print(f"{field}: {value}")


def show_genres():
    genres = active()["genres"]
    print("\nGenres:")
    for g in genres:
        print(f"- {g}")
    print(f"First genre: {genres[0]}")
    print(f"Last genre: {genres[-1]}")


def add_actor():
    actors = active()["actors"]
    name = ask("Enter actor name: ")
    if find_ignore_case(name, actors) is not None:
        print(f"{name} is already in the cast.")
    else:
        actors.append(name)
        print("Actor added successfully!")


def remove_actor():
    actors = active()["actors"]
    name = ask("Enter actor name: ")
    match = find_ignore_case(name, actors)
    if match is None:
        print(f"{name} was not found in the cast.")
    else:
        actors.remove(match)
        print(f"{match} was removed.")


def add_language():
    languages = active()["languages"]
    lang = ask("Enter language: ").title()
    if lang in languages:
        print(f"{lang} is already available.")
    else:
        languages.add(lang)
        print("Language added successfully!")


def update_genre():
    movie = active()
    print("\nCurrent genres:")
    print(movie["genres"])
    old = find_ignore_case(ask("Enter the genre to change: "), movie["genres"])
    if old is None:
        print("That genre is not in this movie's list.")
        return
    new = ask("Enter the new genre: ")

    as_list = list(movie["genres"])        # tuple -> list
    as_list[as_list.index(old)] = new      # change the element
    movie["genres"] = tuple(as_list)       # list -> tuple
    print("\nThe new tuple is:")
    print(movie["genres"])


def search_genre():
    genres = active()["genres"]
    wanted = ask("Enter genre: ")
    match = find_ignore_case(wanted, genres)
    if match is not None:
        print(f"Yes! {match} is one of the genres.")
    else:
        print(f"{wanted} is not one of the genres.")


def show_statistics():
    movie = active()
    print("\n    STATISTICS ")
    print("Movie:", movie["title"])
    print("Year:", movie["year"])
    print("Rating:", movie["rating"])
    print("Number of genres:", len(movie["genres"]))
    print("Number of actors:", len(movie["actors"]))
    print("Number of languages:", len(movie["languages"]))
    print("Actors:")
    print(", ".join(movie["actors"]))
    print("Languages:")
    print(", ".join(sorted(movie["languages"])))


#adding new movie to the library
def add_movie():
    print("\n add New movie ")
    title = ask("Title: ")
    if find_ignore_case(title, [m["title"] for m in library]) is not None:
        print("A movie with that title already exists.")
        return
    year = ask_number("Release year: ", int)
    rating = ask_number("IMDB Rating (e.g. 7.5): ", float)
    genres = tuple(split_words(ask("Genres (comma separated): ")))
    actors = split_words(ask("Actors (comma separated): "))
    languages = set(split_words(ask("Languages (comma separated): ")))

    library.append({
        "title": title,
        "year": year,
        "genres": genres,
        "actors": actors,
        "languages": languages,
        "rating": rating,
    })
    state["current"] = len(library) - 1
    print(f"'{title}' was added and is now the selected movie.")


def list_movies():
    print("\nMovies in your library:")
    for number, m in enumerate(library, start=1):
        marker = "  <-- selected" if number - 1 == state["current"] else ""
        print(f"{number}. {m['title']} ({m['year']}), rating {m['rating']}{marker}")


def switch_movie():
    list_movies()
    number = ask_number("Enter the number of the movie: ", int)
    if 1 <= number <= len(library):
        state["current"] = number - 1
        print(f"Now working on '{active()['title']}'.")
    else:
        print("There is no movie with that number.")


#main
def main():
    running = True
    while running:
        print_menu()
        choice = input("Your choice: ").strip()

        if choice == "1":
            show_movie()
        elif choice == "2":
            show_genres()
        elif choice == "3":
            add_actor()
        elif choice == "4":
            remove_actor()
        elif choice == "5":
            add_language()
        elif choice == "6":
            update_genre()
        elif choice == "7":
            search_genre()
        elif choice == "8":
            show_statistics()
        elif choice == "9":
            print("Goodbye! Enjoy your movie night!")
            running = False
        elif choice == "10":
            add_movie()
        elif choice == "11":
            switch_movie()
        elif choice == "12":
            list_movies()
        else:
            print("Invalid choice, please pick a number from the menu.")


main()