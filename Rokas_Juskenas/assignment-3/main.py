# homework_3.py

m_data={
    "title": "Interstellar",
    "year":2014,
    "genres": ("Sci-Fi" ,"Adventure", "Drama" ),
    "actors": [ "Matthew McConaughey", "Anne Hathaway", "Jessica Chastain" ],
    "languages": { "English" },
    "rating":8.7
}

def show_movie():
    print( "\n--- MOVIE INFO ---" )
    for k , v in m_data.items( ):
        print(f"{k}: {v}")

def show_genres( ):
    print("\n--- GENRES ---")
    for g in m_data["genres"]:
        print( "-",g )
    print("First genre:" , m_data[ "genres" ][0] )
    print("Last genre:",m_data["genres"][ -1 ])

def add_actor( ):
    a_name = input( "Enter actor name: " )
    m_data[ "actors" ].append(a_name )
    print("Actor added successfully!")

def remove_actor():
    act= input("Enter actor name: ")
    if act in m_data[ "actors" ]:
        m_data["actors"].remove( act )
        print(act, "was removed.")
    else:
        print( "Actor not found." )

def add_language():
    lang= input( "Enter language: " )
    m_data["languages"].add( lang )
    print( "Language added successfully!" )

def update_genre():
    print("Current genres:" , m_data[ "genres" ])
    old_g= input("Enter the genre to change: ")
    new_g = input( "Enter the new genre: " )
    
    g_list = list( m_data["genres"] )
    if old_g in g_list:
        idx = g_list.index( old_g )
        g_list[idx]= new_g
        m_data["genres"] = tuple( g_list )
        print("Genre updated successfully!")
    else:
        print( "Genre not found." )

def search_genre():
    g_search = input("Enter genre: ")
    if g_search in m_data[ "genres" ]:
        print("Yes!",g_search,"is one of the genres.")
    else:
        print( g_search , "is not one of the genres." )

def show_statistics():
    print( "\n--- STATISTICS ---" )
    print( "Movie:",m_data[ "title" ] )
    print( "Year:" , m_data["year"] )
    print("Rating:", m_data[ "rating" ])
    print("Number of genres:", len( m_data["genres"] ) )
    print( "Number of actors:", len(m_data[ "actors" ]) )
    print("Number of languages:" , len( m_data["languages"] ) )
    print("\nActors:")
    print(", ".join( m_data["actors"] ) )
    print( "\nLanguages:" )
    print(", ".join( m_data[ "languages" ] ) )

# Main program loop
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
    
    user_choice= input( "Enter your choice: " )
    
    if user_choice =="1":
        show_movie()
    elif user_choice == "2":
        show_genres( )
    elif user_choice == "3":
        add_actor( )
    elif user_choice=="4":
        remove_actor()
    elif user_choice == "5":
        add_language()
    elif user_choice== "6":
        update_genre()
    elif user_choice =="7":
        search_genre( )
    elif user_choice == "8":
        show_statistics( )
    elif user_choice== "9":
        print( "Goodbye!" )
        break
    else:
        print("Invalid choice. Please try again.")