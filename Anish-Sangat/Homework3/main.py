
class Contact_Book:
    def __init__(self, name, number):
        self.name = name
        self.number = number

Contacts = {
    "Anish": 1234,
    "Bibek": 2345,
    "Cristiano": 7777,
    "Messi": 10,
    "Neymar": 11
}

def process():

    name = input("Enter Name: ")

    if name in Contacts:
        print(name, Contacts[name])
        
    else:
        print("No Contact Found")
        
process()

while True:
    choice = input("press C to Continue / E to Exit....")

    if choice == "c":
        process()
    else:
        print("Thanks you for choosing us")
        break
    
    
