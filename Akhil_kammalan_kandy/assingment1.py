# Akhil Kammalan Kandy, ak23204
# hw1

#input
f_name = input("Enter your first name: ")
l_name = input("Enter your last name: ")

# strings
print("Length of first name:", len(f_name))
print("Length of last name:", len(l_name))


def count_vowels(text):
    vowels = "aeiou"
    count = 0
    for char in text:
        if char.lower() in vowels:
            count += 1
    return count


def count_consonants(text):
    consonants = "bcdfghjklmnpqrstvwxyz"
    count = 0
    for char in text:
        if char.lower() in consonants:
            count += 1
    return count


print("Vowels in first name:", count_vowels(f_name))
print("Consonants in first name:", count_consonants(f_name))

print("First name (upper):", f_name.upper())
print("First name (lower):", f_name.lower())
print("Last name (reversed):", l_name[::-1])

# loops
print("Characters in first name (for loop):")
for char in f_name:
    print(char)

print("Characters in first name (while loop):")
remaining = f_name
while len(remaining) > 0:
    print(remaining[0])        # print the first remaining character
    remaining = remaining[1:]  # remove it from the string

# conditions
if len(f_name) > len(l_name):
    print("Comparison result: First name is longer than last name.")
elif len(f_name) < len(l_name):
    print("Comparison result: First name is shorter than last name.")
else:
    print("Comparison result: First name and last name have equal length.")

# pwd
total_chars = len(f_name) + len(l_name)
password = f_name[0] + l_name[-1] + str(total_chars)
print("Generated password:", password)

# lists
l_name_list = list(l_name)
print("Last name as list:", l_name_list)

l_name_list.append("*")
print("After append('*'):", l_name_list)

l_name_list.insert(0, "@")
print("After insert(0, '@'):", l_name_list)

l_name_list.remove("*")
print("After remove('*'):", l_name_list)

l_name_list.reverse()
print("After reverse():", l_name_list)