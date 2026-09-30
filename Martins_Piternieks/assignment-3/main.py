# ----- movie information (dictionary) -----
movie = {
    "title": "Inception",
    "year": 2010,
    "genres": ("Sci-Fi", "Thriller", "Drama"),
    "actors": ["Leonardo DiCaprio", "Tom Hardy"],
    "languages": {"English", "French"},
    "rating": 8.8
}


# ----- show all movie information -----
def show_movie():
    print("\n----- MOVIE INFORMATION -----")
    for key, value in movie.items():
        print(f"{key}: {value}")


# ----- show genres (tuple loop + indexing) -----
def show_genres():
    print("\nGenres:")
    for genre in movie["genres"]:
        print("-", genre)

    print("\nFirst genre:", movie["genres"][0])
    print("Last genre:", movie["genres"][-1])


# ----- add an actor (list method: append) -----
def add_actor():
    actor = input("Enter actor name: ")
    movie["actors"].append(actor)
    print("\nActor added successfully!")


# ----- remove an actor (list method: remove) -----
def remove_actor():
    actor = input("Enter actor name: ")
    if actor in movie["actors"]:
        movie["actors"].remove(actor)
        print(f"\n{actor} was removed.")
    else:
        print(f"\n{actor} is not in the actors list.")


# ----- add a language (set method: add) -----
def add_language():
    language = input("Enter language: ")
    movie["languages"].add(language)
    print("\nLanguage added successfully!")


# ----- update a genre (tuple -> list -> modify -> tuple) -----
def update_genre():
    print("\nCurrent genres:")
    print(movie["genres"])

    old_genre = input("\nEnter the genre to change: ")
    new_genre = input("Enter the new genre: ")

    genres_list = list(movie["genres"])          # tuple -> list

    if old_genre in genres_list:
        index = genres_list.index(old_genre)     # list method: index
        genres_list[index] = new_genre           # modify
        movie["genres"] = tuple(genres_list)     # list -> tuple
        print("\nGenre updated successfully!")
        print("New genres:", movie["genres"])
    else:
        print(f"\n{old_genre} is not one of the genres.")


# ----- search for a genre -----
def search_genre():
    genre = input("Enter genre: ")
    if genre in movie["genres"]:
        print(f"\nYes! {genre} is one of the genres.")
    else:
        print(f"\n{genre} is not one of the genres.")


# ----- show statistics (len + join) -----
def show_statistics():
    print("\n========== STATISTICS ==========")
    print()
    print("Movie:", movie["title"])
    print("Year:", movie["year"])
    print("Rating:", movie["rating"])
    print()
    print("Number of genres:", len(movie["genres"]))
    print("Number of actors:", len(movie["actors"]))
    print("Number of languages:", len(movie["languages"]))
    print()
    print("Actors:")
    print(", ".join(movie["actors"]))
    print()
    print("Languages:")
    print(", ".join(movie["languages"]))


# ----- menu -----
def show_menu():
    print("\n========== MOVIE NIGHT ==========")
    print()
    print("1. Show movie information")
    print("2. Show genres")
    print("3. Add an actor")
    print("4. Remove an actor")
    print("5. Add a language")
    print("6. Update a genre")
    print("7. Search for a genre")
    print("8. Show movie statistics")
    print("9. Exit")


# ----- main loop -----
choice = ""

while choice != "9":
    show_menu()
    choice = input("\nEnter your choice: ")

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
        print("\nGoodbye! Enjoy your movie night!")
    else:
        print("\nInvalid choice. Please enter a number from 1 to 9.")
