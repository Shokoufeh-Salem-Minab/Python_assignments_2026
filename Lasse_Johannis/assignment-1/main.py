# Homework 1 - Name analysis
# Lasse Johannis

vowels = "aeiou"

# ----- input -----
first_name = input("Enter your first name: ")
while first_name == "":
    first_name = input("First name cannot be empty. Enter your first name: ")

last_name = input("Enter your last name: ")
while last_name == "":
    last_name = input("Last name cannot be empty. Enter your last name: ")

# ----- string analysis -----
print("Length of first name:", len(first_name))
print("Length of last name:", len(last_name))

vowel_count = 0
consonant_count = 0
for char in first_name.lower():
    if char in vowels:
        vowel_count += 1
    elif char.isalpha():
        consonant_count += 1

print("Vowels in first name:", vowel_count)
print("Consonants in first name:", consonant_count)
print("First name (upper):", first_name.upper())
print("First name (lower):", first_name.lower())

# accumulate pattern: put each character in front of the result
reversed_last_name = ""
for char in last_name:
    reversed_last_name = char + reversed_last_name
print("Last name (reversed):", reversed_last_name)

# ----- loops -----
print("Characters in first name (for loop):")
for char in first_name:
    print(char)

print("Characters in first name (while loop):")
remaining = first_name
while len(remaining) > 0:
    print(remaining[0])
    remaining = remaining[1:]

# ----- conditions -----
if len(first_name) > len(last_name):
    print("Comparison result: First name is longer than last name.")
elif len(first_name) < len(last_name):
    print("Comparison result: First name is shorter than last name.")
else:
    print("Comparison result: First name and last name have the same length.")

# ----- personal password -----
total_length = len(first_name) + len(last_name)
password = first_name[0] + last_name[-1] + str(total_length)
print("Generated password:", password)

# ----- list methods -----
letters = list(last_name)
letters.append("*")
letters.insert(0, "@")
letters.pop(2)  # delete the second letter of the last name
letters.reverse()
print(letters)
