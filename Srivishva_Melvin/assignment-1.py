# Homework 1
# Srivishva Melvin - sm25017
# Program created on: 25/09/2026

first = input("Enter your first name: ")
while len(first) == 0: # while loop in case user enters empty name 
    print("First name can't be empty.")
    first = input("Enter your first name: ")

last = input("Enter your last name: ")
while len(last) == 0:
    print("Last name can't be empty.")
    last = input("Enter your last name: ")

first_len = len(first)
last_len = len(last)
print("Length of first name:", first_len)
print("Length of last name:", last_len)

vowels = 0
consonants = 0
for letter in first.lower(): # lower() so that any letters passes through
    if letter in "aeiou": # checks if the character is vowel
        vowels += 1
    elif letter.isalpha(): # isalpha() to check if the leftover character is still a letter, and not a number or symbol
        consonants += 1

print("Vowels in first name:", vowels)
print("Consonants in first name:", consonants)
print("First name (upper):", first.upper())
print("First name (lower):", first.lower())
print("Last name (reversed):", last[::-1])

print("Characters in first name (for loop):")
for letter in first:
    print(letter)

print("Characters in first name (while loop):")
temp = first # copying first name so original variable stays unchanged
while len(temp) > 0:
    print(temp[0])
    temp = temp[1:] # slice from index 1 to remove first char

print()
if first_len > last_len:
    print("Comparison result: First name is longer than last name.")
elif first_len < last_len:
    print("Comparison result: First name is shorter than last name.")
else:
    print("Comparison result: First name and last name have the same length.")

total_chars = first_len + last_len
password = first[0] + last[-1] + str(total_chars)
print("Generated password:", password)

last_letters = []
for letter in last:
    last_letters.append(letter)
last_letters.append("*")
last_letters.insert(0, "@")
last_letters.pop(2)
last_letters.reverse()
print(last_letters)
