#Homework1
#Evelina Sadurska es25198

name = input("Enter your first name: ")
surname = input("Enter your last name: ")

name = name.strip()
surname = surname.strip()
name = name.lower()
surname = surname.lower()

#String analysis
name_len = len(name)
print(f"Length of the first name: {name_len}")

surname_len = len(surname)
print(f"Length of the last name: {surname_len}")


vowels = ['a', 'e', 'i', 'o', 'u']
vowel_count = 0
consonant_count = 0

for letter in name:
    if letter.isalpha():
        if letter in vowels:
            vowel_count += 1
        else:
            consonant_count += 1

print(f"Vowels in first name: {vowel_count}")
print(f"Consonants in first name: {consonant_count}")

print(f"First name (upper) {name.upper()}")
print(f"First name lower {name.lower()}")

reverse = surname[::-1]
print(f"Last name (reversed) {reverse}")

 #Excersies for loop practice
print("Characters in first name (for loop): ")
for letter in name:
    print(letter)

print("Characters in first name (while loop):")
del_name = name
while del_name:
    print(del_name[0])
    del_name=del_name[1:]

if name_len > surname_len:
    print("Comparison result: First name is longer than last name")
elif name_len < surname_len:
    print("Comparison result: Last name is longer than first name")
else:
    print("Comparison result: Last name is the same length as the first name")


password = name[0] + surname[-1] + str(name_len + surname_len)
print(f"generated password {password}")

#List methods practice
n_list = list(surname)
n_list.append("*")
n_list.insert (0, "@")
n_list.remove("r")
n_list.reverse()
print(n_list)
