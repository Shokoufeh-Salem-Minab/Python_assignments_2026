# Homework 3
# Srivishva Melvin - sm25017
# Program created on: 03/10/2026

movie = {
    "title": "Inception",
    "year": 2010,
    "genres": ("Sci-Fi", "Thriller", "Drama"),
    "actors": ["Leonardo DiCaprio", "Tom Hardy"],
    "languages": {"English", "French"},
    "rating": 8.8
}

def show_menu():
    print("\n========== MOVIE NIGHT ==========\n")
    print("1. Show movie information")
    print("2. Show genres")
    print("3. Add an actor")
    print("4. Remove an actor")
    print("5. Add a language")
    print("6. Update a genre")
    print("7. Search for a genre")
    print("8. Show movie statistics")
    print("9. Exit\n")

def show_movie(movie):
    print("\nHere's the movie information: ")
    for key, value in movie.items():
        print(key + ":", value)

def show_genres(movie):
    genres = movie["genres"]
    print("\nGenres:")
    for genre in genres:
        print("-", genre)
    print("\nFirst genre:", genres[0])
    print("Last genre:", genres[len(genres) - 1])

def add_actor(movie):
    name = input("Enter actor name: ").strip()
    if name == "":
        print("\nYou didn't type a name")
    elif name in movie["actors"]:
        print("\nActor is already added")
    else:
        movie["actors"].append(name)
        print("\nActor successfully added!")

def remove_actor(movie):
    name = input("\nEnter actor name: ").strip()
    if name in movie["actors"]:
        movie["actors"].remove(name)
        print(name, "was removed.")
    else:
        print("\nThere is no actor of that name")

def add_language(movie):
    language = input("Enter language: ").strip()
    exists = False
    for existing in movie["languages"]:
        if existing.lower() == language.lower(): # to check if language already exists, changes it to lowercase temporarily to compare
            exists = True
    if language == "":
        print("\nYou didn't type a language")
    elif exists:
        print("\nLanguage is already available")
    else:
        movie["languages"].add(language)
        print("\nLanguage added successfully!")

def update_genre(movie):
    print("\nCurrent genres:", movie["genres"])
    old = input("\nEnter the genre to change: ").strip()
    if old not in movie["genres"]:
        print("\nIt is not one of the genres")
        return
    new = input("\nEnter the new genre: ").strip()
    genre_list = list(movie["genres"]) # to convert tuple to list
    index = genre_list.index(old) # to find index of the old genre 
    genre_list[index] = new # replace old genre with the new one 
    movie["genres"] = tuple(genre_list) # making the list back to a tuple
    print("\nThe new genres are:", movie["genres"])

def search_genre(movie):
    search = input("\nEnter genre: ").strip()
    found = False
    for genre in movie["genres"]:
        if genre.lower() == search.lower():
            found = True
    if found:
        print("\nYes!", search, "is one of the genres.")
    else:
        print("\n" + search, "is not one of the genres.")

def show_statistics(movie):
    print("\n========== STATISTICS ==========")
    print("\nMovie:", movie["title"])
    print("Year:", movie["year"])
    print("Rating:", movie["rating"])
    print("\nNumber of genres:", len(movie["genres"]))
    print("Number of actors:", len(movie["actors"]))
    print("Number of languages:", len(movie["languages"]))
    print("\nActors:")
    print(", ".join(movie["actors"]))
    print("\nLanguages:")
    print(", ".join(sorted(movie["languages"]))) # sorted so the order stays the same

choice = ""
while choice != "9":
    show_menu()
    choice = input("Enter your choice: ").strip()
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
        print("Goodbye!")
    else:
        print("Invalid choice. Please try again.")
