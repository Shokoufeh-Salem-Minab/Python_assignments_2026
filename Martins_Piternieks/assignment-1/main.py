# ----- ask for name and surname -----
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")

# ----- print the length of name and surname -----
print("Length of first name:", len(first_name))
print("Length of last name:", len(last_name))

# ----- count the vowels and consonants -----
vowels = 0
consonants = 0
for letter in first_name.lower():
    if letter in "aeiou":
        vowels = vowels + 1
    elif letter.isalpha():
        consonants = consonants + 1

print("Vowels in first name:", vowels)
print("Consonants in first name:", consonants)

# ----- capped, lowered and reversed name printing -----

print("First name (upper):", first_name.upper())
print("First name (lower):", first_name.lower())
print("Last name (reversed):", last_name[::-1])

# ----- print each character of first name -----
print("Characters in first name (for loop):")
for letter in first_name:
    print(letter)

print("Removing characters in first name (while loop):")
name = first_name
while name != "":
    print(name)   # print the first character
    name = name[1:]  # remove the first character

# ----- conditions -----
print("Which is longer first name or last name (ifs):")
if len(first_name) > len(last_name):
    print("First name is longer than last name.")
elif len(first_name) < len(last_name):
    print("First name is shorter than last name.")
else:
    print("First name and last name are the same length.")

# ----- generate a personal password -----
total_length = len(first_name) + len(last_name)
password = first_name[0] + last_name[-1] + str(total_length)
print("Generated password:", password)

# ----- list methods practice -----
letters = list(last_name)
letters.append("*")
letters.insert(0, "@")
letters.pop(2)
letters.reverse()
print(letters)
