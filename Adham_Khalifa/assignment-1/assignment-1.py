first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")

# String analysis
print("Length of first name:", len(first_name))
print("Length of last name:", len(last_name))

vowels = "aeiou"
vowel_count = 0
consonant_count = 0

for character in first_name.lower():
    if character in vowels:
        vowel_count += 1
    elif character.isalpha():
        consonant_count += 1

print("Vowels in first name:", vowel_count)
print("Consonants in first name:", consonant_count)

print("First name (upper):", first_name.upper())
print("First name (lower):", first_name.lower())
print("Last name (reversed):", last_name[::-1])

# For loop
print("\nCharacters in first name (for loop):")

for character in first_name:
    print(character)

# While loop
print("\nCharacters in first name (while loop):")

name_list = list(first_name)

while len(name_list) > 0:
    print(name_list[0])
    name_list.pop(0)

# Conditions
if len(first_name) > len(last_name):
    print("Comparison result: First name is longer than last name.")
elif len(first_name) < len(last_name):
    print("Comparison result: First name is shorter than last name.")
else:
    print("Comparison result: First name and last name have the same length.")

# Generate a personal password
total_characters = len(first_name) + len(last_name)
password = first_name[0] + last_name[-1] + str(total_characters)

print("Generated password:", password)

# List methods practice
last_name_list = list(last_name)

last_name_list.append("*")
last_name_list.insert(0, "@")

last_name_list.remove(last_name_list[1])

last_name_list.reverse()

print("Final last name list:", last_name_list)
