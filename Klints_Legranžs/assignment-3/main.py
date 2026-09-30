# Movie Night Manager

movie = {
    "title": "Inception",
    "year": 2010,
    "genres": ("Sci-Fi", "Thriller", "Drama"),
    "actors": ["Leonardo Dicaprio", "Tom Hardy"],
    "languages": {"English", "French"},
    "rating": 8.8
}

def menu():
    print("\n========== MOVIE NIGHT ==========\n")

    print("1. Show movie information\n"
        + "2. Show genres\n"
        + "3. Add an actor\n"
        + "4. Remove an actor\n"
        + "5. Add a language\n"
        + "6. Update a genre\n"
        + "7. Search for a genre\n"
        + "8. Show movie statistics\n"
        + "9. Exit\n")

    choice = int(input("Enter your choice: "))

    while True:
        if choice == 1:
            show_movies()
            menu()
            break
        elif choice == 2:
            show_genres()
            menu()
            break
        elif choice == 3:
            add_actor()
            menu()
            break
        elif choice == 4:
            remove_actor()
            menu()
            break
        elif choice == 5:
            add_lang()
            menu()
            break
        elif choice == 6:
            update_genre()
            menu()
            break
        elif choice == 7:
            search_genre()
            menu()
            break
        elif choice == 8:
            movie_stats()
            menu()
            break
        elif choice == 9:
            quit()
        else:
            print("Invalid choice, try again.")
            menu()



def show_movies():
    for key, value in movie.items():
        print(str(key) + ": " + str(value))


def show_genres():
    for genre in movie["genres"]:
        print(genre)
    print("First genre: " + movie["genres"][0])
    print("Last genre: " + movie["genres"][-1])


def add_actor():
    new_actor = str(input("Enter a new actor: "))

    movie["actors"].append(new_actor)

    print("Actor added.")


def remove_actor():
    actor_to_remove = str(input("Enter an actor: "))

    for actors in movie["actors"]:
        if actor_to_remove in actors:
            movie["actors"].remove(actor_to_remove)
            print(actor_to_remove + " was removed.")
    print(actor_to_remove + " is not in the list.")


def add_lang():
    new_language = str(input("Enter a new language: "))

    movie["languages"].add(new_language)

    print("Language added.")


def update_genre():
    print("Existing genres:")
    print(movie["genres"])
    existing_genre = str(input("Enter the genre you want to change: "))

    new_genre = str(input("Enter the new genre: "))

    genres = list(movie["genres"])

    if existing_genre in genres:
        genre_index = genres.index(existing_genre)

        genres[genre_index] = new_genre

        movie["genres"] = tuple(genres)

        print("Genre edited.")
    else:
        print("Could not find the genre.")



def search_genre():
    genre = str(input("Enter a genre: "))

    genres = list(movie["genres"])

    if genre in genres:
        print("The genre, " + genre + " exists in the list.")
    else:
        print("The genre, " + genre + " does not exist in the list.")


def movie_stats():
    print("Movie: ", movie["title"])
    print("Year: ", str(movie["year"]))
    print("Rating: ", movie["rating"])
    print("Number of genres: ", len(movie["genres"]))
    print("Number of actors: ", len(movie["actors"]))
    print("Number of languages: ", len(movie["languages"]))
    print("Actors:")
    print(", ".join(movie["actors"]))
    print("Languages:")
    print(", ".join(movie["languages"]))






menu()

