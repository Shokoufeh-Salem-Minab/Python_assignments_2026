# Anna Puteine ap24096

movie = {
    "title": "Little Women",
    "year": 2019,
    "genres": ("Drama", "Romance"),
    "actors": ["Saoirse Ronan", "Emma Watson", "Florence Pugh", "Eliza Scanlen"],
    "languages": {"English", "Chinese"},
    "rating": 7.8
}

def show_info():
    print("Show movie information:\n")

    for key, value in movie.items():
        print(f"{key}: {value}")

def show_genres():
    print("Show genres:\n")

    genres = movie["genres"]
    for genre in genres:
        print(f"- {genre}")

    print()
    print(f"First genre: {genres[0]}")
    print(f"Last genre: {genres[-1]}")

def add_actor():
    print("Add an actor:")

    actor = input("\nEnter actor name: ")
    print()
    if actor in movie["actors"]:
        print("Actor is already in the list.")
    else:
        movie["actors"].append(actor)
        print("Actor added successfully!")

def remove_actor():
    print("Remove an actor:")

    actor = input("\nEnter actor name: ")
    print()
    if actor in movie["actors"]:
        movie["actors"].remove(actor)
        print("Actor removed successfully!")
    else:
        print("Actor is not in the list.")

def add_language():
    print("Add a language:")

    language = input("\nEnter language: ")
    print()
    if language in movie["languages"]:
        print("Language is already added.")
    else:
        movie["languages"].add(language)
        print("Language added successfully!")

def update_genre():
    print("Update genre:")

    old_genre = input("\nEnter genre to change: ")
    new_genre = input("Enter new genre: ")
    print()
    genre_list = list(movie["genres"])
    if old_genre not in genre_list:
        print("No such genre to update")
    elif new_genre in genre_list:
         print("Can not update to this genre")
    else:
        genre_list.remove(old_genre)
        genre_list.append(new_genre)
        movie["genres"] = tuple(genre_list)
        print("Genre updated successfully")

def search_genre():
    print("Search for a genre:")

    genre = input("\nEnter genre: ").capitalize()
    print()

    if genre in movie["genres"]:
        print(f"Yes! {genre} is one of the genres.")
    else:
        print(f"{genre} is not one of the genres.")


def show_statistics():
    print("Show movie statistics:")

    print(f"\nMovie: {movie['title']}")
    print(f"Year: {movie['year']}")
    print(f"Rating: {movie['rating']}")

    print(f"\nNumber of genres: {len(movie['genres'])}")
    print(f"Number of actors: {len(movie['actors'])}")
    print(f"Number of languages: {len(movie['languages'])}")

    print("\nActors:")
    print(", ".join(movie["actors"]))

    print("\nLanguages:")
    print(", ".join(sorted(movie["languages"])))


while True:
    print("========== MOVIE NIGHT ==========")
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
    print()


    x = input("Choose a number: ")

    if x == "1":
        show_info()
    elif x == "2":
        show_genres()
    elif x == "3":
        add_actor()
    elif x == "4":
        remove_actor()
    elif x == "5":
        add_language()
    elif x == "6":
        update_genre()
    elif x == "7":
        search_genre()
    elif x == "8":
        show_statistics()
    elif x == "9":
        print("Goodbye!")
        break
    else:
        print("Please choose from the list (1-9).")

    print()



