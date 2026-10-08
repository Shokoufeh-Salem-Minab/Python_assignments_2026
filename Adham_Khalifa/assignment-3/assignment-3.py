

# Dictionary containing all information about the movie
movie = {
    "title": "Interstellar",
    "year": 2014,
    "genres": ("Sci-Fi", "Drama", "Adventure"),
    "actors": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
    "languages": {"English", "French"},
    "rating": 8.7
}


# Function to show all movie information
def show_movie():
    print("\n========== MOVIE INFORMATION ==========")

    # Use dictionary items() method to display all information
    for key, value in movie.items():
        print(f"{key}: {value}")


# Function to show all genres
def show_genres():
    print("\n========== GENRES ==========")

    # Use a for loop to display each genre
    for genre in movie["genres"]:
        print("-", genre)

    # Use tuple indexing to show the first and last genres
    print("First genre:", movie["genres"][0])
    print("Last genre:", movie["genres"][-1])


# Function to add an actor
def add_actor():
    actor = input("Enter actor name: ")

    # Add the actor to the actors list
    movie["actors"].append(actor)

    print("Actor added successfully!")


# Function to remove an actor
def remove_actor():
    actor = input("Enter actor name: ")

    # Check if the actor exists in the list
    if actor in movie["actors"]:
        movie["actors"].remove(actor)
        print(actor, "was removed.")
    else:
        print("Actor not found.")


# Function to add a language
def add_language():
    language = input("Enter language: ")

    # Add the language to the set
    movie["languages"].add(language)

    print("Language added successfully!")


# Function to update a genre
def update_genre():
    print("Current genres:", movie["genres"])

    old_genre = input("Enter the genre to change: ")
    new_genre = input("Enter the new genre: ")

    # Tuples are immutable, so convert the tuple to a list
    genres = list(movie["genres"])

    # Check if the old genre exists
    if old_genre in genres:
        # Find the position of the old genre
        index = genres.index(old_genre)

        # Replace the old genre with the new genre
        genres[index] = new_genre

        # Convert the list back into a tuple
        movie["genres"] = tuple(genres)

        print("Genre updated successfully!")
    else:
        print("Genre not found.")


# Function to search for a genre
def search_genre():
    genre = input("Enter genre: ")

    # Check if the genre exists in the tuple
    if genre in movie["genres"]:
        print("Yes!", genre, "is one of the genres.")
    else:
        print(genre, "is not one of the genres.")


# Function to show movie statistics
def show_statistics():
    print("\n========== STATISTICS ==========")

    # Display basic movie information
    print("Movie:", movie["title"])
    print("Year:", movie["year"])
    print("Rating:", movie["rating"])

    # Display the number of genres, actors and languages
    print("Number of genres:", len(movie["genres"]))
    print("Number of actors:", len(movie["actors"]))
    print("Number of languages:", len(movie["languages"]))

    # Use join() to display actors as one string
    print("\nActors:")
    print(", ".join(movie["actors"]))

    # Use join() to display languages as one string
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

    # Ask the user to choose an option
    choice = input("Enter your choice: ")

    # Handle the user's choice
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
