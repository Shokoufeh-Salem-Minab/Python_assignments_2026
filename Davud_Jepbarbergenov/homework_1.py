# Home Exercise 1
# Name: Davud Jepbarbergenov

# 1. Ask for first name and last name
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")

# 2. String analysis
print("Length of first name:", len(first_name))
print("Length of last name:", len(last_name))

# Count vowels in the first name
vowels = "aeiou"
vowel_count = 0

for character in first_name.lower():
    if character in vowels:
        vowel_count += 1

print("Vowels in first name:", vowel_count)

# Count consonants in the first name
consonant_count = 0

for character in first_name.lower():
    if character.isalpha() and character not in vowels:
        consonant_count += 1

print("Consonants in first name:", consonant_count)

# Print first name in uppercase and lowercase
print("First name (upper):", first_name.upper())
print("First name (lower):", first_name.lower())

# Reverse the last name
print("Last name (reversed):", last_name[::-1])

# 3. For loop: print each character of the first name
print("Characters in first name (for loop):")

for character in first_name:
    print(character)

# 4. While loop: print and remove characters
print("Characters in first name (while loop):")

remaining_name = first_name

while len(remaining_name) > 0:
    print(remaining_name[0])
    remaining_name = remaining_name[1:]

# 5. Compare the lengths of the names
if len(first_name) > len(last_name):
    print("Comparison result: First name is longer than last name.")
elif len(first_name) < len(last_name):
    print("Comparison result: First name is shorter than last name.")
else:
    print("Comparison result: First name and last name have equal length.")

# 6. Generate a personal password
total_characters = len(first_name) + len(last_name)

if first_name and last_name:
    password = first_name[0] + last_name[-1] + str(total_characters)
    print("Generated password:", password)
else:
    print("Cannot generate password: enter both names.")

# 7. List methods practice
last_name_list = list(last_name)

# Add "*" to the end
last_name_list.append("*")

# Add "@" at the beginning
last_name_list.insert(0, "@")

# Remove one character, if possible
if len(last_name_list) > 2:
    last_name_list.pop(1)

# Reverse the list
last_name_list.reverse()

print("Final last name list:", last_name_list)
