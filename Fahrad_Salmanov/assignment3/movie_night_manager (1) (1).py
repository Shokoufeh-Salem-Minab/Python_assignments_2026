# Homework 3 - Movie Night Manager

# movie info stored in a dictionary
movie = {
    "title": "Inception",
    "year": 2010,
    "genres": ("Sci-Fi", "Thriller", "Drama"),   # tuple
    "actors": ["Leonardo DiCaprio", "Tom Hardy"],   # list
    "languages": {"English", "French"},   # set
    "rating": 8.8
}


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


def show_movie():
    print("\n========== MOVIE INFORMATION ==========")

    # items() gives me the key and the value together
    for key, value in movie.items():
        print(key + ": " + str(value))


def show_genres():
    print("\n========== GENRES ==========")
    print("Genres:")

    # loop through the tuple
    for genre in movie["genres"]:
        print("-", genre)

    # index 0 is the first one, -1 is the last one
    print("\nFirst genre:", movie["genres"][0])
    print("Last genre:", movie["genres"][-1])


def add_actor():
    actor = input("Enter actor name: ").strip()

    # don't want empty names in the list
    if actor == "":
        print("You didn't type anything.")
    elif actor in movie["actors"]:
        print(actor, "is already in the list.")
    else:
        movie["actors"].append(actor)
        print("\nActor added successfully!")


def remove_actor():
    actor = input("Enter actor name: ").strip()

    if actor in movie["actors"]:
        movie["actors"].remove(actor)
        print("\n" + actor + " was removed.")
    else:
        print("\n" + actor + " is not in the actors list.")


def add_language():
    language = input("Enter language: ").strip()

    if language == "":
        print("You didn't type anything.")
    else:
        # a set ignores duplicates by itself so no need to check
        movie["languages"].add(language)
        print("\nLanguage added successfully!")


def update_genre():
    print("\nCurrent genres:")
    print(movie["genres"])

    old_genre = input("\nEnter the genre to change: ").strip()

    # check first so we don't ask for the new genre for no reason
    if old_genre not in movie["genres"]:
        print("\n" + old_genre + " is not one of the genres.")
        return

    new_genre = input("Enter the new genre: ").strip()

    if new_genre == "":
        print("You didn't type anything.")
        return

    # tuples can't be changed so: tuple -> list -> change -> tuple
    genres_list = list(movie["genres"])
    position = genres_list.index(old_genre)
    genres_list[position] = new_genre
    movie["genres"] = tuple(genres_list)

    print("\nThe new tuple is:")
    print(movie["genres"])


def search_genre():
    genre = input("Enter genre: ").strip()

    if genre in movie["genres"]:
        print("\nYes! " + genre + " is one of the genres.")
    else:
        print("\n" + genre + " is not one of the genres.")


def show_statistics():
    print("\n========== STATISTICS ==========")

    print("\nMovie:", movie["title"])
    print("Year:", movie["year"])
    print("Rating:", movie["rating"])

    print("\nNumber of genres:", len(movie["genres"]))
    print("Number of actors:", len(movie["actors"]))
    print("Number of languages:", len(movie["languages"]))

    # join() puts the items into one string with ", " between them
    print("\nActors:")
    print(", ".join(movie["actors"]))

    print("\nLanguages:")
    print(", ".join(movie["languages"]))


# main loop - keeps going until the user picks 9
while True:
    show_menu()
    choice = input("Enter your choice: ").strip()

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
        print("\nGoodbye!")
        break
    else:
        print("\nInvalid choice, please enter a number from 1 to 9.")
