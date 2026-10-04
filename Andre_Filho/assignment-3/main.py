# Assignment 3 - Movie Night Manager
# Andre Filho

movie = {
    "title": "Inception",
    "year": 2010,
    "genres": ("Sci-Fi", "Thriller", "Drama"),
    "actors": ["Leonardo DiCaprio", "Tom Hardy"],
    "languages": {"English", "French"},
    "rating": 8.8
}


def show_movie():
    for key, value in movie.items():
        print(key + ":", value)


def show_genres():
    genres = movie["genres"]
    print("Genres:")
    for genre in genres:
        print("-", genre)
    print("First genre:", genres[0])
    print("Last genre:", genres[-1])


def add_actor():
    name = input("Enter actor name: ")
    movie["actors"].append(name)
    print("Actor added successfully!")


def remove_actor():
    name = input("Enter actor name: ")
    if name in movie["actors"]:
        movie["actors"].remove(name)
        print(name, "was removed.")
    else:
        print(name, "is not in the actors list.")


def add_language():
    language = input("Enter language: ")
    movie["languages"].add(language)
    print("Language added successfully!")


def update_genre():
    print("Current genres:", movie["genres"])
    old = input("Enter the genre to change: ")
    new = input("Enter the new genre: ")
    # tuples cannot be changed directly, so turn it into a list, change it, and back to a tuple
    genres = list(movie["genres"])
    if old in genres:
        genres[genres.index(old)] = new
        movie["genres"] = tuple(genres)
        print("New genres:", movie["genres"])
    else:
        print(old, "is not one of the genres.")


def search_genre():
    genre = input("Enter genre: ")
    if genre in movie["genres"]:
        print("Yes!", genre, "is one of the genres.")
    else:
        print(genre, "is not one of the genres.")


def show_statistics():
    print("========== STATISTICS ==========")
    print("Movie:", movie["title"])
    print("Year:", movie["year"])
    print("Rating:", movie["rating"])
    print("Number of genres:", len(movie["genres"]))
    print("Number of actors:", len(movie["actors"]))
    print("Number of languages:", len(movie["languages"]))
    print("Actors:")
    print(", ".join(movie["actors"]))
    print("Languages:")
    print(", ".join(movie["languages"]))


while True:
    print()
    print("========== MOVIE NIGHT ==========")
    print("1. Show movie information")
    print("2. Show genres")
    print("3. Add an actor")
    print("4. Remove an actor")
    print("5. Add a language")
    print("6. Update a genre")
    print("7. Search for a genre")
    print("8. Show movie statistics")
    print("9. Exit")

    choice = input("Choose an option: ")

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
        print("Goodbye!")
        break
    else:
        print("Invalid option, please try again.")
