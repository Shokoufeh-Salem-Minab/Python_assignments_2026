# Homework 3 - Movie Night Manager
# Lasse Johannis

movie = {
    "title": "Interstellar",                                   # str
    "year": 2014,                                              # int
    "genres": ("Sci-Fi", "Adventure", "Drama"),                # tuple
    "actors": ["Matthew McConaughey", "Anne Hathaway"],        # list
    "languages": {"English", "German"},                        # set
    "rating": 8.7,                                             # float
}


def show_movie(movie):
    print("\n========== MOVIE INFORMATION ==========")
    for key, value in movie.items():
        print(key + ":", value)


def show_genres(movie):
    print("\n========== GENRES ==========")
    print("Genres:")
    for genre in movie["genres"]:
        print("-", genre)
    print()
    print("First genre:", movie["genres"][0])
    print("Last genre:", movie["genres"][-1])


def add_actor(movie):
    actor = input("Enter actor name: ")
    if actor == "":
        print("Actor name cannot be empty.")
    elif actor in movie["actors"]:
        print(actor, "is already in the cast.")
    else:
        movie["actors"].append(actor)
        print("Actor added successfully!")


def remove_actor(movie):
    actor = input("Enter actor name: ")
    if actor in movie["actors"]:
        movie["actors"].remove(actor)
        print(actor, "was removed.")
    else:
        print(actor, "is not in the cast.")


def add_language(movie):
    language = input("Enter language: ")
    if language == "":
        print("Language cannot be empty.")
    else:
        movie["languages"].add(language)
        print("Language added successfully!")


def update_genre(movie):
    print("Current genres:", movie["genres"])
    old_genre = input("Enter the genre to change: ")

    # tuples are immutable: tuple -> list -> modify -> tuple
    genres = list(movie["genres"])
    if old_genre in genres:
        new_genre = input("Enter the new genre: ")
        index = genres.index(old_genre)
        genres[index] = new_genre
        movie["genres"] = tuple(genres)
        print("Genre updated! New genres:", movie["genres"])
    else:
        print(old_genre, "is not one of the genres.")


def search_genre(movie):
    genre = input("Enter genre: ")
    if genre in movie["genres"]:
        print("Yes!", genre, "is one of the genres.")
    else:
        print(genre, "is not one of the genres.")


def show_statistics(movie):
    print("\n========== STATISTICS ==========")
    print("Movie:", movie["title"])
    print("Year:", movie["year"])
    print("Rating:", movie["rating"])
    print()
    print("Number of genres:", len(movie["genres"]))
    print("Number of actors:", len(movie["actors"]))
    print("Number of languages:", len(movie["languages"]))
    print("\nActors:")
    print(", ".join(movie["actors"]))
    print("\nLanguages:")
    print(", ".join(sorted(movie["languages"])))


def show_menu():
    print("\n========== MOVIE NIGHT ==========")
    print("1. Show movie information")
    print("2. Show genres")
    print("3. Add an actor")
    print("4. Remove an actor")
    print("5. Add a language")
    print("6. Update a genre")
    print("7. Search for a genre")
    print("8. Show movie statistics")
    print("9. Exit")


running = True
while running:
    show_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        show_movie(movie)
    elif choice == "2":
        show_genres(movie)
    elif choice == "3":
        add_actor(movie)
    elif choice == "4":
        remove_actor(movie)
    elif choice == "5":
        add_language(movie)
    elif choice == "6":
        update_genre(movie)
    elif choice == "7":
        search_genre(movie)
    elif choice == "8":
        show_statistics(movie)
    elif choice == "9":
        print("Enjoy your movie night. Goodbye!")
        running = False
    else:
        print("Invalid choice. Please enter a number from 1 to 9.")
