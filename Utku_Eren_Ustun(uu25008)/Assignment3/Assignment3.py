# 1. Movie Information initialized with "The Book of Life"
movie = {
    "title": "The Book of Life",
    "year": 2014,
    "genres": ("Animation", "Adventure", "Comedy"),
    "actors": ["Diego Luna", "Zoe Saldana", "Channing Tatum"],
    "languages": {"English", "Spanish"},
    "rating": 7.2,
}


def show_movie():
    """Option 1: Display all movie information using items()."""
    print("\n========== MOVIE NIGHT ==========")
    for key, value in movie.items():
        print(f"{key}: {value}")


def show_genres():
    """Option 2: Display genres with a for loop and tuple indexing."""
    print("\n========== GENRES ==========")
    print("Genres:")
    for genre in movie["genres"]:
        print(f"- {genre}")

    print("First genre:", movie["genres"][0])
    print("Last genre:", movie["genres"][-1])


def add_actor():
    """Option 3: Add an actor using append()."""
    actor = input("Enter actor name: ").strip()
    movie["actors"].append(actor)
    print("Actor added successfully!")


def remove_actor():
    """Option 4: Remove an actor using remove()."""
    actor = input("Enter actor name: ").strip()
    if actor in movie["actors"]:
        movie["actors"].remove(actor)
        print(actor, "was removed.")
    else:
        print("Actor not found.")


def add_language():
    """Option 5: Add a language using add()."""
    language = input("Enter language: ").strip()
    movie["languages"].add(language)
    print("Language added successfully!")


def update_genre():
    """Option 6: Update tuple using tuple -> list -> modify -> tuple."""
    print("Current genres:", movie["genres"])
    old_genre = input("Enter the genre to change: ").strip()
    new_genre = input("Enter the new genre: ").strip()

    genres = list(movie["genres"])
    if old_genre in genres:
        index = genres.index(old_genre)
        genres[index] = new_genre
        movie["genres"] = tuple(genres)
        print("Genre updated successfully!")
    else:
        print("Genre not found.")


def search_genre():
    """Option 7: Search for a genre."""
    genre = input("Enter genre: ").strip()
    if genre in movie["genres"]:
        print("Yes!", genre, "is one of the genres.")
    else:
        print(genre, "is not one of the genres.")


def show_statistics():
    """Option 8: Display statistics with join()."""
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


# 2. Menu loop that runs continuously until choice 9 is entered
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
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")