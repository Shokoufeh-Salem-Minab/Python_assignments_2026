movie = {
    "title": "Inception",
    "year": 2010,
    "genres": ("Sci-Fi", "Thriller", "Drama"),
    "actors": ["Leonardo DiCaprio", "Tom Hardy"],
    "languages": {"English", "French"},
    "rating": 8.8
}

userMessage = """
========== MOVIE NIGHT ==========

1. Show movie information
2. Show genres
3. Add an actor
4. Remove an actor
5. Add a language
6. Update a genre
7. Search for a genre
8. Show movie statistics
9. Exit
"""


def isValidInput(userInput, expectedType):
    if userInput.strip() == "":
        print("No value given, back to the main menu.")
        return False
    if expectedType == int and not userInput.isdigit():
        print("Wrong format or value, back to the main menu.")
        return False
    return True


def movieInformation():
    for key, value in movie.items():
        print(f"{key}: {value}")


def showGenres(fromMain: bool):
    print("Genres:")
    for i in movie["genres"]:
        print("-", i)
    if fromMain:
        print("")
        print("First genre:", movie["genres"][0])
        print("Last genre:", movie["genres"][-1])


def addActor():
    userInput = input("Enter actor name: ").strip()
    if not isValidInput(userInput, str):
        return
    movie["actors"].append(userInput)
    print(userInput, "added successfully!")


def removeActor():
    userInput = input("Enter actor name: ").strip()
    if not isValidInput(userInput, str):
        return
    if userInput not in movie["actors"]:
        print("Actor not found.")
        return
    movie["actors"].remove(userInput)
    print(userInput, "was removed.")


def addLanguage():
    userInput = input("Enter language name: ").strip()
    if not isValidInput(userInput, str):
        return
    movie["languages"].add(userInput)
    print(userInput, "added successfully!")


def updateGenre():
    showGenres(False)
    userInput = input("Enter the genre to change: ").strip()
    if not isValidInput(userInput, str):
        return
    if userInput not in movie["genres"]:
        print("Genre not found.")
        return
    userInputNew = input("Enter new genre: ").strip()
    if not isValidInput(userInputNew, str):
        return
    newGenres = list(movie["genres"])
    newGenres[newGenres.index(userInput)] = userInputNew
    movie["genres"] = tuple(newGenres)
    print("Genre updated successfully!")


def searchGenre():
    userInput = input("Enter genre: ").strip()
    if not isValidInput(userInput, str):
        return
    if userInput in movie["genres"]:
        print("Yes!", userInput, "is one of the genres.")
    else:
        print(userInput, "is not one of the genres.")


def movieStatistics():
    print(f"""
========== STATISTICS ==========
Movie: {movie['title']}
Year: {movie['year']}
Rating: {movie['rating']}
Number of genres: {len(movie['genres'])}
Number of actors: {len(movie['actors'])}
Number of languages: {len(movie['languages'])}

Actors:
{', '.join(movie['actors'])}

Languages:
{', '.join(movie['languages'])}
""")

def main():
    noExit = True
    while noExit:
        print(userMessage)
        userSelection = input("Please enter the number of your choice: ")

        while not (userSelection.isdigit() and 1 <= int(userSelection) <= 9):
            userSelection = input("Invalid input, please input a valid number: ")

        userSelection = int(userSelection)

        if userSelection == 1:
            movieInformation()
        elif userSelection == 2:
            showGenres(True)
        elif userSelection == 3:
            addActor()
        elif userSelection == 4:
            removeActor()
        elif userSelection == 5:
            addLanguage()
        elif userSelection == 6:
            updateGenre()
        elif userSelection == 7:
            searchGenre()
        elif userSelection == 8:
            movieStatistics()
        else:
            print("Goodbye!")
            noExit = False


main()