#Requirements
# • Ask for input:
#     ◦ First name
#     ◦ Last name
# • String analysis:
#     ◦ Print the length of the first name and last name.
#     ◦ Count vowels (a, e, i, o, u) in the first name.
#     ◦ Count consonants in the first name.
#     ◦ Print the first name in uppercase and lowercase.
#     ◦ Print the last name reversed.
# • Loop practice:
#     ◦ Use a for loop to print each character of the first name.
#     ◦ Use a while loop to repeatedly print and remove characters from the first name until nothing is left.
# • Conditions (if/elif/else):
#     ◦ Compare the lengths of the first and last name.
#     ◦ Print a different message depending on whether the first name is longer, shorter, or equal.
# • Generate a personal password:
#     ◦ Combine:
#         ▪ The first letter of the first name
#         ▪ The last letter of the last name
#         ▪ The total number of characters (first name + last name)
# • List methods practice
#     ◦ Create a list that contains each character of your last name.
#     ◦ Use .append() to add a "*" character to the end of the list.
#     ◦ Use .insert() to add "@" at the beginning.
#     ◦ Use .remove() (or .pop()) to delete one character.
#     ◦ Use .reverse() to reverse the list.

vowels = ["a", "e", "i", "o", "u"]
counter = 0

first_name = str(input("Enter your first name: "))
last_name = str(input("Enter your last name: "))

print("Length of first name: " + str(len(first_name)))
print("Length of last name: " + str(len(last_name)))

for i in first_name:
    if i.isalpha() and i in vowels:
        counter+=1
print("Number of vowels in first name: " + str(counter))
counter = 0

for i in first_name:
    if i.isalpha() and i not in vowels:
        counter+=1
print("Number of consonants in first name: " + str(counter))
counter = 0

print("First name (lower): " + first_name + '\n' + "First name (upper): " + first_name.upper())
print("Last name (reversed): " + last_name[::-1])

#loops

for i in first_name:
    print(i)

while len(first_name) != 0:
    print(first_name)
    first_name_reversed = first_name[:len(first_name)-1]

#conditions

if len(first_name) == len(last_name):
    print("Both names are both " + str(len(first)) + " character long.")
elif len(first_name) < len(last_name):
    print("First name is shorter than last name.")
elif len(first_name) > len(last_name):
    print("First name is longer than last name.")


#password
combined_name = len(first_name) + len(last_name)
password = first_name[0] + last_name[-1] + str(combined_name)
print("Generated password: " + password)

name_chars = [char for char in last_name]

name_chars.append("*")
name_chars.insert(0, "@")
name_chars.pop()
name_chars.reverse()

print(name_chars)
