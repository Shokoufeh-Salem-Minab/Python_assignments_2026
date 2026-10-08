# Ask the user to enter their first and last name
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")

# Print the length of the first and last name
print("Length of first name:", len(first_name))
print("Length of last name:", len(last_name))

# Count vowels and consonants in the first name
vowels = "aeiou"
vowel_count = 0
consonant_count = 0

# Check every character in the first name
for character in first_name.lower():
    if character in vowels:
        vowel_count += 1
    elif character.isalpha():
        consonant_count += 1

print("Vowels in first name:", vowel_count)
print("Consonants in first name:", consonant_count)

# Print the first name in uppercase and lowercase
print("First name (upper):", first_name.upper())
print("First name (lower):", first_name.lower())

# Reverse and print the last name
print("Last name (reversed):", last_name[::-1])

# Use a for loop to print each character of the first name
print("\nCharacters in first name (for loop):")

for character in first_name:
    print(character)

# Convert the first name into a list so characters can be removed
name_list = list(first_name)

# Use a while loop to print and remove characters
print("\nCharacters in first name (while loop):")

while len(name_list) > 0:
    print(name_list[0])
    name_list.pop(0)

# Compare the lengths of the first and last names
if len(first_name) > len(last_name):
    print("Comparison result: First name is longer than last name.")
elif len(first_name) < len(last_name):
    print("Comparison result: First name is shorter than last name.")
else:
    print("Comparison result: First name and last name have the same length.")

# Calculate the total number of characters
total_characters = len(first_name) + len(last_name)

# Create a personal password using the required characters
password = first_name[0] + last_name[-1] + str(total_characters)

print("Generated password:", password)

# Create a list containing each character of the last name
last_name_list = list(last_name)

# Add "*" to the end of the list
last_name_list.append("*")

# Add "@" to the beginning of the list
last_name_list.insert(0, "@")

# Remove one character from the list
last_name_list.remove(last_name_list[1])

# Reverse the list
last_name_list.reverse()

# Print the final list
print("Final last name list:", last_name_list)
