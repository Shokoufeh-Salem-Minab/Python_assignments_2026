# Assignment 1 - Python fundamentals
# Andre Filho

# Ask for the user's name
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")

# Length of each name
first_len = len(first_name)
last_len = len(last_name)
print("Length of the first name: " + str(first_len))
print("Length of the last name: " + str(last_len))

# Count vowels and consonants in the first name
vowels = ["a", "e", "i", "o", "u"]
vowel_count = 0
consonant_count = 0
for letter in first_name:
    if letter.lower() in vowels:
        vowel_count += 1
    elif letter.isalpha():
        consonant_count += 1
print("Vowels in first name: " + str(vowel_count))
print("Consonants in first name: " + str(consonant_count))

# Upper case and lower case
print("First name (upper): " + first_name.upper())
print("First name (lower): " + first_name.lower())

# Reverse the last name using slicing
print("Last name (reversed): " + last_name[::-1])

# Print each character of the first name with a for loop
print("Characters (for loop):")
for character in first_name:
    print(character)

# Print each character again with a while loop (remove until the string is empty)
print("Characters (while loop):")
name_copy = first_name
while len(name_copy) > 0:
    print(name_copy[0])
    name_copy = name_copy[1:]

# Compare the lengths of the two names
if first_len > last_len:
    print("Comparison result: First name is longer than last name")
elif first_len < last_len:
    print("Comparison result: Last name is longer than first name")
else:
    print("Comparison result: Both names have the same length")

# Build a simple password
password = first_name[0] + last_name[-1] + str(first_len + last_len)
print("Generated password: " + password)

# List methods practice on the last name characters
letters = list(last_name)
letters.append("*")
letters.insert(0, "@")
letters.pop(1)
letters.reverse()
print("Last name characters after list methods: " + str(letters))
