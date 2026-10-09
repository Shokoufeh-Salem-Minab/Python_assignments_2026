def movie_info(movie):
    for key, value in movie.items():
        print(f"{key}: {value}")

def show_genres(movie):
    for genre in movie["genres"]:
        print(genre)

    print(f"First genre: {movie['genres'][0]}")
    print(f"Last genre: {movie['genres'][-1]}")

def add_actor(movie, actor):
    for actors in movie["actors"]:
        if actors.lower() == actor.lower():
            print("Actor already exists")
            return
    movie["actors"].append(actor)
    print("Actor added successfully")

def remove_actor(movie, actor):
    for actors in movie["actors"]:
        if actors.lower() == actor.lower():
            movie["actors"].remove(actors)
            print("Actor removed successfully")
            return
    print("Actor not found")


def add_language(movie, language):
    for languages in movie["languages"]:
        if languages.lower() == language.lower():
            print("Language already exists")
            return
    movie["languages"].add(language)
    print("Language added successfully!")

def update_genre(movie, old_genre, new_genre):
    genres = list(movie["genres"])

    for i in range(len(genres)):
        if genres[i].lower() == old_genre.lower():
            genres[i] = new_genre
            movie["genres"] = tuple(genres)
            print("Genre updated successfully!")
            return
    print("Genre not found.")

def search_genre(movie, search):
    for genre in movie["genres"]:
        if search.lower() in genre.lower():
            print(f"Genre {search} exists")
            return
    print(f"{search} is not one of the genres")

def movie_stats(movie):
    print("===========STATISTICS=================")
    print(f"Movie: {movie['title']}")
    print(f"Year: {movie['year']}")
    print(f"Rating: {movie['rating']}")

    print(f"Number of genres: {len(movie['genres'])}")
    print(f"Number of actors: {len(movie['actors'])}")
    print(f"Number of languages: {len(movie['languages'])}")

    print("Actors:")
    print(", ".join(movie["actors"]))

    print("Languages:")
    print(", ".join(movie["languages"]))


movie = {
    "title" : "Twilight",
    "year" : 2008,
    "genres" : ("Romance","Fantasy","Drama"),
    "actors" : ["Kristen Stewart", "Robert Pattinson","Taylor Lautner"],
    "languages" : {"English"},
    "rating" : 5.4
}

print("========== MOVIE NIGHT ==========")
print(
"1. Show movie information\n"
"2. Show genres\n"
"3. Add an actor\n"
"4. Remove an actor\n"
"5. Add a language\n"
"6. Update a genre\n"
"7. Search for a genre\n"
"8. Show movie statistics\n"
"9. Exit"
)
choice = input("Enter your choice: ")
while choice !="9":
    if choice == "1":
        movie_info(movie)
    elif choice == "2":
        show_genres(movie)
    elif choice == "3":
        actor_input = input("Enter actor name: ")
        add_actor(movie, actor_input)
    elif choice == "4":
        actor_remove = input("Enter actor name to remove: ")
        remove_actor(movie, actor_remove)
    elif choice == "5":
        language = input("Enter language: ")
        add_language(movie, language)
    elif choice == "6":
        old_genre = input("Enter which genre to change: ")
        new_genre = input("Enter new genre: ")
        update_genre(movie, old_genre, new_genre)
    elif choice == "7":
        search = input("Enter movie genre to search: ")
        search_genre(movie,search)
    elif choice == "8":
        movie_stats(movie)
    else:
        print("Enter a valid choice.")

    print("========== MOVIE NIGHT ==========")
    print(
        "1. Show movie information\n"
        "2. Show genres\n"
        "3. Add an actor\n"
        "4. Remove an actor\n"
        "5. Add a language\n"
        "6. Update a genre\n"
        "7. Search for a genre\n"
        "8. Show movie statistics\n"
        "9. Exit")

    choice = input("Enter your choice: ")






