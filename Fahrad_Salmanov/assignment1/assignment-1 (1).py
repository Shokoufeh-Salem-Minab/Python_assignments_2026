first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
print()

print("Length of first name:", len(first_name))
print("Length of last name:", len(last_name))

vowels = "aeiou"
vowel_count = 0
consonant_count = 0
for letter in first_name.lower():
    if letter in vowels:
        vowel_count += 1
    elif letter.isalpha():
        consonant_count += 1

print("Vowels in first name:", vowel_count)
print("Consonants in first name:", consonant_count)
print("First name (upper):", first_name.upper())
print("First name (lower):", first_name.lower())
print("Last name (reversed):", last_name[::-1])
print()

print("Characters in first name (for loop):")
for letter in first_name:
    print(letter)
print()

print("Characters in first name (while loop):")
temp = first_name
while len(temp) > 0:
    print(temp[0])
    temp = temp[1:]   # cut off the first letter
print()

if len(first_name) > len(last_name):
    print("Comparison result: First name is longer than last name.")
elif len(first_name) < len(last_name):
    print("Comparison result: First name is shorter than last name.")
else:
    print("Comparison result: First name and last name have the same length.")
print()

total = len(first_name) + len(last_name)
password = first_name[0] + last_name[-1] + str(total)
print("Generated password:", password)
print()

chars = list(last_name)
chars.append("*")
chars.insert(0, "@")
chars.remove(last_name[1])   # removes the second letter of the last name
chars.reverse()
print(chars)
