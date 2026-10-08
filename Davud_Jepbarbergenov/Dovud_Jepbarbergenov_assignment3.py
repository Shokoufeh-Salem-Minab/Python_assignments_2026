# Homework 3 - Movie Night Manager

movie = {
    "title": "Inception",
    "year": 2010,
    "genres": ("Sci-Fi", "Thriller", "Drama"),
    "actors": ["Leonardo DiCaprio", "Tom Hardy"],
    "languages": {"English", "French"},
    "rating": 8.8
}


def show_movie():
    print("\n========== MOVIE INFORMATION ==========")

    for key, value in movie.items():
        print(f"{key}: {value}")


def show_genres():
    print("\n========== GENRES ==========")

    for genre in movie["genres"]:
        print("-", genre)

    print("First genre:", movie["genres"][0])
    print("Last genre:", movie["genres"][-1])


def add_actor():
    actor = input("Enter actor name: ")

    movie["actors"].append(actor)

    print("Actor added successfully!")


def remove_actor():
    actor = input("Enter actor name: ")

    if actor in movie["actors"]:
        movie["actors"].remove(actor)
        print(actor, "was removed.")
    else:
        print("Actor not found.")


def add_language():
    language = input("Enter language: ")

    movie["languages"].add(language)

    print("Language added successfully!")


def update_genre():
    print("Current genres:", movie["genres"])

    old_genre = input("Enter the genre to change: ")
    new_genre = input("Enter the new genre: ")

    # Convert tuple to list
    genres = list(movie["genres"])

    if old_genre in genres:
        index = genres.index(old_genre)

        # Change the genre in the list
        genres[index] = new_genre

        # Convert list back to tuple
        movie["genres"] = tuple(genres)

        print("Genre updated successfully!")
    else:
        print("Genre not found.")


def search_genre():
    genre = input("Enter genre: ")

    if genre in movie["genres"]:
        print("Yes!", genre, "is one of the genres.")
    else:
        print(genre, "is not one of the genres.")


def show_statistics():
    print("\n========== STATISTICS ==========")

    print("Movie:", movie["title"])
    print("Year:", movie["year"])
    print("Rating:", movie["rating"])

    print("Number of genres:", len(movie["genres"]))
    print("Number of actors:", len(movie["actors"]))
    print("Number of languages:", len(movie["languages"]))

    print("\nActors:")
    print(", ".join(movie["actors"]))

    print("\nLanguages:")
    print(", ".join(movie["languages"]))


# Main menu
while True:

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

    choice = input("Enter your choice: ")

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
        print("Invalid choice. Please try again.")